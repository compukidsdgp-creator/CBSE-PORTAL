"""Home-page showcase for the Mistake Bank reels: a strip with the latest reel as two cascading phone cards
(English in front, Hindi behind) that fan out on hover/tap. Idempotent block <!-- MISTAKE-STRIP:START/END -->.
    python3 mistake_links.py
"""
import html as H
import re
from pathlib import Path

import generate_mistake_reel as G
import mistake_bank as MB

ROOT = Path(__file__).resolve().parent
A, B = "<!-- MISTAKE-STRIP:START -->", "<!-- MISTAKE-STRIP:END -->"
E = H.escape


def latest():
    """Newest posted reel; before the first post, the first approved one."""
    posted, appr = MB.jload("posted.json"), MB.jload("approvals.json")
    specs = G.load_specs()
    done = [r for r in specs if any(f"{MB.key(r)}/{l}" in posted for l in r["lang"])]
    if done:
        return done[-1], posted
    ok = [r for r in specs if MB.state(r, appr) == "approved"]
    return (ok[0] if ok else None), posted


def strip():
    r, posted = latest()
    if not r:
        return ""
    def card(lang, cls, label):
        info = posted.get(f"{MB.key(r)}/{lang}", {})
        href = info.get("ig_link") or "mistake-bank/"
        thumb = G.thumb_path(r, lang).relative_to(ROOT).as_posix()
        ext = ' target="_blank" rel="noopener"' if info.get("ig_link") else ""
        return (f'<a class="mbh-ph {cls}" href="{E(href)}"{ext} aria-label="Watch Mistake Bank #{r["number"]} in {label}">'
                f'<span class="sc" style="background-image:url({thumb})"></span><span class="nt"></span>'
                f'<span class="pl" aria-hidden="true">▶</span><span class="lg">{label}</span></a>')
    t_en, t_hi = r["lang"]["en"]["title"], r["lang"].get("hi", {}).get("title", "")
    return f"""{A}
<style>
.mbh{{max-width:1100px;margin:26px auto 10px;padding:0 20px}}
.mbh-box{{position:relative;overflow:hidden;border-radius:22px;padding:26px 28px;display:grid;grid-template-columns:1.1fr .9fr;gap:20px;align-items:center;
 background:radial-gradient(700px 400px at 85% 50%,rgba(255,84,112,.28),transparent 60%),linear-gradient(135deg,#3b0a16,#0f2347 65%);border:2px solid #ff5470;color:#fff;box-shadow:0 10px 26px rgba(15,35,71,.25)}}
.mbh-tag{{display:inline-flex;align-items:center;gap:8px;background:#e11d48;font:800 .74rem Inter,sans-serif;letter-spacing:.08em;padding:6px 12px;border-radius:99px}}
.mbh-tag em{{font-style:normal;background:#ffd600;color:#0f2347;border-radius:8px;padding:1px 7px}}
.mbh h2{{font-family:'Crimson Pro',serif;font-size:clamp(1.5rem,3vw,2.05rem);line-height:1.15;margin:12px 0 8px;color:#fff}}
.mbh p{{color:rgba(255,255,255,.85);font-size:.92rem;margin:0 0 12px;max-width:520px}}
.mbh-now{{font-size:.86rem;color:#ffd0d8;margin-bottom:14px}}.mbh-now b{{color:#ffe4a0}}
.mbh-cta{{display:inline-flex;align-items:center;min-height:42px;padding:10px 20px;border-radius:99px;background:#ffd23f;color:#0f2347;font-weight:800;font-size:.82rem;text-decoration:none;transition:transform .2s,box-shadow .2s}}
.mbh-cta:hover{{transform:translateY(-3px);box-shadow:0 8px 18px rgba(255,210,63,.4)}}
.mbh-stack{{position:relative;height:330px;perspective:1200px}}
.mbh-ph{{position:absolute;top:10px;width:168px;height:300px;border-radius:26px;padding:7px;background:#0b0f1a;box-shadow:0 22px 40px rgba(0,0,0,.5),0 0 0 2px rgba(255,255,255,.18) inset;
 text-decoration:none;color:#fff;transition:transform .45s cubic-bezier(.2,.8,.2,1.2),box-shadow .3s}}
.mbh-ph .sc{{position:absolute;inset:7px;border-radius:20px;background:#111 center/cover no-repeat}}
.mbh-ph .nt{{position:absolute;top:12px;left:50%;width:54px;height:12px;margin-left:-27px;border-radius:10px;background:#0b0f1a}}
.mbh-ph .pl{{position:absolute;left:50%;top:50%;width:58px;height:58px;margin:-29px 0 0 -29px;border-radius:50%;background:rgba(255,255,255,.92);color:#e11d48;display:flex;align-items:center;justify-content:center;font-size:24px;padding-left:4px;box-shadow:0 6px 18px rgba(0,0,0,.4)}}
.mbh-ph .lg{{position:absolute;left:12px;bottom:14px;background:#ffd23f;color:#0f2347;font:800 .78rem Inter,Poppins,sans-serif;padding:5px 10px;border-radius:99px}}
.mbh-ph.hi{{left:calc(50% - 30px);transform:rotate(9deg) translateZ(-40px);animation:mbhB 4s ease-in-out infinite}}
.mbh-ph.en{{left:calc(50% - 150px);transform:rotate(-7deg);z-index:2;animation:mbhF 4s ease-in-out infinite}}
@keyframes mbhF{{50%{{transform:rotate(-7deg) translateY(-8px)}}}}@keyframes mbhB{{50%{{transform:rotate(9deg) translateY(6px) translateZ(-40px)}}}}
.mbh-stack:hover .mbh-ph,.mbh-stack:focus-within .mbh-ph{{animation:none}}
.mbh-stack:hover .mbh-ph.en,.mbh-stack:focus-within .mbh-ph.en{{transform:rotate(-12deg) translateX(-40px) translateY(-6px)}}
.mbh-stack:hover .mbh-ph.hi,.mbh-stack:focus-within .mbh-ph.hi{{transform:rotate(12deg) translateX(40px) translateY(-6px)}}
.mbh-ph:hover{{box-shadow:0 26px 48px rgba(0,0,0,.55),0 0 0 3px #ffd23f inset;z-index:3}}
@media(max-width:760px){{.mbh{{padding:0 14px}}.mbh-box{{grid-template-columns:1fr;padding:20px}}.mbh-stack{{height:290px}}.mbh-ph{{width:146px;height:260px}}
 .mbh-ph.en{{left:calc(50% - 140px)}}.mbh-ph.hi{{left:calc(50% - 8px)}}.mbh-cta{{width:100%;justify-content:center}}}}
@media(prefers-reduced-motion:reduce){{.mbh-ph{{animation:none!important;transition:none}}}}
</style>
<section class="mbh" aria-label="Mistake Bank reels"><div class="mbh-box">
<div><span class="mbh-tag">⚠ MISTAKE BANK <em>NEW</em></span>
<h2>Top board-exam mistakes, fixed in 20 seconds</h2>
<p>What students write, why it loses marks, and what to write instead — a new reel every day in <b>English</b> and <b>हिंदी</b>.</p>
<div class="mbh-now">Latest: <b>#{r['number']:02d} · {E(t_en)}</b>{(' · ' + E(t_hi)) if t_hi else ''}</div>
<a class="mbh-cta" href="mistake-bank/">WATCH ALL MISTAKES →</a></div>
<div class="mbh-stack">{card('hi', 'hi', 'हिंदी')}{card('en', 'en', 'English')}</div>
</div></section>
{B}"""


def home():
    f = ROOT / "index.html"
    s = f.read_text(encoding="utf-8")
    o = s
    s = re.sub(re.escape(A) + r".*?" + re.escape(B) + r"\n\n", "", s, flags=re.S)
    blk = strip()
    if blk:
        anchor = "<!-- LEARN-STRIP:START -->"
        s = s.replace(anchor, blk + "\n\n" + anchor, 1) if anchor in s else s
    if s != o:
        f.write_text(s, encoding="utf-8")
    print(f"[mistake-links] home {'updated' if s != o else 'unchanged'}")


if __name__ == "__main__":
    home()
