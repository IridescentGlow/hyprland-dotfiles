import re, glob, os, sys
import colorsys

def saturate(rgb, factor=1.5):
    r, g, b = [c / 255 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = min(1.0, s * factor)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (round(r*255), round(g*255), round(b*255))

wal_colors_file = os.path.expanduser("~/.cache/wal/colors")
src_dir = os.path.expanduser("~/.config/fastfetch/frames_compressed")
dst_dir = os.path.expanduser("~/.config/fastfetch/frames_pywal")
os.makedirs(dst_dir, exist_ok=True)

def hex_to_rgb(h):
    h = h.strip().lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

with open(wal_colors_file) as f:
    palette = [hex_to_rgb(line) for line in f.readlines()]

dark   = palette[0]
accent = palette[5]
light  = palette[9] if len(palette) > 7 else palette[-1]

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def tint(r, g, b):
    lum = (0.299*r + 0.587*g + 0.114*b) / 255
    if lum < 0.02:
        return dark
    if lum < 0.5:
        result = lerp(dark, accent, lum / 0.5)
    else:
        result = lerp(accent, light, (lum - 0.5) / 0.5)
    return saturate(result, 1.6)

cell = re.compile(r'\x1b\[38;2;(\d+);(\d+);(\d+)m([^\x1b]*)')

files = glob.glob(os.path.join(src_dir, "*.txt"))
print(f"Found {len(files)} source frames in {src_dir}", file=sys.stderr)

count = 0
for path in files:
    with open(path, encoding='utf-8', errors='ignore') as f:
        content = f.read()

    def repl(m):
        r, g, b, text = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        nr, ng, nb = tint(r, g, b)
        return f"\x1b[38;2;{nr};{ng};{nb}m{text}"

    new_content = cell.sub(repl, content)
    out_path = os.path.join(dst_dir, os.path.basename(path))
    with open(out_path, 'w') as f:
        f.write(new_content)
    count += 1

print(f"done — wrote {count} frames to {dst_dir}", file=sys.stderr)
