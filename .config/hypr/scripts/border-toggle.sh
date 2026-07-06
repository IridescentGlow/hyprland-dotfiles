#!/usr/bin/env bash

STATE_FILE="/tmp/hypr_border_size"
CURRENT=$(hyprctl getoption general:border_size -j | jq '.int')

if [ "$CURRENT" -gt 0 ]; then
    echo "$CURRENT" > "$STATE_FILE"
    hyprctl eval "hl.config({ general = { border_size = 0 } })"
    notify-send "Border" "disabled" -t 800
else
    PREVIOUS=$(cat "$STATE_FILE" 2>/dev/null || echo 3)
    hyprctl eval "hl.config({ general = { border_size = $PREVIOUS } })"
    notify-send "Border" "enabled ($PREVIOUS)" -t 800
fi
