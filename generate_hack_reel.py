#!/usr/bin/env python3
"""
generate_hack_reel.py — "90+ Score Hack" campaign reels (1080×1920, ~16–24 s): premium dark template, one idea per
screen, kinetic text cards, Kokoro voiceover with word-synced captions, light sound design and the music bed.

Specs: campaign_reels/specs/NN-<slug>.py, each defining REEL (see campaign_reels/WRITING_GUIDE.md).
Card types: title · list · chain · compare · quiz · worked · recap · end.
    python3 generate_hack_reel.py 1 [--out x.mp4] [--preview 3.0]
    python3 generate_hack_reel.py --missing            (render every missing video into campaign_reels/video/)
"""
import argparse
import html as H
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from voiceover import synth, write_wav, SR

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "assets" / "fonts"
MUSIC = ROOT / "formula-posts" / "bg_music.mp3"
W, Hh, FPS = 1080, 1920, 30
LEAD, GAP, OUTRO = 0.30, 0.22, 1.9
BASE = ROOT / "campaign_reels"
SPECS, VIDEOS, THUMBS = BASE / "specs", BASE / "video", BASE / "thumb"

PILLARS = {  # label, accent, deep
    "90+ Score Hack": ("90+ SCORE HACK", "#ffd23f", "#8a6d00"),
    "Board FAQ": ("BOARD FAQ", "#5eead4", "#0f766e"),
    "Beat the Timer": ("BEAT THE TIMER", "#ff7a45", "#9a3412"),
    "Mistake Fix": ("MISTAKE FIX", "#ff5470", "#9f1239"),
    "Exam Rescue": ("EXAM RESCUE", "#a78bfa", "#5b21b6"),
}


def load_specs():
    import importlib.util
    out = []
    for f in sorted(SPECS.glob("[0-9]*.py")):
        sp = importlib.util.spec_from_file_location(f"cr_{f.stem.replace('-', '_')}", f)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        r = dict(m.REEL)
        r["_src"] = str(f.relative_to(ROOT))
        out.append(r)
    return out


def video_path(r):
    return VIDEOS / f"{r['n']:02d}-{r['id']}.mp4"


def thumb_path(r):
    return THUMBS / f"{r['n']:02d}-{r['id']}.jpg"


# ── audio ────────────────────────────────────────────────────────────────────
def tone(freq, dur, vol=0.2, kind="sine", decay=8.0):
    t = np.arange(int(dur * SR)) / SR
    if kind == "sweep":
        f = np.linspace(freq, freq * 3, len(t))
        w = np.sin(2 * np.pi * np.cumsum(f) / SR)
    elif kind == "tick":
        w = np.sign(np.sin(2 * np.pi * freq * t)) * 0.6
    else:
        w = np.sin(2 * np.pi * freq * t)
    return (w * np.exp(-decay * t) * vol).astype(np.float32)


def at(track, t, clip):
    i = max(0, int(t * SR))
    j = min(len(track), i + len(clip))
    if j > i:
        track[i:j] += clip[: j - i]


def build_audio(r, tmp):
    clips, times, t = [], [], LEAD
    for b in r["beats"]:
        a = synth(b["say"], voice=r.get("voice", "af_heart"), speed=r.get("speed", 1.12))
        clips.append(a)
        times.append((t, t + len(a) / SR))
        t += len(a) / SR + GAP + b.get("hold", 0)
    total = t - GAP + OUTRO
    track = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for (s, _), a in zip(times, clips):
        at(track, s, a)
    for i, (b, (s, e)) in enumerate(zip(r["beats"], times)):
        c = b["card"]
        if i:
            at(track, s - 0.22, tone(240, 0.32, 0.12, "sweep", 7))                     # whoosh on each new card
        if c["type"] == "quiz":
            for k in range(3):
                at(track, e + 0.05 + k * 0.33, tone(1200, 0.05, 0.10, "tick", 30))      # countdown ticks
            at(track, e + 1.05, tone(1046, 0.45, 0.18, decay=4) + tone(1568, 0.45, 0.10, decay=4))
        if c["type"] == "compare":
            at(track, s + 0.15, tone(150, 0.35, 0.14, decay=6))
            at(track, s + 0.55 * (e - s), tone(880, 0.16, 0.16) + tone(1320, 0.16, 0.08))
        if c["type"] in ("recap", "end"):
            at(track, s, tone(1046, 0.5, 0.15, decay=4) + tone(1568, 0.5, 0.08, decay=4))
    at(track, 0.02, tone(55, 0.6, 0.30, decay=5) + tone(110, 0.6, 0.12, decay=6))    # opening hit
    track = track[: int(total * SR)]
    write_wav(tmp / "voice.wav", np.clip(track, -1, 1))
    return times, total


# ── visuals ──────────────────────────────────────────────────────────────────
def page_html(r, times, total):
    lbl, acc, deep = PILLARS[r["pillar"]]
    faces = "".join(f"@font-face{{font-family:'{n}';src:url('{(FONTS / f).as_uri()}');font-weight:{w}}}"
                    for n, f, w in [("Inter", "Inter-Regular.otf", 400), ("Inter", "Inter-Bold.otf", 800),
                                    ("Poppins", "Poppins-Bold.ttf", 700), ("Poppins", "Poppins-Medium.ttf", 500)])
    data = json.dumps({"beats": [{"s": s, "e": e, "say": b["say"], "cap": b.get("cap", b["say"]), "card": b["card"],
                                  "hold": b.get("hold", 0)}
                                 for b, (s, e) in zip(r["beats"], times)],
                       "total": total, "n": r["n"], "label": lbl}, ensure_ascii=False).replace("</", "<\\/")
    return """<!doctype html><html><head><meta charset="utf-8"><style>""" + faces + """
:root{--acc:""" + acc + """;--deep:""" + deep + """}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#05080f;font-family:Inter,Poppins,sans-serif;color:#fff}
#bg{position:absolute;inset:0;background:radial-gradient(1000px 800px at 50% 30%,color-mix(in srgb,var(--deep) 55%,#0b1530) 0%,#081022 52%,#04070d 100%)}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:90px 90px;
 -webkit-mask-image:radial-gradient(900px 1200px at 50% 45%,#000 30%,transparent 75%)}
#glow{position:absolute;left:50%;top:860px;width:1200px;height:1200px;margin:-600px 0 0 -600px;border-radius:50%;background:radial-gradient(color-mix(in srgb,var(--acc) 22%,transparent),transparent 62%)}
#prog{position:absolute;left:70px;right:70px;top:120px;height:8px;border-radius:8px;background:rgba(255,255,255,.12)}#prog i{display:block;height:100%;border-radius:8px;background:var(--acc)}
.hdr{position:absolute;left:70px;right:70px;top:162px;display:flex;align-items:center;justify-content:space-between}
.pill{font:800 32px Inter;letter-spacing:.12em;color:#08101f;background:var(--acc);padding:12px 24px;border-radius:99px;box-shadow:0 10px 30px color-mix(in srgb,var(--acc) 40%,transparent)}
.num{font:700 34px Poppins;color:rgba(255,255,255,.75)}
#stage{position:absolute;left:70px;right:70px;top:300px;height:1080px;perspective:1800px}
.card{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;transform-style:preserve-3d;opacity:0}
.kick{font:800 34px Inter;letter-spacing:.16em;color:var(--acc);margin-bottom:26px}
.big{font:700 104px/1.08 Poppins;letter-spacing:-2px;text-shadow:0 10px 40px rgba(0,0,0,.5)}
.big em{font-style:normal;color:var(--acc)}
.ttl{font:700 64px/1.15 Poppins;margin-bottom:40px}
.item{display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:28px;padding:30px 34px;margin-bottom:24px;
 font:700 54px/1.2 Poppins;opacity:0}
.item i{flex:0 0 84px;height:84px;border-radius:50%;background:var(--acc);color:#08101f;display:flex;align-items:center;justify-content:center;font:800 44px Inter;font-style:normal}
.chain{display:flex;flex-direction:column;align-items:center;gap:6px}
.ch{width:92%;text-align:center;background:linear-gradient(135deg,#13254a,#0c1934);border:3px solid var(--acc);border-radius:30px;padding:30px 20px;font:700 60px/1.15 Poppins;opacity:0;box-shadow:0 20px 40px rgba(0,0,0,.4)}
.ch small{display:block;font:700 44px/1.3 Poppins;color:#ffe9a6;margin-top:6px}
.arw{font:800 60px Inter;color:var(--acc);opacity:0;line-height:1}
.cmp{border-radius:30px;overflow:hidden;margin-bottom:34px;box-shadow:0 30px 60px rgba(0,0,0,.45);opacity:0;background:#fffdf6;color:#0f172a}
.cmp .h{padding:24px 34px;font:800 44px Inter;color:#fff;display:flex;gap:14px;align-items:center}
.cmp.bad .h{background:linear-gradient(90deg,#e11d48,#9f1239)}.cmp.good .h{background:linear-gradient(90deg,#16a34a,#14532d)}
.cmp .b{padding:30px 34px 34px;font:700 58px/1.3 Poppins;background-image:linear-gradient(#e8edf5 2px,transparent 2px);background-size:100% 60px}
.cmp.bad .b{color:#9f1239}
.q{font:700 58px/1.22 Poppins;margin-bottom:34px}
.opt{display:flex;align-items:center;gap:24px;border:3px solid rgba(255,255,255,.18);background:rgba(255,255,255,.05);border-radius:24px;padding:22px 28px;margin-bottom:20px;font:700 48px/1.2 Poppins;opacity:0}
.opt b{flex:0 0 70px;height:70px;border-radius:18px;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;font:800 40px Inter}
.opt.ok{border-color:#22c55e;background:rgba(34,197,94,.18)}.opt.ok b{background:#22c55e;color:#04210f}
.opt.dim{opacity:.35!important}
#clock{position:absolute;right:70px;top:250px;width:150px;height:150px;opacity:0}
#clock svg{width:100%;height:100%}#clock span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:800 64px Inter}
.wk{background:#fffdf6;color:#0f172a;border-radius:30px;padding:30px 40px;box-shadow:0 30px 60px rgba(0,0,0,.45);background-image:linear-gradient(#e8edf5 2px,transparent 2px);background-size:100% 76px;background-position:0 20px}
.wl{font:700 52px/1.46 Poppins;opacity:0;display:flex;gap:18px;align-items:baseline}
.wl small{flex:0 0 auto;font:800 30px Inter;color:#fff;background:var(--deep);border-radius:12px;padding:4px 12px}
.wl.fin{color:#14532d}.wl.fin span{background:linear-gradient(transparent 10%,#ffd23f 10%,#ffd23f 90%,transparent 90%);padding:0 10px;border-radius:8px}
.recap{border:4px solid var(--acc);border-radius:40px;padding:60px 50px;text-align:center;background:rgba(8,16,31,.75);box-shadow:0 0 80px color-mix(in srgb,var(--acc) 35%,transparent)}
.recap .big{font-size:96px}
.end{align-items:center;text-align:center}
.end .ctab{font:800 64px/1.2 Poppins;margin-bottom:46px}
.end .url{display:inline-block;white-space:nowrap;font:800 42px Inter;color:#08101f;background:linear-gradient(90deg,#ffd23f,#c9a227);border-radius:80px;padding:30px 50px;box-shadow:0 14px 0 rgba(0,0,0,.35)}
.end .lg{margin-top:70px;font:800 64px Inter}.end .lg b{color:#ffd23f}
#cap{position:absolute;left:60px;right:60px;top:1480px;text-align:center;font:800 54px/1.32 Inter,Poppins;text-shadow:0 4px 18px rgba(0,0,0,.85)}
#cap span{display:inline-block;margin:0 6px}
#wm{position:absolute;left:0;right:0;bottom:120px;text-align:center;font:800 38px Inter;opacity:.55}#wm b{color:#ffd23f}
</style></head><body>
<div id="bg"></div><div id="grid"></div><div id="glow"></div>
<div id="prog"><i></i></div>
<div class="hdr"><div class="pill" id="pill"></div><div class="num" id="num"></div></div>
<div id="clock"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="rgba(8,16,31,.8)" stroke="rgba(255,255,255,.15)" stroke-width="8"/>
<circle id="arc" cx="50" cy="50" r="44" fill="none" stroke="var(--acc)" stroke-width="8" stroke-linecap="round" transform="rotate(-90 50 50)" stroke-dasharray="276.5" stroke-dashoffset="0"/></svg><span id="cnum">3</span></div>
<div id="stage"></div>
<div id="cap"></div>
<div id="wm">CBSE<b>Mock</b> · cbsemock.org.in</div>
<script>
const T=""" + data + """;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2,
 back=x=>{const c=1.6;x=cl(x);return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)},seg=(t,a,d)=>cl((t-a)/d);
$('pill').textContent=T.label;$('num').textContent='#'+String(T.n).padStart(2,'0')+' · 60-DAY BOARD PLAN';
const esc=s=>String(s);
function cardHTML(c){
 if(c.type==='title')return `${c.kicker?`<div class="kick">${esc(c.kicker)}</div>`:''}<div class="big">${esc(c.big)}</div>`;
 if(c.type==='list')return `${c.title?`<div class="ttl">${esc(c.title)}</div>`:''}`+c.items.map((x,i)=>`<div class="item"><i>${c.icons?c.icons[i]:(c.numbered===false?'✓':i+1)}</i><span>${esc(x)}</span></div>`).join('');
 if(c.type==='chain')return `${c.title?`<div class="ttl">${esc(c.title)}</div>`:''}<div class="chain">`+c.items.map((x,i)=>(i?'<div class="arw">↓</div>':'')+`<div class="ch">${esc(x[0]||x)}${x[1]?`<small>${esc(x[1])}</small>`:''}</div>`).join('')+'</div>';
 if(c.type==='compare')return `<div class="cmp bad"><div class="h">✕ ${esc(c.wrong[0])}</div><div class="b">${esc(c.wrong[1])}</div></div><div class="cmp good"><div class="h">✓ ${esc(c.right[0])}</div><div class="b">${esc(c.right[1])}</div></div>`;
 if(c.type==='quiz')return `<div class="q">${esc(c.q)}</div>`+c.opts.map((o,i)=>`<div class="opt" data-i="${i}"><b>${'ABCD'[i]}</b><span>${esc(o)}</span></div>`).join('');
 if(c.type==='worked')return `${c.title?`<div class="ttl">${esc(c.title)}</div>`:''}<div class="wk">`+c.lines.map((l,i)=>`<div class="wl${i===c.lines.length-1?' fin':''}">${l[0]?`<small>${esc(l[0])}</small>`:''}<span>${esc(l[1])}</span></div>`).join('')+'</div>';
 if(c.type==='recap')return `<div class="recap">${c.kicker?`<div class="kick">${esc(c.kicker)}</div>`:''}<div class="big">${esc(c.big)}</div></div>`;
 if(c.type==='end')return `<div class="ctab">${esc(c.cta)}</div><div><span class="url">${esc(c.url)}</span></div><div class="lg">CBSE<b>Mock</b></div>`;
 return '';
}
const stage=$('stage');
T.beats.forEach((b,i)=>{const d=document.createElement('div');d.className='card'+(b.card.type==='end'?' end':'');d.id='c'+i;d.innerHTML=cardHTML(b.card);stage.appendChild(d)});
function setTime(t){
 $('prog').firstChild.style.width=(100*t/T.total)+'%';
 let clockOn=0;
 T.beats.forEach((b,i)=>{
  const el=$('c'+i),nx=T.beats[i+1],start=i?b.s-0.25:0,end=nx?nx.s-0.25:T.total+1;
  const inn=back(seg(t,start,0.5)),out=ease(seg(t,end-0.05,0.35));
  const vis=t>=start-0.01&&t<end+0.4;el.style.display=vis?'flex':'none';if(!vis)return;
  el.style.opacity=cl(seg(t,start,0.25))*(1-out);
  el.style.transform=`translateY(${(1-inn)*160-out*120}px) rotateX(${(1-inn)*-38+out*40}deg) scale(${0.92+0.08*inn-out*.08})`;
  const c=b.card,dur=Math.max(.6,b.e-b.s),p=seg(t,b.s,dur);
  if(c.type==='title'){const big=el.querySelector('.big');big.style.transform=`scale(${1+Math.sin(t*2)*.008})`}
  if(c.type==='list'||c.type==='chain'){
   const its=el.querySelectorAll(c.type==='list'?'.item':'.ch'),arws=el.querySelectorAll('.arw'),n=its.length;
   its.forEach((x,k)=>{const a=seg(t,b.s+dur*(k/n)*0.92,0.35);x.style.opacity=cl(a);x.style.transform=`translateX(${(1-back(a))*-120}px)`});
   arws.forEach((x,k)=>{x.style.opacity=cl(seg(t,b.s+dur*((k+1)/n)*0.92-0.15,0.25))});
  }
  if(c.type==='compare'){const [w,g]=el.querySelectorAll('.cmp');const a=seg(t,b.s,0.4),bb=seg(t,b.s+dur*0.52,0.45);
   w.style.opacity=cl(a);w.style.transform=`translateY(${(1-back(a))*80}px) translateX(${a<1?0:(t<b.s+0.9?Math.sin(t*80)*10:0)}px)`;
   g.style.opacity=cl(bb);g.style.transform=`perspective(1200px) rotateX(${(1-back(bb))*-80}deg)`;}
  if(c.type==='quiz'){const os=el.querySelectorAll('.opt');os.forEach((o,k)=>{const a=seg(t,b.s+0.3+k*0.18,0.3);o.style.opacity=cl(a);o.style.transform=`translateX(${(1-back(a))*80}px)`});
   const cd0=b.e+0.05,rev=b.e+1.05;if(t>=b.s&&t<rev+0.2){clockOn=1;const left=Math.max(0,3-Math.floor((t-cd0)/0.33));$('cnum').textContent=t<cd0?'3':String(Math.max(1,left));
    $('arc').style.strokeDashoffset=276.5*cl((t-b.s)/(rev-b.s))}
   os.forEach((o,k)=>{o.classList.toggle('ok',t>=rev&&k===c.ans);o.classList.toggle('dim',t>=rev&&k!==c.ans)});}
  if(c.type==='worked'){const ls=el.querySelectorAll('.wl'),n=ls.length;ls.forEach((x,k)=>{const a=seg(t,b.s+dur*(k/n)*0.9,0.3);x.style.opacity=cl(a);x.style.transform=`translateY(${(1-ease(a))*24}px)`})}
  if(c.type==='recap'){const rc=el.querySelector('.recap');rc.style.transform=`scale(${0.85+0.15*back(seg(t,b.s,0.5))})`}
  if(c.type==='end'){const u=el.querySelector('.url');u.style.transform=`scale(${back(seg(t,b.s+0.35,0.45))})`}
 });
 $('clock').style.opacity=clockOn;
 // captions
 const cur=T.beats.find(b=>t>=b.s-0.12&&t<b.e+0.3),capEl=$('cap');
 if(cur&&cur.card.type!=='end'){const w=cur.cap.split(' '),n=Math.ceil(w.length*cl((t-cur.s)/(cur.e-cur.s)*1.12));
  capEl.innerHTML=w.map((x,i)=>`<span style="opacity:${i<n?1:.2}">${x}</span>`).join(' ');capEl.style.opacity=1}
 else capEl.style.opacity=0;
 $('wm').style.opacity=T.beats.length&&t>=T.beats[T.beats.length-1].s-0.25?0:.55;
}
window.setTime=setTime;setTime(0);
</script></body></html>"""


def render_frames(html, total, outdir, only=None):
    from playwright.sync_api import sync_playwright
    f = outdir / "reel.html"
    f.write_text(html, encoding="utf-8")
    n = int(round(total * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": Hh}, device_scale_factor=1)
        pg.goto(f.as_uri())
        pg.wait_for_timeout(400)
        for i in ([int(x * FPS) for x in only] if only is not None else range(n)):
            pg.evaluate(f"setTime({i / FPS})")
            pg.screenshot(path=str(outdir / f"frame_{i:05d}.jpg"), type="jpeg", quality=92)
        b.close()
    return n


def build(r, out, preview=None):
    tmp = Path(tempfile.mkdtemp(prefix="hack_"))
    times, total = build_audio(r, tmp)
    html = page_html(r, times, total)
    if preview is not None:
        pts = preview if isinstance(preview, list) else [preview]
        render_frames(html, total, tmp, only=pts)
        for k, x in enumerate(sorted(tmp.glob("frame_*.jpg"))):
            dst = Path(out) if len(pts) == 1 else Path(out).with_name(f"{Path(out).stem}_{k}{Path(out).suffix}")
            shutil.copy(x, dst)
        print(f"[preview] {out} (total {total:.1f}s; beats at {[round(s, 1) for s, _ in times]})")
        return total
    render_frames(html, total, tmp)
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(tmp / "frame_%05d.jpg"), "-i", str(tmp / "voice.wav")]
    if MUSIC.exists():
        cmd += ["-stream_loop", "-1", "-i", str(MUSIC), "-filter_complex",
                f"[2:a]volume=0.08,afade=t=in:st=0:d=1,afade=t=out:st={total - 1.5:.2f}:d=1.5[m];[1:a]volume=1.0[v];"
                "[v][m]amix=inputs=2:duration=first:normalize=0[a]", "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-profile:v", "main", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-c:a", "aac", "-ar", "44100", "-b:a", "128k", "-t", f"{total:.2f}", str(out)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        raise RuntimeError(res.stderr[-800:])
    # cover image = the hook card fully in
    THUMBS.mkdir(parents=True, exist_ok=True)
    k = int(min(times[0][1], 1.6) * FPS)
    from PIL import Image
    Image.open(tmp / f"frame_{k:05d}.jpg").convert("RGB").save(thumb_path(r), quality=88, optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[OK] {out} ({Path(out).stat().st_size / 1048576:.1f} MB, {total:.1f}s)")
    return total


def find(key):
    for r in load_specs():
        if key in (r["id"], str(r["n"]), f"{r['n']:02d}"):
            return r
    raise SystemExit(f"no campaign reel {key}")


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("reel", nargs="?", default="1")
    a.add_argument("--out")
    a.add_argument("--preview", type=float, nargs="*")
    a.add_argument("--missing", action="store_true")
    a = a.parse_args()
    if a.missing:
        VIDEOS.mkdir(parents=True, exist_ok=True)
        for r in load_specs():
            if not video_path(r).exists():
                build(r, video_path(r))
    else:
        r = find(a.reel)
        VIDEOS.mkdir(parents=True, exist_ok=True)
        build(r, a.out or str(video_path(r)), a.preview if a.preview else None)
