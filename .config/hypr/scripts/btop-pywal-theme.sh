#!/usr/bin/env bash

WAL_COLORS=~/.cache/wal/colors
THEME_FILE=~/.config/btop/themes/pywal.theme

mkdir -p ~/.config/btop/themes

BG=$(sed -n '1p' "$WAL_COLORS")
FG=$(sed -n '8p' "$WAL_COLORS")
ACCENT=$(sed -n '5p' "$WAL_COLORS")
ACCENT2=$(sed -n '6p' "$WAL_COLORS")
INACTIVE=$(sed -n '9p' "$WAL_COLORS")

cat > "$THEME_FILE" << EOF
theme[main_bg]="$BG"
theme[main_fg]="$FG"
theme[title]="$FG"
theme[hi_fg]="$ACCENT"
theme[selected_bg]="$ACCENT"
theme[selected_fg]="$BG"
theme[inactive_fg]="$INACTIVE"
theme[graph_text]="$FG"
theme[proc_misc]="$ACCENT2"
theme[cpu_box]="$ACCENT"
theme[mem_box]="$ACCENT"
theme[net_box]="$ACCENT"
theme[proc_box]="$ACCENT"
theme[div_line]="$INACTIVE"
theme[temp_start]="$ACCENT2"
theme[temp_mid]="$ACCENT"
theme[temp_end]="$ACCENT"
theme[cpu_start]="$ACCENT2"
theme[cpu_mid]="$ACCENT"
theme[cpu_end]="$ACCENT"
theme[free_start]="$ACCENT2"
theme[free_mid]="$ACCENT"
theme[free_end]="$ACCENT"
theme[cached_start]="$ACCENT2"
theme[cached_mid]="$ACCENT"
theme[cached_end]="$ACCENT"
theme[available_start]="$ACCENT2"
theme[available_mid]="$ACCENT"
theme[available_end]="$ACCENT"
theme[download_start]="$ACCENT2"
theme[download_mid]="$ACCENT"
theme[download_end]="$ACCENT"
theme[upload_start]="$ACCENT2"
theme[upload_mid]="$ACCENT"
theme[upload_end]="$ACCENT"
EOF
