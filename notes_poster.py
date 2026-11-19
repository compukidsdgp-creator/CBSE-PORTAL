"""Designed cover/poster for a chapter-notes page (1080×1350): subject theme colours, a faint pattern of the
subject's own symbols, the chapter number as a big outlined numeral, the title, a 'notebook page' card showing one
of the chapter's real diagrams, stat tiles and a gold call to action. Rendered from HTML with Playwright.
    python3 notes_poster.py [chapter-id ...]      (all live chapters when no id is given)
"""
import html as H
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "assets" / "fonts"
E = H.escape

THEMES = {   # bg1, bg2, accent, symbols
    "science":   ("#0d4f4a", "#0b1d3a", "#5eead4", ["H₂O", "pH", "CO₂", "→", "NaCl", "O₂", "⚗", "Δ", "ATP", "e⁻", "Fe", "λ"]),
    "chemistry": ("#4a1d6e", "#0f1a3a", "#d8b4fe", ["mol", "ΔH", "⇌", "K꜀", "pH", "e⁻", "C₆H₆", "→", "Eᵒ", "sp³", "NH₃", "k"]),
    "physics":   ("#0b4a7a", "#071a33", "#7dd3fc", ["F=ma", "V=IR", "λ", "Ω", "∮", "E", "B", "ħ", "1/f", "μ", "θ", "c"]),
    "biology":   ("#1d5c2e", "#0b1d2a", "#86efac", ["DNA", "RNA", "ATP", "2n", "n", "🧬", "XY", "mRNA", "Aa", "O₂", "CO₂", "♀"]),
    "maths":     ("#3b2a8a", "#0d1638", "#fcd34d", ["π", "∑", "√", "∫", "x²", "θ", "Δ", "∞", "a/b", "≈", "sin", "dy/dx"]),
    "social-science": ("#7a3b12", "#1a1530", "#fdba74", ["🌍", "⚖", "₹", "🗳", "1857", "GDP", "🏛", "⛰", "🌾", "📜", "N", "🧭"]),
    "english":   ("#7a1d3b", "#1a1030", "#f9a8d4", ["Aa", "“ ”", "¶", "—", "!", "?", "…", "§", "&", ";", "ABC", "✎"]),
}
DEFAULT = ("#1a3a6b", "#0f2347", "#e8cc6a", ["✦", "★", "✎", "→", "✓", "Δ", "π", "λ", "∑", "Ω", "∞", "#"])


def pick_diagram(ch):
    """The most colourful diagram makes the most eye-catching hero."""
    best, score = None, -1
    for k, cap, svg in ch.get("diagrams", []):
        cols = len(set(re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]{3,6})"', svg)))
        if cols > score:
            best, score = (k, cap, svg), cols
    return best


def font_face():
    faces = [("Inter", "Inter-Regular.otf", 400), ("Inter", "Inter-Bold.otf", 800), ("Poppins", "Poppins-Bold.ttf", 700),
             ("Poppins", "Poppins-Medium.ttf", 500), ("Serif", "DejaVuSerif-Bold.ttf", 700)]
    return "".join(f"@font-face{{font-family:'{n}';src:url('{(FONTS / f).as_uri()}');font-weight:{w}}}" for n, f, w in faces)


def poster_html(ch):
    bg1, bg2, acc, syms = THEMES.get(ch["subject_slug"], DEFAULT)
    num = int(ch["number"])
    diag = pick_diagram(ch)
    svg = re.sub(r"<title[^>]*>.*?</title>", "", diag[2].strip(), flags=re.S) if diag else ""
    svg = re.sub(r"<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', svg, count=1)
    cap = diag[1] if diag else ""
    # scattered symbol pattern (deterministic positions)
    pat = ""
    for i in range(34):
        x = (i * 263) % 1040 + 10
        y = (i * 389) % 1300 + 20
        r = (i * 37) % 50 - 25
        sz = 30 + (i * 13) % 34
        pat += f'<span style="left:{x}px;top:{y}px;font-size:{sz}px;transform:rotate({r}deg)">{E(syms[i % len(syms)])}</span>'
    stats = [(len(ch.get("diagrams", [])), "Labelled<br>diagrams"), (len(ch.get("worked", [])), "Worked board<br>questions"),
             (len(ch.get("mistakes", [])), "Common<br>mistakes"), (len(ch.get("revision", [])), "Quick-revision<br>points")]
    tiles = "".join(f'<div class="t"><b>{n}</b><span>{l}</span></div>' for n, l in stats)
    title = E(ch["title"])
    tsize = 92 if len(ch["title"]) <= 22 else 80 if len(ch["title"]) <= 34 else 68
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_face()}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Inter,sans-serif;color:#fff;position:relative;background:
 radial-gradient(900px 700px at 85% 8%,{acc}33,transparent 60%),
 radial-gradient(800px 600px at 0% 100%,#c9a22733,transparent 60%),
 linear-gradient(160deg,{bg1} 0%,{bg2} 70%)}}
.pat span{{position:absolute;font-family:Serif,serif;color:#fff;opacity:.06;white-space:nowrap}}
.grain{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:6px 6px}}
.top{{position:absolute;left:70px;right:70px;top:62px;display:flex;justify-content:space-between;align-items:center}}
.logo{{font:800 40px Inter;letter-spacing:-.5px}}.logo b{{color:#e8cc6a}}
.pill{{font:800 24px Inter;letter-spacing:.08em;background:#e8cc6a;color:#0f2347;padding:12px 24px;border-radius:99px}}
.num{{position:absolute;right:30px;top:120px;font:700 520px/1 Poppins;color:transparent;-webkit-text-stroke:3px {acc}55;letter-spacing:-20px}}
.head{{position:absolute;left:70px;top:172px;width:900px;max-height:400px;display:flex;flex-direction:column;gap:10px}}
.eyebrow{{font:800 26px Inter;letter-spacing:.22em;color:{acc}}}
.ch{{font:500 34px Poppins;color:rgba(255,255,255,.8);margin-bottom:6px}}
.title{{font:700 {tsize}px/1.04 Poppins;letter-spacing:-1.5px;text-shadow:0 6px 24px rgba(0,0,0,.35)}}
.title::after{{content:"";display:block;width:150px;height:8px;border-radius:8px;background:linear-gradient(90deg,#e8cc6a,{acc});margin-top:26px}}
.stack{{position:absolute;left:150px;top:610px;width:780px;height:440px}}
.sheet{{position:absolute;inset:0;border-radius:18px}}
.s1{{background:{acc};opacity:.35;transform:rotate(5deg) translate(18px,10px)}}
.s2{{background:#fdf8ea;transform:rotate(2.2deg) translate(8px,4px);box-shadow:0 20px 40px rgba(0,0,0,.3)}}
.page{{position:absolute;inset:0;background:#fff;border-radius:18px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.45);overflow:hidden;
 background-image:linear-gradient(#eef2f7 1px,transparent 1px);background-size:100% 34px}}
.page .hd{{height:58px;background:linear-gradient(90deg,#0f2347,#1a3a6b);display:flex;align-items:center;justify-content:space-between;padding:0 26px;color:#ffe4a0;font:800 20px Inter;letter-spacing:.06em}}
.page .hd i{{font-style:normal;color:#fff;opacity:.75;font-weight:600;letter-spacing:0}}
.page .fig{{position:absolute;left:30px;right:30px;top:76px;bottom:52px;display:flex;align-items:center;justify-content:center}}
.page .fig svg{{width:100%;height:100%}}
.page .cap{{position:absolute;left:30px;right:30px;bottom:14px;font:600 18px Inter;color:#334155;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.clip{{position:absolute;left:640px;top:586px;width:46px;height:120px;border:7px solid #e8cc6a;border-radius:30px;transform:rotate(14deg);box-shadow:0 4px 8px rgba(0,0,0,.3)}}
.tiles{{position:absolute;left:70px;right:70px;top:1092px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.t{{background:rgba(255,255,255,.09);border:1.5px solid rgba(255,255,255,.22);border-radius:18px;padding:12px 16px;display:flex;align-items:center;gap:12px}}
.t b{{font:700 50px/1 Poppins;color:#e8cc6a}}.t span{{font:600 17px/1.2 Inter;color:rgba(255,255,255,.88)}}
.cta{{position:absolute;left:70px;right:70px;top:1210px;height:92px;border-radius:46px;background:linear-gradient(90deg,#e8cc6a,#c9a227);display:flex;align-items:center;justify-content:space-between;padding:0 18px 0 40px;box-shadow:0 10px 0 rgba(0,0,0,.25)}}
.cta b{{font:800 34px Inter;color:#0f2347;letter-spacing:.02em}}.cta span{{font:800 26px Inter;color:#e8cc6a;background:#0f2347;border-radius:40px;padding:16px 26px}}
.free{{position:absolute;left:72px;top:568px;font:800 22px Inter;letter-spacing:.14em;color:#0f2347;background:{acc};padding:8px 16px;border-radius:10px;transform:rotate(-4deg);box-shadow:0 6px 14px rgba(0,0,0,.3);z-index:3}}
</style></head><body>
<div class="pat">{pat}</div><div class="grain"></div>
<div class="num">{num:02d}</div>
<div class="top"><div class="logo">CBSE<b>Mock</b></div><div class="pill">CLASS {E(str(ch['class']))} · {E(ch['subject'].upper())}</div></div>
<div class="head"><div class="eyebrow">FULL CHAPTER NOTES</div><div class="ch">Chapter {num}</div><div class="title">{title}</div></div>
<div class="free">NEW · FREE</div>
<div class="stack"><div class="sheet s1"></div><div class="sheet s2"></div>
 <div class="page"><div class="hd">CHAPTER {num} NOTES <i>cbsemock.org.in</i></div><div class="fig">{svg}</div><div class="cap">{E(cap)}</div></div></div>
<div class="clip"></div>
<div class="tiles">{tiles}</div>
<div class="cta"><b>Read the full notes free</b><span>cbsemock.org.in →</span></div>
</body></html>"""


def render(ch, out):
    from playwright.sync_api import sync_playwright
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".html")
    tmp.write_text(poster_html(ch), encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(300)
        png = out.with_suffix(".png")
        pg.screenshot(path=str(png))
        b.close()
    tmp.unlink()
    from PIL import Image
    Image.open(png).convert("RGB").save(out, quality=90, optimize=True)
    png.unlink()
    return out


if __name__ == "__main__":
    from notes_pages import load_chapters
    from announce_notes import poster_path
    want = set(sys.argv[1:])
    for ch in load_chapters():
        if (want and ch["_id"] not in want) or (not want and ch.get("status") != "live"):
            continue
        print("[poster]", render(ch, poster_path(ch)).relative_to(ROOT))
