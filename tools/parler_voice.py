"""Make the Hindi narration clips for Mistake Bank reels with AI4Bharat Indic Parler-TTS (voice: Rohit).
Runs on GitHub Actions (needs the HF_TOKEN secret). Writes mistake_reels/voice/<reel-id>/<lang>/<beat>.wav and campaign_reels/voice/<id>/hi/b<i>.wav
    python3 tools/parler_voice.py            (every reel/beat whose clip is missing)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import generate_mistake_reel as G

STYLE = {"rohit": "Rohit speaks with a clear, confident and expressive tone at a moderately fast pace, like a teacher explaining "
                  "to students. The recording is very clear with no background noise."}
todo = []
for reel in G.load_specs():
    for lang, L in reel["lang"].items():
        if L.get("engine") != "parler":
            continue
        for key, text, _ in L["beats"]:
            out = G.VOICE_DIR / reel["id"] / lang / f"{key}.wav"
            if not out.exists():
                todo.append((out, text, STYLE[L["voice"]]))
# 60-day campaign reels: Hindi block REEL["hi"] → campaign_reels/voice/<id>/hi/b<i>.wav
import generate_hack_reel as GH
for reel in GH.load_specs():
    for lang in GH.langs(reel):
        L = GH.view(reel, lang)
        if L.get("engine") != "parler":
            continue
        for i, b in enumerate(L["beats"]):
            out = GH.VOICE / reel["id"] / lang / f"b{i}.wav"
            if not out.exists():
                todo.append((out, b["say"], STYLE[L["voice"]]))
print(f"{len(todo)} clip(s) to make")
if todo:
    mid = "ai4bharat/indic-parler-tts"
    model = ParlerTTSForConditionalGeneration.from_pretrained(mid)
    tok = AutoTokenizer.from_pretrained(mid)
    dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
    for out, text, desc in todo:
        torch.manual_seed(7)
        d, p = dtok(desc, return_tensors="pt"), tok(text, return_tensors="pt")
        with torch.no_grad():
            a = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask,
                               prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
        out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(out, a.cpu().numpy().squeeze(), model.config.sampling_rate)
        print("[ok]", out)
