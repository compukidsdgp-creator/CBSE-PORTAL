#!/usr/bin/env python3
"""
Formula Board — builds /formula-board/ from the formula images.

Every image in formula-posts/queue and formula-posts/posted gets
  formula-board/img/<slug>.jpg     (900 px wide, for the big view / download)
  formula-board/thumb/<slug>.webp  (400 px wide, for the wall)
and formula-board/index.html is rewritten with the full list.

The copies live in their own folder, so the board keeps working when the
poster moves an image from queue/ to posted/. Run it again whenever images
are added (the posting workflow does this automatically); files that already
exist are skipped, and copies of images that were deleted are removed.

    python3 formula_board_page.py
"""
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

from post_formula_image import parse_filename, SUBJECT_META

ROOT = Path(__file__).resolve().parent
SOURCES = [ROOT / "formula-posts" / "queue", ROOT / "formula-posts" / "posted"]
OUT = ROOT / "formula-board"
FULL_W, THUMB_W = 900, 400
SUBJECT_ORDER = ["physics", "chemistry", "maths", "biology", "science", "cs"]


def slugify(stem: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def describe(stem: str) -> dict:
    info = parse_filename(stem)
    subj = {"mathematics": "maths", "computer": "cs"}.get(info["subject"], info["subject"])
    topic = info["topic"]
    if subj == "cbse" and "lens" in topic.lower():
        subj = "physics"
    if subj not in SUBJECT_META:
        subj = "other"
    cls = info["class"].replace("class", "") if info["class"] else ""
    return {"subject": subj, "topic": topic, "cls": cls}


def collect():
    seen, items = set(), []
    for folder in SOURCES:
        if not folder.is_dir():
            continue
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            slug = slugify(f.stem)
            if not slug or slug in seen:
                continue
            seen.add(slug)
            items.append((slug, f))
    return items


def build_images(items):
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    (OUT / "thumb").mkdir(parents=True, exist_ok=True)
    data, made = [], 0
    for slug, src in items:
        full, thumb = OUT / "img" / f"{slug}.jpg", OUT / "thumb" / f"{slug}.webp"
        try:
            if not (full.exists() and thumb.exists()):
                im = Image.open(src).convert("RGB")
                w, h = im.size
                fw = min(FULL_W, w)
                im.resize((fw, round(h * fw / w)), Image.LANCZOS).save(
                    full, "JPEG", quality=76, optimize=True, progressive=True)
                im.resize((THUMB_W, round(h * THUMB_W / w)), Image.LANCZOS).save(
                    thumb, "WEBP", quality=74, method=6)
                made += 1
            with Image.open(full) as fi:
                w, h = fi.size
        except Exception as exc:                      # a broken upload must not stop the board
            print(f"[WARN] skipped {src.name}: {exc}")
            continue
        d = describe(src.stem)
        d.update({"id": slug, "r": round(w / h, 3)})
        data.append(d)
    keep = {d["id"] for d in data}
    for folder, ext in ((OUT / "img", ".jpg"), (OUT / "thumb", ".webp")):
        for f in folder.glob(f"*{ext}"):
            if f.stem not in keep:
                f.unlink()
    # a fixed shuffle: subjects are mixed, and the order does not jump between builds
    data.sort(key=lambda d: hashlib.md5(d["id"].encode()).hexdigest())
    return data, made


def build_page(data):
    subjects = [s for s in SUBJECT_ORDER if any(d["subject"] == s for d in data)]
    labels = {s: SUBJECT_META[s]["pill"] for s in subjects}
    labels["maths"] = "Maths"
    classes = sorted({d["cls"] for d in data if d["cls"] in ("10", "12")}, key=int)
    page = (TEMPLATE
            .replace("__DATA__", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
            .replace("__SUBJECTS__", json.dumps([[s, labels[s]] for s in subjects]))
            .replace("__CLASSES__", json.dumps(classes))
            .replace("__COUNT__", str(len(data))))
    (OUT / "index.html").write_text(page, encoding="utf-8")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Formula Board — CBSE Class 10 &amp; 12 Formula Cards in 3D | CBSEMock</title>
<meta name="description" content="Swipe through __COUNT__ free CBSE formula cards for Class 10 and 12 — Physics, Chemistry, Maths and Biology — on a 3D formula board. Tap any card to zoom, save or share.">
<link rel="canonical" href="https://cbsemock.org.in/formula-board/">
<meta property="og:title" content="Formula Board — CBSE Formula Cards in 3D | CBSEMock">
<meta property="og:description" content="Free formula cards for Class 10 &amp; 12. Swipe, zoom, save and share.">
<meta property="og:url" content="https://cbsemock.org.in/formula-board/">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0a1730">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<style>
:root{--ink:#0a1730;--ink2:#0f2347;--gold:#e8cc6a;--gold2:#c9a227;--text:#eef2fb;--muted:#9fb0cf;--line:rgba(255,255,255,.14);
  --physics:#5cb8ff;--chemistry:#ff8f8f;--maths:#ffd43b;--biology:#6fdc8c;--science:#c6a2ff;--cs:#63e6e2;--other:#e8cc6a}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--text);font-family:'Inter',system-ui,Arial,sans-serif;line-height:1.5;overflow-x:hidden}
a{color:inherit}
button{font:inherit;color:inherit}
.top{padding:14px 16px;position:relative;z-index:5}
.top-in{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px}
.brand{font-weight:700;font-size:1.05rem;text-decoration:none;color:#fff}.brand b{color:var(--gold)}
.back{font-size:.82rem;text-decoration:none;border:1px solid rgba(255,255,255,.3);border-radius:20px;padding:5px 14px;color:#fff;white-space:nowrap}
.back:hover{background:var(--gold);color:var(--ink2);border-color:var(--gold)}

/* ── the 3D cascade ── */
.sky{position:relative;background:radial-gradient(1200px 520px at 50% -8%,#28509a 0%,rgba(40,80,154,0) 62%),linear-gradient(180deg,#0f2347 0%,#0a1730 78%);overflow:hidden}
.sky:before{content:"";position:absolute;inset:auto -20% 0 -20%;height:46%;pointer-events:none;
  background-image:linear-gradient(rgba(232,204,106,.2) 1px,transparent 1px),linear-gradient(90deg,rgba(232,204,106,.2) 1px,transparent 1px);
  background-size:56px 56px;transform:perspective(520px) rotateX(64deg);transform-origin:50% 100%;
  -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 55%);mask-image:linear-gradient(180deg,transparent 0%,#000 55%)}
.hero{text-align:center;padding:6px 16px 0;position:relative;z-index:2}
.hero h1{font-family:'Crimson Pro',Georgia,serif;font-size:clamp(2rem,6.4vw,3.3rem);margin:0;line-height:1.05;letter-spacing:.01em}
.hero h1 span{color:var(--gold)}
.hero p{margin:8px auto 0;max-width:560px;color:var(--muted);font-size:.95rem}
.chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:16px auto 0;max-width:760px;padding:0 4px}
.chips button{border:1px solid var(--line);background:rgba(255,255,255,.06);border-radius:20px;padding:6px 14px;font-size:.82rem;font-weight:600;cursor:pointer;color:var(--text)}
.chips button:hover{border-color:var(--gold)}
.chips button.on{background:var(--gold);border-color:var(--gold);color:var(--ink2)}
.chips i{width:1px;background:var(--line);margin:4px 2px}
.stage{--cw:min(64vw,330px);--dx:34px;--dy:40px;--dz:130px;position:relative;z-index:2;height:calc(var(--cw)*1.25 + 200px);
  perspective:1300px;perspective-origin:50% 38%;touch-action:pan-y;user-select:none;-webkit-user-select:none;cursor:grab;outline:none}
.stage.drag{cursor:grabbing}
.deck{position:absolute;left:50%;top:150px;width:0;height:0;transform-style:preserve-3d;
  transform:translateX(calc(var(--dx)*-1.3)) rotateX(var(--rx,7deg)) rotateY(var(--ry,-15deg));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.fc{position:absolute;left:calc(var(--cw)/-2);top:0;width:var(--cw);aspect-ratio:4/5;border-radius:16px;overflow:hidden;background:#101f3f;
  border:1px solid rgba(255,255,255,.22);box-shadow:0 26px 46px rgba(0,0,0,.5);transform-style:preserve-3d;will-change:transform,opacity;
  transition:transform .62s cubic-bezier(.2,.75,.2,1),opacity .5s ease,filter .5s ease}
.fc img{width:100%;height:100%;object-fit:contain;display:block;pointer-events:none;-webkit-user-drag:none}
.fc:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(120deg,rgba(255,255,255,.2) 0%,rgba(255,255,255,0) 32%)}
.fc.front{cursor:zoom-in}
.nav{position:absolute;top:calc(150px + var(--cw)*.62);z-index:6;width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.3);
  background:rgba(10,23,48,.72);font-size:22px;line-height:1;cursor:pointer;display:grid;place-items:center;transform:translateY(-50%)}
.nav:hover{background:var(--gold);color:var(--ink2);border-color:var(--gold)}
.nav.p{left:max(10px,calc(50% - 420px))}.nav.n{right:max(10px,calc(50% - 420px))}
.cap{position:relative;z-index:3;text-align:center;padding:0 16px 30px;margin-top:-18px}
.cap .pill{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:20px;padding:3px 12px;color:var(--ink2);background:var(--c,var(--gold))}
.cap h2{font-family:'Crimson Pro',Georgia,serif;font-size:clamp(1.25rem,4.4vw,1.7rem);margin:8px 0 2px;line-height:1.2}
.cap small{color:var(--muted);font-size:.84rem}
.cap .hint{display:block;margin-top:8px;font-size:.78rem;color:var(--muted)}
.cap.none{margin-top:24px}
.empty{text-align:center;color:var(--muted);padding:60px 16px}

/* ── the wall ── */
main{max-width:1100px;margin:0 auto;padding:30px 16px 46px}
.wall-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.wall-head h2{font-family:'Crimson Pro',Georgia,serif;font-size:1.6rem;margin:0}
.wall-head small{color:var(--muted);font-size:.85rem}
.wall{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:16px;perspective:1100px}
.tile{position:relative;display:block;padding:0;border:0;background:none;cursor:zoom-in;text-align:left;transform-style:preserve-3d;
  opacity:0;transform:rotateY(-62deg) translateZ(-90px) translateY(26px);transform-origin:0 50%;
  transition:transform .7s cubic-bezier(.2,.75,.2,1),opacity .55s ease;transition-delay:var(--d,0ms)}
.tile.in{opacity:1;transform:rotateX(var(--tx,0deg)) rotateY(var(--ty,0deg))}
.tile.tilt{transition:transform .12s linear}
.tile .ph{display:block;aspect-ratio:4/5;border-radius:12px;overflow:hidden;background:#101f3f;border:1px solid var(--line);
  box-shadow:0 7px 0 rgba(0,0,0,.28),0 16px 26px rgba(0,0,0,.36)}
.tile:hover .ph,.tile:focus-visible .ph{border-color:var(--c,var(--gold))}
.tile img{width:100%;height:100%;object-fit:contain;display:block}
.tile b{display:block;font-size:.8rem;font-weight:600;margin-top:9px;line-height:1.3}
.tile span{display:block;font-size:.7rem;color:var(--c,var(--gold));font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-top:1px}
.follow{margin-top:36px;border:1px solid var(--line);border-radius:16px;padding:18px;text-align:center;background:rgba(255,255,255,.04)}
.follow p{margin:0 0 12px;color:var(--muted);font-size:.9rem}
.follow a{display:inline-block;text-decoration:none;font-weight:700;font-size:.85rem;border-radius:22px;padding:8px 18px;margin:4px;color:#fff}
footer{text-align:center;color:var(--muted);font-size:.8rem;padding:0 16px 34px}
footer a{color:var(--gold)}

/* ── big view ── */
.lb{position:fixed;inset:0;z-index:100000;background:rgba(4,10,24,.94);display:none;flex-direction:column;align-items:center;justify-content:center;padding:54px 12px 14px}
.lb.on{display:flex}
.lb figure{margin:0;flex:1;min-height:0;width:100%;display:flex;align-items:center;justify-content:center;perspective:1200px}
.lb img{max-width:100%;max-height:100%;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.6);animation:pop .45s cubic-bezier(.2,.8,.2,1)}
@keyframes pop{from{opacity:0;transform:rotateY(-38deg) scale(.82)}to{opacity:1;transform:none}}
.lb .x{position:absolute;top:10px;right:12px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.14);font-size:24px;line-height:1;cursor:pointer}
.lb .t{position:absolute;top:14px;left:16px;right:64px;font-weight:600;font-size:.92rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb .acts{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;padding-top:12px}
.lb .acts a,.lb .acts button{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);border-radius:22px;padding:8px 16px;font-size:.84rem;font-weight:600;cursor:pointer;text-decoration:none}
.lb .acts .go{background:var(--gold);border-color:var(--gold);color:var(--ink2)}
@media(max-width:600px){.stage{--dx:20px;--dy:30px;--dz:110px}.nav{width:40px;height:40px;font-size:19px;top:auto;bottom:6px;transform:none}.nav.p{left:22%}.nav.n{right:22%}
  .wall{grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.cap{margin-top:8px}.cap.none{margin-top:24px}}
@media(prefers-reduced-motion:reduce){.fc,.deck,.tile,.lb img{transition:none;animation:none}.tile{opacity:1;transform:none}}
</style>
</head>
<body>
<div class="sky">
  <header class="top"><div class="top-in">
    <a class="brand" href="../index.html">CBSE<b>Mock</b></a>
    <a class="back" href="../index.html">← Back to portal</a>
  </div></header>
  <div class="hero">
    <h1>Formula <span>Board</span></h1>
    <p>__COUNT__ formula cards for Class 10 &amp; 12. Swipe the stack, tap a card to zoom, save or share it.</p>
    <div class="chips" id="chips" role="group" aria-label="Filter formula cards"></div>
  </div>
  <div class="stage" id="stage" tabindex="0" aria-roledescription="carousel" aria-label="Formula cards">
    <div class="deck" id="deck"></div>
    <button class="nav p" id="prev" type="button" aria-label="Previous card">‹</button>
    <button class="nav n" id="next" type="button" aria-label="Next card">›</button>
  </div>
  <div class="cap" id="cap" aria-live="polite"></div>
</div>

<main>
  <div class="wall-head"><h2>All formula cards</h2><small id="count"></small></div>
  <div class="wall" id="wall"></div>
  <div class="follow">
    <p>New formula cards go up every morning and evening. Follow us to get them as they arrive.</p>
    <a href="https://t.me/cbsemockportal" target="_blank" rel="noopener" style="background:#229ED9">Telegram</a>
    <a href="https://www.instagram.com/cbsemock/" target="_blank" rel="noopener" style="background:linear-gradient(45deg,#f09433,#dc2743 50%,#bc1888)">Instagram</a>
    <a href="https://www.facebook.com/profile.php?id=61596243964780" target="_blank" rel="noopener" style="background:#1877f2">Facebook</a>
  </div>
</main>
<footer>© CBSEMock · <a href="../index.html">cbsemock.org.in</a> · <a href="../free-mock-papers/">Free mock papers</a></footer>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Formula card">
  <div class="t" id="lbT"></div>
  <button class="x" id="lbX" type="button" aria-label="Close">&times;</button>
  <figure><img id="lbI" alt=""></figure>
  <div class="acts">
    <button type="button" id="lbP">‹ Prev</button>
    <a class="go" id="lbD" download>Save card</a>
    <button type="button" id="lbS">Share</button>
    <button type="button" id="lbN">Next ›</button>
  </div>
</div>

<script>
(function () {
  var ALL = __DATA__, SUBJECTS = __SUBJECTS__, CLASSES = __CLASSES__;
  var NAMES = { other: 'CBSE' }; SUBJECTS.forEach(function (s) { NAMES[s[0]] = s[1]; });
  var $ = function (id) { return document.getElementById(id); };
  var stage = $('stage'), deck = $('deck'), cap = $('cap'), wall = $('wall');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fCls = '', fSub = '', list = ALL.slice(), cur = 0, els = {}, auto = null, touched = false;
  var BEHIND = 5;

  function label(d) { return NAMES[d.subject] || 'CBSE'; }
  function sub(d) { return label(d) + (d.cls ? ' · Class ' + d.cls : ''); }
  function col(d) { return 'var(--' + (NAMES[d.subject] && d.subject !== 'other' ? d.subject : 'other') + ')'; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ── filters ── */
  function chip(text, on, fn) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = text;
    if (on) b.className = 'on'; b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.addEventListener('click', fn); return b;
  }
  function drawChips() {
    var c = $('chips'); c.innerHTML = '';
    c.appendChild(chip('All', !fCls && !fSub, function () { fCls = ''; fSub = ''; apply(); }));
    CLASSES.forEach(function (k) { c.appendChild(chip('Class ' + k, fCls === k, function () { fCls = fCls === k ? '' : k; apply(); })); });
    if (CLASSES.length && SUBJECTS.length) c.appendChild(document.createElement('i'));
    SUBJECTS.forEach(function (s) { c.appendChild(chip(s[1], fSub === s[0], function () { fSub = fSub === s[0] ? '' : s[0]; apply(); })); });
  }
  function apply() {
    touched = true; stop();
    list = ALL.filter(function (d) { return (!fCls || d.cls === fCls) && (!fSub || d.subject === fSub); });
    cur = 0; drawChips(); clearDeck(); layout(); drawWall();
  }

  /* ── cascade ── */
  function clearDeck() { Object.keys(els).forEach(function (k) { deck.removeChild(els[k]); }); els = {}; }
  function place(el, pos) {
    var t, o = 1, z = 50 - pos;
    if (pos < 0) { t = 'translate3d(-130%,60px,220px) rotateZ(-16deg) rotateY(28deg)'; o = 0; z = 60; }
    else if (pos > BEHIND) { t = 'translate3d(calc(var(--dx)*' + pos + '),calc(var(--dy)*-' + pos + '),calc(var(--dz)*-' + pos + '))'; o = 0; }
    else { t = 'translate3d(calc(var(--dx)*' + pos + '),calc(var(--dy)*-' + pos + '),calc(var(--dz)*-' + pos + '))'; o = pos === 0 ? 1 : Math.max(.28, 1 - pos * .15); }
    el.style.transform = t; el.style.opacity = o; el.style.zIndex = z;
    el.style.filter = pos > 0 ? 'brightness(' + Math.max(.55, 1 - pos * .09) + ')' : 'none';
    el.classList.toggle('front', pos === 0);
    el.setAttribute('aria-hidden', pos === 0 ? 'false' : 'true');
  }
  function layout() {
    var n = list.length;
    stage.style.display = n ? '' : 'none'; cap.classList.toggle('none', !n);
    if (!n) { cap.innerHTML = '<div class="empty">No cards for this choice yet. Try another filter.</div>'; return; }
    var want = {};
    for (var p = -1; p <= BEHIND + 1; p++) {
      if (n === 1 && p !== 0) continue;
      var i = cur + p;
      if (i < 0 || i >= n) { if (n <= BEHIND + 2) continue; i = (i % n + n) % n; }
      if (want[i] === undefined) want[i] = p;
    }
    Object.keys(els).forEach(function (k) { if (want[k] === undefined) { deck.removeChild(els[k]); delete els[k]; } });
    Object.keys(want).forEach(function (k) {
      var pos = want[k], el = els[k];
      if (!el) {
        var d = list[k];
        el = document.createElement('div'); el.className = 'fc';
        el.innerHTML = '<img alt="' + esc(d.topic + ' — ' + sub(d)) + '" src="thumb/' + d.id + '.webp" decoding="async" draggable="false">';
        el._id = d.id;
        place(el, pos < 0 ? -1 : BEHIND + 1);            /* start off-stage, then glide in */
        deck.appendChild(el); els[k] = el;
        void el.offsetWidth;
      }
      place(el, pos);
      if (pos >= 0 && pos <= 1 && !el._hd) {              /* sharp copy only for the card in front and the next one */
        el._hd = 1; (function (im, src) { var hd = new Image(); hd.onload = function () { im.src = src; }; hd.src = src; })(el.firstChild, 'img/' + el._id + '.jpg');
      }
    });
    var d0 = list[cur];
    cap.style.setProperty('--c', col(d0));
    cap.innerHTML = '<span class="pill">' + esc(label(d0)) + '</span><h2>' + esc(d0.topic) + '</h2><small>' +
      (d0.cls ? 'Class ' + d0.cls + ' · ' : '') + (cur + 1) + ' of ' + n + '</small>' +
      '<span class="hint">Swipe or use the arrows · tap the card to zoom</span>';
  }
  function go(step) { var n = list.length; if (n < 2) return; cur = ((cur + step) % n + n) % n; layout(); }
  function stop() { if (auto) { clearInterval(auto); auto = null; } }
  function user() { touched = true; stop(); }

  $('next').addEventListener('click', function (e) { e.stopPropagation(); user(); go(1); });
  $('prev').addEventListener('click', function (e) { e.stopPropagation(); user(); go(-1); });
  stage.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { user(); go(1); } else if (e.key === 'ArrowLeft') { user(); go(-1); }
    else if (e.key === 'Enter' && list.length) { user(); openBig(cur); }
  });

  var down = null;
  stage.addEventListener('pointerdown', function (e) {
    if (e.target.closest('.nav')) return;
    down = { x: e.clientX, y: e.clientY, t: Date.now(), front: !!e.target.closest('.fc.front') };
    stage.classList.add('drag');
  });
  window.addEventListener('pointerup', function (e) {
    if (!down) return;
    var dx = e.clientX - down.x, dy = e.clientY - down.y, d = down; down = null; stage.classList.remove('drag');
    if (Math.abs(dx) > 42 && Math.abs(dx) > Math.abs(dy)) { user(); go(dx < 0 ? 1 : -1); }
    else if (Math.abs(dx) < 8 && Math.abs(dy) < 8 && d.front) { user(); openBig(cur); }
  });
  window.addEventListener('pointercancel', function () { down = null; stage.classList.remove('drag'); });
  /* the whole stack leans towards the pointer (mouse only) */
  if (!reduce && window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    stage.addEventListener('pointermove', function (e) {
      var r = stage.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      deck.style.setProperty('--ry', (-15 + x * 18).toFixed(1) + 'deg'); deck.style.setProperty('--rx', (7 - y * 10).toFixed(1) + 'deg');
    });
    stage.addEventListener('pointerleave', function () { deck.style.removeProperty('--ry'); deck.style.removeProperty('--rx'); });
  }

  /* ── wall ── */
  var io = 'IntersectionObserver' in window && !reduce ? new IntersectionObserver(function (en) {
    var k = 0;
    en.forEach(function (x) { if (x.isIntersecting) { x.target.style.setProperty('--d', (k++ * 70) + 'ms'); x.target.classList.add('in'); io.unobserve(x.target); } });
  }, { rootMargin: '0px 0px -6% 0px' }) : null;
  var fine = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce;
  function drawWall() {
    wall.innerHTML = '';
    $('count').textContent = list.length + (list.length === 1 ? ' card' : ' cards');
    list.forEach(function (d, i) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'tile'; b.style.setProperty('--c', col(d));
      b.innerHTML = '<span class="ph"><img loading="lazy" decoding="async" alt="' + esc(d.topic) + '" src="thumb/' + d.id + '.webp" width="400" height="' + Math.round(400 / d.r) + '"></span>' +
        '<b>' + esc(d.topic) + '</b><span>' + esc(sub(d)) + '</span>';
      b.addEventListener('click', function () { user(); openBig(i); });
      if (fine) {
        b.addEventListener('pointermove', function (e) {
          var r = b.getBoundingClientRect(); b.classList.add('tilt'); b.style.setProperty('--d', '0ms');
          b.style.setProperty('--ty', (((e.clientX - r.left) / r.width - .5) * 22).toFixed(1) + 'deg');
          b.style.setProperty('--tx', ((.5 - (e.clientY - r.top) / r.height) * 16).toFixed(1) + 'deg');
        });
        b.addEventListener('pointerleave', function () { b.classList.remove('tilt'); b.style.setProperty('--ty', '0deg'); b.style.setProperty('--tx', '0deg'); });
      }
      wall.appendChild(b);
      if (io) io.observe(b); else b.classList.add('in');
    });
  }

  /* ── big view ── */
  var lb = $('lb'), big = -1, lastFocus = null;
  function showBig(i) {
    var n = list.length; big = ((i % n) + n) % n; var d = list[big];
    var img = $('lbI'); img.style.animation = 'none'; void img.offsetWidth; img.style.animation = '';
    img.src = 'img/' + d.id + '.jpg'; img.alt = d.topic + ' — ' + sub(d);
    $('lbT').textContent = d.topic + ' · ' + sub(d);
    var a = $('lbD'); a.href = 'img/' + d.id + '.jpg'; a.setAttribute('download', 'cbsemock-' + d.id + '.jpg');
    try { history.replaceState(null, '', '#' + d.id); } catch (e) {}
  }
  function openBig(i) {
    if (!list.length) return;
    lastFocus = document.activeElement; showBig(i); lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('lbX').focus();
    if (window.gtag) { try { gtag('event', 'formula_card_open', { card: list[big].id }); } catch (e) {} }
  }
  function closeBig() {
    lb.classList.remove('on'); document.body.style.overflow = '';
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    if (big >= 0 && big !== cur) { cur = big; layout(); }
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  $('lbX').addEventListener('click', closeBig);
  $('lbP').addEventListener('click', function () { showBig(big - 1); });
  $('lbN').addEventListener('click', function () { showBig(big + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE') closeBig(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('on')) return;
    if (e.key === 'Escape') closeBig(); else if (e.key === 'ArrowRight') showBig(big + 1); else if (e.key === 'ArrowLeft') showBig(big - 1);
  });
  var sx = null;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null; if (Math.abs(dx) > 50) showBig(big + (dx < 0 ? 1 : -1)); }, { passive: true });
  $('lbS').addEventListener('click', function () {
    var d = list[big], url = 'https://cbsemock.org.in/formula-board/#' + d.id, text = d.topic + ' — ' + sub(d) + ' formula card (free) on CBSEMock';
    if (navigator.share) { navigator.share({ title: 'CBSEMock Formula Board', text: text, url: url }).catch(function () {}); }
    else { window.open('https://wa.me/?text=' + encodeURIComponent(text + ' ' + url), '_blank', 'noopener'); }
  });

  /* ── start ── */
  drawChips(); layout(); drawWall();
  var h = decodeURIComponent(location.hash.slice(1));
  if (h) { for (var i = 0; i < list.length; i++) if (list[i].id === h) { cur = i; layout(); touched = true; openBig(i); break; } }
  if (!reduce && !touched && list.length > 1) {
    auto = setInterval(function () { if (document.hidden || lb.classList.contains('on')) return; var r = stage.getBoundingClientRect(); if (r.bottom > 80 && r.top < innerHeight) go(1); }, 3400);
  }
})();
</script>
</body>
</html>
"""


def main():
    items = collect()
    data, made = build_images(items)
    build_page(data)
    print(f"[formula-board] {len(data)} cards on the board ({made} new image copies made)")


if __name__ == "__main__":
    main()
