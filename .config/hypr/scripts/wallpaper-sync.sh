#!/usr/bin/env bash
WALLPAPER="$1"
echo "Key path: $WALLPAPER" >> /tmp/wallpaper_debug.log
waypaper --wallpaper "$WALLPAPER"
wal -i "$WALLPAPER"
ln -sf "$WALLPAPER" ~/.cache/wal/current_wallpaper
python3 ~/.config/neofetch/recolor_frames.py
BORDER_COLOR=$(sed -n '5p' ~/.cache/wal/colors | sed 's/#//')
hyprctl eval "hl.config({ general = { col = { active_border = 'rgb($BORDER_COLOR)' } } })"
~/.config/hypr/scripts/btop-pywal-theme.sh
notify-send "Theme updated" "btop colors will refresh next time it's opened" -t 1500
