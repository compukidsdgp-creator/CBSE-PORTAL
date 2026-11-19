"""Hindi TTS comparison (runs on GitHub Actions, which can reach Hugging Face): same script, several engines.
Writes tts-samples/<engine>.mp3"""
import os, subprocess, sys, time, wave
from pathlib import Path
import numpy as np
OUT = Path("tts-samples"); OUT.mkdir(exist_ok=True)
LINES = ["बोर्ड एग्ज़ाम की टॉप गलती, नंबर वन!",
         "इक्वेशन बैलेंस करते समय, सबस्क्रिप्ट कभी मत बदलो!",
         "एच टू प्लस ओ टू से एच टू ओ बनता है। लेकिन ऑक्सीजन बैलेंस नहीं है।",
         "तो क्या एच टू ओ टू बना दें? बिल्कुल गलत! ये तो हाइड्रोजन पेरोक्साइड है, पानी नहीं।",
         "सिर्फ़ आगे का नंबर बदलो। टू एच टू, प्लस ओ टू, देता है टू एच टू ओ।",
         "अब दोनों तरफ़ बराबर। बैलेंस्ड!"]
TEXT = " ".join(LINES)

def to_mp3(wav, name):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-ar", "44100", "-b:a", "128k", str(OUT / f"{name}.mp3")], check=True)
    print("[ok]", name)

def piper(voice):
    import urllib.request
    base = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/{voice}/medium/hi_IN-{voice}-medium"
    for ext in (".onnx", ".onnx.json"):
        urllib.request.urlretrieve(base + ext, f"/tmp/{voice}{ext}")
    from piper import PiperVoice
    v = PiperVoice.load(f"/tmp/{voice}.onnx")
    wav = Path(f"/tmp/piper_{voice}.wav")
    with wave.open(str(wav), "wb") as w:
        v.synthesize_wav(TEXT, w)
    to_mp3(wav, f"piper-{voice}")

def parler(name, desc):
    import torch, soundfile as sf
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer
    mid = "ai4bharat/indic-parler-tts"
    model = ParlerTTSForConditionalGeneration.from_pretrained(mid)
    tok = AutoTokenizer.from_pretrained(mid)
    dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
    parts = []
    for line in LINES:
        t = time.time()
        d = dtok(desc, return_tensors="pt"); p = tok(line, return_tensors="pt")
        with torch.no_grad():
            a = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask, prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
        a = a.cpu().numpy().squeeze(); parts += [a, np.zeros(int(0.18 * model.config.sampling_rate))]
        print(f"  {name}: {len(a)/model.config.sampling_rate:.1f}s audio in {time.time()-t:.0f}s")
    wav = Path(f"/tmp/parler_{name}.wav"); sf.write(wav, np.concatenate(parts), model.config.sampling_rate)
    to_mp3(wav, f"indic-parler-{name}")

which = sys.argv[1]
if which == "piper":
    for v in ("priyamvada", "pratham", "rohan"):
        try: piper(v)
        except Exception as e: print("[fail] piper", v, e)
else:
    parler("divya", "Divya speaks with a clear, energetic and friendly tone at a moderately fast pace, like a teacher explaining to students. The recording is very clear with no background noise.")
    parler("rohit", "Rohit speaks with a clear, confident and expressive tone at a moderately fast pace, like a teacher explaining to students. The recording is very clear with no background noise.")
