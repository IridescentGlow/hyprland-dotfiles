#!/usr/bin/env bash

SOCKET="unix:/tmp/kitty-now-playing"
ART_RAW="/tmp/now_playing_art_raw.jpg"
ART_BLURRED="/tmp/now_playing_art_blurred.jpg"
ART_THUMB="/tmp/now_playing_art_thumb.jpg"

update_display() {
    local artist title arturl
    artist=$(playerctl metadata --format '{{ artist }}' 2>/dev/null)
    title=$(playerctl metadata --format '{{ title }}' 2>/dev/null)
    arturl=$(playerctl metadata --format '{{ mpris:artUrl }}' 2>/dev/null)

    if [ -z "$artist" ] && [ -z "$title" ]; then
        clear
        echo ""
        echo "  Nothing playing"
        return
    fi

    if [[ "$arturl" == file://* ]]; then
        cp "${arturl#file://}" "$ART_RAW" 2>/dev/null
    elif [[ "$arturl" == http* ]]; then
        curl -s -o "$ART_RAW" "$arturl"
    fi

    if [ -f "$ART_RAW" ]; then
        magick "$ART_RAW" -blur 0x12 -brightness-contrast -25x0 "$ART_BLURRED" 2>/dev/null
        magick "$ART_RAW" -resize 300x300 "$ART_THUMB" 2>/dev/null
        kitty @ --to "$SOCKET" set-background-image "$ART_RAW" 2>/dev/null
    fi

    clear
    echo ""
    echo -e "\033[1;97m  ${title}\033[0m"
    echo -e "\033[2;37m  ${artist}\033[0m"
    echo ""

    if [ -f "$ART_THUMB" ]; then
        kitty +kitten icat --align left --place 20x10@2x0 "$ART_THUMB" 2>/dev/null
    fi
}

update_display

playerctl --follow status metadata 2>/dev/null | while read -r _; do
    update_display
done
