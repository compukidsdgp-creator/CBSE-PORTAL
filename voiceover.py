#!/usr/bin/env python3
"""
voiceover.py — narration for reels, fully offline.

Uses the Kokoro text-to-speech model (open source, runs on the CPU, no account,
no API key). The model files (~350 MB) are downloaded once into KOKORO_DIR
(default ~/.cache/kokoro); on GitHub Actions that folder is cached between runs.

    from voiceover import synth, SR
    audio = synth("V equals I R.")          # float32 numpy array at SR Hz
"""
import os
import urllib.request
from pathlib import Path

import numpy as np

KOKORO_DIR = Path(os.environ.get("KOKORO_DIR", Path.home() / ".cache" / "kokoro"))
MODEL_URL  = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
VOICE = os.environ.get("REEL_VOICE", "af_heart")     # warm, clear female voice
SPEED = float(os.environ.get("REEL_VOICE_SPEED", "1.0"))
SR = 24000

_K = None


def _fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 1_000_000:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    print(f"[voice] downloading {dest.name} …")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(dest)


def _engine():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        model, voices = KOKORO_DIR / "kokoro.onnx", KOKORO_DIR / "voices.bin"
        _fetch(MODEL_URL, model)
        _fetch(VOICES_URL, voices)
        _K = Kokoro(str(model), str(voices))
    return _K


def _trim(a, thr=0.012, keep=0.04):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx):
        return a
    k = int(keep * SR)
    return a[max(0, idx[0] - k): min(len(a), idx[-1] + k)]


def synth(text, voice=VOICE, speed=SPEED):
    """Speak `text`; returns float32 mono audio at SR Hz with edge silence trimmed."""
    lang = "en-gb" if voice.startswith("b") else "en-us"
    audio, sr = _engine().create(text, voice=voice, speed=speed, lang=lang)
    assert sr == SR, sr
    return _trim(np.asarray(audio, dtype=np.float32))


def write_wav(path, audio):
    import soundfile as sf
    sf.write(str(path), audio, SR)
