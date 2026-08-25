#!/bin/bash
delay=${1:-0.1}
ascii_row=1
ascii_col=1
text_col=60
cache_file="$HOME/.cache/fastfetch.txt"
mkdir -p ~/.cache
old_stty=$(stty -g)

cleanup() {
    stty "$old_stty" 2>/dev/null
    stty sane 2>/dev/null
    printf '\e[<u' 2>/dev/null
    tput cnorm 2>/dev/null
    clear
}
trap 'cleanup; exit 0' INT TERM
trap cleanup EXIT ERR

if [[ ! -f "$cache_file" || $(find "$cache_file" -mmin +60 2>/dev/null) ]]; then
    fastfetch --logo none > "$cache_file" 2>/dev/null
fi

frames=(~/.config/fastfetch/frames_pywal/*.txt)
if [[ ${#frames[@]} -eq 0 ]]; then
    cleanup
    exit 0
fi

clear
tput civis

row="$ascii_row"
while IFS= read -r line; do
    tput cup "$row" "$text_col"
    printf '%s\n' "$line"
    ((row++))
done < "$cache_file"

while true; do
    for frame in "${frames[@]}"; do
        tput cup "$ascii_row" "$ascii_col"
        cat "$frame"
        sleep "$delay"
    done
done
