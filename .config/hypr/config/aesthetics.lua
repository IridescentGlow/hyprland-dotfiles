-- Refer to https://wiki.hypr.land/Configuring/Basics/Variables/
hl.config({
    general = {
        gaps_in          = 5,
        gaps_out         = 20,

        border_size      = 0,

        col              = {
            active_border   = "rgba(00BFFF00)",
            inactive_border = "rgba(59595900)",
        },

        -- Set to true to enable resizing windows by clicking and dragging on borders and gaps
        resize_on_border = false,

        -- Please see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Tearing/ before you turn this on
        allow_tearing    = false,

        layout           = "dwindle",
    },

    decoration = {
        rounding         = 15,
        rounding_power   = 3,

        -- Change transparency of focused and unfocused windows
        active_opacity   = 1.0,
        inactive_opacity = 1.0,

        shadow           = {
            enabled      = true,
            range        = 15,
            render_power = 4,
            color        = 0xaa1a1a1a,
        },

        blur             = {
            enabled           = true,
            size              = 4,
            passes            = 3,
            vibrancy          = 0.1696,
            new_optimizations = true,
        },
    },

    animations = {
        enabled = true,
    },
})

-- Default curves and animations, see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Animations/
hl.curve("easeOutQuint", { type = "bezier", points = { { 0.23, 1 }, { 0.32, 1 } } })
hl.curve("easeInOutCubic", { type = "bezier", points = { { 0.65, 0.05 }, { 0.36, 1 } } })
hl.curve("linear", { type = "bezier", points = { { 0, 0 }, { 1, 1 } } })
hl.curve("almostLinear", { type = "bezier", points = { { 0.5, 0.5 }, { 0.75, 1 } } })
hl.curve("quick", { type = "bezier", points = { { 0.15, 0 }, { 0.1, 1 } } })

-- Custom bounce
hl.curve("bouncy", {
    type = "spring",
    mass = 0.8,
    stiffness = 300,
    dampening = 20,
})

-- Default springs

-- hl.animation({ leaf = "global", enabled = true, speed = 3, bezier = "default" })
-- hl.animation({ leaf = "border", enabled = true, speed = 5.39, bezier = "easeOutQuint" })

---- Custom Window Animations ----
hl.animation({ leaf = "windows", enabled = true, speed = 2, spring = "bouncy" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 2, spring = "bouncy", style = "slide" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 2, bezier = "easeOutQuint", style = "slide" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 4, bezier = "easeInOutCubic" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 4, bezier = "easeInOutCubic" })
hl.animation({ leaf = "fade", enabled = true, speed = 4, bezier = "easeInOutCubic" })
hl.animation({ leaf = "layers", enabled = true, speed = 5, bezier = "easeInOutCubic" })
hl.animation({ leaf = "layersIn", enabled = true, speed = 5, bezier = "easeInOutCubic", style = "slide" })
hl.animation({ leaf = "layersOut", enabled = true, speed = 5, bezier = "easeInOutCubic", style = "slide" })
hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 1.5, bezier = "easeInOutCubic" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 1.5, bezier = "easeInOutCubic" })

---- Custom Workspace animations ----
hl.animation({ leaf = "workspaces", enabled = true, speed = 2.5, bezier = "easeOutQuint", style = "slide" })
hl.animation({ leaf = "workspacesIn", enabled = true, speed = 2.5, bezier = "easeOutQuint", style = "slide" })
hl.animation({ leaf = "workspacesOut", enabled = true, speed = 2.5, bezier = "easeOutQuint", style = "slide" })
hl.animation({ leaf = "zoomFactor", enabled = true, speed = 7, bezier = "quick" })

-- Ref https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/
-- "Smart gaps" / "No gaps when only"
-- uncomment all if you wish to use that.
-- hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
-- hl.workspace_rule({ workspace = "f[1]",   gaps_out = 0, gaps_in = 0 })
-- hl.window_rule({
--     name  = "no-gaps-wtv1",
--     match = { float = false, workspace = "w[tv1]" },
--     border_size = 0,
--     rounding    = 0,
-- })
-- hl.window_rule({
--     name  = "no-gaps-f1",
--     match = { float = false, workspace = "f[1]" },
--     border_size = 0,
--     rounding    = 0,
-- })

-- See https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/ for more
hl.config({
    dwindle = {
        preserve_split = true, -- You probably want this
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Master-Layout/ for more
hl.config({
    master = {
        new_status = "master",
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Scrolling-Layout/ for more
hl.config({
    scrolling = {
        fullscreen_on_one_column = true,
    },
})

hl.layer_rule({
    match = { namespace = "^swaync-control-center$" },
    blur = true,
    ignore_alpha = 0.058,
    animation = "slide right"
})

hl.layer_rule({
    match = { namespace = "^swaync-notification-window$" },
    blur = true,
    ignore_alpha = 0.058
})

hl.layer_rule({
    match = { namespace = "^waybar$" },
    blur = true,
    ignore_alpha = 0.1
})

hl.window_rule({
    match = { class = "^(firefox)$" },
    opacity = "0.85 0.75"
})

hl.window_rule({
    match = { class = "^(kitty)$" },
    opacity = "0.85 0.75"
})

hl.window_rule({
    match = { class = "^(dev.zed.Zed)$" },
    opacity = "0.85 0.75"
})

hl.window_rule({
    match = { class = "^(Spotify)$" },
    opacity = "0.85 0.75",
    workspace = 3
})

hl.window_rule({
    match = { class = "^(org.kde.dolphin)$" },
    opacity = "0.85 0.75"
})

hl.layer_rule({
    match = { namespace = "^rofi$" },
    blur = true,
    ignore_alpha = 0.1,
})

-- hl.layer_rule({
--     match = { namespace = "rofi" },
--     shadow = true,
-- })

--------------------------------------------------------

-- hl.window_rule({
--     match = { class = "^(kitty)$", title = "^(btop)$" },
--     float = true,
--     size = "monitor_w*0.5 monitor_h*1.0",
--     move = "monitor_w*0.5 monitor_h*0.0"
-- })

-- hl.window_rule({
--     match = { class = "^(kitty)$", title = "^(pipes\\.sh)$" },
--     float = true,
--     size = "monitor_w*0.5 monitor_h*0.25",
--     move = "monitor_w*0.0 monitor_h*0.0"
-- })

-- hl.window_rule({
--     match = { class = "^(kitty)$", title = "^(eyepic-dash)$" },
--     float = true,
--     size = "monitor_w*0.5 monitor_h*0.25",
--     move = "monitor_w*0.0 monitor_h*0.25"
-- })

-- hl.window_rule({
--     match = { class = "^(kitty)$", title = "^(cmatrix)$" },
--     float = true,
--     size = "monitor_w*0.5 monitor_h*0.25",
--     move = "monitor_w*0.0 monitor_h*0.5"
-- })

-- hl.window_rule({
--     match = { class = "^(kitty)$", title = "^(cava)$" },
--     float = true,
--     size = "monitor_w*0.5 monitor_h*0.25",
--     move = "monitor_w*0.0 monitor_h*0.75"
-- })

-------------------------------------------------------------------
---
