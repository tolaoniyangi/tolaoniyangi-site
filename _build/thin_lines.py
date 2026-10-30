"""Thin the drawn lines in diagram SVGs (run after the diagram scripts).
White strokes (roads, gaps between panels) are left alone."""
import re, sys, glob
FACTOR, FLOOR = 0.55, 0.5
def thin_tag(tag):
    if 'data-fine' in tag: return tag
    m = re.search(r'stroke="([^"]+)"', tag)
    if not m or m.group(1).lower() in ("#fff", "#ffffff", "none", "white"): return tag
    def sw(mm):
        v = float(mm.group(1)); return f'stroke-width="{max(FLOOR, round(v*FACTOR,2))}"'
    if 'stroke-width' in tag:
        return re.sub(r'stroke-width="([\d.]+)"', sw, tag)
    return tag.replace('stroke=', f'stroke-width="{FLOOR+0.2}" stroke=', 1)   # default 1 -> 0.7
for f in sys.argv[1:]:
    s = open(f).read()
    if 'data-thinned' in s: print("already thin", f); continue
    s = re.sub(r'<(?:line|rect|path|circle|polyline|g)\b[^>]*>', lambda m: thin_tag(m.group(0)), s)
    s = s.replace('<svg ', '<svg data-thinned="1" ', 1) if 'data-thinned' not in s else s
    open(f, 'w').write(s)
    print("thinned", f)
