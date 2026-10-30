# Cut and fill: plan above, section below, linked by section line A-A'.
import math
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
W,H=720,600; b=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Plan and section of a site: in plan, the site is split into an area to cut and an area to fill; the section along line A to A prime shows soil above the target elevation being cut and hollows below it being filled">']
b.append(f'''<defs><pattern id="hf" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{INK}" stroke-width=".6"/></pattern>
<clipPath id="sheet"><rect width="{W}" height="300"/></clipPath>
<clipPath id="site"><path d="M150 70 L470 50 L540 200 L430 280 L170 262 Z"/></clipPath></defs>''')
b.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
# ---- plan
for k in range(-6,8):
    pts=" ".join(f"{x},{150+k*30+24*math.sin(x/110)+10*math.sin(x/37):.1f}" for x in range(0,W+1,10))
    b.append(f'<polyline clip-path="url(#sheet)" points="{pts}" fill="none" stroke="{MUTED}" stroke-width="{.8 if k%4==0 else .5}" stroke-opacity=".7"/>')
b.append(f'<g clip-path="url(#site)"><path d="M0 0 H{W} V95 C 520 130, 420 110, 340 165 S 170 245, 0 215 Z" fill="{ACC}" fill-opacity=".45"/><path d="M{W} 95 C 520 130, 420 110, 340 165 S 170 245, 0 215 V300 H{W} Z" fill="url(#hf)"/></g>')
b.append(f'<path d="M150 70 L470 50 L540 200 L430 280 L170 262 Z" fill="none" stroke="{INK}" stroke-width="1.2"/>')
# section line A-A'
sy=170
b.append(f'<line x1="90" y1="{sy}" x2="610" y2="{sy}" stroke="{INK}" stroke-width=".8" stroke-dasharray="10 4 2 4"/>')
for x,l in ((90,"A"),(610,"A′")):
    b.append(f'<circle cx="{x}" cy="{sy}" r="11" fill="#fff" stroke="{INK}" stroke-width=".8"/>'+T(x,sy+4,l,a="middle",s=11,w=700))
b.append(T(200,120,"CUT",s=13,w=700,ls=1.5)); b.append(T(380,236,"FILL",s=13,w=700,ls=1.5))
b.append(T(20,24,"PLAN",s=11,w=600,op=.6,ls=1))
b.append(f'<line x1="0" y1="300" x2="{W}" y2="300" stroke="{LINE}" stroke-width=".8"/>')
# ---- section (x aligned with plan)
top=330; base=560
def ground(x): return 445-46*math.sin((x-90)/95+0.4)-14*math.sin(x/41+1.1)
xs=list(range(90,611,5)); g=[(x,ground(x)) for x in xs]
level=round(sum(y for _,y in g)/len(g),1)
path="M"+" L".join(f"{x} {y:.1f}" for x,y in g)
b.append(f'<clipPath id="ab"><rect x="0" y="0" width="{W}" height="{level}"/></clipPath><clipPath id="be"><rect x="0" y="{level}" width="{W}" height="{H}"/></clipPath>')
b.append(f'<path d="{path} L610 {base} L90 {base} Z" fill="#DCD6CB"/>')
b.append(f'<path d="{path} L610 {level} L90 {level} Z" fill="{ACC}" fill-opacity=".45" clip-path="url(#ab)"/>')
b.append(f'<path d="{path} L610 {level} L90 {level} Z" fill="url(#hf)" clip-path="url(#be)"/>')
b.append(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="1"/>')
b.append(f'<line x1="70" y1="{level}" x2="630" y2="{level}" stroke="{INK}" stroke-width=".8" stroke-dasharray="6 4"/>')
b.append(T(100,level+20,"Target elevation, where cut = fill",s=11,w=600))
for x,l in ((90,"A"),(610,"A′")):
    b.append(T(x,top+6,l,a="middle",s=11,w=700))
b.append(T(20,top-6,"SECTION A–A′",s=11,w=600,op=.6,ls=1))
b.append(T(20,H-14,"NOT TO SCALE",s=10,op=.5,ls=1))
b.append('</svg>')
open('images/fig-cutfill-combined.svg','w').write("\n".join(b))
print("ok")
