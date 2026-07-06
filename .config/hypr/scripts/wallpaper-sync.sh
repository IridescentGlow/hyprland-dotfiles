#!/usr/bin/env bash

WALLPAPER="$1"

echo "Key path: $WALLPAPER" >> /tmp/wallpaper_debug.log

waypaper --wallpaper "$WALLPAPER"
wal -i "$WALLPAPER"

BORDER_COLOR=$(sed -n '5p' ~/.cache/wal/colors | sed 's/#//')
hyprctl eval "hl.config({ general = { col = { active_border = 'rgb($BORDER_COLOR)' } } })"
