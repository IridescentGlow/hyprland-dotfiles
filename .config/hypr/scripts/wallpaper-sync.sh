#!/usr/bin/env bash
# The single entry point for changing the wallpaper.
#
# Everything that reacts to the wallpaper is refreshed here, in one place, so
# no caller can accidentally change the image without also updating the theme:
#
#   parallax surface -> what you actually see (wipes to the new image); it is
#                       the only wallpaper layer
#   current_wallpaper-> the symlink rofi shows in its left-hand pane
#   wal              -> regenerates ~/.cache/wal/* (waybar, rofi, kitty, ...)
#   kitty            -> every open kitty gets the palette as its *default*, so
#                       programs that reset the terminal (pipes.sh, `reset`)
#                       come back to the new colours, not the ones kitty
#                       started with
#   waybar           -> restarted so it picks up the regenerated CSS
#
# Usage: wallpaper-sync.sh /path/to/image
set -u

WALLPAPER="${1:-}"
SCRIPTS="$HOME/.config/hypr/scripts"

# One run at a time. Two quick wallpaper keypresses used to interleave, so the
# image could end up from one run and the palette from the other. Queued runs
# execute in order, which makes the last keypress win everywhere.
exec 9>"${XDG_RUNTIME_DIR:-/tmp}/wallpaper-sync.lock"
flock -w 60 9 || { echo "wallpaper-sync: another run is stuck" >&2; exit 1; }

if [ -z "$WALLPAPER" ]; then
    echo "usage: wallpaper-sync.sh /path/to/image" >&2
    exit 2
fi

# Resolve to an absolute path; rofi and wal both need a real file.
WALLPAPER="$(readlink -f -- "$WALLPAPER")"
if [ ! -f "$WALLPAPER" ]; then
    notify-send "Wallpaper not found" "$WALLPAPER" -u critical -t 3000
    echo "wallpaper-sync: no such file: $WALLPAPER" >&2
    exit 1
fi

# ---- 1. the visible wallpaper -------------------------------------------
# The parallax surface is what's on screen; it wipes to the new image.
"$SCRIPTS/wallpaper-parallax.py" --set "$WALLPAPER"
# (No awww layer any more: parallax restores its own image at login, so a
# second wallpaper daemon underneath only caused a double render at boot.)

# ---- 2. colours ----------------------------------------------------------
# rofi's left pane renders this symlink directly.
mkdir -p "$HOME/.cache/wal"
ln -sfn "$WALLPAPER" "$HOME/.cache/wal/current_wallpaper"

# rofi has no background-position, so it always anchors an image at the left
# edge -- which on an ultrawide means you only ever see the far left of it.
# Pre-crop a centred slice instead, so the middle of the wallpaper shows.
#
# The slice is deliberately a little TALLER than the pane's 350:494 aspect.
# config.rasi scales it with `width`, so it fills the pane horizontally and
# overflows vertically (cropped). If it were shorter, scaling to width would
# leave a vertical gap and rofi tiles gaps -- which is what made the image
# look duplicated.
magick "$WALLPAPER" -resize 700x1030^ -gravity center -extent 700x1030 \
    "$HOME/.cache/wal/rofi-wallpaper.png" 2>/dev/null

# Regenerates ~/.cache/wal/{colors,colors-waybar.css,colors-rofi-dark.rasi,...}
# -n skips setting the desktop wallpaper (we already did that ourselves).
if ! wal -i "$WALLPAPER" -n -q; then
    notify-send "pywal failed" "$(basename "$WALLPAPER")" -u critical -t 3000
    echo "wallpaper-sync: wal failed on $WALLPAPER" >&2
    exit 1
fi

# rofi's translucent panel colours, derived from the new palette.
[ -x "$HOME/.config/rofi/generate_transparency.sh" ] && \
    "$HOME/.config/rofi/generate_transparency.sh"

# wal only recolours open terminals *live* (escape sequences). A terminal
# reset -- which pipes.sh does, as does `reset` -- throws live changes away and
# falls back to the palette kitty started with. --configured moves that
# baseline too. Sockets come from `listen_on` in kitty.conf; ones left behind
# by dead processes simply fail and are skipped.
for sock in /tmp/kitty-socket-*; do
    [ -S "$sock" ] || continue
    timeout 3 kitty @ --to "unix:$sock" set-colors --all --configured \
        "$HOME/.cache/wal/colors-kitty.conf" >/dev/null 2>&1
done

# ---- 3. everything that reads those colours ------------------------------
[ -f "$HOME/.config/fastfetch/recolor_frames.py" ] && \
    python3 "$HOME/.config/fastfetch/recolor_frames.py" >/dev/null 2>&1

[ -x "$SCRIPTS/btop-pywal-theme.sh" ] && "$SCRIPTS/btop-pywal-theme.sh"

# Hyprland's active window border, from colour 5 of the new palette.
BORDER_COLOR=$(sed -n '5p' "$HOME/.cache/wal/colors" | tr -d '#')
if [ -n "$BORDER_COLOR" ]; then
    hyprctl eval "hl.config({ general = { col = { active_border = 'rgb($BORDER_COLOR)' } } })" >/dev/null
fi

# waybar reads its CSS only at startup, so it has to be restarted.
"$SCRIPTS/waybar-restart.sh"

notify-send "Wallpaper updated" "$(basename "$WALLPAPER")" -t 1500
