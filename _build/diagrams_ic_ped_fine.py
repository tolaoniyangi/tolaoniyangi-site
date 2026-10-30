# Fine-line versions: Intelligent City process, census-to-street method, marquee tile fix.
import random
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
def svg(W,H,label,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'+"\n".join(body)+'</svg>'
def arrow(b,x1,y,x2): b.append(f'<line x1="{x1}" y1="{y}" x2="{x2-7}" y2="{y}" stroke="{INK}" stroke-width=".8"/><path d="M{x2} {y} l-8 -3.5 v7 z" fill="{INK}"/>')

# ---------- Intelligent City: lines -> panel building -> carbon + cost ----------
W,H=720,380; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
pw,ph,py=200,220,50; xs=[20,260,500]
for x in xs: b.append(f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" fill="#fff" stroke="{LINE}" stroke-width=".8"/>')
# 1. lines in Rhino: construction grid + accent curves with control points
x0=xs[0]
b.append(f'<g stroke="{LINE}" stroke-width=".5">'+"".join(f'<line x1="{x0+gx}" y1="{py}" x2="{x0+gx}" y2="{py+ph}"/>' for gx in range(20,pw,20))+"".join(f'<line x1="{x0}" y1="{py+gy}" x2="{x0+pw}" y2="{py+gy}"/>' for gy in range(20,ph,20))+'</g>')
pts=[(40,60),(150,60),(150,110),(120,110),(120,170),(40,170)]
d="M"+" L".join(f"{x0+a} {py+c}" for a,c in pts)+" Z"
b.append(f'<path d="{d}" fill="none" stroke="{ACC}" stroke-width="1.2"/>')
b.append(f'<line x1="{x0+40}" y1="{py+115}" x2="{x0+120}" y2="{py+115}" stroke="{ACC}" stroke-width=".8" stroke-dasharray="4 3"/>')
for a,c in pts: b.append(f'<rect x="{x0+a-2.5}" y="{py+c-2.5}" width="5" height="5" fill="#fff" stroke="{ACC}" stroke-width=".8"/>')
b.append(T(x0+40,py+196,"Footprint and floors as curves",s=10,op=.6))
# 2. generated building from the panel system (isometric, panelized)
x0=xs[1]; bx,by=x0+48,py+190; w,dpt,h=80,60,120; ddx,ddy=dpt*.75,dpt*.42
front=[(bx,by),(bx+w,by),(bx+w,by-h),(bx,by-h)]
side=[(bx+w,by),(bx+w+ddx,by-ddy),(bx+w+ddx,by-ddy-h),(bx+w,by-h)]
top=[(bx,by-h),(bx+w,by-h),(bx+w+ddx,by-ddy-h),(bx+ddx,by-ddy-h)]
P=lambda pts:"M"+" L".join(f"{a:.1f} {c:.1f}" for a,c in pts)+" Z"
b.append(f'<path d="{P(front)}" fill="#F6F4EF" stroke="{INK}" stroke-width=".9"/>')
b.append(f'<path d="{P(side)}" fill="#ECE8E0" stroke="{INK}" stroke-width=".9"/>')
b.append(f'<path d="{P(top)}" fill="#fff" stroke="{INK}" stroke-width=".9"/>')
for k in range(1,4):  # panel columns on front
    xx=bx+k*w/4; b.append(f'<line x1="{xx}" y1="{by}" x2="{xx}" y2="{by-h}" stroke="{INK}" stroke-width=".5" stroke-opacity=".6"/>')
for k in range(1,6):  # floors
    yy=by-k*h/6; b.append(f'<line x1="{bx}" y1="{yy}" x2="{bx+w}" y2="{yy}" stroke="{INK}" stroke-width=".5" stroke-opacity=".6"/>')
    b.append(f'<line x1="{bx+w}" y1="{yy}" x2="{bx+w+ddx}" y2="{yy-ddy}" stroke="{INK}" stroke-width=".5" stroke-opacity=".6"/>')
for k in range(1,3):
    t=k/3; b.append(f'<line x1="{bx+w+ddx*t}" y1="{by-ddy*t}" x2="{bx+w+ddx*t}" y2="{by-ddy*t-h}" stroke="{INK}" stroke-width=".5" stroke-opacity=".6"/>')
# highlight one panel
b.append(f'<rect x="{bx+w/4}" y="{by-3*h/6}" width="{w/4}" height="{h/6}" fill="{ACC}" fill-opacity=".55" stroke="{ACC}" stroke-width=".8"/>')
b.append(T(x0+20,py+212,"Every piece is a standard panel",s=10,op=.6))
# 3. carbon + cost dashboard
x0=xs[2]
b.append(T(x0+16,py+30,"Embodied carbon",s=11,w=600))
for i,(lab,wd) in enumerate([("Timber",54),("Concrete",88),("Steel",36)]):
    y=py+46+i*20
    b.append(T(x0+16,y+8,lab,s=10,op=.7)); b.append(f'<rect x="{x0+76}" y="{y}" width="{wd}" height="9" fill="{ACC}" fill-opacity="{.35+.2*i}"/>')
b.append(f'<line x1="{x0+16}" y1="{py+118}" x2="{x0+pw-16}" y2="{py+118}" stroke="{LINE}" stroke-width=".8"/>')
b.append(T(x0+16,py+140,"Cost",s=11,w=600))
for i,(lab,wd) in enumerate([("Structure",96),("Envelope",64),("Interiors",44)]):
    y=py+156+i*20
    b.append(T(x0+16,y+8,lab,s=10,op=.7)); b.append(f'<rect x="{x0+76}" y="{y}" width="{wd}" height="9" fill="{INK}" fill-opacity="{.25+.15*i}"/>')
for i,x in enumerate(xs):
    t,sub=[("Draw lines in Rhino","The designer sketches the massing"),("Generate the building","A real design from the set panel system"),("Estimate carbon and cost","Quantities pulled from every design")][i]
    b.append(T(x,py+ph+30,f"{i+1}  {t}",s=13,w=700)); b.append(T(x,py+ph+48,sub,s=11,op=.7))
arrow(b,xs[0]+pw+8,py+ph/2,xs[1]-8); arrow(b,xs[1]+pw+8,py+ph/2,xs[2]-8)
open('images/fig-ic.svg','w').write(svg(W,H,"Diagram in three steps: lines drawn in Rhino, a building generated from the standard timber panel system, and a dashboard estimating embodied carbon and cost",b))

# ---------- Census to street: calmer first panel ----------
W,H=720,320; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
random.seed(5)
blds=[(30+c*34+random.uniform(0,6),70+r*34+random.uniform(0,6),random.choice([20,24,26]),random.choice([18,22,26]),random.random()) for r in range(4) for c in range(4)]
def panel(ox,title,sub,mode):
    b.append(f'<g transform="translate({ox} 0)">')
    b.append(f'<rect x="20" y="60" width="160" height="150" fill="#fff" stroke="{LINE}" stroke-width=".8"/>')
    for (x,y,w,h,v) in blds:
        if mode==0: b.append(f'<rect x="{x-10}" y="{y-10}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width=".5" stroke-opacity=".35"/>')
        if mode==1: b.append(f'<rect x="{x-10}" y="{y-10}" width="{w}" height="{h}" fill="{ACC}" fill-opacity="{.12+.6*v:.2f}" stroke="{INK}" stroke-width=".5" stroke-opacity=".5"/>')
        if mode==2: b.append(f'<rect x="{x-10}" y="{y-10}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width=".5" stroke-opacity=".35"/>')
    if mode==0:
        b.append(f'<rect x="26" y="66" width="148" height="138" fill="none" stroke="{ACC}" stroke-width="1" stroke-dasharray="5 3"/>')
        b.append(f'<rect x="58" y="120" width="84" height="30" fill="#fff" stroke="{ACC}" stroke-width=".8"/>')
        b.append(T(100,134,"One total",a="middle",s=10,w=600,fill=ACC)); b.append(T(100,146,"for the whole area",a="middle",s=9,op=.7))
    if mode==2:
        for k,yy in enumerate([84,118,152,186]):
            b.append(f'<line x1="20" y1="{yy}" x2="180" y2="{yy}" stroke="{ACC}" stroke-width="{1+((k*7)%5)*.7:.1f}" stroke-opacity=".75"/>')
        for k,xx in enumerate([48,82,116,150]):
            b.append(f'<line x1="{xx}" y1="60" x2="{xx}" y2="210" stroke="{ACC}" stroke-width="{.8+((k*3)%4)*.6:.1f}" stroke-opacity=".55"/>')
    b.append(T(20,240,title,s=14,w=700)); b.append(T(20,258,sub,s=12,op=.7))
    b.append('</g>')
panel(0,"Census counts","Residents and workers per area",0)
panel(250,"Split to buildings","By size and use",1)
panel(500,"Activity on the street","The “buzz metric”",2)
for ax in (200,450): arrow(b,ax+6,135,ax+64)
b.append(T(20,34,"FROM CENSUS COUNTS TO STREET-LEVEL ACTIVITY",s=11,w=600,op=.6,ls=1))
open('images/fig-ped.svg','w').write(svg(W,H,"Diagram: census counts for an area are split across its buildings by size and use, then turned into estimated activity on each street",b))
print("ok")
