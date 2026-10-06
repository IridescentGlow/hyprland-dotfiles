#!/usr/bin/env bash
# Refresh waybar so it re-reads its CSS (it only parses style.css at startup,
# so a pywal colour change needs a fresh process).
#
# If waybar is NOT running this does nothing at all. Having deliberately
# closed the bar (SUPER+SHIFT+W), changing the wallpaper shouldn't bring it
# back from the dead.
set -u

pgrep -x waybar >/dev/null || exit 0

pkill -x waybar 2>/dev/null

# Wait for the old process to release its layer surface before starting the
# new one, so the two don't fight over the exclusive zone.
for _ in $(seq 1 30); do
    pgrep -x waybar >/dev/null || break
    sleep 0.1
done

setsid waybar >/dev/null 2>&1 &
