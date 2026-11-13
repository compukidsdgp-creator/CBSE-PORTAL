#!/usr/bin/env python3
"""
mock_paper_pdf.py — exam-style PDF for the free mock papers
────────────────────────────────────────────────────────────
Black-and-white question paper in the classic board layout:
Times-style type, Series / Roll No. / Code No. line, centred titles,
boxed General Instructions, ruled section banners, "Q1." numbering with
marks in square brackets on the right, two-column MCQ options and
"— OR —" dividers.

    from mock_paper_pdf import build_mock_pdf
    build_mock_pdf(meta, "paper.pdf", "16 November 2026", paper_id="science10-P01")

`meta` comes from mock_bank.paper_sections(subject_key, ids, raw=True).
"""
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT     = Path(__file__).parent
FONT_DIR = ROOT / "assets" / "fonts"

SERIF, SERIF_B, SERIF_I, SERIF_BI = "MockSerif", "MockSerif-Bold", "MockSerif-Italic", "MockSerif-BoldItalic"
FALLBACK, FALLBACK_B = "MockFallback", "MockFallback-Bold"
_MISSING = None          # characters the main font lacks (drawn with the fallback font)

SUBJECT_CODES = {("Science", "X"): "086", ("Mathematics", "X"): "041", ("Physics", "XII"): "042",
                 ("Chemistry", "XII"): "043", ("Biology", "XII"): "044", ("Mathematics", "XII"): "041"}
SHORT = {"Science": "SCI", "Mathematics": "MATH", "Physics": "PHY", "Chemistry": "CHEM", "Biology": "BIO"}
TYPE_NAMES = {"MCQ": "Multiple Choice", "A/R": "Assertion-Reasoning", "VSA": "Very Short Answer",
              "SA": "Short Answer", "LA": "Long Answer", "CBQ": "Case-Study Based"}
AR_OPTIONS = ["(A) Both A and R are true and R is the correct explanation of A.",
              "(B) Both A and R are true, but R is not the correct explanation of A.",
              "(C) A is true, but R is false.",
              "(D) A is false, but R is true."]
RULE = colors.black
TINT = colors.HexColor("#f4f6f8")


def _register():
    global _MISSING
    if _MISSING is not None:
        return
    files = {SERIF: "LiberationSerif-Regular.ttf", SERIF_B: "LiberationSerif-Bold.ttf",
             SERIF_I: "LiberationSerif-Italic.ttf", SERIF_BI: "LiberationSerif-BoldItalic.ttf",
             FALLBACK: "DejaVuSerif.ttf", FALLBACK_B: "DejaVuSerif-Bold.ttf"}
    for name, fn in files.items():
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / fn)))
    registerFontFamily(SERIF, normal=SERIF, bold=SERIF_B, italic=SERIF_I, boldItalic=SERIF_BI)
    registerFontFamily(FALLBACK, normal=FALLBACK, bold=FALLBACK_B, italic=FALLBACK, boldItalic=FALLBACK_B)
    have = pdfmetrics.getFont(SERIF).face.charToGlyph
    fb   = pdfmetrics.getFont(FALLBACK).face.charToGlyph
    _MISSING = {c for c in range(0x80, 0x3000) if c not in have and c in fb}


def mk(text: str) -> str:
    """Plain text -> paragraph markup: escape, keep line breaks, patch missing glyphs."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = []
    for ch in text:
        out.append(f'<font name="{FALLBACK}">{ch}</font>' if ord(ch) in _MISSING else ch)
    return "".join(out).replace("\n", "<br/>")


def _styles():
    def st(name, **kw):
        kw.setdefault("fontName", SERIF); kw.setdefault("fontSize", 11); kw.setdefault("leading", 14.6)
        kw.setdefault("textColor", colors.black)
        return ParagraphStyle(name, **kw)
    return {
        "top":    st("top", fontName=SERIF_B, fontSize=9.5, leading=12),
        "top_c":  st("top_c", fontName=SERIF_B, fontSize=9.5, leading=12, alignment=TA_CENTER),
        "top_r":  st("top_r", fontName=SERIF_B, fontSize=9.5, leading=12, alignment=TA_RIGHT),
        "h1":     st("h1", fontName=SERIF_B, fontSize=14, leading=18, alignment=TA_CENTER),
        "h2":     st("h2", fontName=SERIF_B, fontSize=11.5, leading=15, alignment=TA_CENTER),
        "h3":     st("h3", fontName=SERIF_B, fontSize=9.5, leading=13, alignment=TA_CENTER),
        "meta_l": st("meta_l", fontName=SERIF_B, fontSize=10.5, leading=13),
        "meta_r": st("meta_r", fontName=SERIF_B, fontSize=10.5, leading=13, alignment=TA_RIGHT),
        "ins_h":  st("ins_h", fontName=SERIF_B, fontSize=9.5, leading=12),
        "ins":    st("ins", fontSize=9.3, leading=12.2, leftIndent=13, firstLineIndent=-13),
        "banner": st("banner", fontName=SERIF_B, fontSize=10.5, leading=13, alignment=TA_CENTER),
        "qn":     st("qn", fontName=SERIF_B),
        "q":      st("q"),
        "opt":    st("opt", fontSize=10.8, leading=14),
        "marks":  st("marks", fontName=SERIF_B, alignment=TA_RIGHT),
        "or":     st("or", fontName=SERIF_BI, alignment=TA_CENTER, spaceBefore=2, spaceAfter=2),
        "dir":    st("dir", fontSize=9.5, leading=12.5),
        "end":    st("end", fontName=SERIF_B, fontSize=10.5, leading=14, alignment=TA_CENTER),
        "end2":   st("end2", fontSize=9.5, leading=13, alignment=TA_CENTER),
    }


def _banner_text(sec, qs):
    letter = sec["name"].split()[-1]
    marks = sorted({q["marks"] for q in qs})
    if len(marks) == 1:
        tail = f"{len(qs)} × {marks[0]} = {len(qs) * marks[0]} MARKS"
    else:
        tail = f"{sec['marks']} MARKS"
    title = sec.get("title", "")
    generic = {"MCQ & Assertion-Reason", "Very Short Answer", "Short Answer", "Long Answer", "Case Study"}
    name = f"SECTION – {letter}" + (f" : {title.upper()}" if title and title not in generic else "")
    return f"{name} ({tail})"


def _instructions(meta, total_q):
    secs = [s for s in meta["sections"] if s["questions"]]
    letters = [s["name"].split()[-1] for s in secs]
    names = ", ".join(letters[:-1]) + " and " + letters[-1] if len(letters) > 1 else letters[0]
    words = {3: "three", 4: "four", 5: "five", 6: "six"}.get(len(secs), str(len(secs)))
    lines = [f"Please check that this question paper contains <b>{total_q} questions</b> divided into {words} sections: <b>Section {names}</b>.",
             "All questions are compulsory. However, internal choices have been provided in some questions. Attempt only one of the choices in such questions."]
    n = 1
    for s in secs:
        qs = s["questions"]; a, z = n, n + len(qs) - 1; n = z + 1
        letter = s["name"].split()[-1]
        marks = sorted({q["marks"] for q in qs})
        kinds = list(dict.fromkeys(q["type"] for q in qs))
        if len(marks) == 1:
            if kinds == ["MCQ", "A/R"] or kinds == ["MCQ"]:
                nm = sum(q["type"] == "MCQ" for q in qs); na = len(qs) - nm
                detail = f"{nm} MCQs" + (f" and {na} Assertion-Reasoning questions" if na else "")
                lines.append(f"<b>Section {letter}</b> consists of {len(qs)} questions (Q.{a} to Q.{z}). Each question carries <b>{marks[0]} Mark</b> ({detail}).")
            else:
                lines.append(f"<b>Section {letter}</b> consists of {len(qs)} {TYPE_NAMES[kinds[0]]} questions (Q.{a} to Q.{z}). Each question carries <b>{marks[0]} Marks</b>.")
        else:
            lines.append(f"<b>Section {letter}</b> ({s.get('title', '')}) consists of {len(qs)} questions (Q.{a} to Q.{z}) carrying <b>{s['marks']} Marks</b> in all. The marks for each question are shown against it.")
    lines.append("This is a practice paper prepared by <b>CBSEMock.org.in</b> on the CBSE pattern. It is not an official CBSE question paper.")
    return lines


def _options_block(options, st, width):
    paras = [Paragraph(mk(o), st["opt"]) for o in options]
    if all(len(o) <= 40 for o in options):
        t = Table([[paras[0], paras[1]], [paras[2], paras[3]]], colWidths=[width / 2, width / 2])
    else:
        t = Table([[p] for p in paras], colWidths=[width])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _question(q, num, st, widths):
    wn, wb, wm = widths
    text = q["text"]
    if q["type"] == "A/R":
        text = mk(text).replace("Assertion (A):", "<b>Assertion (A):</b>").replace("Reason (R):", "<b>Reason (R):</b>")
        parts = [text]
    else:
        parts = [mk(p.strip()) for p in re.split(r"\n\s*OR\s*\n", text)]
    rows = [[Paragraph(f"Q{num}.", st["qn"]), Paragraph(parts[0], st["q"]), Paragraph(f"[{q['marks']}]", st["marks"])]]
    if q.get("options"):
        rows.append(["", _options_block(q["options"], st, wb - 6), ""])
    for p in parts[1:]:
        rows.append(["", Paragraph("— OR —", st["or"]), ""])
        rows.append(["", Paragraph(p, st["q"]), ""])
    t = Table(rows, colWidths=[wn, wb, wm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (1, 0), (1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                           ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))
    return t


def build_mock_pdf(meta: dict, out_path: str, paper_date: str, paper_id: str = "") -> str:
    _register()
    st = _styles()
    subject, cls = meta["subject"], meta["class"]
    code = SUBJECT_CODES.get((subject, cls), "")
    setno = (re.search(r"P(\d+)$", paper_id or "") or [None, "1"])[1].lstrip("0") or "1"
    short = SHORT.get(subject, subject[:4].upper())
    margin = 17 * mm
    width = A4[0] - 2 * margin
    foot = f"CBSEMock.org.in  •  Class {cls} {subject}  •  Practice Paper Set {setno}  •  {paper_date}"

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont(SERIF, 8.5)
        canvas.setFillColor(colors.HexColor("#333333"))
        canvas.drawString(margin, 9 * mm, foot)
        canvas.drawRightString(A4[0] - margin, 9 * mm, f"Page {doc.page}")
        canvas.setLineWidth(0.5)
        canvas.line(margin, 12.5 * mm, A4[0] - margin, 12.5 * mm)
        canvas.restoreState()

    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=margin, rightMargin=margin,
                            topMargin=15 * mm, bottomMargin=17 * mm,
                            title=f"Class {cls} {subject} — Pre-Board Practice Paper Set {setno}",
                            author="CBSEMock.org.in",
                            subject=f"Class {cls} {subject} practice paper, {paper_date}")
    story = []
    total_q = sum(len(s["questions"]) for s in meta["sections"])

    # ── Top line and titles ──────────────────────────────────────────────────
    top = Table([[Paragraph(f"Series: CBSEMOCK-{cls}-{short}-SET-{setno}", st["top"]),
                  Paragraph("Roll No.: ____________________", st["top_c"]),
                  Paragraph(f"Code No. {code or short}/{cls}/PRE-{int(setno):02d}", st["top_r"])]],
                colWidths=[width * 0.36, width * 0.32, width * 0.32])
    top.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [top,
              Paragraph("CBSEMOCK.ORG.IN — FREE MOCK PAPER SERIES", st["h1"]),
              Paragraph(f"PRE-BOARD PRACTICE EXAMINATION (CBSE PATTERN) — CLASS {cls}", st["h2"]),
              Paragraph(f"<u>{subject.upper()}" + (f" (SUBJECT CODE: {code})" if code else "") + "</u>", st["h2"]),
              Paragraph(f"PRACTICE QUESTION PAPER — SET {setno}", st["h3"]),
              Spacer(1, 5)]
    tm = Table([[Paragraph(f"Time Allowed: {meta['time']}", st["meta_l"]),
                 Paragraph(f"Maximum Marks: {meta['max_marks']}", st["meta_r"])]], colWidths=[width / 2, width / 2])
    tm.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    story += [tm, Spacer(1, 5)]

    # ── General instructions box ─────────────────────────────────────────────
    ins = [Paragraph("<u>General Instructions:</u>", st["ins_h"]), Spacer(1, 2)]
    ins += [Paragraph(f"{i}. {t}", st["ins"]) for i, t in enumerate(_instructions(meta, total_q), 1)]
    box = Table([[ins]], colWidths=[width])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, RULE), ("BACKGROUND", (0, 0), (-1, -1), TINT),
                             ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                             ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [box, Spacer(1, 4)]

    # ── Sections ─────────────────────────────────────────────────────────────
    widths = (11 * mm, width - 11 * mm - 10 * mm, 10 * mm)
    n = 1
    for sec in meta["sections"]:
        qs = sec["questions"]
        if not qs:
            continue
        banner = Table([[Paragraph(mk(_banner_text(sec, qs)), st["banner"])]], colWidths=[width])
        banner.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), 1.3, RULE), ("LINEBELOW", (0, 0), (-1, -1), 1.3, RULE),
                                    ("BACKGROUND", (0, 0), (-1, -1), TINT),
                                    ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        ar_nums = [n + k for k, q in enumerate(qs) if q["type"] == "A/R"]
        first = True
        for k, q in enumerate(qs):
            block = []
            if first:
                block += [Spacer(1, 8), banner, Spacer(1, 7)]; first = False
            if q["type"] == "A/R" and ar_nums and (n + k) == ar_nums[0]:
                rng = f"Q.{ar_nums[0]}" + (f" to Q.{ar_nums[-1]}" if len(ar_nums) > 1 else "")
                d = [Paragraph(f"<b>Directions ({rng}):</b> In the following question{'s' if len(ar_nums) > 1 else ''}, a statement of "
                               f"Assertion (A) is followed by a statement of Reason (R). Choose the correct option:", st["dir"])]
                d += [Paragraph(mk(o), st["dir"]) for o in AR_OPTIONS]
                dbox = Table([[d]], colWidths=[width])
                dbox.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#555555"), None, (2, 2)),
                                          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
                block += [dbox, Spacer(1, 6)]
            block.append(_question(q, n + k, st, widths))
            story.append(KeepTogether(block))
        n += len(qs)

    # ── End ──────────────────────────────────────────────────────────────────
    end = Table([[[Paragraph("— END OF QUESTION PAPER —", st["end"]),
                   Paragraph("New free mock papers for Class X and XII every Monday, Wednesday and Friday at "
                             "<b>www.cbsemock.org.in</b>. Every paper is new — no question is repeated.", st["end2"])]]],
                colWidths=[width])
    end.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), 1.3, RULE), ("TOPPADDING", (0, 0), (-1, -1), 6)]))
    story += [Spacer(1, 10), KeepTogether([end])]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return out_path
