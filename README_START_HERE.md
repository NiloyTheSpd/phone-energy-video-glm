# Why Your Phone Gets Heavier When You Charge It
### a ~10-minute hand-drawn iPad-sketch explainer — PLAN + ASSETS + SCRIPT + AUDIO + WHISPER SYNC + QA STILLS

**The final video has deliberately NOT been rendered.** Everything up to the
render is done and verified; the last step runs on your GPU laptop with the
commands below.

---

## 1. What this is

A 629.8 s (10:29.8) film in the **Tablet Sketch Explainer** style
(`styles/ipad-sketch/`) of the [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)
library, made exactly as the master prompt required:

- the repository was cloned manually with `git clone` (no plugin, no marketplace);
- the style files (`STYLE.md`, `DEMO.md`, `style.json`, `poster.jpg`, the full
  demo folder) were downloaded/copied manually into `project/style/`;
- the demo was used as grammar only — its story, props, shots, timings, title
  and end card are not reused (different story, different opening, different
  signature shots, different camera path, different ending: **no whole-page
  pull-back**);
- one continuous cream canvas (4320×2400 world units) fills progressively
  across **12 chapter cells**, each with its own drawings, notes, swatches,
  arrows and camera moves;
- 675 marks (pencil strokes, stroke-by-stroke lettering, off-register colour
  blocks), 126 camera shots, 120 narration lines, 83 subtitle cues — all timed
  from the real Kokoro audio and Whisper word timestamps.

## 2. Quick start on the GPU laptop

```sh
unzip phone-energy-video.zip && cd phone-energy-video

# once — installs everything locally inside this folder (~2 GB):
sh render_manifest/gpu_render_commands.sh deps

# then — the whole film in one command:
sh project/build.sh
# …or chapter by chapter (resumable):
sh render_manifest/gpu_render_commands.sh chapters
sh render_manifest/gpu_render_commands.sh concat
```

Result: `project/why-your-phone-gets-heavier-when-you-charge-it.mp4`
(1920×1080, 24 fps, −14 LUFS, subtitles burned in) + the `.srt` next to it.

Requirements: Node 20+, ffmpeg 7+, Python 3.11–3.13, ~2 GB free for deps.
Nothing is installed globally. Expected render time: ~40–80 min with 2–3 workers.

## 3. What is where

| Path | Contents |
|---|---|
| `project/` | the film: `index.html` (engine + 12 scenes), `mix.py`, `build.sh`, fonts, glyphs, storyboard, script, voice timing |
| `audio/` | 120 Kokoro `af_heart` WAVs, `dur.json`, `words.json`, `voice_manifest.json` |
| `whisper/` | `transcript.json`, `word_timestamps.json`, `sync_manifest.json` |
| `qa_stills/` | the 62 QA PNG stills (re-rendered after QA round 4) (the only images rendered here) |
| `render_manifest/` | `render_plan.md`, `chapters/ch01–12.json`, `concat_order.txt`, `audio_mix_plan.md`, `subtitle_burnin_plan.md`, `gpu_render_commands.sh` |
| `qa_report.md` | the full QA report (per-still listing + every issue found and fixed) |
| `repo/` | the cloned lemo-opuscar library (without node_modules/.venv/models — `deps` restores them) |
| `output/` | empty — QA artifacts only, no final video |

## 4. The pipeline that produced this package

```
tools/make_lines.py        narration → voice_lines.json + chapters.json (1,398 words / 120 lines)
repo: core/tts/tts.py      Kokoro af_heart, speed 0.74–0.82 → audio/*.wav + dur.json
tools/asr_overrides.py     faster-whisper line check → 0 mismatches (32 benign mishears mapped)
tools/build_timeline.py    real WAV timing → timeline.json, cues.json, subtitles.srt,
                           whisper/*.json, audio/voice_manifest.json
project/index.html         the page: marks scheduled from the narration clock
tools/make_qa_list.py      the 62 QA still timestamps
project/tools/qa_stills.mjs   rendered them (stills only — never video)
core: readcheck / events   on-page reading times + 1119 foley events
tools/dump_storyboard.mjs  project/storyboard/*.json from the live page
tools/make_render_manifest.py  render_manifest/chapters/*.json + concat order
```

Re-run any stage from `tools/`; nothing depends on estimates — every timing
comes from the generated audio.

## 5. Credits & licences

- **lemo-opuscar library** (engine, render tools, TTS/ASR pipeline) — see `repo/LICENSE`
- **Caveat Bold / Medium** — SIL Open Font License 1.1 (`project/fonts/OFL-caveat.txt`)
- **Kokoro v1.0** (voice) and **faster-whisper / base.en** (alignment) — downloaded
  by `sh tools/fetch.sh voice` / pip; see their licences in the library
- Facts in the narration follow the source transcript you provided; the
  historical figures (Lavoisier 1789, Landolt 1908, Curie 1902-03, Poincaré 1900,
  Einstein 1905/06, Cockcroft-Walton 1932, Bainbridge 1933, Eddington 1920) are
  standard physics history. Verified numbers: 1 kWh weighs 4.0×10⁻⁸ g (40 billionths
  of a gram); a 10 Wh phone charge weighs 4×10⁻¹⁰ g — less than a billionth of a gram;
  a gram of radium's yearly heat (~116 W) weighs 4.1×10⁻⁸ g = 40 **billionths** of a
  gram (as the source transcript said); Li-7 + p → 2 He⁴ releases 17.35 MeV
  (17.2 measured in 1932, 16.8 predicted with Bainbridge's 1933 mass).
