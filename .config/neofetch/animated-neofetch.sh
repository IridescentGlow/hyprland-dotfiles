#!/bin/bash
delay=${1:-0.1}
ascii_row=1
ascii_col=1
text_col=60
cache_file="$HOME/.cache/neofetch.txt"
mkdir -p ~/.cache
old_stty=$(stty -g)

cleanup() {
    stty "$old_stty" 2>/dev/null
    stty sane 2>/dev/null
    printf '\e[<u' 2>/dev/null
    tput cnorm 2>/dev/null
    tput rs1 2>/dev/null
    clear
}
trap 'cleanup; exit 0' INT TERM
trap cleanup EXIT ERR

if [[ ! -f "$cache_file" || $(find "$cache_file" -mmin +60 2>/dev/null) ]]; then
  if command -v fastfetch >/dev/null 2>&1; then
    fastfetch --logo none > "$cache_file" 2>/dev/null
  else
    neofetch --disable ascii > "$cache_file" 2>/dev/null
  fi
fi

frames=(~/.config/neofetch/frames_compressed/*.txt)
if [[ ${#frames[@]} -eq 0 ]]; then
    cleanup
    exit 0
fi

clear
tput civis
tput cup "$ascii_row" "$text_col"
cat "$cache_file"

while true; do
    for frame in "${frames[@]}"; do
        tput cup "$ascii_row" "$ascii_col"
        cat "$frame"
        sleep "$delay"
    done
done
