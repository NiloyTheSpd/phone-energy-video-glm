"""Sound for «Why Your Phone Gets Heavier When You Charge It» (10:30): English narration + pencil foley.

- Foley is driven by the page (events.json: one event per mark, gestures, punches, the done cue).
- Narration: voice/<id>.wav placed at voice/cues.json "start"; compressed, then set ~10 dB (RMS)
  above the foley bed, which stays gentle throughout. No music bed by default — see
  render_manifest/audio_mix_plan.md for the optional score and how to add it.
Run from the library root:  .venv/bin/python <project>/mix.py [from] [to]   (build.sh does)
"""
import json, os, sys
import numpy as np, soundfile as sf
LIB = os.environ.get('LIB') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'repo'))
sys.path.insert(0, LIB)
from core.audio.sfx import SR, bp, lp, hp, add, compress, limit, click

HERE = os.path.dirname(os.path.abspath(__file__))
FROM = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
TO = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
D = json.load(open(os.path.join(HERE, 'events.json')))
DUR = float(D['dur']); EV = D['ev']
N = int(round(DUR * SR))
rng = np.random.default_rng(11)
VO = json.load(open(os.path.join(HERE, 'voice', 'cues.json')))


def activity(kinds):
    a = np.zeros(N); pw = np.zeros(N)
    for e in EV:
        if e['type'] not in kinds: continue
        i0 = int(e['t'] * SR); i1 = min(N, int((e['t'] + max(e['d'], 0.035)) * SR))
        if i1 <= i0: continue
        n = i1 - i0; env = np.ones(n)
        r = min(n // 3, int(0.01 * SR))
        if r > 0: env[:r] = np.linspace(0, 1, r); env[-r:] = np.linspace(1, 0, r)
        a[i0:i1] += env; pw[i0:i1] += env * e.get('pan', 0)
    pan = np.where(a > 1e-6, pw / np.maximum(a, 1e-6), 0)
    level = 1 - np.exp(-a * 1.1)
    k = int(0.015 * SR); ker = np.ones(k) / k
    return np.convolve(level, ker, 'same'), np.convolve(pan, ker, 'same')


def tooth_noise(lo, hi, grain_hz, depth, seed):
    r = np.random.default_rng(seed)
    x = bp(r.standard_normal(N), lo, hi, 2)
    g = lp(np.abs(r.standard_normal(N)), grain_hz, 1); g = g / (np.percentile(g, 95) + 1e-9)
    return x * ((1 - depth) + depth * np.clip(g, 0, 2.5))


def hand(rate, seed, sharp=1.0):
    r = np.random.default_rng(seed)
    ph = np.cumsum(rate * (1 + 2.5 * lp(r.standard_normal(N), 3, 1)) / SR) * 2 * np.pi
    return (0.5 + 0.5 * np.abs(np.sin(ph))) ** sharp


def pan_st(x, pan):
    th = (pan + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)], 1)



def _compress(x, thr=0.05, ratio=3.5, att=0.004, rel=0.12):
    """Vectorised stereo compressor (the library's is per-sample Python; too slow for 10 min)."""
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    out = np.empty_like(x)
    for c in range(x.shape[1]):
        env = uniform_filter1d(maximum_filter1d(np.abs(x[:, c]), size=int(att * SR) * 2 + 1), size=int(rel * SR))
        g = np.where(env > thr, (thr + (env - thr) / ratio) / np.maximum(env, 1e-9), 1.0)
        out[:, c] = x[:, c] * uniform_filter1d(g, size=int(0.01 * SR))
    return out

# ---------------- pencil foley (from the page's marks) ----------------
fol = np.zeros((N, 2))
lv, pn = activity(['pencil']); fol += pan_st(tooth_noise(700, 4200, 380, 0.9, 1) * hand(5, 2) * lv, pn * 0.55) * 0.26
lv, pn = activity(['light']); fol += pan_st(tooth_noise(1400, 5200, 500, 0.9, 3) * hand(7, 4) * lv, pn * 0.55) * 0.10
lv, pn = activity(['write']); fol += pan_st(tooth_noise(900, 4800, 450, 0.92, 5) * hand(10, 6, 1.6) * lv, pn * 0.55) * 0.25
lv, pn = activity(['color']); fol += pan_st(tooth_noise(320, 2600, 220, 0.75, 7) * hand(13, 8, 2.0) * lv, pn * 0.55) * 0.21
for e in EV:
    t, d, p = e['t'], e['d'], e.get('pan', 0)
    if e['type'] == 'tap':
        add(fol, hp(click(pitch=0.7 + rng.random() * 0.25, v=1.0), 1800) * 0.032, t, 1.0, p * 0.5)
    elif e['type'] in ('gesture', 'punch'):
        n = int(max(d, 0.12) * SR); x = lp(hp(rng.standard_normal(n), 150), 1300, 2)
        u = np.linspace(0, 1, n); env = np.sin(np.pi * u) ** 1.5
        g = np.stack([x * env, np.roll(x, 211) * env], 1) * (0.045 if e['type'] == 'gesture' else 0.065)
        i0 = int(t * SR); i1 = min(N, i0 + n); fol[i0:i1] += g[:i1 - i0]
    elif e['type'] == 'done':   # the end card landing: a soft double tick
        add(fol, hp(click(pitch=1.3, v=0.8), 2400) * 0.05, t, 1.0, 0)
        add(fol, hp(click(pitch=1.8, v=0.6), 2700) * 0.04, t + 0.16, 1.0, 0)

# ---------------- narration ----------------
vo = np.zeros((N, 2))
AUDIO = os.path.abspath(os.path.join(HERE, '..', 'audio'))   # the Kokoro WAVs live in <root>/audio
for lid, t0 in VO['start'].items():
    path = os.path.join(AUDIO, f'{lid}.wav')
    if not os.path.exists(path): path = os.path.join(HERE, 'voice', f'{lid}.wav')   # fallback
    y, sr = sf.read(path, always_2d=True)
    if sr != SR:
        import soxr
        y = np.stack([soxr.resample(y[:, c], sr, SR, quality='HQ') for c in range(y.shape[1])], 1)
    i0 = int(t0 * SR); i1 = min(N, i0 + len(y))
    if i1 > i0: vo[i0:i1] += y[:i1 - i0]
vo = _compress(vo, thr=0.05, ratio=3.5)        # TTS has a high peak-to-average ratio

# ---------------- balance: voice about 10 dB above the foley ----------------
vr = np.sqrt(np.mean(vo ** 2) + 1e-12)
fr = np.sqrt(np.mean(fol ** 2) + 1e-12)
target = 10 ** (-14 / 20) * 0.65               # a comfortable working level
if fr > 1e-9: fol *= target / (10 ** (10 / 20)) / fr
if vr > 1e-9: vo *= target / vr
mix = vo + fol
mix = np.stack([limit(mix[:, c], 0.89) for c in range(mix.shape[1])], 1)   # true-peak safety; mux.sh does the final -14 LUFS

i0, i1 = int(FROM * SR), min(N, int(TO * SR))
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
out = os.path.join(HERE, 'out', 'mix.wav')
sf.write(out, mix[i0:i1], SR)
print(f'mix.wav  {os.path.relpath(out)}  {(i1 - i0) / SR:.2f}s of {DUR:.2f}s  (voice {len(VO["start"])} lines, {len(EV)} foley events)')
