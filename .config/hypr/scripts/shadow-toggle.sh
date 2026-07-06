#!/usr/bin/env bash

CURRENT=$(hyprctl getoption decoration:shadow:enabled -j | jq '.bool')

if [ "$CURRENT" = "true" ]; then
    NEW=false
    STATE="disabled"
else
    NEW=true
    STATE="enabled"
fi

hyprctl eval "hl.config({ decoration = { shadow = { enabled = $NEW } } })"
notify-send "Shadows" "$STATE" -t 800
