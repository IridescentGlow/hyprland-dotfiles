#!/usr/bin/env bash
# Toggle the laptop display between the two useful scales.
#
#   1.0 -> 1920x1200 logical. Pixel-exact, sharpest text.
#   0.8 -> 2400x1500 logical. More usable space, but the compositor downsamples
#          that onto a 1920x1200 panel, so text softens slightly.
#
# Applied live with `hyprctl eval` rather than `hyprctl reload`, so runtime
# toggles like shadow-toggle.sh and border-toggle.sh are not reset. The value is
# also written back to config/monitors.lua so it survives a restart.
set -euo pipefail

OUTPUT="eDP-1"
MONITORS="$HOME/.config/hypr/config/monitors.lua"

current=$(hyprctl monitors -j | jq -r --arg o "$OUTPUT" '.[] | select(.name==$o) | .scale')
[[ -n $current ]] || { notify-send "Display scale" "Monitor $OUTPUT not found" -t 1500; exit 1; }

# hyprctl prints 1.0 as "1", so compare numerically rather than as a string.
if awk -v c="$current" 'BEGIN { exit !(c > 0.9) }'; then
    new="0.8"; label="0.8  ·  more space, slightly softer"
else
    new="1.0"; label="1.0  ·  pixel-exact, sharpest"
fi

hyprctl eval "hl.monitor({ output = \"$OUTPUT\", mode = \"preferred\", position = \"auto\", scale = \"$new\" })" >/dev/null

# Persist, so a restart or reload keeps the choice.
sed -i -E "s/(scale[[:space:]]*=[[:space:]]*\")[0-9.]+(\")/\1${new}\2/" "$MONITORS"

notify-send "Display scale" "$label" -t 1200
