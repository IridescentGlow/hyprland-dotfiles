#!/usr/bin/env bash
# Runs battery-alert.sh whenever upower reports a power change, plus once a
# minute regardless as a backstop. Event-driven so "charger connected" shows
# up immediately rather than on the next poll tick.
#
# `read -t` returns >128 on timeout and 1 on EOF, which lets one loop cover
# both the event and the periodic case.

set -uo pipefail

CHECK="$HOME/.config/hypr/scripts/battery-alert.sh"
[ -x "$CHECK" ] || { echo "missing $CHECK" >&2; exit 1; }

"$CHECK"    # establish baseline state at startup

upower --monitor 2>/dev/null | while :; do
    if IFS= read -r -t 60 _; then
        :                       # a power event arrived
    else
        rc=$?
        [ "$rc" -le 128 ] && break   # upower exited; let systemd restart us
    fi
    "$CHECK"
done
