#!/bin/bash
BG=$(sed -n '1p' ~/.cache/wal/colors | sed 's/#//')
R=$((16#${BG:0:2}))
G=$((16#${BG:2:2}))
B=$((16#${BG:4:2}))

cat > ~/.cache/wal/colors-rofi-alpha.rasi <<EOF
* {
    bg-col-alpha: rgba($R, $G, $B, 75%);
    bg-col-window: rgba($R, $G, $B, 92%);
}
EOF
