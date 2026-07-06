#!/usr/bin/env bash

PROPERTY=$1
DIRECTION=$2

CURRENT=$(hyprctl getoption decoration:blur:$PROPERTY -j | jq '.int')

if [ "$DIRECTION" = "up" ]; then
    NEW=$((CURRENT + 1))
else
    NEW=$((CURRENT - 1))
    if [ "$NEW" -lt 0 ]; then
        NEW=0
    fi
fi

hyprctl eval "hl.config({ decoration = { blur = { $PROPERTY = $NEW } } })"
notify-send "Blur $PROPERTY" "$NEW" -t 800
