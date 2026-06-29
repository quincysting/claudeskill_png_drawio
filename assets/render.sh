#!/usr/bin/env bash
# Render a .drawio to PNG + SVG via the draw.io desktop CLI.
#   bash render.sh file.drawio [scale]      (default scale 1.5)
# Notes:
#  - macOS has no `timeout`; we poll for the output file.
#  - The harmless Electron "task_policy_set" warning is suppressed.
#  - To overlay on the original for alignment, make the "bglayer" visible in the
#    .drawio (the builder hides it by default) and re-render.
set -u
DRAWIO="${DRAWIO:-/Applications/draw.io.app/Contents/MacOS/draw.io}"
F="${1:?usage: render.sh file.drawio [scale]}"
S="${2:-1.5}"
BASE="${F%.drawio}"
[ -x "$DRAWIO" ] || { echo "draw.io CLI not found at $DRAWIO (brew install --cask drawio)"; exit 1; }

rm -f "${BASE}.png" "${BASE}.svg" 2>/dev/null || true
"$DRAWIO" --export --format png --scale "$S" --border 8 --output "${BASE}.png" "$F" --no-sandbox >/dev/null 2>&1
"$DRAWIO" --export --format svg --border 8 --output "${BASE}.svg" "$F" --no-sandbox >/dev/null 2>&1
for i in $(seq 1 30); do [ -s "${BASE}.png" ] && break; sleep 2; done
[ -s "${BASE}.png" ] && echo "rendered ${BASE}.png" || { echo "render failed"; exit 1; }
[ -s "${BASE}.svg" ] && echo "rendered ${BASE}.svg"
