import math, random
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
# ---- Fig: drag to select ----
random.seed(7)
W,H=720,440
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Diagram: a dashed box dragged over map points selects them, and the same items show as checked in a side panel">']
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
# street grid, slightly rotated
o.append(f'<defs><clipPath id="map"><rect width="{W}" height="{H}"/></clipPath></defs><g clip-path="url(#map)"><g stroke="{LINE}" stroke-width="1" transform="rotate(-8 260 220)">')
for x in range(-120,620,46): o.append(f'<line x1="{x}" y1="-80" x2="{x}" y2="520"/>')
for y in range(-80,520,38): o.append(f'<line x1="-120" y1="{y}" x2="620" y2="{y}"/>')
o.append(f'<path d="M-100 330 C 80 300, 200 420, 560 250" stroke="{LINE}" stroke-width="10" fill="none"/></g></g>')
bx,by,bw,bh=150,105,230,175
pts=[]
while len(pts)<46:
    x,y=random.uniform(30,480),random.uniform(30,410)
    if all((x-a)**2+(y-b)**2>26**2 for a,b in pts): pts.append((x,y))
sel=0
for x,y in pts:
    inside=bx<x<bx+bw and by<y<by+bh
    if inside:
        sel+=1; o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{ACC}" stroke="#fff" stroke-width="2"/>')
    else:
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{ACC}" fill-opacity=".08" stroke="{ACC}" stroke-width="2" stroke-dasharray="7 5"/>')
cx,cy=bx+bw,by+bh
o.append(f'<path d="M{cx} {cy} l0 22 l6 -6 l5 11 l4 -2 l-5 -11 l9 0 z" fill="{INK}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>')
o.append(f'<circle cx="{bx}" cy="{by}" r="4" fill="{ACC}"/>')
# panel
px=510
o.append(f'<rect x="{px}" y="24" width="186" height="392" fill="#fff" stroke="{LINE}"/>')
o.append(f'<text x="{px+16}" y="54" {F} font-size="13" font-weight="700" fill="{INK}">Project</text>')
o.append(f'<text x="{px+16}" y="74" {F} font-size="12" fill="{ACC}" font-weight="600">{sel} selected</text>')
for i in range(9):
    y=100+i*34; on=i<6
    o.append(f'<line x1="{px}" y1="{y-12}" x2="{px+186}" y2="{y-12}" stroke="{LINE}"/>')
    o.append(f'<rect x="{px+16}" y="{y}" width="14" height="14" rx="2" fill="{ACC if on else "#fff"}" stroke="{ACC if on else MUTED}" stroke-width="1.5"/>')
    if on: o.append(f'<path d="M{px+19} {y+7} l3 3 l6 -6" stroke="#fff" stroke-width="2" fill="none"/>')
    o.append(f'<rect x="{px+40}" y="{y+3}" width="{70+(i*29)%60}" height="8" rx="4" fill="{INK if on else LINE}" fill-opacity="{.75 if on else 1}"/>')
o.append('</svg>')
open('images/fig-select.svg','w').write("\n".join(o))

# ---- Fig: cut and fill section ----
W,H=720,330
def ground(x):
    return 170-48*math.sin(x/120+0.9)-16*math.sin(x/51+1.3)
xs=list(range(0,W+1,6)); g=[(x,ground(x)) for x in xs]
level=round(sum(y for _,y in g)/len(g),1)
path="M"+" L".join(f"{x} {y:.1f}" for x,y in g)
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Section diagram: soil above the target level is cut, the gap below it is filled, and the tool finds the level where they balance">']
o.append(f'''<defs>
<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1.2"/></pattern>
<clipPath id="above"><rect x="0" y="0" width="{W}" height="{level}"/></clipPath>
<clipPath id="below"><rect x="0" y="{level}" width="{W}" height="{H}"/></clipPath>
</defs>''')
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
o.append(f'<path d="{path} L{W} {H} L0 {H} Z" fill="#D8D2C6"/>')  # earth
o.append(f'<path d="{path} L{W} {level} L0 {level} Z" fill="{ACC}" fill-opacity=".6" clip-path="url(#above)"/>')  # cut
o.append(f'<path d="{path} L{W} {level} L0 {level} Z" fill="url(#hatch)" clip-path="url(#below)"/>')  # fill
o.append(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="2"/>')
o.append(f'<line x1="0" y1="{level}" x2="{W}" y2="{level}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="8 6"/>')
o.append(f'<text x="16" y="34" {F} font-size="13" font-weight="700" fill="{INK}">Target elevation <tspan font-weight="400" fill-opacity=".7">(dashed): where cut volume = fill volume</tspan></text>')
# labels
xc=min(xs,key=lambda x:ground(x)); xf=max(xs,key=lambda x:ground(x))
o.append(f'<text x="{xc}" y="{ground(xc)-16:.0f}" text-anchor="middle" {F} font-size="15" font-weight="800" letter-spacing="1.5" fill="{INK}">CUT</text>')
o.append(f'<text x="{xf}" y="{ground(xf)+28:.0f}" text-anchor="middle" {F} font-size="15" font-weight="800" letter-spacing="1.5" fill="{INK}">FILL</text>')
o.append(f'<text x="16" y="{H-14}" {F} font-size="11" letter-spacing="1" fill="{INK}" fill-opacity=".6">SITE SECTION · NOT TO SCALE</text>')
o.append('</svg>')
open('images/fig-cutfill.svg','w').write("\n".join(o))
print("ok")
