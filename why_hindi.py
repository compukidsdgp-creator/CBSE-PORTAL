#!/usr/bin/env python3
"""
why_hindi.py — Hindi versions of the WHY? reels.

A why_reels module gets a Hindi version by adding a HINDI = {...} block (see why_reels/WRITING_GUIDE.md).
The "WHY? Hindi" workflow makes the Hindi voice (Indic Parler-TTS, voice Rohit) and renders
formula-posts/why/hindi/why_<module>_hi.mp4 (+ .txt caption), then sends the owner a private Telegram preview.

Posting: the 8 PM formula-reel slot on Sun / Wed / Fri (IST) — one Hindi WHY? reel instead of the formula reel.
Posting only starts once the owner has approved the pilot: formula-posts/why/hindi/ENABLED must exist.
Order: the pilot (PILOT) first, then Hindi versions of reels already posted in English, then the rest.

    python3 why_hindi.py render-missing      render every module with HINDI but no Hindi video (prints new files)
    python3 why_hindi.py due                 exit 0 if a Hindi reel should post in the 8 PM slot now
    python3 why_hindi.py post [--dry-run]
    python3 why_hindi.py next                the module the nightly adapter should translate next (JSON)
    python3 why_hindi.py status
"""
import importlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WHY = ROOT / "formula-posts" / "why"
HI_DIR, HI_POSTED = WHY / "hindi", WHY / "hindi" / "posted"
ENABLED = HI_DIR / "ENABLED"
STATE = HI_DIR / "state.json"
IST = timezone(timedelta(hours=5, minutes=30))
DAYS = {6, 2, 4}            # Sun, Wed, Fri (Monday = 0)
PILOT = ["trig_identity", "trig_sec", "sin30_half", "elevation_depression", "circle_area"]


def _mod_of(path):
    return Path(path).stem.split("_why_", 1)[-1]


def has_hi(name):
    f = ROOT / "why_reels" / f"{name}.py"
    return f.exists() and re.search(r"^HINDI\s*=", f.read_text(encoding="utf-8"), re.M) is not None


def video(name):
    return HI_DIR / f"why_{name}_hi.mp4"


def posted(name):
    return (HI_POSTED / f"why_{name}_hi.mp4").exists()


def order():
    """Every WHY? module in Hindi posting order (pilot → posted in English → main queue → backup → the rest)."""
    seen, out = set(), []
    def add(n):
        if n not in seen and (ROOT / "why_reels" / f"{n}.py").exists():
            seen.add(n); out.append(n)
    for n in PILOT:
        add(n)
    for d in ("posted", "queue", "backup"):
        for f in sorted((WHY / d).glob("*.mp4")) if (WHY / d).exists() else []:
            add(_mod_of(f))
    for f in sorted((ROOT / "why_reels").glob("[a-z]*.py")):
        add(f.stem)
    return out


def render_missing():
    HI_DIR.mkdir(parents=True, exist_ok=True)
    new = []
    for name in order():
        if not has_hi(name) or video(name).exists() or posted(name):
            continue
        if not (WHY / "voice_hi" / name / "end.wav").exists():
            print(f"[hindi] {name}: voice missing — skipped"); continue
        print(f"[hindi] rendering {name} …", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "why_kit.py"), "--reel", name, "--lang", "hi"])
        if r.returncode == 0 and video(name).exists():
            new.append(str(video(name).relative_to(ROOT)))
    print("\n".join(new) if new else "[hindi] nothing to render")
    return new


def state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def next_ready():
    return next((n for n in order() if video(n).exists() and not posted(n)), None)


def due():
    now = datetime.now(IST)
    if not ENABLED.exists() or now.weekday() not in DAYS:
        return None
    if state().get("last") == now.date().isoformat():
        return None
    return next_ready()


def post(dry=False):
    import post_formula_reel as P
    import social_links as SL
    P.LOG_CSV = HI_DIR / "hindi_log.csv"
    name = due() if not dry else (due() or next_ready())
    if not name:
        print("[hindi] nothing due"); return False
    mp4, txt = video(name), video(name).with_suffix(".txt")
    cap = txt.read_text(encoding="utf-8").strip() if txt.exists() else importlib.import_module(f"why_reels.{name}").HINDI["caption"].strip()
    print(f"[hindi] posting {mp4.name}\n{cap[:200]}")
    fb = P._upload_video_fb(mp4, cap, dry_run=dry)
    ig = P._upload_reel_instagram(mp4, SL.ig_caption(cap), dry_run=dry)
    P.log_reel(mp4.name, fb, ig, dry)
    if not dry and (fb or ig):
        HI_POSTED.mkdir(parents=True, exist_ok=True)
        shutil.move(str(mp4), str(HI_POSTED / mp4.name))
        if txt.exists():
            shutil.move(str(txt), str(HI_POSTED / txt.name))
        st = state(); st["last"] = datetime.now(IST).date().isoformat()
        st.setdefault("posted", []).append({"module": name, "fb": fb, "ig": ig, "at": datetime.now(IST).isoformat(timespec="seconds")})
        STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"FB: {fb or 'FAILED'} | IG: {ig or 'FAILED'}")
    return bool(fb or ig)


def next_job():
    """Next module without a HINDI block, in posting order (for the nightly Hindi adapter)."""
    n = next((n for n in order() if not has_hi(n)), None)
    return {"action": "translate", "module": n} if n else {"action": "none"}


def status():
    o = order()
    ready = [n for n in o if video(n).exists() and not posted(n)]
    print(f"posting: {'ON' if ENABLED.exists() else 'OFF (waiting for the owner to approve the pilot)'} · Sun/Wed/Fri 8 PM")
    print(f"modules: {len(o)} · with Hindi text: {sum(has_hi(n) for n in o)} · ready videos: {len(ready)} · "
          f"posted: {len(list(HI_POSTED.glob('*.mp4'))) if HI_POSTED.exists() else 0}")
    print("next to post:", ready[0] if ready else "none")
    print("next to translate:", next_job().get("module"))


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    if a[0] == "render-missing":
        render_missing()
    elif a[0] == "due":
        sys.exit(0 if due() else 1)
    elif a[0] == "post":
        sys.exit(0 if post("--dry-run" in a) else 1)
    elif a[0] == "next":
        print(json.dumps(next_job(), indent=1))
    else:
        status()
