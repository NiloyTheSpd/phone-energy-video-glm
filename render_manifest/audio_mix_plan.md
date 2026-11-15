# Audio mix plan

## What the mix is

`project/mix.py` writes `project/out/mix.wav` (48 kHz stereo, full film length):

1. **Narration** — the 120 Kokoro `af_heart` WAVs from `audio/`, placed at their
   Whisper-aligned starts from `project/voice/cues.json` ("start" map), resampled
   to 48 kHz, compressed (3.5:1 above −26 dBFS, vectorised), then balanced to the
   working level.
2. **Pencil foley** — driven by `project/events.json` (1119 events exported from
   the page by `core/render/events.mjs`):
   - `pencil` strokes → band noise 0.7–4.2 kHz with paper-tooth bumps and hand rhythm
   - `light` construction lines → lighter, higher (1.4–5.2 kHz)
   - `write` lettering → choppier, 10 Hz back-and-forth
   - `color` blocks → broad and low (0.3–2.6 kHz, 13 Hz sweep)
   - `tap` (stylus touching down after a lift) → tiny high click
   - `gesture` / `punch` (camera moves) → soft sheet-slide noise
   - `done` (end card complete) → a soft double tick
   - every sound is panned to where its mark sits on screen
3. **Balance** — voice set ≈10 dB (RMS) above the foley bed; limiter at 0.89.

Final loudness is applied at mux: `core/render/mux.sh` runs a two-pass
`loudnorm` to **−14 LUFS integrated, true peak ≤ −1 dBTP**, and prints the
measurement. Measured pre-mix: −13.7 LUFS integrated, peak 0.89.

## Optional music bed (not rendered by default)

The style asks for a warm, small, acoustic score (nylon guitar, double bass,
soft shaker, soft-mallet vibraphone). To add one on the laptop:

1. Fetch a sample library once: `sh tools/fetch.sh instruments freepats`
   (or `karoryfer` / `vcsl`; licences in `core/audio/INSTRUMENTS.md`).
2. In `project/mix.py`, before the balance step, build `mus` from
   `core/audio/sampler.py` events — one soft accent note per chapter capsule
   (times in `project/storyboard/chapters.json` → `camera_keyframes[0].t`),
   a gentle pulse under the derivation chapters (7–8), and a held chord under
   the end card (`events.json` → the `done` event).
3. Keep the music ≈10 dB under the voice and dip it 300 Hz–4 kHz while
   someone speaks (`core/audio/sfx.py` has the filters), then add it to `mix`.

## Loudness targets

| Stage | Target |
|---|---|
| mix.wav (working) | peak ≤ 0.89, voice ≈ 10 dB above foley |
| final mux | −14 LUFS integrated, ≤ −1 dBTP (two-pass loudnorm in mux.sh) |
| voice pacing | af_heart 0.74–0.82 ≈ 2.2–2.5 words/s (style band 2.3–2.6) |
