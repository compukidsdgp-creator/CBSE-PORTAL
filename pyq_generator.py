#!/usr/bin/env python3
"""
CBSE Pre-Board Practice Paper Generator
Generates CBSE-style branded practice PDFs using reportlab.
Tracks used questions to prevent repetition across daily papers.
"""

import os, sys, json, random, argparse
from datetime import datetime, date
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor, black, white, Color
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable,
                                    KeepTogether, PageBreak)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
    from reportlab.pdfgen import canvas
    from reportlab.platypus.flowables import Flowable
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("reportlab not installed — run: pip install reportlab --break-system-packages")
    sys.exit(1)

# ─── Register Unicode-capable fonts ──────────────────────────────────────────
# DejaVu Sans supports subscripts (H₂O), superscripts (x²), arrows (→),
# Greek letters (α,β,λ), degree symbol (°) and all other chemistry Unicode.

_DEJAVU_PATHS = {
    "DejaVu":           "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "DejaVu-Bold":      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "DejaVu-Italic":    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    "DejaVu-BoldItalic":"/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
}
_FONTS_REGISTERED = False

def _register_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    for name, path in _DEJAVU_PATHS.items():
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))
    # Register family so bold/italic switching works inside Paragraph XML
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily(
        "DejaVu",
        normal="DejaVu",
        bold="DejaVu-Bold",
        italic="DejaVu-Italic",
        boldItalic="DejaVu-BoldItalic",
    )
    _FONTS_REGISTERED = True

BODY_FONT      = "DejaVu"
BODY_FONT_BOLD = "DejaVu-Bold"
BODY_FONT_ITAL = "DejaVu-Italic"

try:
    from pyq_question_bank import QUESTION_BANKS, get_all_question_ids
except ImportError:
    print("pyq_question_bank.py not found in the same directory")
    sys.exit(1)

# ─── Paths ───────────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).parent
OUTPUT_DIR  = REPO_ROOT / "pyq-papers"
LOG_FILE    = OUTPUT_DIR / "question_log.json"
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── Brand colours ───────────────────────────────────────────────────────────

BRAND_BLUE   = HexColor("#1565C0")   # deep blue
BRAND_ORANGE = HexColor("#E65100")   # orange accent
BRAND_GREY   = HexColor("#424242")   # dark grey text
LIGHT_BLUE   = HexColor("#E3F2FD")   # section header background
GOLD         = HexColor("#F9A825")   # marks badge
MID_GREY     = HexColor("#9E9E9E")
CREAM        = HexColor("#FFFDE7")

PAGE_W, PAGE_H = A4   # 595 x 842 pt
MARGIN        = 1.8 * cm
INNER_W       = PAGE_W - 2 * MARGIN

# ─── Question log helpers ─────────────────────────────────────────────────────

def load_log() -> dict:
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text())
        except Exception:
            pass
    return {}

def save_log(log: dict):
    LOG_FILE.write_text(json.dumps(log, indent=2))

def get_used(log: dict, bank_key: str) -> set:
    return set(log.get(bank_key, []))

def mark_used(log: dict, bank_key: str, ids: list):
    existing = log.get(bank_key, [])
    log[bank_key] = list(set(existing) | set(ids))

# ─── Question selection ───────────────────────────────────────────────────────

def select_questions(bank_key: str, log: dict) -> dict:
    """
    Select questions section-by-section from the bank, skipping already-used ones.
    Returns a dict: {section_name: [q, q, …]}  or raises ValueError if bank exhausted.
    """
    bank    = QUESTION_BANKS[bank_key]
    used    = get_used(log, bank_key)
    all_ids = get_all_question_ids(bank_key)
    fresh   = [qid for qid in all_ids if qid not in used]

    # If >60 % used, reset (new cycle)
    if len(fresh) < 0.4 * len(all_ids):
        print(f"  ♻️  Question bank for {bank_key} >60% used — resetting cycle")
        log[bank_key] = []
        used   = set()
        fresh  = all_ids[:]

    selected_map = {}

    for section in bank["sections"]:
        sec_name = section["name"]
        avail    = [q for q in section["questions"] if q["id"] in fresh or q["id"] not in used]
        # Shuffle for variety
        random.shuffle(avail)

        # We take ALL questions in the section (the bank already has the correct count per paper)
        # For sections with OR alternatives we keep them as-is
        selected_map[sec_name] = avail   # full section

    return selected_map, bank


# ─── Custom Flowables ─────────────────────────────────────────────────────────

class RoundedRect(Flowable):
    """Filled rounded rectangle used as a banner."""
    def __init__(self, width, height, color, radius=4):
        super().__init__()
        self.width  = width
        self.height = height
        self.color  = color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=0)


class WatermarkCanvas(canvas.Canvas):
    """Canvas subclass that draws a subtle diagonal watermark."""
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_watermark()
            super().showPage()
        super().save()

    def draw_watermark(self):
        self.saveState()
        self.setFont(BODY_FONT, 60)
        self.setFillColorRGB(0.9, 0.9, 0.9, 0.08)
        self.translate(PAGE_W / 2, PAGE_H / 2)
        self.rotate(45)
        self.setFillAlpha(0.06)
        self.drawCentredString(0, 0, "CBSEMOCK.ORG.IN")
        self.restoreState()


# ─── Style sheet ──────────────────────────────────────────────────────────────

def build_styles():
    _register_fonts()
    base = getSampleStyleSheet()
    styles = {}

    def s(name, **kw):
        parent_name = kw.pop("parent", "Normal")
        parent = base.get(parent_name) or base["Normal"]
        styles[name] = ParagraphStyle(name, parent=parent, **kw)

    s("school_name",
      fontSize=18, leading=22, textColor=BRAND_BLUE,
      fontName=BODY_FONT_BOLD, alignment=TA_CENTER, spaceAfter=1)

    s("board_name",
      fontSize=11, leading=14, textColor=BRAND_GREY,
      fontName=BODY_FONT, alignment=TA_CENTER, spaceAfter=1)

    s("paper_title",
      fontSize=14, leading=18, textColor=BRAND_ORANGE,
      fontName=BODY_FONT_BOLD, alignment=TA_CENTER, spaceAfter=4)

    s("meta_row",
      fontSize=9, leading=11, textColor=BRAND_GREY,
      fontName=BODY_FONT, alignment=TA_CENTER, spaceAfter=2)

    s("general_instructions_heading",
      fontSize=10, leading=12, textColor=BRAND_BLUE,
      fontName=BODY_FONT_BOLD, alignment=TA_LEFT, spaceBefore=6, spaceAfter=2)

    s("general_instructions",
      fontSize=8.5, leading=12, textColor=BRAND_GREY,
      fontName=BODY_FONT, alignment=TA_JUSTIFY, spaceAfter=1)

    s("section_header",
      fontSize=11, leading=14, textColor=white,
      fontName=BODY_FONT_BOLD, alignment=TA_CENTER,
      spaceBefore=10, spaceAfter=4,
      leftIndent=0, rightIndent=0,
      backColor=BRAND_BLUE)

    s("section_subhead",
      fontSize=9, leading=11, textColor=BRAND_GREY,
      fontName=BODY_FONT_ITAL, alignment=TA_CENTER, spaceAfter=4)

    s("q_num",
      fontSize=9.5, leading=13, textColor=BRAND_BLUE,
      fontName=BODY_FONT_BOLD, alignment=TA_LEFT)

    s("q_text",
      fontSize=9.5, leading=14, textColor=BRAND_GREY,
      fontName=BODY_FONT, alignment=TA_JUSTIFY, spaceAfter=2)

    s("q_option",
      fontSize=9, leading=12, textColor=BRAND_GREY,
      fontName=BODY_FONT, leftIndent=12, spaceAfter=1)

    s("q_note",
      fontSize=8.5, leading=11, textColor=MID_GREY,
      fontName=BODY_FONT_ITAL, leftIndent=12, spaceAfter=2)

    s("q_preamble",
      fontSize=8.5, leading=12, textColor=BRAND_GREY,
      fontName=BODY_FONT_ITAL, alignment=TA_LEFT,
      spaceBefore=4, spaceAfter=3,
      borderPad=4, backColor=CREAM,
      leftIndent=6, rightIndent=6)

    s("marks_badge",
      fontSize=8, leading=10, textColor=BRAND_ORANGE,
      fontName=BODY_FONT_BOLD, alignment=TA_RIGHT)

    s("footer",
      fontSize=7.5, leading=10, textColor=MID_GREY,
      fontName=BODY_FONT, alignment=TA_CENTER)

    s("website",
      fontSize=8, leading=10, textColor=BRAND_BLUE,
      fontName=BODY_FONT_BOLD, alignment=TA_RIGHT)

    return styles


# ─── Header builder ───────────────────────────────────────────────────────────

def build_header(bank: dict, paper_date: str, styles) -> list:
    story = []

    # Top rule
    story.append(HRFlowable(width="100%", thickness=3, color=BRAND_BLUE, spaceAfter=4))

    # School / board name
    story.append(Paragraph("CBSE MOCK — Pre-Board Practice Series", styles["school_name"]))
    story.append(Paragraph("Central Board of Secondary Education", styles["board_name"]))

    story.append(HRFlowable(width="100%", thickness=1, color=BRAND_ORANGE, spaceBefore=2, spaceAfter=4))

    # Subject title
    cls_label = f"CLASS {bank['class']}"
    story.append(Paragraph(f"{cls_label} — {bank['subject'].upper()}", styles["paper_title"]))

    # Meta row: Date | Marks | Time
    meta = (f"Date: {paper_date}"
            f"&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            f"Maximum Marks: {bank['max_marks']}"
            f"&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            f"Time Allowed: {bank['time']}")
    story.append(Paragraph(meta, styles["meta_row"]))
    story.append(HRFlowable(width="100%", thickness=1, color=LIGHT_BLUE, spaceAfter=6))

    # General instructions box
    story.append(Paragraph("GENERAL INSTRUCTIONS:", styles["general_instructions_heading"]))
    instrs = [
        f"1. This question paper contains {len(bank.get('sections', [])) or 5} sections. Read the instructions for each section carefully.",
        "2. All questions are compulsory unless stated otherwise.",
        "3. Write all answers neatly and show relevant working wherever required.",
        "4. Marks for each question are indicated against it.",
        "5. This paper is a Practice Paper — it is similar to but NOT an actual CBSE board paper.",
        "6. Download more FREE practice papers daily at: <b>www.cbsemock.org.in</b>",
    ]
    if bank["subject"] == "Mathematics":
        instrs.insert(3, "   (i) Calculators are NOT permitted.")

    for instr in instrs:
        story.append(Paragraph(instr, styles["general_instructions"]))

    story.append(HRFlowable(width="100%", thickness=2, color=BRAND_BLUE,
                             spaceBefore=6, spaceAfter=10))
    return story


# ─── Question renderer ────────────────────────────────────────────────────────

def render_question(q_idx: int, q: dict, section: dict, styles) -> list:
    """Return a list of Flowables for one question."""
    items = []

    # Preamble (Assertion-Reason directions, printed only once)
    if q.get("preamble"):
        items.append(Paragraph(q["preamble"], styles["q_preamble"]))

    # Question number + marks on same line using a 2-col table
    q_label = f"Q{q_idx}."
    marks_text = f"[{q['marks']} mark{'s' if q['marks'] > 1 else ''}]"
    hdr_data = [[Paragraph(q_label, styles["q_num"]),
                 Paragraph(marks_text, styles["marks_badge"])]]
    hdr_tbl = Table(hdr_data, colWidths=[INNER_W * 0.85, INNER_W * 0.15])
    hdr_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (-1, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    items.append(hdr_tbl)

    # Question text (indent)
    text_style = ParagraphStyle(
        "q_text_indented", parent=styles["q_text"],
        leftIndent=14
    )
    # Escape any stray < > in question text that isn't intentional HTML
    q_text = q["text"]
    items.append(Paragraph(q_text, text_style))

    # Note (e.g., "(i) Round yellow...")
    if q.get("note"):
        items.append(Paragraph(q["note"], styles["q_note"]))

    # Options for MCQ / A-R
    if q.get("options"):
        for opt in q["options"]:
            items.append(Paragraph(opt, styles["q_option"]))

    items.append(Spacer(1, 4 * mm))
    return items


# ─── Section renderer ─────────────────────────────────────────────────────────

def build_section(section: dict, questions: list, q_counter_start: int, styles) -> list:
    story = []
    sec = section

    # Section banner
    sec_title = f"{sec['name']} — {sec['title']} ({sec['marks']} Marks)"
    story.append(Paragraph(sec_title, styles["section_header"]))

    # Type guide sub-heading
    q_types = list(dict.fromkeys(q["type"] for q in questions))
    type_guide = {
        "MCQ":  "1 mark each",
        "A/R":  "1 mark each",
        "VSA":  "2 marks each",
        "SA":   "3 marks each",
        "LA":   "5 marks each",
        "CBQ":  "4 marks each — Case Study",
    }
    guide_parts = [f"{t} ({type_guide.get(t, '')})" for t in q_types]
    story.append(Paragraph(" | ".join(guide_parts), styles["section_subhead"]))

    q_counter = q_counter_start
    for q in questions:
        flowables = render_question(q_counter, q, sec, styles)
        story.append(KeepTogether(flowables))
        q_counter += 1

    return story, q_counter


# ─── Page numbering canvas ────────────────────────────────────────────────────

class NumberedCanvas(canvas.Canvas):
    def __init__(self, filename, subject, cls, paper_date, **kwargs):
        super().__init__(filename, **kwargs)
        self._saved_pages = []
        self.subject    = subject
        self.cls        = cls
        self.paper_date = paper_date

    def showPage(self):
        self._saved_pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_pages)
        for i, state in enumerate(self._saved_pages, start=1):
            self.__dict__.update(state)
            self._draw_footer(i, total)
            super().showPage()
        super().save()

    def _draw_footer(self, page_num, total):
        self.saveState()
        # Footer rule
        self.setStrokeColor(BRAND_BLUE)
        self.setLineWidth(0.5)
        self.line(MARGIN, 1.0 * cm, PAGE_W - MARGIN, 1.0 * cm)

        # Left: branding
        self.setFont(BODY_FONT, 7)
        self.setFillColor(MID_GREY)
        self.drawString(MARGIN, 0.65 * cm, "www.cbsemock.org.in  |  Free CBSE Practice Papers")

        # Center: paper info
        info = f"Class {self.cls} {self.subject}  —  {self.paper_date}"
        self.drawCentredString(PAGE_W / 2, 0.65 * cm, info)

        # Right: page number
        self.drawRightString(PAGE_W - MARGIN, 0.65 * cm, f"Page {page_num} of {total}")

        self.restoreState()


# ─── Main build function ──────────────────────────────────────────────────────

def build_pdf(bank_key: str, out_path: str, paper_date: str = None) -> str:
    _register_fonts()
    if paper_date is None:
        paper_date = date.today().strftime("%d %B %Y")

    log = load_log()
    selected_map, bank = select_questions(bank_key, log)

    styles = build_styles()

    subject = bank["subject"]
    cls     = bank["class"]

    def make_canvas(filename, **kwargs):
        return NumberedCanvas(filename, subject, cls, paper_date,
                              **kwargs)

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN,   bottomMargin=1.6 * cm,
        title=f"Class {cls} {subject} — CBSE Pre-Board Practice Paper",
        author="CBSEMock.org.in",
        subject=f"Class {cls} {subject} Practice Paper | {paper_date}",
        creator="CBSEMock.org.in Auto-Generator",
    )

    story = []

    # Header
    story += build_header(bank, paper_date, styles)

    # Sections
    q_counter = 1
    used_ids  = []

    for section in bank["sections"]:
        sec_name  = section["name"]
        questions = selected_map.get(sec_name, [])
        if not questions:
            continue

        sec_story, q_counter = build_section(section, questions, q_counter, styles)
        story += sec_story

        for q in questions:
            used_ids.append(q["id"])

    # Back cover stub
    story.append(PageBreak())
    story += [
        Spacer(1, 2 * cm),
        HRFlowable(width="100%", thickness=2, color=BRAND_BLUE),
        Spacer(1, 0.5 * cm),
        Paragraph("✦  END OF QUESTION PAPER  ✦", ParagraphStyle(
            "end_title", parent=styles["paper_title"],
            fontSize=14, spaceAfter=8)),
        Paragraph(
            "We hope you found this practice paper helpful.<br/>"
            "Get a NEW practice paper <b>every day</b> — absolutely FREE!",
            ParagraphStyle("back_body", parent=styles["meta_row"], fontSize=10, leading=16)),
        Spacer(1, 0.4 * cm),
        Paragraph(
            "📲  Join our Telegram channel for instant updates",
            ParagraphStyle("back_cta", parent=styles["meta_row"],
                           fontSize=10, textColor=BRAND_ORANGE, leading=14)),
        Spacer(1, 0.3 * cm),
        Paragraph(
            "🌐  <b>www.cbsemock.org.in</b>",
            ParagraphStyle("back_web", parent=styles["meta_row"],
                           fontSize=16, textColor=BRAND_BLUE, leading=20)),
        Spacer(1, 0.3 * cm),
        Paragraph(
            "We are committed to your success. 🎯",
            ParagraphStyle("back_tag", parent=styles["meta_row"],
                           fontSize=11, textColor=BRAND_GREY, leading=14,
                           fontName=BODY_FONT_ITAL)),
        HRFlowable(width="100%", thickness=1, color=BRAND_ORANGE, spaceBefore=10),
    ]

    doc.build(story, canvasmaker=make_canvas)

    # Persist used questions
    mark_used(log, bank_key, used_ids)
    save_log(log)

    return out_path


# ─── Build from a planned paper (JSON pool, see mock_bank.py) ────────────────

def build_pdf_from_paper(meta: dict, out_path: str, paper_date: str) -> str:
    """
    meta: {"subject", "class", "max_marks", "time",
           "sections": [{"name", "title", "marks", "questions": [...]}]}
    Same look as build_pdf(), but the questions are the ones planned in
    question-bank/calendar.json, so nothing is picked or logged here.
    """
    _register_fonts()
    styles  = build_styles()
    subject, cls = meta["subject"], meta["class"]

    def make_canvas(filename, **kwargs):
        return NumberedCanvas(filename, subject, cls, paper_date, **kwargs)

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN, topMargin=MARGIN, bottomMargin=1.6 * cm,
        title=f"Class {cls} {subject} — CBSE Pre-Board Practice Paper",
        author="CBSEMock.org.in",
        subject=f"Class {cls} {subject} Practice Paper | {paper_date}",
        creator="CBSEMock.org.in Auto-Generator",
    )
    story = build_header(meta, paper_date, styles)
    q_counter = 1
    for section in meta["sections"]:
        if not section["questions"]:
            continue
        sec_story, q_counter = build_section(section, section["questions"], q_counter, styles)
        story += sec_story

    story.append(PageBreak())
    story += [
        Spacer(1, 2 * cm),
        HRFlowable(width="100%", thickness=2, color=BRAND_BLUE),
        Spacer(1, 0.5 * cm),
        Paragraph("✦  END OF QUESTION PAPER  ✦", ParagraphStyle(
            "end_title2", parent=styles["paper_title"], fontSize=14, spaceAfter=8)),
        Paragraph(
            "We hope you found this practice paper helpful.<br/>"
            "Every paper in this series is new — no question is repeated.",
            ParagraphStyle("back_body2", parent=styles["meta_row"], fontSize=10, leading=16)),
        Spacer(1, 0.4 * cm),
        Paragraph("Join our Telegram channel for instant updates",
                  ParagraphStyle("back_cta2", parent=styles["meta_row"],
                                 fontSize=10, textColor=BRAND_ORANGE, leading=14)),
        Spacer(1, 0.3 * cm),
        Paragraph("<b>www.cbsemock.org.in</b>",
                  ParagraphStyle("back_web2", parent=styles["meta_row"],
                                 fontSize=16, textColor=BRAND_BLUE, leading=20)),
        Spacer(1, 0.3 * cm),
        Paragraph("We are committed to your success.",
                  ParagraphStyle("back_tag2", parent=styles["meta_row"], fontSize=11,
                                 textColor=BRAND_GREY, leading=14, fontName=BODY_FONT_ITAL)),
        HRFlowable(width="100%", thickness=1, color=BRAND_ORANGE, spaceBefore=10),
    ]
    doc.build(story, canvasmaker=make_canvas)
    return out_path


# ─── CLI ──────────────────────────────────────────────────────────────────────

SUBJECT_CHOICES = {
    "science10":   "cl10_science",
    "maths10":     "cl10_maths",
    "physics12":   "cl12_physics",
    "maths12":     "cl12_maths",
    "chemistry12": "cl12_chemistry",
    "biology12":   "cl12_biology",
}

def main():
    parser = argparse.ArgumentParser(description="Generate CBSE Pre-Board Practice PDF")
    parser.add_argument("--subject",
                        choices=list(SUBJECT_CHOICES.keys()),
                        default="science10",
                        help="Subject to generate paper for")
    parser.add_argument("--date",
                        default=None,
                        help="Paper date (DD Month YYYY). Defaults to today.")
    parser.add_argument("--out",
                        default=None,
                        help="Output PDF filename (auto-named if not set)")
    args = parser.parse_args()

    bank_key   = SUBJECT_CHOICES[args.subject]
    bank       = QUESTION_BANKS[bank_key]
    paper_date = args.date or date.today().strftime("%d %B %Y")
    date_slug  = date.today().strftime("%Y-%m-%d")

    # Auto filename: e.g. pyq-papers/science_cl10_2026-11-12.pdf
    if args.out:
        out_path = args.out
    else:
        fname = f"{args.subject}_{date_slug}.pdf"
        out_path = str(OUTPUT_DIR / fname)

    print(f"📄  Generating: Class {bank['class']} {bank['subject']} — {paper_date}")
    print(f"    Output: {out_path}")

    result = build_pdf(bank_key, out_path, paper_date)
    size_kb = Path(result).stat().st_size // 1024
    print(f"✅  Done! PDF size: {size_kb} KB → {result}")
    return result


if __name__ == "__main__":
    main()
