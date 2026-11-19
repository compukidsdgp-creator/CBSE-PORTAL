#!/usr/bin/env python3
"""
generate_mistake_reel.py — "Mistake Bank" reels (≈15 s, 1080×1920): one common board-exam mistake, shown
wrong → right with a 3D-styled animation, narrated (Kokoro TTS, offline) with on-screen captions,
sound effects and the usual music bed. Scenes are HTML/CSS drawn per frame and captured with Playwright.

Sample: Class 10 Chemistry, Ch 1 — "Never change subscripts to balance an equation".
    python3 generate_mistake_reel.py --out mistake_subscripts.mp4 [--lang en|hi] [--preview 6.0]
"""
import argparse
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
W, H, FPS = 1080, 1920, 30
LEAD, GAP, OUTRO = 0.35, 0.18, 1.6

REEL = {
    "id": "class10-chemistry-subscripts",
    "number": 1,
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Changing subscripts to balance",
            "stamp": ("WRONG", "H₂O₂ is hydrogen peroxide,<br>not water!"),
            "rule": ("Subscripts = what it is", "Coefficients = how many"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "beats": [   # (key, narration, caption shown on screen)
                ("intro", "Top board exam mistake, number one!", "Top board-exam mistakes · #1"),
                ("hook", "Never change subscripts to balance!", "Never change subscripts to balance!"),
                ("setup", "H two, plus O two, gives H two O. Oxygen doesn't balance.", "H₂ + O₂ → H₂O … oxygen doesn't balance"),
                ("wrong", "Make it H two O two? Wrong! That's hydrogen peroxide.", "Make it H₂O₂? WRONG — that's hydrogen peroxide!"),
                ("right", "Change only coefficients. Two H two, plus O two, gives two H two O.", "Change only coefficients: 2H₂ + O₂ → 2H₂O"),
                ("done", "Now it's balanced!", "Balanced ✓"),
            ],
        },
        "hi": {
            "voice": "hf_beta", "speed": 1.4,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "बैलेंस करने के लिए subscript बदलना",
            "stamp": ("गलत!", "H₂O₂ हाइड्रोजन पेरोक्साइड है,<br>पानी नहीं!"),
            "rule": ("Subscript = पहचान (क्या है)", "Coefficient = संख्या (कितने)"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर वन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #1"),
                ("hook", "बैलेंस करते समय सबस्क्रिप्ट कभी मत बदलो!", "बैलेंस के लिए subscript कभी मत बदलो!"),
                ("setup", "एच टू प्लस ओ टू, एच टू ओ। ऑक्सीजन कम है।", "H₂ + O₂ → H₂O … ऑक्सीजन कम है"),
                ("wrong", "एच टू ओ टू बना दिया? गलत! ये हाइड्रोजन पेरोक्साइड है।", "H₂O₂ बना दिया? गलत — ये हाइड्रोजन पेरोक्साइड है!"),
                ("right", "सिर्फ़ आगे का नंबर बदलो। टू एच टू, प्लस ओ टू, टू एच टू ओ।", "सिर्फ़ आगे का नंबर (coefficient) बदलो: 2H₂ + O₂ → 2H₂O"),
                ("done", "अब बैलेंस्ड!", "बैलेंस ✓"),
            ],
        },
    },
}


# ── audio ────────────────────────────────────────────────────────────────────
def tone(freq, dur, vol=0.25, kind="sine", decay=8.0):
    t = np.arange(int(dur * SR)) / SR
    if kind == "buzz":
        w = np.sign(np.sin(2 * np.pi * freq * t)) * 0.5 + np.sin(2 * np.pi * freq * 1.5 * t) * 0.5
    elif kind == "sweep":
        f = np.linspace(freq, freq * 3, len(t))
        w = np.sin(2 * np.pi * np.cumsum(f) / SR)
    else:
        w = np.sin(2 * np.pi * freq * t)
    return (w * np.exp(-decay * t) * vol).astype(np.float32)


def sfx_at(track, t, clip):
    i = int(t * SR)
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i]


def build_audio(L, tmp):
    clips, times, t = [], [], LEAD
    for key, text, cap in L["beats"]:
        a = synth(text, voice=L["voice"], speed=L["speed"])
        clips.append(a)
        times.append((key, t, t + len(a) / SR, cap))
        t += len(a) / SR + GAP
    total = t - GAP + OUTRO
    track = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for (key, s, e, _), a in zip(times, clips):
        sfx_at(track, s, a)
    T = {k: (s, e) for k, s, e, _ in times}
    # sound effects on the visual events
    sfx_at(track, max(0, T["intro"][0] - 0.3), tone(55, 0.6, 0.35, decay=5) + tone(110, 0.6, 0.15, decay=6))   # intro hit
    sfx_at(track, T["hook"][0] - 0.25, tone(220, 0.35, 0.18, "sweep", 6))                 # whoosh in
    sfx_at(track, T["wrong"][0] + 0.55, tone(660, 0.12, 0.22))                           # subscript pop
    sfx_at(track, T["wrong"][0] + 1.05, tone(140, 0.45, 0.20, "buzz", 5))                # WRONG buzz
    for k in (0.55, 1.75):
        sfx_at(track, T["right"][0] + k, tone(880, 0.14, 0.22) + tone(1320, 0.14, 0.10))  # coefficient pops
    sfx_at(track, T["done"][0], tone(1046, 0.5, 0.20, decay=4) + tone(1568, 0.5, 0.12, decay=4))   # ding
    track = track[: int(total * SR)]
    write_wav(tmp / "voice.wav", np.clip(track, -1, 1))
    return times, total


# ── visuals ──────────────────────────────────────────────────────────────────
def page_html(reel, L, times, total):
    faces = "".join(f"@font-face{{font-family:'{n}';src:url('{(FONTS / f).as_uri()}');font-weight:{w}}}"
                    for n, f, w in [("Inter", "Inter-Regular.otf", 400), ("Inter", "Inter-Bold.otf", 800),
                                    ("Poppins", "Poppins-Bold.ttf", 700), ("Poppins", "Poppins-Medium.ttf", 500)])
    tl = json.dumps({"beats": [{"k": k, "s": s, "e": e, "cap": c} for k, s, e, c in times], "total": total,
                     "rule": L["rule"], "title": L["title"], "badge": L["badge"], "n": reel["number"],
                     "intro": L["intro"], "stamp": L["stamp"], "cta": L["cta"]})
    return """<!doctype html><html><head><meta charset="utf-8"><style>""" + faces + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#060c1d;font-family:Inter,Poppins,sans-serif;color:#fff}
#intro{position:absolute;left:0;right:0;top:470px;height:900px;display:flex;flex-direction:column;align-items:center;justify-content:center;perspective:1400px;text-align:center}
#intro .fire{font-size:150px;line-height:1;filter:drop-shadow(0 0 40px rgba(255,120,40,.7))}
#intro .l1{font:700 92px/1.25 Poppins;letter-spacing:1px;margin-top:20px}
#intro .l2{font:700 150px/1.3 Poppins;padding:0 20px;background:linear-gradient(90deg,#ffd23f,#ff5470);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none}
#intro .n1{margin-top:30px;font:800 64px Inter;color:#0f2347;background:#ffd23f;border-radius:24px;padding:10px 34px;box-shadow:0 12px 0 rgba(0,0,0,.3)}
#rays{position:absolute;left:50%;top:820px;width:1600px;height:1600px;margin:-800px 0 0 -800px;border-radius:50%;background:repeating-conic-gradient(rgba(255,210,63,.10) 0 8deg,transparent 8deg 18deg);-webkit-mask-image:radial-gradient(#000 20%,transparent 65%)}
#bg{position:absolute;inset:0;background:radial-gradient(1100px 900px at 50% 38%,#16305f 0%,#08122a 55%,#050913 100%)}
#tint{position:absolute;inset:0;pointer-events:none}
#floor{position:absolute;left:-400px;right:-400px;top:1020px;height:1400px;transform-origin:50% 0;transform:perspective(900px) rotateX(72deg);
 background-image:linear-gradient(rgba(94,234,212,.22) 2px,transparent 2px),linear-gradient(90deg,rgba(94,234,212,.22) 2px,transparent 2px);background-size:110px 110px;
 -webkit-mask-image:linear-gradient(#000 0%,transparent 75%)}
.hdr{position:absolute;left:70px;right:70px;top:150px;display:flex;align-items:center;justify-content:space-between}
.badge{display:flex;align-items:center;gap:14px;background:linear-gradient(90deg,#e11d48,#be123c);padding:14px 26px;border-radius:99px;font:800 34px Inter;letter-spacing:.08em;box-shadow:0 10px 30px rgba(225,29,72,.45)}
.num{font:700 36px Poppins;color:#ffd23f}
.sub{position:absolute;left:72px;top:250px;font:600 30px Inter;color:rgba(255,255,255,.75)}
#hook{position:absolute;left:70px;right:70px;top:640px;height:420px;perspective:1400px}
#hookCard{position:absolute;inset:0;border-radius:30px;background:linear-gradient(135deg,#1e3a6e,#0f2347);border:3px solid #ffd23f;display:flex;align-items:center;gap:26px;padding:0 40px;
 box-shadow:0 30px 60px rgba(0,0,0,.5);transform-style:preserve-3d}
#hookCard .x{flex:0 0 170px;height:170px;font-size:110px!important;border-radius:50%;background:#e11d48;display:flex;align-items:center;justify-content:center;font:800 80px Inter;box-shadow:0 0 0 10px rgba(225,29,72,.25)}
#hookCard b{font:700 76px/1.06 Poppins}
#stage{position:absolute;left:0;right:0;top:640px;height:520px;perspective:1600px}
#row{position:absolute;left:0;right:0;top:0;height:520px;display:flex;align-items:center;justify-content:center;gap:10px;transform-style:preserve-3d}
.mol{position:relative;width:250px;height:340px;transform-style:preserve-3d}
.op{font:700 90px Poppins;color:#ffd23f;width:80px;text-align:center;text-shadow:0 6px 20px rgba(0,0,0,.5)}
.atom{position:absolute;border-radius:50%;box-shadow:0 22px 30px rgba(0,0,0,.45)}
.H{width:78px;height:78px;background:radial-gradient(circle at 32% 30%,#ffffff 0%,#dfe7f2 35%,#8d9bb3 100%)}
.O{width:118px;height:118px;background:radial-gradient(circle at 32% 30%,#ffb3b3 0%,#ef4444 40%,#7f1d1d 100%)}
.lbl{position:absolute;left:0;right:0;bottom:6px;text-align:center;font:700 74px Poppins;letter-spacing:-1px}
.lbl sub{font-size:.62em}.lbl .co{color:#ffd23f;display:inline-block}.lbl .bad{color:#ff5470;display:inline-block}
.shadow{position:absolute;left:30px;right:30px;bottom:96px;height:34px;border-radius:50%;background:radial-gradient(rgba(0,0,0,.55),transparent 70%)}
#scale{position:absolute;left:190px;right:190px;top:1170px;height:230px}
#beam{position:absolute;left:0;right:0;top:40px;height:16px;border-radius:8px;background:linear-gradient(#e5e7eb,#9ca3af);transform-origin:50% 50%}
#post{position:absolute;left:50%;top:48px;width:16px;height:150px;margin-left:-8px;background:linear-gradient(90deg,#9ca3af,#e5e7eb,#9ca3af)}
#base{position:absolute;left:50%;top:190px;width:180px;height:22px;margin-left:-90px;border-radius:10px;background:#9ca3af}
.pan{position:absolute;top:56px;width:250px;transform-origin:50% 0}
.pan .str{height:50px;border-left:3px solid #cbd5e1;border-right:3px solid #cbd5e1;margin:0 30px}
.pan .dish{height:92px;border-radius:0 0 125px 125px;background:linear-gradient(#1f3b6d,#0e1f3d);border:3px solid #5eead4;display:flex;flex-direction:column;align-items:center;justify-content:center;font:800 30px Inter}
.pan .dish i{font-style:normal;font:700 36px Poppins;color:#ffd23f}
#stamp{position:absolute;left:110px;right:110px;top:720px;height:300px;border:12px solid #ff3355;border-radius:30px;display:flex;flex-direction:column;align-items:center;justify-content:center;
 color:#ff3355;background:rgba(20,0,8,.82);box-shadow:0 0 60px rgba(255,51,85,.5);text-align:center}
#stamp b{font:800 120px/1.3 Inter,Poppins;letter-spacing:.06em}#stamp span{font:700 44px Poppins;color:#ffd0d8;margin-top:12px}
#ok{position:absolute;left:50%;top:700px;width:260px;height:260px;margin-left:-130px;border-radius:50%;background:radial-gradient(#22c55e,#15803d);display:flex;align-items:center;justify-content:center;
 font:800 170px Inter;box-shadow:0 0 0 22px rgba(34,197,94,.25),0 0 90px rgba(34,197,94,.6)}
#rule{position:absolute;left:80px;right:80px;top:1040px;border-radius:28px;background:linear-gradient(135deg,#0f2347,#13306a);border:3px solid #5eead4;padding:30px 36px;box-shadow:0 30px 60px rgba(0,0,0,.45)}
#rule p{font:700 48px/1.3 Poppins}#rule p:first-child{color:#5eead4}#rule p:last-child{color:#ffd23f}
#cap{position:absolute;left:70px;right:70px;top:1440px;text-align:center;font:800 54px/1.3 Inter,Poppins;text-shadow:0 4px 18px rgba(0,0,0,.8)}
#cap .w{display:inline-block;margin:0 6px}
#cta{position:absolute;left:80px;right:80px;top:1440px;height:150px;border-radius:75px;background:linear-gradient(90deg,#ffd23f,#c9a227);color:#0f2347;display:flex;align-items:center;justify-content:center;gap:18px;font:800 46px Inter;box-shadow:0 14px 0 rgba(0,0,0,.3)}
#logo{position:absolute;left:0;right:0;top:1620px;text-align:center;font:800 44px Inter}#logo b{color:#ffd23f}
#prog{position:absolute;left:70px;right:70px;top:110px;height:8px;border-radius:8px;background:rgba(255,255,255,.12)}#prog i{display:block;height:100%;border-radius:8px;background:#ffd23f}
</style></head><body>
<div id="bg"></div><div id="rays"></div><div id="floor"></div><div id="tint"></div>
<div id="intro"><div class="fire">🔥</div><div class="l1" id="i1"></div><div class="l2" id="i2"></div><div class="n1">#01</div></div>
<div id="prog"><i></i></div>
<div class="hdr"><div class="badge">⚠ MISTAKE BANK</div><div class="num" id="num"></div></div>
<div class="sub" id="sub"></div>
<div id="hook"><div id="hookCard"><div class="x">✕</div><b id="hookT"></b></div></div>
<div id="stage"><div id="row"></div></div>
<div id="scale"><div id="post"></div><div id="base"></div><div id="beam"></div>
 <div class="pan" id="panL" style="left:-60px"><div class="str"></div><div class="dish">LEFT<i id="cL"></i></div></div>
 <div class="pan" id="panR" style="right:-60px"><div class="str"></div><div class="dish">RIGHT<i id="cR"></i></div></div></div>
<div id="stamp"><b id="s1"></b><span id="s2"></span></div>
<div id="ok">✓</div>
<div id="rule"><p id="r1"></p><p id="r2"></p></div>
<div id="cap"></div>
<div id="cta"></div>
<div id="logo">CBSE<b>Mock</b></div>
<script>
const T=""" + tl + """;
const B={};T.beats.forEach(b=>B[b.k]=b);
document.getElementById('num').textContent='#'+String(T.n).padStart(2,'0');
document.getElementById('sub').textContent=T.badge;
document.getElementById('hookT').textContent=T.title;
document.getElementById('i1').textContent=T.intro[0];document.getElementById('i2').textContent=T.intro[1];
document.getElementById('s1').textContent=T.stamp[0];document.getElementById('s2').innerHTML=T.stamp[1];document.getElementById('cta').textContent=T.cta;
document.getElementById('r1').textContent=T.rule[0];document.getElementById('r2').textContent=T.rule[1];
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2,
 back=x=>{const c=1.7;x=cl(x);return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)},
 seg=(t,a,d)=>cl((t-a)/d);
// molecules: a group of atoms (x,y relative, kind)
const MOL={H2:[['H',58,120],['H',118,120]],O2:[['O',38,95],['O',118,95]],H2O:[['O',66,96],['H',30,70],['H',160,70]],
           H2O2:[['O',30,100],['O',120,100],['H',8,72],['H',196,72]]};
function atoms(kind,extra){return MOL[kind].map(([k,x,y],i)=>`<div class="atom ${k}" style="left:${x}px;top:${y}px"></div>`).join('')}
function mol(id,kind,label){return `<div class="mol" id="${id}"><div class="shadow"></div><div class="atoms">${atoms(kind)}</div><div class="lbl">${label}</div></div>`}
const row=$('row');
function lay(state){ // state: 'base','wrong','right'
  const co=c=>`<span class="co">${c}</span>`;
  let L1='H<sub>2</sub>',R1='H<sub>2</sub>O',rk='H2O';
  if(state==='wrong'){R1='H<sub>2</sub>O<span class="bad"><sub>2</sub></span>';rk='H2O2'}
  if(state==='right'){L1=co('2')+'H<sub>2</sub>';R1=co('2')+'H<sub>2</sub>O'}
  row.innerHTML=mol('m1','H2',L1)+'<div class="op">+</div>'+mol('m2','O2','O<sub>2</sub>')+'<div class="op">→</div>'+mol('m3',rk,R1);
  if(state==='right'){ // ghost second molecules behind (depth)
    ['m1','m3'].forEach(id=>{const m=$(id),a=m.querySelector('.atoms');const g=a.cloneNode(true);g.className='atoms ghost';g.style.cssText='position:absolute;inset:0;transform:translate(34px,-58px) scale(.86);opacity:0';m.insertBefore(g,a)});
  }
}
let laid='';
function setTime(t){
  $('prog').firstChild.style.width=(100*t/T.total)+'%';
  const h=B.hook,s=B.setup,w=B.wrong,r=B.right,d=B.done,it=B.intro;
  const ii=back(seg(t,0,0.55)),io=ease(seg(t,h.s-0.35,0.35));
  $('intro').style.opacity=cl(seg(t,0,0.2))*(1-io);
  $('intro').style.transform=`scale(${(0.6+0.4*ii)*(1+io*.4)}) rotateX(${(1-ii)*50}deg)`;
  document.querySelector('#intro .n1').style.transform=`scale(${back(seg(t,it.s+1.2,0.4))}) rotate(${(1-back(seg(t,it.s+1.2,0.4)))*-20}deg)`;
  document.querySelector('#intro .fire').style.transform=`scale(${1+Math.sin(t*9)*.06}) translateY(${Math.sin(t*5)*6}px)`;
  $('rays').style.opacity=(1-io)*.9;$('rays').style.transform=`rotate(${t*14}deg)`;
  $('hook').style.visibility=t<h.s-0.35?'hidden':'visible';
  // hook card flips in, then folds away to the top
  const hin=back(seg(t,h.s-0.3,0.6)),hout=ease(seg(t,s.s-0.1,0.5));
  $('hookCard').style.transform=`rotateX(${(1-hin)*-90+hout*60}deg) rotateZ(${Math.sin(t*3)*1.2}deg) scale(${1-hout*.35}) translateY(${-hout*380}px)`;
  $('hook').style.opacity=1-hout;
  // stage state
  let st='base';if(t>=w.s+0.5&&t<r.s+0.25)st='wrong';if(t>=r.s+0.25)st='right';
  if(st!==laid){lay(st);laid=st}
  const sin=back(seg(t,s.s-0.05,0.7));
  $('stage').style.opacity=cl(seg(t,s.s-0.2,0.4));
  $('row').style.transform=`translateY(${(1-sin)*200}px) rotateX(${12+(1-sin)*30}deg) rotateY(${Math.sin(t*1.3)*6}deg)`;
  document.querySelectorAll('.mol .atoms').forEach((a,i)=>{if(!a.classList.contains('ghost'))a.style.transform=`translateY(${Math.sin(t*2.4+i)*8}px) rotateZ(${Math.sin(t*1.7+i)*4}deg)`});
  // morph pop in the wrong phase
  if(st==='wrong'){const p=back(seg(t,w.s+0.5,0.35));const b=document.querySelector('.lbl .bad');if(b)b.style.transform=`scale(${p*1.0}) translateY(${(1-p)*-40}px)`;
    const shake=seg(t,w.s+1.0,0.5)<1&&t>w.s+1.0?Math.sin(t*90)*14*(1-seg(t,w.s+1.0,0.5)):0;$('row').style.transform+=` translateX(${shake}px)`}
  if(st==='right'){const p1=back(seg(t,r.s+0.55,0.35)),p2=back(seg(t,r.s+1.75,0.35));const cs=document.querySelectorAll('.lbl .co');
    if(cs[0])cs[0].style.transform=`scale(${p1})`;if(cs[1])cs[1].style.transform=`scale(${p2})`;
    const gs=document.querySelectorAll('.ghost');if(gs[0])gs[0].style.opacity=cl(seg(t,r.s+0.55,0.4))*.9;if(gs[1])gs[1].style.opacity=cl(seg(t,r.s+1.75,0.4))*.9}
  // counts on the scale
  let cl_='H 2 · O 2',cr='H 2 · O 1';
  if(st==='wrong'){cr='H 2 · O 2'}
  if(st==='right'){const a=t>=r.s+0.55,b=t>=r.s+1.75;cl_=a?'H 4 · O 2':'H 2 · O 2';cr=b?'H 4 · O 2':'H 2 · O 1'}
  $('cL').textContent=cl_;$('cR').textContent=cr;
  // tilt (left pan lower = left heavier): keyframes, eased
  const K=[[0,-9],[w.s+0.5,-9],[w.s+0.9,0],[r.s+0.25,0],[r.s+0.55,-9],[r.s+0.6,-9],[r.s+0.95,-13],[r.s+1.75,-13],[r.s+2.15,0]];
  let tilt=K[K.length-1][1];for(let i=0;i<K.length-1;i++){if(t<K[i+1][0]){const a=K[i],b=K[i+1];tilt=a[1]+(b[1]-a[1])*ease(cl((t-a[0])/Math.max(.001,b[0]-a[0])));break}}
  $('beam').style.transform=`rotate(${tilt}deg)`;
  $('panL').style.transform=`translateY(${-Math.sin(tilt*Math.PI/180)*170}px)`;$('panR').style.transform=`translateY(${Math.sin(tilt*Math.PI/180)*170}px)`;
  $('scale').style.opacity=cl(seg(t,s.s+0.4,0.5))*(1-cl(seg(t,d.s+0.6,0.4)));
  // WRONG stamp + red tint
  const wi=seg(t,w.s+1.0,0.25),wo=seg(t,r.s-0.1,0.3);
  $('stamp').style.opacity=wi*(1-wo);$('stamp').style.transform=`rotate(${-8+ (1-back(wi))*30}deg) scale(${2.2-1.2*back(wi)})`;
  $('tint').style.background=`rgba(255,30,60,${0.22*wi*(1-wo)})`;
  // done: tick + green tint, then rule card
  const di=back(seg(t,d.s,0.45));$('ok').style.opacity=cl(seg(t,d.s,0.2))*(1-seg(t,d.s+0.9,0.3));$('ok').style.transform=`scale(${di}) rotate(${(1-di)*-90}deg)`;
  if(t>=d.s)$('tint').style.background=`rgba(34,197,94,${0.16*(1-seg(t,d.s+0.8,0.6))})`;
  const ri=back(seg(t,d.s+0.6,0.5));$('rule').style.opacity=cl(seg(t,d.s+0.6,0.3));$('rule').style.transform=`perspective(1200px) rotateX(${(1-ri)*80}deg) translateY(${(1-ri)*60}px)`;
  $('stage').style.transform=`translateY(${-ease(seg(t,d.s+0.6,0.5))*80}px) scale(${1-ease(seg(t,d.s+0.6,0.5))*.12})`;
  // captions: words appear with the voice
  const cur=T.beats.find(b=>t>=b.s-0.15&&t<b.e+0.25);const capEl=$('cap');
  if(cur&&cur.k!=='done'&&cur.k!=='intro'){const words=cur.cap.split(' ');const n=Math.ceil(words.length*cl((t-cur.s)/(cur.e-cur.s)*1.15));
    capEl.innerHTML=words.map((x,i)=>`<span class="w" style="opacity:${i<n?1:.18};color:${cur.k==='wrong'&&/WRONG|गलत/.test(x)?'#ff5470':(cur.k==='right'&&/^2/.test(x)?'#ffd23f':'#fff')}">${x}</span>`).join(' ');capEl.style.opacity=1}
  else capEl.style.opacity=0;
  // outro CTA
  const ci=back(seg(t,d.s+1.2,0.5));$('cta').style.opacity=cl(seg(t,d.s+1.2,0.3));$('cta').style.transform=`scale(${ci})`;
  $('logo').style.opacity=cl(seg(t,d.s+1.4,0.4));
}
window.setTime=setTime;setTime(0);
</script></body></html>"""


def render_frames(html, total, outdir, only=None):
    from playwright.sync_api import sync_playwright
    page_file = outdir / "reel.html"
    page_file.write_text(html, encoding="utf-8")
    n = int(round(total * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(page_file.as_uri())
        pg.wait_for_timeout(400)
        frames = [int(only * FPS)] if only is not None else range(n)
        for i in frames:
            pg.evaluate(f"setTime({i / FPS})")
            pg.screenshot(path=str(outdir / f"frame_{i:05d}.jpg"), type="jpeg", quality=92)
        b.close()
    return n


def build(reel, out, preview=None, lang="en"):
    L = reel["lang"][lang]
    tmp = Path(tempfile.mkdtemp(prefix="mistake_"))
    times, total = build_audio(L, tmp)
    html = page_html(reel, L, times, total)
    if preview is not None:
        render_frames(html, total, tmp, only=preview)
        shutil.copy(next(tmp.glob("frame_*.jpg")), out)
        print(f"[preview] {out} at {preview}s (total {total:.1f}s)")
        return
    render_frames(html, total, tmp)
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(tmp / "frame_%05d.jpg"), "-i", str(tmp / "voice.wav")]
    if MUSIC.exists():
        cmd += ["-stream_loop", "-1", "-i", str(MUSIC), "-filter_complex",
                f"[2:a]volume=0.09,afade=t=in:st=0:d=1,afade=t=out:st={total - 1.5:.2f}:d=1.5[m];[1:a]volume=1.0[v];"
                "[v][m]amix=inputs=2:duration=first:normalize=0[a]", "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-profile:v", "main", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-c:a", "aac", "-ar", "44100", "-b:a", "128k", "-t", f"{total:.2f}", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-800:])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[OK] {out} ({Path(out).stat().st_size / 1048576:.1f} MB, {total:.1f}s)")


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--out", default="mistake_reel.mp4")
    a.add_argument("--preview", type=float)
    a.add_argument("--lang", default="en", choices=["en", "hi"])
    a = a.parse_args()
    build(REEL, a.out, a.preview, a.lang)
