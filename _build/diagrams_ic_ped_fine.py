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
for d,wd in [("M38 150 C 60 70, 120 60, 160 96 S 150 170, 104 160", 1.3),
             ("M50 172 C 90 150, 130 176, 170 150", .9),
             ("M70 84 C 86 112, 96 128, 132 136", .8)]:
    b.append(f'<path d="M{x0} 0 m0 {py}" fill="none"/><path transform="translate({x0} {py})" d="{d}" fill="none" stroke="{ACC}" stroke-width="{wd}" stroke-linecap="round"/>')
b.append(T(x0+20,py+204,"Loose, gestural curves",s=10,op=.6))
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
    t,sub=[("Draw lines in Rhino","Quick gestures, not plans"),("Generate the building","A real design from the set panel system"),("Estimate carbon and cost","Quantities pulled from every design")][i]
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
    if mode==0:
        b.append(f'<rect x="26" y="66" width="148" height="138" fill="none" stroke="{ACC}" stroke-width="1" stroke-dasharray="5 3"/>')
        b.append(f'<rect x="58" y="120" width="84" height="30" fill="#fff" stroke="{ACC}" stroke-width=".8"/>')
        b.append(T(100,134,"One total",a="middle",s=10,w=600,fill=ACC)); b.append(T(100,146,"for the whole area",a="middle",s=9,op=.7))
    if mode==2:
        xs_=[20,48,82,116,150,180]; ys_=[60,84,118,152,186,210]
        for i in range(5):
            for j in range(5):
                b.append(f'<rect x="{xs_[i]+5}" y="{ys_[j]+5}" width="{xs_[i+1]-xs_[i]-10}" height="{ys_[j+1]-ys_[j]-10}" fill="#fff" stroke="{INK}" stroke-width=".5" stroke-opacity=".35"/>')
        streets=[("h",84),("h",118),("h",152),("h",186),("v",48),("v",82),("v",116),("v",150)]
        for o,p in streets:
            if o=="h": b.append(f'<line x1="20" y1="{p}" x2="180" y2="{p}" stroke="{LINE}" stroke-width="3"/>')
            else: b.append(f'<line x1="{p}" y1="60" x2="{p}" y2="210" stroke="{LINE}" stroke-width="3"/>')
        busy=[("h",118,20,116,.85),("h",152,48,180,.6),("v",82,60,186,.75),("v",116,84,210,.45),("h",84,82,150,.3)]
        for o,p,a,c,v in busy:
            if o=="h": b.append(f'<line x1="{a}" y1="{p}" x2="{c}" y2="{p}" stroke="{ACC}" stroke-width="3" stroke-opacity="{v}"/>')
            else: b.append(f'<line x1="{p}" y1="{a}" x2="{p}" y2="{c}" stroke="{ACC}" stroke-width="3" stroke-opacity="{v}"/>')
        b.append(f'<defs><linearGradient id="busy"><stop offset="0" stop-color="{LINE}"/><stop offset="1" stop-color="{ACC}"/></linearGradient></defs>')
        b.append(f'<rect x="20" y="276" width="90" height="6" fill="url(#busy)"/>')
        b.append(T(20,296,"Quiet",s=9,op=.6)); b.append(T(110,296,"Busy",a="end",s=9,op=.6))
    b.append(T(20,240,title,s=14,w=700)); b.append(T(20,258,sub,s=12,op=.7))
    b.append('</g>')
panel(0,"Census counts","Residents and workers per area",0)
panel(250,"Split to buildings","By size and use",1)
panel(500,"Busy streets","The “buzz metric”",2)
for ax in (200,450): arrow(b,ax+6,135,ax+64)
b.append(T(20,34,"FROM CENSUS COUNTS TO STREET-LEVEL ACTIVITY",s=11,w=600,op=.6,ls=1))
open('images/fig-ped.svg','w').write(svg(W,H,"Diagram: census counts for an area are split across its buildings by size and use, then turned into estimated activity on each street",b))
print("ok")
