#!/usr/bin/env bash

SWAYNC_CONFIG="/home/luminara/.config/swaync/config.json"

if pgrep -x waybar > /dev/null; then
    pkill -x waybar
    jq '.["control-center-margin-top"] = 0 | .["control-center-margin-bottom"] = 0' \
        "$SWAYNC_CONFIG" > /tmp/swaync_config.tmp && mv /tmp/swaync_config.tmp "$SWAYNC_CONFIG"
else
    setsid waybar &
    jq '.["control-center-margin-top"] = 0 | .["control-center-margin-bottom"] = 0' \
        "$SWAYNC_CONFIG" > /tmp/swaync_config.tmp && mv /tmp/swaync_config.tmp "$SWAYNC_CONFIG"
fi

pkill swaync
sleep 0.2
setsid swaync &
