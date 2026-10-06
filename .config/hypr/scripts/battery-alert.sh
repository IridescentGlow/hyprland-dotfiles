#!/usr/bin/env bash
# One idempotent battery check. Safe to run as often as you like -- it only
# notifies on an actual change, using a state file to remember what it has
# already said.
#
# Fires on four events:
#   charger connected      AC appears
#   charger disconnected   AC goes away
#   low battery            <= 25% while running on battery
#   charge limit reached   >= 80% while plugged in
#
# Driven by battery-alert-watch.sh (upower events + a 60s backstop).

set -uo pipefail

BATTERY=BAT1
AC=ACAD
LOW=25            # warn at or below this, on battery
HIGH=80           # warn at or above this, on AC
LOW_CLEAR=30      # re-arm the low warning above this
HIGH_CLEAR=75     # re-arm the high warning below this

STATE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/battery-alert"
STATE="$STATE_DIR/state"
mkdir -p "$STATE_DIR"

cap=$(cat "/sys/class/power_supply/$BATTERY/capacity" 2>/dev/null) || exit 0
ac=$(cat "/sys/class/power_supply/$AC/online" 2>/dev/null) || exit 0
[ -n "$cap" ] && [ -n "$ac" ] || exit 0

# Previous state. prev_ac is empty on the very first run, which deliberately
# suppresses a spurious "connected/disconnected" toast at login.
prev_ac=""; low_warned=0; high_warned=0
# shellcheck disable=SC1090
[ -f "$STATE" ] && . "$STATE"

notify() { notify-send -u "$1" -t "$2" "$3" "$4" -i "$5" 2>/dev/null; }

# --- charger plugged / unplugged --------------------------------------------
if [ -n "$prev_ac" ] && [ "$ac" != "$prev_ac" ]; then
    if [ "$ac" = "1" ]; then
        notify normal 2500 "Charger connected" "Battery at ${cap}%" battery-good-charging
    else
        notify normal 2500 "Charger disconnected" "Battery at ${cap}% - running on battery" battery-good
    fi
fi

# --- low battery, on battery only -------------------------------------------
if [ "$ac" = "0" ] && [ "$cap" -le "$LOW" ] && [ "$low_warned" -eq 0 ]; then
    notify critical 6000 "Battery low" "${cap}% remaining - plug in the charger" battery-caution
    low_warned=1
elif [ "$cap" -gt "$LOW_CLEAR" ] || [ "$ac" = "1" ]; then
    low_warned=0
fi

# --- 80% reached, on AC only ------------------------------------------------
if [ "$ac" = "1" ] && [ "$cap" -ge "$HIGH" ] && [ "$high_warned" -eq 0 ]; then
    notify normal 6000 "Battery at ${cap}%" "Unplug the charger to protect the battery" battery-full-charging
    high_warned=1
elif [ "$cap" -lt "$HIGH_CLEAR" ] || [ "$ac" = "0" ]; then
    high_warned=0
fi

printf 'prev_ac=%s\nlow_warned=%s\nhigh_warned=%s\n' "$ac" "$low_warned" "$high_warned" > "$STATE"
