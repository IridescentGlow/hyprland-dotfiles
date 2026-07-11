#!/usr/bin/env bash

BATTERY="BAT1"
STATE_FILE="/tmp/battery_alert_state"

CAPACITY=$(cat /sys/class/power_supply/$BATTERY/capacity)
STATUS=$(cat /sys/class/power_supply/$BATTERY/status)

LAST_ALERT=$(cat "$STATE_FILE" 2>/dev/null || echo "none")

if [ "$STATUS" = "Discharging" ]; then
    if [ "$CAPACITY" -le 20 ] && [ "$LAST_ALERT" != "20" ]; then
        notify-send -u critical "Battery Critical" "Battery at ${CAPACITY}% - plug in now" -i battery-caution
        echo "20" > "$STATE_FILE"
    elif [ "$CAPACITY" -le 99 ] && [ "$CAPACITY" -gt 20 ] && [ "$LAST_ALERT" != "40" ] && [ "$LAST_ALERT" != "20" ]; then
        notify-send -u normal "Battery Low" "Battery at ${CAPACITY}%" -i battery-low
        echo "40" > "$STATE_FILE"
    fi
else
    # Reset state once charging, so alerts fire again next time it discharges
    rm -f "$STATE_FILE"
fi
