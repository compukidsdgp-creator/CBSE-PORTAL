"""Publish approved lab drafts: virtual-labs/<subject>/_drafts/<file> → virtual-labs/<subject>/<file>.
Removes the noindex meta and the draft bar, then deletes the draft. Only drafts that pass lab_check --live are moved.
    python3 labs_publish.py
"""
import re
from pathlib import Path

import lab_check
import lab_registry as LR

ROOT = Path(__file__).resolve().parent


def publish():
    appr = LR.approvals()
    done = []
    for lab in LR.labs():
        if not lab["draft"] or appr.get(lab["id"], {}).get("status") != "approved":
            continue
        draft, target = ROOT / lab["draft"], ROOT / lab["file"]
        s = draft.read_text(encoding="utf-8")
        s = re.sub(r'\s*<meta name="robots" content="noindex[^"]*">', "", s, count=1)
        s = re.sub(r'\s*<div class="lab-draft"[^>]*>.*?</div>', "", s, count=1, flags=re.S)
        s = s.replace("../../../", "../../")              # drafts live one folder deeper than the published lab
        tmp = draft.with_suffix(".publish.html")
        tmp.write_text(s, encoding="utf-8")
        probs = lab_check.check(tmp, live=True)
        if probs:
            tmp.unlink()
            print(f"::warning::{lab['id']} approved but not published: " + "; ".join(probs))
            continue
        target.write_text(s, encoding="utf-8")
        tmp.unlink()
        draft.unlink()
        try:
            import favicon_tags
            favicon_tags.add(target)
        except Exception:
            pass
        done.append(lab["id"])
        print(f"[labs] published {lab['id']}")
    for d in (ROOT / "virtual-labs").glob("*/_drafts"):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    return done


if __name__ == "__main__":
    print(f"[labs] {len(publish())} lab(s) published")
