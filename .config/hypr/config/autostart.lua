hl.on("hyprland.start", function()
    ---- BACKGROUND APPS ----
    -- hl.exec_cmd("brightnessctl set 80%")
    hl.exec_cmd("nm-applet")
    hl.exec_cmd("keychain --eval --quiet id_ed25519")
    -- Smooth parallax wallpaper: a layer-shell surface on the `bottom` layer
    -- that slides the image as you change workspaces. It listens to Hyprland's
    -- event socket itself, so there is no Lua side to this. Change the image
    -- with `wallpaper-parallax.py --set <file>`; it refuses to start twice.
    -- It is the ONLY wallpaper layer: it restores its own last image at login.
    -- awww-daemon used to run underneath it as a hidden fallback, which meant
    -- two wallpaper renders at boot (awww's, then this one covering it).
    hl.exec_cmd("/home/Luminara/.config/hypr/scripts/wallpaper-parallax.py")
    hl.exec_cmd("waybar")
    -- Re-themes the wallpaper to match Spotify's album art. Single-instance;
    -- toggle it with SUPER+ALT+W.
    hl.exec_cmd("/home/Luminara/.config/hypr/scripts/spotify-wallpaper-toggle.sh autostart")
    hl.exec_cmd("firefox", { workspace = "1 silent" })
    hl.exec_cmd("bluetoothctl connect E4:61:F4:BB:2A:67")

    ---- WORKSPACE 1 TILE ARRANGEMENT ----
    -- hl.exec_cmd("sh -c \"" ..
    --     "sleep 5; hyprctl dispatch workspace 1; sleep 0.5; " ..
    --     "kitty -e zsh -c 'fastfetch --file ~/.config/fastfetch/Au5_ascii.fastfetch.txt --logo-color-1 magenta; exec zsh' & sleep 1; " ..
    --     "hyprctl dispatch layoutmsg preselect r; " ..
    --     "kitty -e yazi & sleep 1; " ..
    --     "hyprctl dispatch layoutmsg preselect d; " ..
    --     "kitty -e zsh -c 'while true; do tty-clock -b -C 6 -S -t -c -D; done' & sleep 1; " ..
    --     "hyprctl dispatch layoutmsg preselect d; " ..
    --     "kitty -e cmatrix -b -C white & sleep 1; " ..
    --     "hyprctl dispatch layoutmsg preselect d; " ..
    --     "kitty -e zsh -c 'cava; exec zsh' &" ..
    --     "\"")

    ---- AFTERTHOUGHT PROGRAMS ----
    -- hl.exec_cmd("swaync")
    -- hl.exec_cmd("zeditor", { workspace = "3 silent" })
    hl.exec_cmd("picom")
    hl.exec_cmd("hyprsunset")
    hl.exec_cmd("notify-send 'Lua event works'")

    ---- TERMINAL TEXT-SCRAMBLE EFFECT ----
    -- Watches Hyprland events and plays the scramble overlay on kitty
    -- windows. It refuses to start a second copy (pidfile guard), so this
    -- is safe across config reloads. Status/diagnosis:
    --   ~/.config/hypr/scripts/term-scramble-status.sh
    -- Turn it off:
    --   ~/.config/hypr/scripts/term-scramble-disable.sh
    hl.exec_cmd("/home/Luminara/.config/hypr/scripts/term-scramble-listener.sh")
end)
