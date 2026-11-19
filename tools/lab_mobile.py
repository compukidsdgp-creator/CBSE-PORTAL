"""Mobile layer for the older (pre-standard) virtual labs, until each one is rebuilt to virtual-labs/LAB_STANDARD.md.
Injects one idempotent block (<!-- LAB-MOBILE:START/END -->) before </head> of every lab page that does not yet
carry the new standard: bigger tap targets (back bar, buttons, inputs, sliders, switches), compact share buttons
that keep clear of the content, and a small script that lifts any text under 12 px to 12 px on phones.
    python3 tools/lab_mobile.py            (all labs)      python3 tools/lab_mobile.py --remove
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- LAB-MOBILE:START -->", "<!-- LAB-MOBILE:END -->"
BLOCK = START + """
<style>
@media (max-width:760px){
 .portal-backbar #portal-back,.portal-backbar a{min-height:40px;display:inline-flex;align-items:center}
 .share-fab-wrap{bottom:calc(12px + env(safe-area-inset-bottom,0px))!important;right:10px!important;gap:8px!important}
 .share-fab{width:42px!important;height:42px!important;opacity:.92}
 .share-fab .fab-tooltip{display:none!important}
 body{padding-bottom:64px}
 input[type=range]{min-height:36px;touch-action:pan-y}
 input[type=checkbox],input[type=radio]{min-width:22px;min-height:22px}
 input:not([type=range]):not([type=checkbox]):not([type=radio]):not([type=hidden]):not([type=color]),select,textarea{min-height:40px;font-size:max(16px,1em)}
 button:not(.toggle):not(.share-fab),.btn,[role=button],a.button{min-height:40px}
 .toggle{position:relative}.toggle::before{content:"";position:absolute;inset:-9px -4px}
 img,video,canvas{max-width:100%}
 pre,code{white-space:pre-wrap;word-break:break-word}
}
</style>
<script>
(function(){if(!window.matchMedia||!matchMedia('(max-width:760px)').matches)return;var runs=0,t=null;
function lift(){runs++;var els=document.body.getElementsByTagName('*');for(var i=0;i<els.length;i++){var e=els[i];if(e.closest&&e.closest('svg'))continue;
 var txt=false;for(var n=e.firstChild;n;n=n.nextSibling){if(n.nodeType===3&&n.textContent.trim().length>1){txt=true;break}}if(!txt)continue;
 var fs=parseFloat(getComputedStyle(e).fontSize);if(fs&&fs<12)e.style.fontSize='12px'}}
function soon(){if(runs>25)return;clearTimeout(t);t=setTimeout(lift,450)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',lift);else lift();
try{new MutationObserver(soon).observe(document.body,{childList:true,subtree:true})}catch(e){}})();
</script>
""" + END


def targets():
    for f in sorted((ROOT / "virtual-labs").glob("**/*.html")):
        if "_drafts" in f.parts:
            continue
        s = f.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in s or "<title>Moved" in s:
            continue
        yield f, s


def main(remove=False):
    n = 0
    for f, s in targets():
        new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
        if not remove and 'name="cbse-lab-standard"' not in new and "</head>" in new:
            new = new.replace("</head>", BLOCK + "\n</head>", 1)
        if new != s:
            f.write_text(new, encoding="utf-8")
            n += 1
    print(f"[lab_mobile] {'removed from' if remove else 'updated'} {n} page(s)")


if __name__ == "__main__":
    main("--remove" in sys.argv)
