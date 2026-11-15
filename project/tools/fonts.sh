#!/bin/sh
# Fonts for this film (English only): Caveat Bold / Medium, SIL OFL 1.1.
# Cut from the Google Fonts variable font with fontTools, licences copied next to them.
set -e
F="$1/fonts"; PY="$2"; T=$(mktemp -d); mkdir -p "$F"
G=https://github.com/google/fonts/raw/main/ofl
curl -sfL -o "$T/Caveat.ttf" "$G/caveat/Caveat%5Bwght%5D.ttf"
"$PY" -m fontTools.varLib.instancer "$T/Caveat.ttf" wght=700 -o "$F/Caveat-Bold.ttf" -q
"$PY" -m fontTools.varLib.instancer "$T/Caveat.ttf" wght=500 -o "$F/Caveat-Medium.ttf" -q
curl -sfL -o "$F/OFL-caveat.txt" "$G/caveat/OFL.txt"
rm -rf "$T"
echo "fonts ok"
