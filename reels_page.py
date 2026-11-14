#!/usr/bin/env python3
"""
reels_page.py — builds the two 3D reel showcase pages:

    /formula-reels/   voiced Formula Flash reels  (formula-posts/videos/queue + posted)
    /why-reels/       WHY? series reels           (formula-posts/why/queue + posted)

The videos are NOT copied (the repo is already large): each page points at the file
where it currently lives. Small poster images are made once per reel in <page>/thumb/.
Run it again whenever reels move between queue/ and posted/ — the posting workflows do.

    python3 reels_page.py
"""
import importlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def poster(src: Path, dest: Path, at=0.42):
    if dest.exists():
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(src)], capture_output=True, text=True, timeout=60).stdout.strip() or 20)
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur * at:.2f}", "-i", str(src), "-frames:v", "1",
                            "-vf", "scale=360:-2", "-q:v", "5", str(dest)], capture_output=True, timeout=120)
        return r.returncode == 0 and dest.exists()
    except Exception as e:                    # no ffmpeg / broken file: page still works, just no poster
        print(f"[WARN] poster for {src.name}: {e}")
        return False


def find(folder_queue: Path, folder_posted: Path, pattern="*.mp4"):
    out = {}
    for d in (folder_posted, folder_queue):            # queue wins if a name exists in both
        if d.is_dir():
            for f in sorted(d.glob(pattern)):
                out[f.name] = f
    return out


# ── Formula Flash reels ──────────────────────────────────────────────────────
def formula_items():
    from formula_topics_master import TOPICS
    from generate_formula_reel_v3 import split_rows, queue_name, class_label
    files = find(ROOT / "formula-posts/videos/queue", ROOT / "formula-posts/videos/posted")
    items = []
    for tid, d in TOPICS.items():
        n = len(split_rows(d["rows"]))
        for p in range(1, n + 1):
            name = queue_name(tid, p, n)
            if name not in files:
                continue
            subj = {"Mathematics": "Maths", "CS": "CS"}.get(d["subject"], d["subject"])
            title = f"{d['title_line1']} {d['title_line2']}".replace("— ", "").replace("Electro- chemistry", "Electrochemistry")
            title = re.sub(r"\s+", " ", title).strip()
            cls = class_label(d.get("chapter_tag", "")).replace("Class ", "")
            items.append({"id": Path(name).stem, "title": title + (f" · Part {p}" if n > 1 else ""),
                          "cat": subj, "cls": cls if cls in ("10", "12") else "",
                          "src": str(files[name].relative_to(ROOT))})
    import hashlib                      # fixed shuffle so subjects are mixed in the stack
    items.sort(key=lambda d: hashlib.md5(d["id"].encode()).hexdigest())
    return items


# ── WHY? reels ───────────────────────────────────────────────────────────────
WHY_CAT = [("AI", "AI"), ("Computer Science", "CS"), ("Maths", "Maths"), ("Physics", "Science"), ("Science", "Science")]


def why_items():
    files = find(ROOT / "formula-posts/why/queue", ROOT / "formula-posts/why/posted")
    items = []
    for name, f in files.items():
        m = re.match(r"(\d+)_why_(.+)\.mp4$", name)
        if not m:
            continue
        slug = m.group(2)
        title, cat, cls = slug.replace("_", " ").capitalize(), "Science", ""
        try:
            parts, mod = slug.split("_"), None
            for k in range(len(parts), 0, -1):          # 01_why_circle_area_pi_r_squared -> why_reels.circle_area
                try:
                    mod = importlib.import_module("why_reels." + "_".join(parts[:k]))
                    break
                except ModuleNotFoundError:
                    continue
            if mod is None:
                raise ModuleNotFoundError(slug)
            first = mod.CAPTION.strip().splitlines()[0]
            title = first.split("WHY? —", 1)[-1].strip() or title
            tags = getattr(mod, "TAGS", "")
            cat = next((v for k, v in WHY_CAT if k in tags), cat)
            cls = "10" if "Class 10" in tags else ("12" if "Class 12" in tags else "")
        except Exception as e:
            print(f"[WARN] {slug}: {e}")
        items.append({"id": f"{m.group(1)}-{slug}", "n": int(m.group(1)), "title": title, "cat": cat, "cls": cls,
                      "src": str(f.relative_to(ROOT))})
    items.sort(key=lambda d: d["n"])
    return items


PAGES = {
    "formula-reels": {
        "items": formula_items, "title": "Formula Reels", "accent": "#2ad4ff",
        "h1": 'Formula <span>Reels</span>',
        "lead": "__COUNT__ voiced formula reels for Class 10 &amp; 12. Swipe the stack, tap a reel to play.",
        "meta": "Watch __COUNT__ free voiced CBSE formula reels for Class 10 and 12 — Physics, Chemistry, Maths, Biology and CS — on a 3D reel wall.",
        "cats": ["Physics", "Chemistry", "Maths", "Biology", "CS"],
    },
    "why-reels": {
        "items": why_items, "title": "WHY? Reels", "accent": "#ffd23f",
        "h1": 'WHY? <span>Reels</span>',
        "lead": "__COUNT__ animated answers to the \"why\" behind Maths, Science, AI and Computer Science. New every Sunday &amp; Wednesday.",
        "meta": "Watch __COUNT__ free animated WHY? reels — why formulas work in Maths, Science, AI and Computer Science for CBSE Class 10 and 12.",
        "cats": ["Maths", "Science", "AI", "CS"],
    },
}


def build(slug, cfg):
    out = ROOT / slug
    items = cfg["items"]()
    keep = set()
    for it in items:
        th = out / "thumb" / f"{it['id']}.jpg"
        it["thumb"] = f"thumb/{it['id']}.jpg" if poster(ROOT / it["src"], th) else ""
        it["src"] = "../" + it["src"]
        keep.add(th.name)
    for f in (out / "thumb").glob("*.jpg") if (out / "thumb").is_dir() else []:
        if f.name not in keep:
            f.unlink()
    cats = [cc for cc in cfg["cats"] if any(i["cat"] == cc for i in items)]
    html = (TEMPLATE.replace("__TITLE__", cfg["title"]).replace("__H1__", cfg["h1"])
            .replace("__LEAD__", cfg["lead"]).replace("__META__", cfg["meta"]).replace("__ACCENT__", cfg["accent"])
            .replace("__SLUG__", slug).replace("__DATA__", json.dumps(items, ensure_ascii=False, separators=(",", ":")))
            .replace("__CATS__", json.dumps(cats)).replace("__COUNT__", str(len(items))))
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    print(f"[reels] /{slug}/  {len(items)} reels")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — Free CBSE Video Reels in 3D | CBSEMock</title>
<meta name="description" content="__META__">
<link rel="canonical" href="https://cbsemock.org.in/__SLUG__/">
<meta property="og:title" content="__TITLE__ | CBSEMock">
<meta property="og:description" content="__META__">
<meta property="og:url" content="https://cbsemock.org.in/__SLUG__/">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0a1730">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<style>
:root{--ink:#0a1730;--ink2:#0f2347;--acc:__ACCENT__;--gold:#e8cc6a;--text:#eef2fb;--muted:#9fb0cf;--line:rgba(255,255,255,.14);
  --Physics:#5cb8ff;--Chemistry:#ff8f8f;--Maths:#ffd43b;--Biology:#6fdc8c;--CS:#63e6e2;--AI:#c6a2ff;--Science:#5cb8ff}
*{box-sizing:border-box}
body{margin:0;background:var(--ink);color:var(--text);font-family:'Inter',system-ui,Arial,sans-serif;line-height:1.5;overflow-x:hidden}
a{color:inherit}button{font:inherit;color:inherit}
.top{padding:14px 16px;position:relative;z-index:5}
.top-in{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px}
.brand{font-weight:700;font-size:1.05rem;text-decoration:none;color:#fff}.brand b{color:var(--gold)}
.back{font-size:.82rem;text-decoration:none;border:1px solid rgba(255,255,255,.3);border-radius:20px;padding:5px 14px;color:#fff;white-space:nowrap}
.back:hover{background:var(--gold);color:var(--ink2);border-color:var(--gold)}
.sky{position:relative;background:radial-gradient(1200px 520px at 50% -8%,#28509a 0%,rgba(40,80,154,0) 62%),linear-gradient(180deg,#0f2347 0%,#0a1730 78%);overflow:hidden}
.sky:before{content:"";position:absolute;inset:auto -20% 0 -20%;height:46%;pointer-events:none;
  background-image:linear-gradient(rgba(232,204,106,.2) 1px,transparent 1px),linear-gradient(90deg,rgba(232,204,106,.2) 1px,transparent 1px);
  background-size:56px 56px;transform:perspective(520px) rotateX(64deg);transform-origin:50% 100%;
  -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 55%);mask-image:linear-gradient(180deg,transparent 0%,#000 55%)}
.hero{text-align:center;padding:6px 16px 0;position:relative;z-index:2}
.hero h1{font-family:'Crimson Pro',Georgia,serif;font-size:clamp(2rem,6.4vw,3.3rem);margin:0;line-height:1.05}
.hero h1 span{color:var(--acc)}
.hero p{margin:8px auto 0;max-width:580px;color:var(--muted);font-size:.95rem}
.chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:16px auto 0;max-width:760px}
.chips button{border:1px solid var(--line);background:rgba(255,255,255,.06);border-radius:20px;padding:6px 14px;font-size:.82rem;font-weight:600;cursor:pointer}
.chips button:hover{border-color:var(--acc)}
.chips button.on{background:var(--acc);border-color:var(--acc);color:var(--ink2)}
.stage{--cw:min(52vw,260px);--dx:34px;--dy:36px;--dz:120px;position:relative;z-index:2;height:calc(var(--cw)*1.78 + 150px);
  perspective:1300px;perspective-origin:50% 36%;touch-action:pan-y;user-select:none;-webkit-user-select:none;cursor:grab;outline:none}
.deck{position:absolute;left:50%;top:120px;width:0;height:0;transform-style:preserve-3d;
  transform:translateX(calc(var(--dx)*-1.3)) rotateX(var(--rx,6deg)) rotateY(var(--ry,-15deg));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.fc{position:absolute;left:calc(var(--cw)/-2);top:0;width:var(--cw);aspect-ratio:9/16;border-radius:16px;overflow:hidden;background:#101f3f;
  border:1px solid rgba(255,255,255,.22);box-shadow:0 26px 46px rgba(0,0,0,.5);will-change:transform,opacity;
  transition:transform .62s cubic-bezier(.2,.75,.2,1),opacity .5s ease,filter .5s ease}
.fc img{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.fc:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(120deg,rgba(255,255,255,.18) 0%,rgba(255,255,255,0) 32%)}
.fc .pl{position:absolute;left:50%;top:50%;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;background:rgba(10,23,48,.72);
  border:2px solid rgba(255,255,255,.85);display:grid;place-items:center;opacity:0;transition:opacity .3s}
.fc .pl:before{content:"";border-left:20px solid #fff;border-top:12px solid transparent;border-bottom:12px solid transparent;margin-left:5px}
.fc.front{cursor:pointer}.fc.front .pl{opacity:1}
.nav{position:absolute;top:calc(120px + var(--cw)*.89);z-index:6;width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.3);
  background:rgba(10,23,48,.72);font-size:22px;line-height:1;cursor:pointer;display:grid;place-items:center;transform:translateY(-50%)}
.nav:hover{background:var(--acc);color:var(--ink2);border-color:var(--acc)}
.nav.p{left:max(10px,calc(50% - 400px))}.nav.n{right:max(10px,calc(50% - 400px))}
.cap{position:relative;z-index:3;text-align:center;padding:0 16px 30px;margin-top:-6px}
.cap .pill{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:20px;padding:3px 12px;color:var(--ink2);background:var(--c,var(--acc))}
.cap h2{font-family:'Crimson Pro',Georgia,serif;font-size:clamp(1.2rem,4.2vw,1.6rem);margin:8px auto 2px;line-height:1.2;max-width:640px}
.cap small{color:var(--muted);font-size:.84rem}
.empty{text-align:center;color:var(--muted);padding:60px 16px}
main{max-width:1100px;margin:0 auto;padding:30px 16px 46px}
.wall-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.wall-head h2{font-family:'Crimson Pro',Georgia,serif;font-size:1.6rem;margin:0}
.wall-head small{color:var(--muted);font-size:.85rem}
.wall{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px;perspective:1100px}
.tile{position:relative;display:block;padding:0;border:0;background:none;cursor:pointer;text-align:left;
  opacity:0;transform:rotateY(-62deg) translateZ(-90px) translateY(26px);transform-origin:0 50%;
  transition:transform .7s cubic-bezier(.2,.75,.2,1),opacity .55s ease;transition-delay:var(--d,0ms)}
.tile.in{opacity:1;transform:rotateX(var(--tx,0deg)) rotateY(var(--ty,0deg))}
.tile.tilt{transition:transform .12s linear}
.tile .ph{position:relative;display:block;aspect-ratio:9/16;border-radius:12px;overflow:hidden;background:#101f3f;border:1px solid var(--line);
  box-shadow:0 7px 0 rgba(0,0,0,.28),0 16px 26px rgba(0,0,0,.36)}
.tile:hover .ph,.tile:focus-visible .ph{border-color:var(--c,var(--acc))}
.tile img{width:100%;height:100%;object-fit:cover;display:block}
.tile .ph:after{content:"▶";position:absolute;right:8px;bottom:8px;width:28px;height:28px;border-radius:50%;background:rgba(10,23,48,.75);
  display:grid;place-items:center;font-size:12px;color:#fff}
.tile b{display:block;font-size:.8rem;font-weight:600;margin-top:9px;line-height:1.3}
.tile span{display:block;font-size:.7rem;color:var(--c,var(--acc));font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-top:1px}
.follow{margin-top:36px;border:1px solid var(--line);border-radius:16px;padding:18px;text-align:center;background:rgba(255,255,255,.04)}
.follow p{margin:0 0 12px;color:var(--muted);font-size:.9rem}
.follow a{display:inline-block;text-decoration:none;font-weight:700;font-size:.85rem;border-radius:22px;padding:8px 18px;margin:4px;color:#fff}
footer{text-align:center;color:var(--muted);font-size:.8rem;padding:0 16px 34px}footer a{color:var(--gold)}
.lb{position:fixed;inset:0;z-index:100000;background:rgba(4,10,24,.95);display:none;flex-direction:column;align-items:center;justify-content:center;padding:54px 12px 14px}
.lb.on{display:flex}
.lb .vw{flex:1;min-height:0;width:100%;display:flex;align-items:center;justify-content:center}
.lb video{max-width:100%;max-height:100%;aspect-ratio:9/16;border-radius:14px;background:#000;box-shadow:0 20px 60px rgba(0,0,0,.6)}
.lb .x{position:absolute;top:10px;right:12px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.14);font-size:24px;line-height:1;cursor:pointer}
.lb .t{position:absolute;top:14px;left:16px;right:64px;font-weight:600;font-size:.92rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb .acts{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;padding-top:12px}
.lb .acts a,.lb .acts button{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);border-radius:22px;padding:8px 16px;font-size:.84rem;font-weight:600;cursor:pointer;text-decoration:none}
.lb .acts .go{background:var(--acc);border-color:var(--acc);color:var(--ink2)}
@media(max-width:600px){.stage{--dx:18px;--dy:26px;--dz:100px}.nav{width:40px;height:40px;font-size:19px;top:auto;bottom:4px;transform:none}.nav.p{left:22%}.nav.n{right:22%}
  .wall{grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
@media(prefers-reduced-motion:reduce){.fc,.deck,.tile{transition:none}.tile{opacity:1;transform:none}}
</style>
</head>
<body>
<div class="sky">
  <header class="top"><div class="top-in">
    <a class="brand" href="../index.html">CBSE<b>Mock</b></a>
    <a class="back" href="../index.html">← Back to portal</a>
  </div></header>
  <div class="hero">
    <h1>__H1__</h1>
    <p>__LEAD__</p>
    <div class="chips" id="chips" role="group" aria-label="Filter reels"></div>
  </div>
  <div class="stage" id="stage" tabindex="0" aria-roledescription="carousel" aria-label="Reels">
    <div class="deck" id="deck"></div>
    <button class="nav p" id="prev" type="button" aria-label="Previous reel">‹</button>
    <button class="nav n" id="next" type="button" aria-label="Next reel">›</button>
  </div>
  <div class="cap" id="cap" aria-live="polite"></div>
</div>
<main>
  <div class="wall-head"><h2>All reels</h2><small id="count"></small></div>
  <div class="wall" id="wall"></div>
  <div class="follow">
    <p>New reels every week. Follow us to get them as they arrive.</p>
    <a href="https://www.instagram.com/cbsemock/" target="_blank" rel="noopener" style="background:linear-gradient(45deg,#f09433,#dc2743 50%,#bc1888)">Instagram</a>
    <a href="https://t.me/cbsemockportal" target="_blank" rel="noopener" style="background:#229ED9">Telegram</a>
    <a href="https://www.facebook.com/profile.php?id=61596243964780" target="_blank" rel="noopener" style="background:#1877f2">Facebook</a>
  </div>
</main>
<footer>© CBSEMock · <a href="../index.html">cbsemock.org.in</a> · <a href="../formula-board/">Formula Board</a> · <a href="../free-mock-papers/">Free mock papers</a></footer>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Reel player">
  <div class="t" id="lbT"></div>
  <button class="x" id="lbX" type="button" aria-label="Close">&times;</button>
  <div class="vw"><video id="lbV" controls playsinline preload="metadata"></video></div>
  <div class="acts">
    <button type="button" id="lbP">‹ Prev</button>
    <button type="button" id="lbS" class="go">Share</button>
    <button type="button" id="lbN">Next ›</button>
  </div>
</div>
<script>
(function () {
  var ALL = __DATA__, CATS = __CATS__, SLUG = "__SLUG__";
  var $ = function (id) { return document.getElementById(id); };
  var stage = $('stage'), deck = $('deck'), cap = $('cap'), wall = $('wall');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fCat = '', fCls = '', list = ALL.slice(), cur = 0, els = {}, auto = null, touched = false, BEHIND = 5;
  function col(d) { return 'var(--' + d.cat + ',var(--acc))'; }
  function sub(d) { return d.cat + (d.cls ? ' · Class ' + d.cls : ''); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function chip(t, on, fn) { var b = document.createElement('button'); b.type = 'button'; b.textContent = t; if (on) b.className = 'on'; b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.addEventListener('click', fn); return b; }
  function drawChips() {
    var c = $('chips'); c.innerHTML = '';
    c.appendChild(chip('All', !fCat && !fCls, function () { fCat = ''; fCls = ''; apply(); }));
    ['10', '12'].forEach(function (k) { if (ALL.some(function (d) { return d.cls === k; })) c.appendChild(chip('Class ' + k, fCls === k, function () { fCls = fCls === k ? '' : k; apply(); })); });
    CATS.forEach(function (k) { c.appendChild(chip(k === 'CS' ? 'Computer Science' : k, fCat === k, function () { fCat = fCat === k ? '' : k; apply(); })); });
  }
  function apply() { touched = true; stop(); list = ALL.filter(function (d) { return (!fCat || d.cat === fCat) && (!fCls || d.cls === fCls); }); cur = 0; drawChips(); clearDeck(); layout(); drawWall(); }
  function clearDeck() { Object.keys(els).forEach(function (k) { deck.removeChild(els[k]); }); els = {}; }
  function place(el, pos) {
    var t, o = 1, z = 50 - pos;
    if (pos < 0) { t = 'translate3d(-130%,60px,220px) rotateZ(-16deg) rotateY(28deg)'; o = 0; z = 60; }
    else { t = 'translate3d(calc(var(--dx)*' + pos + '),calc(var(--dy)*-' + pos + '),calc(var(--dz)*-' + pos + '))'; o = pos > BEHIND ? 0 : (pos === 0 ? 1 : Math.max(.28, 1 - pos * .15)); }
    el.style.transform = t; el.style.opacity = o; el.style.zIndex = z;
    el.style.filter = pos > 0 ? 'brightness(' + Math.max(.55, 1 - pos * .09) + ')' : 'none';
    el.classList.toggle('front', pos === 0); el.setAttribute('aria-hidden', pos === 0 ? 'false' : 'true');
  }
  function layout() {
    var n = list.length; stage.style.display = n ? '' : 'none';
    if (!n) { cap.innerHTML = '<div class="empty">No reels for this choice yet. Try another filter.</div>'; return; }
    var want = {};
    for (var p = -1; p <= BEHIND + 1; p++) { if (n === 1 && p !== 0) continue; var i = cur + p; if (i < 0 || i >= n) { if (n <= BEHIND + 2) continue; i = (i % n + n) % n; } if (want[i] === undefined) want[i] = p; }
    Object.keys(els).forEach(function (k) { if (want[k] === undefined) { deck.removeChild(els[k]); delete els[k]; } });
    Object.keys(want).forEach(function (k) {
      var pos = want[k], el = els[k];
      if (!el) { var d = list[k]; el = document.createElement('div'); el.className = 'fc';
        el.innerHTML = (d.thumb ? '<img alt="' + esc(d.title) + '" src="' + d.thumb + '" decoding="async" draggable="false">' : '') + '<span class="pl"></span>';
        place(el, pos < 0 ? -1 : BEHIND + 1); deck.appendChild(el); els[k] = el; void el.offsetWidth; }
      place(el, pos);
    });
    var d0 = list[cur]; cap.style.setProperty('--c', col(d0));
    cap.innerHTML = '<span class="pill">' + esc(d0.cat === 'CS' ? 'Computer Science' : d0.cat) + '</span><h2>' + esc(d0.title) + '</h2><small>' + (d0.cls ? 'Class ' + d0.cls + ' · ' : '') + (cur + 1) + ' of ' + n + ' · tap to play</small>';
  }
  function go(s) { var n = list.length; if (n < 2) return; cur = ((cur + s) % n + n) % n; layout(); }
  function stop() { if (auto) { clearInterval(auto); auto = null; } }
  function user() { touched = true; stop(); }
  $('next').addEventListener('click', function (e) { e.stopPropagation(); user(); go(1); });
  $('prev').addEventListener('click', function (e) { e.stopPropagation(); user(); go(-1); });
  stage.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { user(); go(1); } else if (e.key === 'ArrowLeft') { user(); go(-1); } else if (e.key === 'Enter' && list.length) { user(); openV(cur); } });
  var down = null;
  stage.addEventListener('pointerdown', function (e) { if (e.target.closest('.nav')) return; down = { x: e.clientX, y: e.clientY, front: !!e.target.closest('.fc.front') }; });
  window.addEventListener('pointerup', function (e) { if (!down) return; var dx = e.clientX - down.x, dy = e.clientY - down.y, d = down; down = null;
    if (Math.abs(dx) > 42 && Math.abs(dx) > Math.abs(dy)) { user(); go(dx < 0 ? 1 : -1); } else if (Math.abs(dx) < 8 && Math.abs(dy) < 8 && d.front) { user(); openV(cur); } });
  window.addEventListener('pointercancel', function () { down = null; });
  if (!reduce && window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    stage.addEventListener('pointermove', function (e) { var r = stage.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      deck.style.setProperty('--ry', (-15 + x * 18).toFixed(1) + 'deg'); deck.style.setProperty('--rx', (6 - y * 10).toFixed(1) + 'deg'); });
    stage.addEventListener('pointerleave', function () { deck.style.removeProperty('--ry'); deck.style.removeProperty('--rx'); });
  }
  var io = 'IntersectionObserver' in window && !reduce ? new IntersectionObserver(function (en) { var k = 0;
    en.forEach(function (x) { if (x.isIntersecting) { x.target.style.setProperty('--d', (k++ * 70) + 'ms'); x.target.classList.add('in'); io.unobserve(x.target); } }); }, { rootMargin: '0px 0px -6% 0px' }) : null;
  var fine = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce;
  function drawWall() {
    wall.innerHTML = ''; $('count').textContent = list.length + (list.length === 1 ? ' reel' : ' reels');
    list.forEach(function (d, i) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'tile'; b.style.setProperty('--c', col(d));
      b.innerHTML = '<span class="ph">' + (d.thumb ? '<img loading="lazy" decoding="async" alt="' + esc(d.title) + '" src="' + d.thumb + '" width="360" height="640">' : '') + '</span><b>' + esc(d.title) + '</b><span>' + esc(sub(d)) + '</span>';
      b.addEventListener('click', function () { user(); openV(i); });
      if (fine) { b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); b.classList.add('tilt'); b.style.setProperty('--d', '0ms');
          b.style.setProperty('--ty', (((e.clientX - r.left) / r.width - .5) * 22).toFixed(1) + 'deg'); b.style.setProperty('--tx', ((.5 - (e.clientY - r.top) / r.height) * 16).toFixed(1) + 'deg'); });
        b.addEventListener('pointerleave', function () { b.classList.remove('tilt'); b.style.setProperty('--ty', '0deg'); b.style.setProperty('--tx', '0deg'); }); }
      wall.appendChild(b); if (io) io.observe(b); else b.classList.add('in');
    });
  }
  var lb = $('lb'), vid = $('lbV'), big = -1, lastFocus = null;
  function showV(i) { var n = list.length; big = ((i % n) + n) % n; var d = list[big];
    vid.poster = d.thumb || ''; vid.src = d.src; $('lbT').textContent = d.title + ' · ' + sub(d);
    var p = vid.play(); if (p && p.catch) p.catch(function () {});
    try { history.replaceState(null, '', '#' + d.id); } catch (e) {}
    if (window.gtag) { try { gtag('event', 'reel_play', { page: SLUG, reel: d.id }); } catch (e) {} } }
  function openV(i) { if (!list.length) return; lastFocus = document.activeElement; lb.classList.add('on'); document.body.style.overflow = 'hidden'; showV(i); $('lbX').focus(); }
  function closeV() { vid.pause(); vid.removeAttribute('src'); vid.load(); lb.classList.remove('on'); document.body.style.overflow = '';
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    if (big >= 0 && big !== cur) { cur = big; layout(); } if (lastFocus && lastFocus.focus) lastFocus.focus(); }
  vid.addEventListener('ended', function () { showV(big + 1); });
  $('lbX').addEventListener('click', closeV);
  $('lbP').addEventListener('click', function () { showV(big - 1); });
  $('lbN').addEventListener('click', function () { showV(big + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('vw')) closeV(); });
  document.addEventListener('keydown', function (e) { if (!lb.classList.contains('on')) return; if (e.key === 'Escape') closeV(); else if (e.key === 'ArrowRight') showV(big + 1); else if (e.key === 'ArrowLeft') showV(big - 1); });
  $('lbS').addEventListener('click', function () { var d = list[big], url = 'https://cbsemock.org.in/' + SLUG + '/#' + d.id, text = d.title + ' — free CBSE reel on CBSEMock';
    if (navigator.share) navigator.share({ title: 'CBSEMock', text: text, url: url }).catch(function () {}); else window.open('https://wa.me/?text=' + encodeURIComponent(text + ' ' + url), '_blank', 'noopener'); });
  drawChips(); layout(); drawWall();
  var h = decodeURIComponent(location.hash.slice(1));
  if (h) { for (var i = 0; i < list.length; i++) if (list[i].id === h) { cur = i; layout(); touched = true; openV(i); break; } }
  if (!reduce && !touched && list.length > 1) auto = setInterval(function () { if (document.hidden || lb.classList.contains('on')) return; var r = stage.getBoundingClientRect(); if (r.bottom > 80 && r.top < innerHeight) go(1); }, 3400);
})();
</script>
</body>
</html>
"""


def main():
    for slug, cfg in PAGES.items():
        build(slug, cfg)


if __name__ == "__main__":
    main()
