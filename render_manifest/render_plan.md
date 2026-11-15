# Render plan — «Why Your Phone Gets Heavier When You Charge It»

A 10:29.8 (629.8 s) hand-drawn iPad-sketch science explainer in the
**Tablet Sketch Explainer** (`styles/ipad-sketch/`) style of the
[lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) library.
**Nothing has been rendered to video yet** — this package contains the
finished source, the voice, the sync data and QA stills; the final render
runs on your GPU laptop with the commands below.

## What is in this package

```
phone-energy-video/
├── repo/                    the lemo-opuscar library, cloned manually (git)
│   └── core/tts/            Kokoro model + voices (downloaded via tools/fetch.sh voice)
├── project/                 THE FILM
│   ├── index.html           the page: engine + 12 chapter scenes + end card (window.render(t))
│   ├── mix.py               voice + pencil foley -> out/mix.wav
│   ├── build.sh             one-command build (events -> picture -> sound -> mux)
│   ├── fonts/               Caveat Bold/Medium (SIL OFL 1.1)
│   ├── glyphs.json          stroke skeletons for the pencil lettering
│   ├── events.json          DUR + 1119 foley/cue events exported from the page
│   ├── voice/               timeline.json (the narration clock) + cues.json (subtitle timing)
│   ├── script/              master_narration.txt · chapters.json · voice_lines.json · subtitles.srt
│   ├── storyboard/          chapters.json · shots.json · camera.json · marks.json · audio_sync.json
│   ├── style/               STYLE.md + DEMO.md + style.json + poster.jpg + ipad-sketch.srt
│   │   └── ipad-sketch-full/  the complete demo source (reference only, not rendered)
│   ├── skills/lemo-opuscar/ the library's skill (copied manually per the master prompt)
│   ├── tools/               fonts.sh · skeleton.py · cues-building helpers · QA still tools
│   └── out/                 empty (render output goes here)
├── audio/                   120 Kokoro af_heart WAVs + dur.json + words.json + voice_manifest.json
├── whisper/                 transcript.json · word_timestamps.json · sync_manifest.json
├── qa_stills/               62 QA PNG stills (all that was rendered here — no video)
├── render_manifest/         this folder
└── output/                  empty (QA artifacts only)
```

## Film facts

| | |
|---|---|
| Duration | 629.8 s (10:29.8), 15,115 frames |
| Resolution / fps | 1920×1080 @ 24 fps, on ones |
| Canvas | one continuous 4320×2400 cream page (4640×2760 world with overscan), 12 chapter cells of 1080×800 in a 4×3 grid |
| Marks | 675 (387 pencil strokes, 176 handwritten texts, 81 colour blocks, 29 construction lines, 22 occlusions), 126 camera shots |
| Narration | 120 lines, 1,398 words, Kokoro `af_heart`, speeds 0.74–0.82, ASR-verified 0 mismatches |
| Subtitles | 83 cues from real audio timing; every cue holds ≥ max(1.8 s, speech + 0.6 s); zero overlaps |
| Sound | narration + procedural pencil foley driven by the page's marks; mux two-pass loudnorm −14 LUFS |
| End card | drawn into ch12's empty top-right; **no whole-page pull-back** |

## Requirements (the GPU laptop)

- **Node 20+** and **ffmpeg 7+** (system installs)
- **Python 3.11–3.13**
- ~2 GB free for deps (npm packages + headless Chromium + venv + Kokoro model)
- ~16 GB RAM recommended (each render worker's browser uses ~1 GB for the big page; 2 workers ≈ 2.5 GB)
- A GPU helps but is not required (this style is Canvas 2D, not WebGL)

## Install (once)

```sh
cd phone-energy-video
sh render_manifest/gpu_render_commands.sh deps
```

which runs, inside `repo/`:
1. `npm install --no-audit --no-fund` (playwright-core, three — from package.json)
2. `node node_modules/playwright-core/cli.js install chromium-headless-shell`
3. `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-voice.txt`
   (numpy, scipy, soundfile, soxr, pillow, fonttools, kokoro-onnx, edge-tts, faster-whisper, av<19)
4. `sh tools/fetch.sh voice` (Kokoro v1.0 ONNX model + voices, ~350 MB, from the library's GitHub release)

No global installs; no plugin manager; everything lives in this folder.
The fonts and glyphs are already in `project/` (no download needed at render time).

## Render

Option A — one command (simplest):
```sh
sh project/build.sh
```

Option B — chapter by chapter (resumable, less RAM):
```sh
sh render_manifest/gpu_render_commands.sh chapters   # out/ch01..ch12.mp4 (see chapters/*.json)
sh render_manifest/gpu_render_commands.sh concat     # join + mix + mux + srt
```

Option C — the raw commands themselves (what the scripts wrap):
```sh
cd repo
node core/render/events.mjs ../project
node core/render/video.mjs ../project --fps 24 --workers 3 --out ../project/out/video.mp4
.venv/bin/python ../project/mix.py
sh core/render/mux.sh ../project/out/video.mp4 ../project/out/mix.wav \
   ../project/why-your-phone-gets-heavier-when-you-charge-it.mp4 24 1
cp ../project/script/subtitles.srt ../project/why-your-phone-gets-heavier-when-you-charge-it.srt
```

Expected wall time: ~40–80 min with 2–3 workers on a modern laptop
(each frame ≈ 0.2–0.4 s to raster the big page; JPEG frames pipe straight into ffmpeg).

## Chapter slice commands

Each chapter is a frame-exact `?from=&to=` slice of the same page
(the page draws film second `from + t`, so slices join seamlessly — see DEMO.md).
Exact numbers live in `chapters/ch01..ch12.json`; e.g. chapter 7:

```sh
node core/render/video.mjs ../project --fps 24 --workers 2 \
  --q 'from=266.86&to=341.43' --out ../project/out/ch07.mp4
```

Frame ranges, output names and the join order are listed in `concat_order.txt`.

## If anything goes wrong

- **OOM / crashed worker** → use `--workers 1`, or render per chapter.
- **Window.READY never true** → the page needs `project/voice/timeline.json` + `cues.json` + `glyphs.json` + `fonts/`; all are in the zip.
- **Missing voice at mix time** → `audio/` must sit next to `project/` (mix.py reads `../audio/*.wav`).
- **Regenerating voice/subtitles** → see `tools/` at the project root of this zip (make_lines.py, build_timeline.py, asr_overrides.py).
