#!/usr/bin/env bash
# Take a screenshot with hyprshot, then ask where to put it.
#
# The capture lands in SHOT_DIR straight away (so a capture is never lost),
# the image goes to the clipboard as usual, and a native save dialog opens
# asking where it should live. Cancelling the dialog just keeps the file in
# SHOT_DIR.
#
# Usage: screenshot.sh -m <window|region|output> [more hyprshot args]
set -u

SHOT_DIR="$HOME/Pictures/screenshots"
SCRIPTS="$HOME/.config/hypr/scripts"

mkdir -p "$SHOT_DIR"

NAME="$(date '+%Y-%m-%d_%H-%M-%S').png"

# -s: hyprshot stays quiet, we do our own notification once we know the
# final path. hyprshot still copies the image to the clipboard.
# Output must not go to a pipe: hyprshot's wl-copy child keeps the inherited
# stdout open for as long as it owns the clipboard, which would hang us.
hyprshot "$@" -s -o "$SHOT_DIR" -f "$NAME" >/dev/null 2>&1

SAVED="$SHOT_DIR/$NAME"
if [ ! -f "$SAVED" ]; then
    # Selection cancelled, or the mode produced nothing.
    exit 0
fi

# Ask where it should go. On cancel the dialog exits non-zero and we simply
# leave the file where it already is.
if DEST=$("$SCRIPTS/save-dialog.py" "$SHOT_DIR" "$NAME" "Save screenshot"); then
    DEST_DIR=$(dirname -- "$DEST")
    mkdir -p "$DEST_DIR"
    if [ "$(readlink -f -- "$DEST")" != "$(readlink -f -- "$SAVED")" ]; then
        if mv -f -- "$SAVED" "$DEST"; then
            SAVED="$DEST"
        else
            notify-send "Screenshot" "Could not move to $DEST -- kept in $SHOT_DIR" \
                -u critical -t 4000
        fi
    fi
fi

notify-send "Screenshot saved" "$SAVED" -t 3000 -i "$SAVED"
