hl.on("hyprland.start", function()
    ---- BACKGROUND APPS ----
    hl.exec_cmd("brightnessctl set 80%")
    hl.exec_cmd("nm-applet")
    hl.exec_cmd("waypaper --restore")
    hl.exec_cmd("firefox", { workspace = "1 silent" })
    hl.exec_cmd("bluetoothctl connect E4:61:F4:BB:2A:67")

    ---- WORKSPACE 1 TILE ARRANGEMENT ----
    -- hl.exec_cmd("sh -c \"" ..
    --     "sleep 5; hyprctl dispatch workspace 1; sleep 0.5; " ..
    --     "kitty -e zsh -c 'neofetch --ascii ~/Documents/Au5_ascii.txt; exec zsh' & sleep 1; " ..
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
    hl.exec_cmd("swaync")
    -- hl.exec_cmd("zeditor", { workspace = "3 silent" })
    hl.exec_cmd("picom")
    hl.exec_cmd("notify-send 'Lua event works'")
end)
