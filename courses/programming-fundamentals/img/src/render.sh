#!/bin/sh
# Зняти PNG схеми у світлій і темній темі, щоб подивитись очима (macOS, Google Chrome):
#   ./render.sh pointers [тека]     — тека за замовчуванням: /tmp/ember-img
# Темна тема вмикається підміною media query в копії файлу; сам SVG не змінюється.
set -e
cd "$(dirname "$0")/.."
t="$1"; out="${2:-/tmp/ember-img}"
[ -n "$t" ] || { echo "usage: ./render.sh <тема> [тека]"; exit 1; }
mkdir -p "$out"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
size=$(sed -n 's/.*viewBox="0 0 \([0-9]*\) \([0-9]*\)".*/\1,\2/p' "$t.uk.svg" | head -1)
for f in "$t.uk" "$t"; do
    sed 's/@media (prefers-color-scheme: dark)/@media all/' "$f.svg" > "$out/$f.dark.svg"
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1.5 \
        --window-size="$size" --screenshot="$out/$f.light.png" "file://$PWD/$f.svg" 2>/dev/null
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1.5 \
        --window-size="$size" --screenshot="$out/$f.dark.png" "file://$out/$f.dark.svg" 2>/dev/null
done
ls "$out"/"$t"*.png
