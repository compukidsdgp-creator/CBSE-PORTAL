"""Send a poster to Telegram by uploading the file itself (multipart), so it never depends on GitHub
serving a freshly pushed image. Returns True on success and prints Telegram's error text on failure."""
import json
import os
import urllib.error
import urllib.request
import uuid
from pathlib import Path


def send_photo(path, caption, chat=None, token=None, parse_mode=None):
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = chat or os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        print("[TG] no token/chat — skipped")
        return False
    b = uuid.uuid4().hex
    fields = {"chat_id": str(chat), "caption": caption[:1024]}
    if parse_mode:
        fields["parse_mode"] = parse_mode
    body = b""
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    p = Path(path)
    body += (f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="{p.name}"\r\n'
             f"Content-Type: image/jpeg\r\n\r\n").encode() + p.read_bytes() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendPhoto", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            ok = json.load(r).get("ok", False)
            print("[TG] posted" if ok else "[TG] not ok")
            return ok
    except urllib.error.HTTPError as e:
        print(f"::warning::Telegram post failed ({e.code}): {e.read().decode()[:300]}")
    except Exception as e:
        print(f"::warning::Telegram post failed: {e}")
    return False
