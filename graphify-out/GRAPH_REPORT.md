# Graph Report - dotfiles  (2026-10-01)

## Corpus Check
- Large corpus: 214 files · ~1,690,503 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 647 nodes · 706 edges · 72 communities (54 shown, 18 thin omitted)
- Extraction: 87% EXTRACTED · 12% INFERRED · 1% AMBIGUOUS · INFERRED: 86 edges (avg confidence: 0.82)
- Token cost: 444,939 input · 0 output

## Community Hubs (Navigation)
- Pink & Purple Dashboard Variants
- Amber & Blue Dashboard Variants
- Swaync Schema Property Primitives
- Fastfetch Splash & Kitty Theme Workflow
- Swaync Control Center Config
- Frame Recolor & Clock Scripts
- Swaync Widget Schema Refs
- Swaync Widget Pattern Refs
- Swaync Control Icons
- Swaync Notification Scripts Schema
- Swaync Backlight Widget Schema
- Swaync Widget Config Keys
- Kitty Theme Swift Converters
- Kitty Palette SVG Generator
- Swaync MPRIS Widget Schema
- Swaync Buttons Grid Schema
- Kitty Theme Preview Generation
- Swaync Title Widget Schema
- Swaync Inhibitors Widget Schema
- Swaync DND Widget Schema
- Wallpaper Palette Drivers
- Anime Eyes Terminal Backdrops
- Swaync Schema Root
- Control Center Height Setting
- Control Center PositionX
- Control Center PositionY
- Control Center Width
- CSS Priority Setting
- Image Visibility Setting
- Max Lines Setting
- Notification Layer Setting
- Body Image Height Setting
- Body Image Width Setting
- Notification Icon Size
- Notification PositionX
- Notification PositionY
- Swaync Volume Widget Schema
- Appearance & Theming Icons
- Margin Bottom Setting
- Margin Left Setting
- Margin Right Setting
- Margin Top Setting
- Fit To Screen Setting
- Hide On Action Setting
- Hide On Clear Setting
- Keyboard Shortcuts Setting
- Notification Window Width
- Schema Metadata Root
- Script Fail Notify Setting
- Notification Timeout Setting
- Critical Timeout Setting
- Low Timeout Setting
- Transition Time Setting
- Microphone Control Icons
- Animated Fastfetch Script
- Now Playing MPRIS Script
- Theme Previews Script
- Battery Alert Script
- Blur Adjust Script
- Border Toggle Script
- Btop Pywal Theme Script
- Lockscreen Script
- Shadow Toggle Script
- Wallpaper Sync Script
- Waybar Toggle Script
- Color Table Script
- VSCode Theme Extractor
- Kitty Conf Generator
- Markdown Preview Script
- Transparency Generator

## God Nodes (most connected - your core abstractions)
1. `patternProperties` - 10 edges
2. `widgets` - 10 edges
3. `Amber Dashboard Screenshot` - 9 edges
4. `^.{1,}$` - 8 edges
5. `Blue Dashboard Screenshot (Btop Layout)` - 8 edges
6. `Dashboard Screenshot - Purple Variant 1` - 8 edges
7. `text` - 7 edges
8. `actions` - 7 edges
9. `label` - 7 edges
10. `kitty-themes Collection` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Image-only kitty Window (no prompt, hidden cursor)` --semantically_similar_to--> `animated-fastfetch.sh — Animated ASCII Splash`  [INFERRED] [semantically similar]
  README.md → .config/fastfetch/README.md
- `Au5 Logo ASCII Art (fastfetch variant)` --semantically_similar_to--> `Au5 Logo ASCII Art (neofetch ${c1} variant)`  [INFERRED] [semantically similar]
  .config/fastfetch/Au5_ascii.fastfetch.txt → pictures/Au5_ascii.txt
- `Wallpaper & Color Sync (waypaper/swww + pywal)` --semantically_similar_to--> `Live Theme Preview (kitty @ set-colors / -o include)`  [INFERRED] [semantically similar]
  README.md → .config/kitty/kitty-themes/README.md
- `Anime Eyes Colour-Variant Art Set (blue/green/purple)` --semantically_similar_to--> `kitty-themes Project Banner Art`  [INFERRED] [semantically similar]
  pictures/system/anime-eyes/anime-eyes-blue.jpg → .config/kitty/kitty-themes/.github/kitty-themes.jpg
- `Custom Fastfetch ASCII Art (randomized bold keyboard chars)` --conceptually_related_to--> `Dionysus Fastfetch Config (shheersh v1.0)`  [INFERRED]
  README.md → .config/fastfetch/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Animated Fastfetch Splash Flow** — _config_fastfetch_readme_interactive_shell_splash_hook, _config_fastfetch_readme_animated_fastfetch_sh, _config_fastfetch_readme_frames_colour_directory, _config_fastfetch_readme_fastfetch_output_cache, _config_fastfetch_myascii_blank_spacer_logo [INFERRED 0.85]
- **kitty-themes Theme Adoption Pipeline** — _config_kitty_kitty_themes__github_issue_template_theme_request_theme_request_template, _config_kitty_kitty_themes__github_pull_request_template_pull_request_template, _config_kitty_kitty_themes_contributing_theme_contribution_workflow, _config_kitty_kitty_themes__tools_readme_theme_generation_pipeline, _config_kitty_kitty_themes_license_mit_license, _config_kitty_kitty_themes_readme_kitty_themes_collection [EXTRACTED 1.00]
- **pywal Desktop Re-theming Flow** — readme_wallpaper_color_sync, readme_waybar_nova_dark_theme, readme_workspace_1_dashboard, readme_fastfetch_custom_ascii, readme_hyprland_lua_config [EXTRACTED 1.00]
- **Fastfetch Dashboard Panel Composition** — screenshots_dashboard_amber_fastfetch_panel, screenshots_dashboard_amber_yazi_file_manager, screenshots_dashboard_amber_ttyclock_widget, screenshots_dashboard_amber_cmatrix_panel, screenshots_dashboard_amber_cava_visualizer [EXTRACTED 1.00]
- **Btop Dashboard Panel Composition** — screenshots_dashboard_blue2_btop_panel, screenshots_dashboard_blue2_pipes_panel, screenshots_dashboard_blue2_image_viewer_panel, screenshots_dashboard_blue2_cava_visualizer, screenshots_dashboard_blue2_cmatrix_panel [EXTRACTED 1.00]
- **Amber/Cyan/Green Theme Variant Family** — screenshots_dashboard_amber_palette, screenshots_dashboard_blue1_palette, screenshots_dashboard_green1_palette, screenshots_dashboard_amber_wallust_accent_sync [INFERRED 0.85]
- **Kitty Tiled Dashboard Composition (fetch + files + clock + matrix + visualizer)** — screenshots_dashboard_pink_fastfetch_panel, screenshots_dashboard_pink_yazi_file_panel, screenshots_dashboard_pink_clock_widget, screenshots_dashboard_pink_cmatrix_panel, screenshots_dashboard_pink_cava_panel [EXTRACTED 1.00]
- **Single Dashboard Layout Recoloured Across Theme Variants** — screenshots_dashboard_pink, screenshots_dashboard_purple1, screenshots_dashboard_purple2, screenshots_dashboard_sakura, screenshots_waybar_swaync [INFERRED 0.85]
- **SwayNC Control Center Stack (notifications + quick actions + media + volume)** — screenshots_waybar_swaync_notification_panel, screenshots_waybar_swaync_quick_actions_row, screenshots_waybar_swaync_mpris_player_widget, screenshots_waybar_swaync_volume_slider [EXTRACTED 1.00]
- **Pixel-art landscape wallpapers sharing a retro dithered 16-bit rendering style** — wallpapers_wallpaper10, wallpapers_wallpaper12, wallpapers_wallpaper13, wallpapers_wallpaper14, wallpapers_wallpaper3 [INFERRED 0.85]
- **Wallpapers whose dominant sky/sea blues would drive a blue theme variant** — wallpapers_wallpaper12, wallpapers_wallpaper13, wallpapers_wallpaper3 [INFERRED 0.85]
- **Wallpapers whose dominant pink/magenta/violet tones would drive a sakura, pink or purple theme variant** — wallpapers_wallpaper2, wallpapers_wallpaper4, wallpapers_wallpaper22 [INFERRED 0.75]
- **Brightness Level Ladder (20/40/60/80/100 states of one slider)** — _config_swaync_icons_brightness_20, _config_swaync_icons_brightness_40, _config_swaync_icons_brightness_60, _config_swaync_icons_brightness_80, _config_swaync_icons_brightness_100 [INFERRED 0.95]
- **Volume Level Ladder (mute/low/mid/high states of one slider)** — _config_swaync_icons_volume_mute, _config_swaync_icons_volume_low, _config_swaync_icons_volume_mid, _config_swaync_icons_volume_high [INFERRED 0.95]
- **Appearance Controls: wallpaper, colorscheme and visual effects** — _config_swaync_icons_picture, _config_swaync_icons_palette, _config_swaync_icons_wand [INFERRED 0.75]
- **Colour-indexed anime-eye kitty backdrops driven by eyePics[1..3]** — _config_hypr_hyprland_eyepics, pictures_system_anime_eyes_anime_eyes_blue_image, pictures_system_anime_eyes_anime_eyes_green_image, pictures_system_anime_eyes_anime_eyes_purple_image [EXTRACTED 1.00]
- **Terminal visual identity: art palette plus kitty theme collection** — pictures_system_anime_eyes_colour_variant_set, _config_kitty_kitty_themes__github_kitty_themes_banner, _config_hypr_hyprland_eyepics [INFERRED 0.75]

## Communities (72 total, 18 thin omitted)

### Community 0 - "Pink & Purple Dashboard Variants"
Cohesion: 0.06
Nodes (44): Dashboard Screenshot - Pink Variant, cava Audio Visualizer Panel, Large Seven-Segment Clock Widget, cmatrix Character Rain Panel, Fastfetch System Info Panel (luminara@archlinux), htop Process Monitor Panel, Pink/Magenta Theme Variant, Tiled Terminal Dashboard Grid Layout (+36 more)

### Community 1 - "Amber & Blue Dashboard Variants"
Cohesion: 0.07
Nodes (39): Amber Dashboard Screenshot, Amber Cava Audio Visualizer, Amber Character Rain Panel, Fastfetch Dashboard Layout Pattern, Amber Fastfetch Sysinfo Panel, Hyprland Transparent Tiling Grid, Amber Timestamp Toast Widget, Amber Accent Palette Variant (+31 more)

### Community 2 - "Swaync Schema Property Primitives"
Cohesion: 0.05
Nodes (39): properties, description, type, description, type, description, type, description (+31 more)

### Community 3 - "Fastfetch Splash & Kitty Theme Workflow"
Cohesion: 0.06
Nodes (27): Au5 Logo ASCII Art (fastfetch variant), L Monogram ASCII Art (fastfetch logo), Blank Spacer Logo (all-whitespace fastfetch logo block), animated-fastfetch.sh — Animated ASCII Splash, Dionysus Fastfetch Config (shheersh v1.0), frames_colour — Swappable Animation Frames, Theme Request Issue Template, kitty-themes Pull Request Template (+19 more)

### Community 4 - "Swaync Control Center Config"
Cohesion: 0.06
Nodes (34): control-center-height, control-center-layer, control-center-margin-bottom, control-center-margin-left, control-center-margin-right, control-center-margin-top, control-center-positionX, control-center-positionY (+26 more)

### Community 5 - "Frame Recolor & Clock Scripts"
Cohesion: 0.08
Nodes (11): lerp(), repl(), saturate(), tint(), bg(), extract_configuration_pair(), fg(), is_valid() (+3 more)

### Community 6 - "Swaync Widget Schema Refs"
Cohesion: 0.06
Nodes (34): description, items, $ref, type, additionalProperties, description, properties, type (+26 more)

### Community 7 - "Swaync Widget Pattern Refs"
Cohesion: 0.09
Nodes (23): $ref, $ref, $ref, $ref, $ref, $ref, $ref, ^backlight(#[a-zA-Z0-9_-]{1,}){0,1}?$ (+15 more)

### Community 8 - "Swaync Control Icons"
Cohesion: 0.12
Nodes (18): Bolt / Lightning Icon, Brightness 100% Icon, Brightness 20% Icon, Brightness 40% Icon, Brightness 60% Icon, Brightness 80% Icon, Brightness Control (swaync widget concept), Gamemode Controller Icon (+10 more)

### Community 9 - "Swaync Notification Scripts Schema"
Cohesion: 0.11
Nodes (18): additionalProperties, description, minProperties, required, type, additionalProperties, description, minProperties (+10 more)

### Community 10 - "Swaync Backlight Widget Schema"
Cohesion: 0.11
Nodes (18): additionalProperties, description, properties, type, default, description, type, default (+10 more)

### Community 11 - "Swaync Widget Config Keys"
Cohesion: 0.13
Nodes (15): actions, image-radius, image-size, button-text, clear-all-button, text, label, show-per-app (+7 more)

### Community 12 - "Kitty Theme Swift Converters"
Cohesion: 0.21
Nodes (8): AppKit, Cocoa, generate_conf_line(), hex(), process(), process_color(), CoreGraphics.CGWindow, Foundation

### Community 13 - "Kitty Palette SVG Generator"
Cohesion: 0.22
Nodes (6): draw_all_palettes(), draw_theme_palette(), extract_configuration_pair(), is_valid(), main(), read_configuration()

### Community 14 - "Swaync MPRIS Widget Schema"
Cohesion: 0.15
Nodes (13): default, description, type, default, description, type, additionalProperties, description (+5 more)

### Community 15 - "Swaync Buttons Grid Schema"
Cohesion: 0.18
Nodes (12): additionalProperties, description, properties, type, additionalProperties, default, description, type (+4 more)

### Community 17 - "Kitty Theme Preview Generation"
Cohesion: 0.31
Nodes (6): generate_theme_preview.sh script, generate_themes_previews.sh script, capture(), capture_linux(), capture_osx(), libcapture.sh script

### Community 18 - "Swaync Title Widget Schema"
Cohesion: 0.22
Nodes (9): default, description, type, button-text, additionalProperties, description, properties, type (+1 more)

### Community 19 - "Swaync Inhibitors Widget Schema"
Cohesion: 0.22
Nodes (9): default, description, type, additionalProperties, description, properties, type, clear-all-button (+1 more)

### Community 20 - "Swaync DND Widget Schema"
Cohesion: 0.22
Nodes (9): additionalProperties, description, properties, type, text, default, description, type (+1 more)

### Community 21 - "Wallpaper Palette Drivers"
Cohesion: 0.43
Nodes (8): Pixel Art Forest Meadow with Figure Resting by Teal Lake (green palette), Pixel Art Ancient Island City of Classical Ruins in Turquoise Sea (blue/teal palette), Pixel Art Blossoming Pink Tree on Sea Cliff under Cumulus Sky (blue palette with sakura accent), Pixel Art Misty Forest Waterfalls with Golden Turtle (muted green palette), Stylized 3D Japanese Rural Railway Scene with Cherry Blossoms and Wildflowers (sakura pink palette), Neon Cyberpunk Megacity Skyline in Violet Haze (purple palette), Pixel Art Anime Girl and Cat on Seawall above Reef Fish under Cumulus Sky (blue palette), Minimal Painterly Dusk Sky with Utility Pole, Two Birds and Crescent Moon (pink/magenta palette)

### Community 22 - "Anime Eyes Terminal Backdrops"
Cohesion: 0.60
Nodes (6): hyprland.lua eyePics table and themed kitty-backdrop keybinds, kitty-themes Project Banner Art, Anime Eyes Blue - Crystalline Blue-Eyed Portrait Art, Anime Eyes Green - Foliage Green-Eyed Portrait Art, Anime Eyes Purple - Dark Violet-Eyed Portrait Art, Anime Eyes Colour-Variant Art Set (blue/green/purple)

### Community 23 - "Swaync Schema Root"
Cohesion: 0.40
Nodes (4): additionalProperties, $schema, title, type

### Community 24 - "Control Center Height Setting"
Cohesion: 0.40
Nodes (5): default, description, minimum, type, control-center-height

### Community 25 - "Control Center PositionX"
Cohesion: 0.40
Nodes (5): default, description, enum, type, control-center-positionX

### Community 26 - "Control Center PositionY"
Cohesion: 0.40
Nodes (5): default, description, enum, type, control-center-positionY

### Community 27 - "Control Center Width"
Cohesion: 0.40
Nodes (5): default, description, minimum, type, control-center-width

### Community 28 - "CSS Priority Setting"
Cohesion: 0.40
Nodes (5): default, description, enum, type, cssPriority

### Community 29 - "Image Visibility Setting"
Cohesion: 0.40
Nodes (5): default, description, enum, type, image-visibility

### Community 30 - "Max Lines Setting"
Cohesion: 0.40
Nodes (5): properties, default, description, type, max-lines

### Community 31 - "Notification Layer Setting"
Cohesion: 0.40
Nodes (5): default, description, enum, type, layer

### Community 32 - "Body Image Height Setting"
Cohesion: 0.40
Nodes (5): default, description, minimum, type, notification-body-image-height

### Community 33 - "Body Image Width Setting"
Cohesion: 0.40
Nodes (5): default, description, minimum, type, notification-body-image-width

### Community 34 - "Notification Icon Size"
Cohesion: 0.40
Nodes (5): default, description, minimum, type, notification-icon-size

### Community 35 - "Notification PositionX"
Cohesion: 0.40
Nodes (5): default, description, enum, type, positionX

### Community 36 - "Notification PositionY"
Cohesion: 0.40
Nodes (5): default, description, enum, type, positionY

### Community 37 - "Swaync Volume Widget Schema"
Cohesion: 0.40
Nodes (5): additionalProperties, description, properties, type, volume

### Community 38 - "Appearance & Theming Icons"
Cohesion: 0.83
Nodes (4): Appearance and Theming Control, Palette / Colorscheme Icon, Picture / Wallpaper Icon, Magic Wand / Effects Icon

### Community 39 - "Margin Bottom Setting"
Cohesion: 0.50
Nodes (4): default, description, type, control-center-margin-bottom

### Community 40 - "Margin Left Setting"
Cohesion: 0.50
Nodes (4): default, description, type, control-center-margin-left

### Community 41 - "Margin Right Setting"
Cohesion: 0.50
Nodes (4): default, description, type, control-center-margin-right

### Community 42 - "Margin Top Setting"
Cohesion: 0.50
Nodes (4): default, description, type, control-center-margin-top

### Community 43 - "Fit To Screen Setting"
Cohesion: 0.50
Nodes (4): default, description, type, fit-to-screen

### Community 44 - "Hide On Action Setting"
Cohesion: 0.50
Nodes (4): default, description, type, hide-on-action

### Community 45 - "Hide On Clear Setting"
Cohesion: 0.50
Nodes (4): default, description, type, hide-on-clear

### Community 46 - "Keyboard Shortcuts Setting"
Cohesion: 0.50
Nodes (4): default, description, type, keyboard-shortcuts

### Community 47 - "Notification Window Width"
Cohesion: 0.50
Nodes (4): default, description, type, notification-window-width

### Community 48 - "Schema Metadata Root"
Cohesion: 0.50
Nodes (4): properties, $schema, description, type

### Community 49 - "Script Fail Notify Setting"
Cohesion: 0.50
Nodes (4): script-fail-notify, default, description, type

### Community 50 - "Notification Timeout Setting"
Cohesion: 0.50
Nodes (4): timeout, default, description, type

### Community 51 - "Critical Timeout Setting"
Cohesion: 0.50
Nodes (4): timeout-critical, default, description, type

### Community 52 - "Low Timeout Setting"
Cohesion: 0.50
Nodes (4): timeout-low, default, description, type

### Community 53 - "Transition Time Setting"
Cohesion: 0.50
Nodes (4): transition-time, default, description, type

### Community 54 - "Microphone Control Icons"
Cohesion: 1.00
Nodes (3): Microphone / Audio Input Control, Microphone Active Icon, Microphone Muted Icon

## Ambiguous Edges - Review These
- `animated-fastfetch.sh — Animated ASCII Splash` → `Blank Spacer Logo (all-whitespace fastfetch logo block)`  [AMBIGUOUS]
  .config/fastfetch/myascii.txt · relation: conceptually_related_to
- `Amber Seven-Segment TTY Clock` → `Amber Timestamp Toast Widget`  [AMBIGUOUS]
  screenshots/dashboard-amber.png · relation: conceptually_related_to
- `Minimal zsh Prompt with Right-Aligned Timestamp` → `Fastfetch Panel (Sakura Tint)`  [AMBIGUOUS]
  screenshots/dashboard-purple1.png · relation: conceptually_related_to
- `Pixel Art Blossoming Pink Tree on Sea Cliff under Cumulus Sky (blue palette with sakura accent)` → `Pixel Art Misty Forest Waterfalls with Golden Turtle (muted green palette)`  [AMBIGUOUS]
  wallpapers/wallpaper13.png · relation: conceptually_related_to
- `Bolt / Lightning Icon` → `Brightness Control (swaync widget concept)`  [AMBIGUOUS]
  .config/swaync/icons/bolt.png · relation: conceptually_related_to
- `Picture / Wallpaper Icon` → `Magic Wand / Effects Icon`  [AMBIGUOUS]
  .config/swaync/icons/wand.png · relation: semantically_similar_to
- `Stopwatch / Timer Icon` → `Media Playback Control (mpris widget concept)`  [AMBIGUOUS]
  .config/swaync/icons/timer.png · relation: conceptually_related_to

## Knowledge Gaps
- **332 isolated node(s):** `battery-alert.sh script`, `blur-adjust.sh script`, `border-toggle.sh script`, `btop-pywal-theme.sh script`, `lockscreen.sh script` (+327 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 385 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `animated-fastfetch.sh — Animated ASCII Splash` and `Blank Spacer Logo (all-whitespace fastfetch logo block)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Amber Seven-Segment TTY Clock` and `Amber Timestamp Toast Widget`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Minimal zsh Prompt with Right-Aligned Timestamp` and `Fastfetch Panel (Sakura Tint)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Pixel Art Blossoming Pink Tree on Sea Cliff under Cumulus Sky (blue palette with sakura accent)` and `Pixel Art Misty Forest Waterfalls with Golden Turtle (muted green palette)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Bolt / Lightning Icon` and `Brightness Control (swaync widget concept)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Picture / Wallpaper Icon` and `Magic Wand / Effects Icon`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Stopwatch / Timer Icon` and `Media Playback Control (mpris widget concept)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._