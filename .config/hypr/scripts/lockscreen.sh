#!/usr/bin/env bash
# Don't use hyprlock-minimal.conf: its `path = screenshot` background renders
# a fully black lock screen here (fractional scale + hybrid Intel/NVIDIA).
hyprlock -c ~/.config/hypr/hyprlock.conf
