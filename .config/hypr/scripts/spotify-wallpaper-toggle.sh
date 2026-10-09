#!/usr/bin/env bash
# On/off switch for the "wallpaper follows the Spotify cover" watcher.
# Spicetify's dynamic colours live inside Spotify and are never affected.
#
#   spotify-wallpaper-toggle.sh            flip it (the keybind does this)
#   spotify-wallpaper-toggle.sh on|off     force a state
#   spotify-wallpaper-toggle.sh autostart  login: start unless you turned it off
#
# The choice is remembered across logins in ~/.local/state/spotify-wallpaper/.
set -u

SCRIPT="$HOME/.config/hypr/scripts/spotify-wallpaper.py"
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/spotify-wallpaper"
FLAG="$STATE/disabled"
PIDFILE="${XDG_RUNTIME_DIR:-/tmp}/spotify-wallpaper.pid"

running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }

turn_on() {
    rm -f "$FLAG"
    running || setsid "$SCRIPT" >/dev/null 2>&1 &
}

turn_off() {
    mkdir -p "$STATE" && touch "$FLAG"
    "$SCRIPT" --quit >/dev/null 2>&1
}

case "${1:-toggle}" in
    autostart) [ -e "$FLAG" ] || turn_on; exit 0 ;;
    on)  turn_on;  msg="Wallpaper follows Spotify cover: ON" ;;
    off) turn_off; msg="Wallpaper follows Spotify cover: OFF" ;;
    toggle)
        if running; then turn_off; msg="Wallpaper follows Spotify cover: OFF"
        else turn_on; msg="Wallpaper follows Spotify cover: ON"; fi ;;
    *) echo "usage: $0 [toggle|on|off|autostart]" >&2; exit 2 ;;
esac

notify-send -t 1500 "Spotify wallpaper" "$msg"
