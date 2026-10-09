#!/usr/bin/env python3
"""
Match the wallpaper to the colour of the album art Spotify is showing.

Watches Spotify over MPRIS (playerctl), pulls the dominant colour out of the
cover, and -- if a wallpaper in your library is a clearly better colour match
than the current one -- hands it to wallpaper-sync.sh, which re-themes
waybar/rofi/kitty/borders exactly as if you had picked it in waypaper.

  start:   spotify-wallpaper.py            (autostart does this)
  stop:    spotify-wallpaper.py --quit     (this is also your off switch)
  dry run: spotify-wallpaper.py --once     (print the pick for the current track)
  index:   spotify-wallpaper.py --list     (show each wallpaper's colour)

Wallpaper folders and tuning knobs are in CONFIG below.
"""

import colorsys
import hashlib
import json
import math
import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HOME = Path.home()

CONFIG = {
    # "cover":   the wallpaper IS the album art (blurred fill + sharp cover).
    # "library": pick the closest-coloured image from the folders below.
    "mode": "cover",
    # cover mode: canvas size (wider than the screen, for the parallax pan),
    # how dark the blurred fill is, and the sharp cover's share of the height.
    "canvas": (4200, 1500),
    "dim": 0.6,
    # Blur of the fill, in tenths of a pixel-radius at wallpaper scale: ~10x
    # this many pixels on screen. Lower = sharper background.
    "blur": 7,
    "cover_height": 0.58,
    # Folders searched for wallpapers (not recursive).
    "dirs": [
        HOME / "Pictures",
        HOME / "Pictures/system/ultra-wide-wallpapers",
    ],
    # Skip small images (banners, icons) -- a wallpaper is at least this wide.
    "min_width": 2400,
    # Only swap when the best wallpaper beats the current one by this much
    # (OKLab distance). Stops the background flip-flopping between two
    # near-identical matches on consecutive songs.
    "hysteresis": 0.05,
    # Never change the wallpaper more often than this (seconds); each change
    # restarts waybar.
    "min_interval": 25,
    "sync_script": HOME / ".config/hypr/scripts/wallpaper-sync.sh",
}

CACHE_DIR = HOME / ".cache/spotify-wallpaper"
INDEX_FILE = CACHE_DIR / "index.json"
PIDFILE = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "spotify-wallpaper.pid"
CURRENT = HOME / ".cache/wal/current_wallpaper"
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}


# ---- colour maths ---------------------------------------------------------

def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def srgb_to_oklab(rgb):
    r, g, b = (_lin(v / 255) for v in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )


def distance(a, b):
    """OKLab distance with chroma/hue counting more than lightness: the goal
    is 'same colour', not 'same brightness' (a dark red cover should still
    pick a red wallpaper, not a pale pink one)."""
    return math.sqrt(0.5 * (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def dominant_colour(img):
    """The colour a person would call this image's colour: the most prominent
    *vivid* swatch, falling back to the average for greyscale images."""
    small = img.convert("RGB").resize((96, 96))
    pal = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT).convert("RGB")
    counts = pal.getcolors(96 * 96)
    total = sum(n for n, _ in counts)
    best, best_score = None, -1.0
    for n, rgb in counts:
        h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
        # Coverage matters, but saturated mid-brightness swatches win over
        # large grey/black/white areas.
        score = (n / total) * (0.15 + s) * (0.3 + min(v, 1 - 0.4 * v))
        if score > best_score:
            best, best_score = rgb, score
    return best


# ---- wallpaper index ------------------------------------------------------

def wallpapers():
    out = []
    for d in CONFIG["dirs"]:
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir()):
            if p.suffix.lower() in IMG_EXT and p.is_file():
                out.append(p.resolve())
    return out


def load_index():
    """{path: {mtime, rgb, lab}} -- recomputed only for new/changed files."""
    try:
        cache = json.loads(INDEX_FILE.read_text())
    except (OSError, ValueError):
        cache = {}
    index, dirty = {}, False
    for p in wallpapers():
        key, mtime = str(p), p.stat().st_mtime
        hit = cache.get(key)
        if hit and hit.get("mtime") == mtime and "width" in hit:
            if hit["width"] >= CONFIG["min_width"]:
                index[key] = hit
            continue
        try:
            with Image.open(p) as im:
                width = im.width
                if width < CONFIG["min_width"]:
                    cache[key] = {"mtime": mtime, "width": width}
                    dirty = True
                    continue
                im.draft("RGB", (400, 400))
                rgb = dominant_colour(im)
        except Exception as e:  # unreadable image: skip it, keep going
            print(f"skip {p.name}: {e}", file=sys.stderr)
            continue
        index[key] = cache[key] = {"mtime": mtime, "width": width,
                                   "rgb": rgb, "lab": srgb_to_oklab(rgb)}
        dirty = True
    if dirty:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        INDEX_FILE.write_text(json.dumps(cache))
    return index


# ---- album art ------------------------------------------------------------

def fetch_art(url):
    if url.startswith("file://"):
        return Image.open(url[7:])
    tmp = Path(tempfile.gettempdir()) / f"spotify-art-{hashlib.md5(url.encode()).hexdigest()}"
    if not tmp.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "spotify-wallpaper"})
        with urllib.request.urlopen(req, timeout=10) as r:
            tmp.write_bytes(r.read())
    return Image.open(tmp)


def current_wallpaper():
    try:
        return str(CURRENT.resolve())
    except OSError:
        return ""


def pick(art_lab, index):
    ranked = sorted((distance(art_lab, v["lab"]), k) for k, v in index.items())
    return ranked


def compose_cover(art, url):
    """Build a wallpaper out of the cover: a blurred, darkened copy fills the
    whole canvas and the sharp cover sits in the middle with rounded corners
    and a soft shadow. The canvas is wider than the screen so the workspace
    parallax still has room to pan."""
    W, H = CONFIG["canvas"]
    art = art.convert("RGB")

    # Background: crop the cover to the canvas aspect, blur it at low
    # resolution (fast, and smoother than a big radius), then scale up.
    sw, sh = W // 10, H // 10
    side = min(art.width, art.height)
    crop_h = int(side * H / W)
    bg = art.crop((0, (art.height - crop_h) // 2, art.width, (art.height + crop_h) // 2)) \
        if art.width / art.height < W / H else art
    bg = bg.resize((sw, sh), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(CONFIG["blur"]))
    bg = bg.resize((W, H), Image.Resampling.BICUBIC)
    bg = ImageEnhance.Color(bg).enhance(1.25)
    bg = ImageEnhance.Brightness(bg).enhance(CONFIG["dim"])

    # Foreground cover.
    size = int(H * CONFIG["cover_height"])
    fg = art.resize((size, size), Image.Resampling.LANCZOS)
    radius = size // 14
    mask = Image.new("L", (size * 2, size * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * 2 - 1, size * 2 - 1), radius * 2, fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)

    x, y = (W - size) // 2, (H - size) // 2
    shadow = Image.new("L", (W, H), 0)
    shadow.paste(Image.new("L", (size, size), 150), (x, y + size // 30), mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(size // 18))
    bg.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), shadow)
    bg.paste(fg, (x, y), mask)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out = CACHE_DIR / f"cover-{hashlib.md5(url.encode()).hexdigest()[:12]}.jpg"
    bg.save(out, quality=92)
    # Keep only the few most recent covers.
    old = sorted(CACHE_DIR.glob("cover-*.jpg"), key=lambda p: p.stat().st_mtime)[:-6]
    for p in old:
        if str(p) != current_wallpaper():
            p.unlink(missing_ok=True)
    return str(out)


def handle_cover(url, state, dry=False):
    if not dry:
        wait = CONFIG["min_interval"] - (time.monotonic() - state["last"])
        if wait > 0:
            time.sleep(wait)
            url = current_art_url() or url  # skip past songs we waited through
    with fetch_art(url) as art:
        path = compose_cover(art, url)
    print(f"cover -> {Path(path).name}", flush=True)
    if dry or path == current_wallpaper():
        return
    subprocess.run([str(CONFIG["sync_script"]), path], check=False)
    state["last"] = time.monotonic()


def handle(url, index, state, dry=False):
    if CONFIG["mode"] == "cover":
        return handle_cover(url, state, dry)
    with fetch_art(url) as art:
        rgb = dominant_colour(art)
    lab = srgb_to_oklab(rgb)
    ranked = pick(lab, index)
    if not ranked:
        print("no wallpapers indexed", file=sys.stderr)
        return
    best_d, best = ranked[0]
    cur = current_wallpaper()
    cur_d = next((d for d, k in ranked if k == cur), None)
    hexc = "#%02x%02x%02x" % rgb
    print(f"art {hexc} -> {Path(best).name} (d={best_d:.3f})"
          + (f", current {Path(cur).name} d={cur_d:.3f}" if cur_d is not None else ""), flush=True)
    if dry:
        return
    if best == cur or (cur_d is not None and cur_d - best_d < CONFIG["hysteresis"]):
        return
    wait = CONFIG["min_interval"] - (time.monotonic() - state["last"])
    if wait > 0:
        time.sleep(wait)
    subprocess.run([str(CONFIG["sync_script"]), best], check=False)
    state["last"] = time.monotonic()


def current_art_url():
    r = subprocess.run(["playerctl", "-p", "spotify", "metadata", "mpris:artUrl"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def quit_running():
    try:
        os.kill(int(PIDFILE.read_text()), signal.SIGTERM)
        print("stopped")
    except (OSError, ValueError):
        print("not running")


def main():
    args = sys.argv[1:]
    if "--quit" in args:
        return quit_running()
    if "--list" in args:
        for k, v in load_index().items():
            print("#%02x%02x%02x  %s" % (*v["rgb"], Path(k).name))
        return
    if "--once" in args:
        url = current_art_url()
        if not url:
            sys.exit("Spotify has no cover art right now")
        return handle(url, load_index(), {"last": 0}, dry=True)

    # Single instance.
    try:
        os.kill(int(PIDFILE.read_text()), 0)
        sys.exit("already running")
    except (OSError, ValueError):
        pass
    PIDFILE.write_text(str(os.getpid()))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

    index = load_index()
    state = {"last": 0.0}
    last_url = None
    while True:
        # --follow ends when Spotify exits; loop so we pick it up again.
        proc = subprocess.Popen(
            ["playerctl", "-p", "spotify", "--follow", "metadata", "mpris:artUrl"],
            stdout=subprocess.PIPE, text=True)
        for line in proc.stdout:
            url = line.strip()
            if not url or url == last_url:
                continue
            last_url = url
            try:
                index = load_index()  # cheap: only re-reads changed files
                handle(url, index, state)
            except Exception as e:
                print(f"error: {e}", file=sys.stderr, flush=True)
        proc.wait()
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    finally:
        try:
            if PIDFILE.exists() and int(PIDFILE.read_text()) == os.getpid():
                PIDFILE.unlink()
        except (OSError, ValueError):
            pass
