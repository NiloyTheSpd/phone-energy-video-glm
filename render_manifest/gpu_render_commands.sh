#!/bin/sh
# ============================================================================
# «Why Your Phone Gets Heavier When You Charge It» — final render, GPU laptop
# ============================================================================
# Run from the UNZIPPED project root (the folder containing repo/ and project/):
#     sh render_manifest/gpu_render_commands.sh deps     # once: install everything
#     sh render_manifest/gpu_render_commands.sh chapters # render the 12 chapters
#     sh render_manifest/gpu_render_commands.sh concat   # join + mix + mux + srt
#     sh render_manifest/gpu_render_commands.sh all      # deps-check + one full render
# ============================================================================
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
LIB=${LIB:-$ROOT/repo}
export LIB
cd "$LIB"
[ -f core/render/video.mjs ] || { echo "library not at $LIB — unzip fully or set LIB"; exit 1; }
PY="$LIB/.venv/bin/python"
FPS=24

deps() {
  echo "== 1. Node packages (playwright-core, three) =="
  npm install --no-audit --no-fund --loglevel=error
  echo "== 2. headless browser =="
  node node_modules/playwright-core/cli.js install chromium-headless-shell
  echo "== 3. Python venv (numpy scipy soundfile soxr pillow fonttools + voice tier) =="
  [ -x "$PY" ] || python3 -m venv .venv
  "$PY" -m pip install -r requirements.txt -r requirements-voice.txt
  echo "== 4. Kokoro voice model (~350 MB, once) =="
  sh tools/fetch.sh voice
  echo "deps ready."
}

render_chapter() {  # $1 = n (01..12)
  N=$1
  FROM=$( .venv-fix 2>/dev/null; "$PY" - "$ROOT/render_manifest/chapters/ch$N.json" <<'EOF'
import json, sys
print(json.load(open(sys.argv[1]))["from"])
EOF
)
  TO=$( "$PY" - "$ROOT/render_manifest/chapters/ch$N.json" <<'EOF'
import json, sys
print(json.load(open(sys.argv[1]))["to"])
EOF
)
  echo "== chapter $N: frames $FROM..${TO}s =="
  node core/render/video.mjs "$ROOT/project" --fps $FPS --workers 2 \
    --q "from=$FROM&to=$TO" --out "$ROOT/project/out/ch$N.mp4"
}

chapters() {
  for N in 01 02 03 04 05 06 07 08 09 10 11 12; do render_chapter $N; done
  echo "chapters done -> project/out/ch01..ch12.mp4"
}

concat() {
  echo "== join chapters (lossless) =="
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$HERE/concat_order.txt" \
    -c copy "$ROOT/project/out/video.mp4"
  echo "== sound: voice + pencil foley =="
  "$PY" "$ROOT/project/mix.py"
  echo "== mux: two-pass loudnorm -14 LUFS, true peak <= -1 dB, grain 1 =="
  sh core/render/mux.sh "$ROOT/project/out/video.mp4" "$ROOT/project/out/mix.wav" \
    "$ROOT/project/why-your-phone-gets-heavier-when-you-charge-it.mp4" $FPS 1
  cp "$ROOT/project/script/subtitles.srt" \
     "$ROOT/project/why-your-phone-gets-heavier-when-you-charge-it.srt"
  echo "FILM: $ROOT/project/why-your-phone-gets-heavier-when-you-charge-it.mp4"
}

all() {
  echo "== single full render (simpler than chapters; same result) =="
  node core/render/events.mjs "$ROOT/project"
  node core/render/video.mjs "$ROOT/project" --fps $FPS --workers 3 \
    --out "$ROOT/project/out/video.mp4"
  "$PY" "$ROOT/project/mix.py"
  sh core/render/mux.sh "$ROOT/project/out/video.mp4" "$ROOT/project/out/mix.wav" \
    "$ROOT/project/why-your-phone-gets-heavier-when-you-charge-it.mp4" $FPS 1
  cp "$ROOT/project/script/subtitles.srt" \
     "$ROOT/project/why-your-phone-gets-heavier-when-you-charge-it.srt"
  echo "FILM: $ROOT/project/why-your-phone-gets-heavier-when-you-charge-it.mp4"
}

case "${1:-all}" in
  deps) deps ;;
  chapters) chapters ;;
  concat) concat ;;
  all) all ;;
  *) echo "usage: sh $0 [deps|chapters|concat|all]"; exit 2 ;;
esac
