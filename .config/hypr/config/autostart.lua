hl.on("hyprland.start", function()
    ---- BACKGROUND APPS ----
    hl.exec_cmd("nm-applet")
    hl.exec_cmd("waypaper --restore")
    hl.exec_cmd("firefox", { workspace = "2 silent" })

    ---- WORKSPACE 1 TILE ARRANGEMENT ----
    hl.exec_cmd("kitty -e zsh -c 'neofetch --ascii ~/Documents/Au5_ascii.txt; exec zsh'", { workspace = "1" })
    hl.exec_cmd("kitty -e yazi", { workspace = "1" })
    hl.exec_cmd("kitty -e tty-clock -b -C 6 -S -t -c", { workspace = "1" })
    hl.exec_cmd("kitty -e cmatrix -b -C white", { workspace = "1" })
    hl.exec_cmd("kitty -e zsh -c 'cava; exec zsh'", { workspace = "1" })

    ---- AFTERTHOUGHT PROGRAMS ----
    hl.exec_cmd("swaync")
    hl.exec_cmd("zeditor", { workspace = "3" })
    hl.exec_cmd("picom")
    hl.exec_cmd("notify-send 'Lua event works'")
end)
