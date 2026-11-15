#!/bin/sh
# One-command build for «Why Your Phone Gets Heavier When You Charge It».
# Run on the GPU laptop. Requires: Node 20+, ffmpeg 7+, and the library set up
# (see ../render_manifest/gpu_render_commands.sh for the full install).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-$(cd "$HERE/../repo" && pwd)}
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the lemo-opuscar library folder"; exit 1; }
cd "$LIB"
echo "— events (DUR + foley cues from the page)"
node core/render/events.mjs "$HERE"
echo "— picture (24 fps, every frame; ~40-70 min with 3 workers on a laptop)"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --out "$HERE/out/video.mp4"
echo "— sound (voice + pencil foley -> out/mix.wav)"
"$LIB/.venv/bin/python" "$HERE/mix.py"
echo "— mux (two-pass loudnorm to -14 LUFS, grain 1)"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/why-your-phone-gets-heavier-when-you-charge-it.mp4" 24 1
cp "$HERE/script/subtitles.srt" "$HERE/why-your-phone-gets-heavier-when-you-charge-it.srt"
echo "done: $HERE/why-your-phone-gets-heavier-when-you-charge-it.mp4"
