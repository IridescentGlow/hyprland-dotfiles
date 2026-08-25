import re, glob, os

src_dir = os.path.expanduser("~/.config/fastfetch/frames_colour")
dst_dir = os.path.expanduser("~/.config/fastfetch/frames_compressed")
os.makedirs(dst_dir, exist_ok=True)

cell = re.compile(r'\x1b\[38;2;(\d+);(\d+);(\d+)m(.)\x1b\[0m')

for path in glob.glob(os.path.join(src_dir, "*.txt")):
    with open(path, encoding='utf-8', errors='ignore') as f:
        lines = f.read().split('\n')
    out_lines = []
    for line in lines:
        cells = cell.findall(line)
        if not cells:
            out_lines.append(line)
            continue
        out, last = [], None
        for r, g, b, ch in cells:
            if (r, g, b) != last:
                out.append(f"\x1b[38;2;{r};{g};{b}m")
                last = (r, g, b)
            out.append(ch)
        out.append("\x1b[0m")
        out_lines.append(''.join(out))
    with open(os.path.join(dst_dir, os.path.basename(path)), 'w') as f:
        f.write('\n'.join(out_lines))

print("done")
