#!/usr/bin/env python3
"""Calibrate Kokoro af_heart speaking rate: generate sample lines at several speeds, measure wpm."""
import json, os, sys, time
import numpy as np, soundfile as sf

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "repo"))
sys.path.insert(0, os.path.join(REPO, ".venv", "lib", "python3.12", "site-packages"))
from kokoro_onnx import Kokoro

k = Kokoro(os.path.join(REPO, "core", "tts", "kokoro-v1.0.onnx"), os.path.join(REPO, "core", "tts", "voices-v1.0.bin"))
tests = [
    ("t1", "Take two phones that are identical in every way.", 0.74),
    ("t2", "because for every electron that flowed in through one wire, another flowed back out through the other.", 0.74),
    ("t3", "He sealed a piece of tin inside a glass vessel, melting the glass shut so that nothing could get in or out, and weighed the whole thing.", 0.74),
    ("t4", "Take two phones that are identical in every way.", 0.78),
    ("t5", "Take two phones that are identical in every way.", 0.70),
    ("t6", "In nineteen oh five, that was Albert Einstein. Poincaré and Lavoisier, lithium and helium, radium and kinetic energy, seventeen point two million electron volts.", 0.74),
]
out = "/tmp/kokoro_cal"
os.makedirs(out, exist_ok=True)
for lid, text, speed in tests:
    t0 = time.time()
    a, sr = k.create(text, voice="af_heart", speed=speed, lang="en-us")
    gen = time.time() - t0
    sf.write(f"{out}/{lid}.wav", a, sr)
    dur = len(a) / sr
    nz = np.where(np.abs(a) > np.abs(a).max() * .02)[0]
    if len(nz):
        a2 = a[max(0, nz[0] - int(.03 * sr)): nz[-1] + int(.08 * sr)]
        dur = len(a2) / sr
    words = len(text.split())
    print(f"{lid} speed={speed} words={words} dur={dur:.2f}s wpm={words/dur*60:.0f} gen={gen:.1f}s")
