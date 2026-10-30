import random
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
def svg(W,H,label,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'+"\n".join(body)+'</svg>'
def arrow(b,x1,y1,x2,y2): b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2-8}" y2="{y2}" stroke="{INK}" stroke-width="1.5"/><path d="M{x2} {y2} l-10 -5 v10 z" fill="{INK}"/>')

# ---------- Intelligent City: inputs -> generator -> forms -> data ----------
W,H=720,420; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
b.append(T(20,30,"FROM RULES TO BUILDINGS TO NUMBERS",s=11,w=600,op=.6,ls=1))
for i,(t,sub) in enumerate([("Site","Lot, zoning"),("Program","Units, mix"),("Timber system","What the factory makes")]):
    y=80+i*92
    b.append(f'<rect x="20" y="{y}" width="140" height="62" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
    b.append(T(32,y+26,t,s=13,w=700)); b.append(T(32,y+44,sub,s=11,op=.7))
    b.append(f'<line x1="160" y1="{y+31}" x2="196" y2="210" stroke="{INK}" stroke-opacity=".35"/>')
arrow(b,196,210,214,210)
# generator: grid of massings (iso boxes)
gx,gy=218,70
b.append(f'<rect x="{gx}" y="{gy}" width="250" height="280" fill="#fff" stroke="{ACC}" stroke-width="2"/>')
b.append(T(gx+12,gy+24,"Parametric generator",s=13,w=700,fill=ACC))
random.seed(9)
def box(x,y,w,d,h,hl):
    # simple isometric extrusion
    dx,dy=d*0.6,d*0.35
    top=f"M{x} {y-h} l{w} 0 l{dx} {-dy} l{-w} 0 z"
    side=f"M{x+w} {y-h} l{dx} {-dy} l0 {h} l{-dx} {dy} z"
    front=f"M{x} {y-h} h{w} v{h} h{-w} z"
    fill=ACC if hl else "#F6F4EF"
    return (f'<path d="{front}" fill="{fill}" fill-opacity="{.9 if hl else 1}" stroke="{INK}" stroke-width=".8"/>'
            f'<path d="{side}" fill="{fill}" fill-opacity="{.6 if hl else .55}" stroke="{INK}" stroke-width=".8"/>'
            f'<path d="{top}" fill="#fff" stroke="{INK}" stroke-width=".8"/>')
for r in range(3):
    for c in range(3):
        x=gx+26+c*76; y=gy+104+r*70
        hl=(r,c)==(1,1)
        w=random.choice([26,32,38]); h=random.choice([26,36,46,54]); d=random.choice([18,24])
        b.append(box(x,y,w,d,h,hl))
        if random.random()<.5: b.append(box(x+w-4,y+4,16,d,h*0.5,hl))
b.append(T(gx+12,gy+268,"200% more forms it could produce",s=11,op=.75))
arrow(b,gx+250,210,gx+290,210)
# data card -> dashboard
dx0=gx+296
b.append(f'<rect x="{dx0}" y="96" width="186" height="226" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
b.append(T(dx0+12,120,"Every design, measured",s=13,w=700))
for i,(k,v) in enumerate([("Timber","m³"),("Steel","t"),("Concrete","m³"),("Cost","$"),("Emissions","tCO₂e")]):
    y=146+i*30
    b.append(f'<line x1="{dx0}" y1="{y-16}" x2="{dx0+186}" y2="{y-16}" stroke="{LINE}"/>')
    b.append(T(dx0+12,y,k,s=12)); b.append(f'<rect x="{dx0+96}" y="{y-9}" width="{26+(i*13)%30}" height="8" rx="4" fill="{ACC if k in ("Cost","Emissions") else INK}" fill-opacity="{.85 if k in ("Cost","Emissions") else .3}"/>')
    b.append(T(dx0+176,y,v,a="end",s=10,op=.6))
b.append(T(dx0+12,310,"→ client dashboard",s=12,w=600))
open('images/fig-ic.svg','w').write(svg(W,H,"Diagram: site, program and the timber system feed a parametric generator that produces many building forms; each design is measured for materials, cost and emissions and shown in a client dashboard",b))

# ---------- Four ways to select (corrected) ----------
W,H=720,300; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
b.insert(0,'')
b.append(f'<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>')
pw=156; gap=(W-40-4*pw)/3
random.seed(3); dots=[]
while len(dots)<13:
    p=(random.uniform(14,pw-14),random.uniform(14,130))
    if all((p[0]-a)**2+(p[1]-c)**2>22**2 for a,c in dots): dots.append(p)
def rows(x0,y0,mode):
    for r in range(6):
        yy=y0+18+r*22
        if mode=="check":
            on=r in (1,2)
            b.append(f'<rect x="{x0+14}" y="{yy}" width="12" height="12" rx="2" fill="{ACC if on else "#fff"}" stroke="{ACC if on else MUTED}" stroke-width="1.3"/>')
            b.append(f'<rect x="{x0+34}" y="{yy+3}" width="{70+(r*23)%40}" height="6" rx="3" fill="{INK if on else LINE}" fill-opacity="{.7 if on else 1}"/>')
        else:
            on=1<=r<=4 if mode=="drag" else r==2
            if on: b.append(f'<rect x="{x0+8}" y="{yy-4}" width="{pw-16}" height="20" fill="{ACC}" fill-opacity=".14"/>')
            b.append(f'<rect x="{x0+16}" y="{yy+3}" width="{80+(r*23)%40}" height="6" rx="3" fill="{INK if on else LINE}" fill-opacity="{.7 if on else 1}"/>')
def mapbg(x0,y0):
    b.append(f'<g stroke="{LINE}" stroke-width="1">'+"".join(f'<line x1="{x0+xx}" y1="{y0}" x2="{x0+xx}" y2="{y0+160}"/>' for xx in range(26,pw,32))+"".join(f'<line x1="{x0}" y1="{y0+yy}" x2="{x0+pw}" y2="{y0+yy}"/>' for yy in range(24,160,32))+'</g>')
def cursor(x,y): b.append(f'<path d="M{x} {y} l0 16 l4 -4 l4 8 l3 -1.5 l-4 -8 l6 0 z" fill="{INK}" stroke="#fff" stroke-width="1"/>')
names=[("Checkbox","in the panel"),("Click","in the panel or on the map"),("Drag","in the panel"),("Marquee","on the map · new")]
for i,(n,sub) in enumerate(names):
    x0=20+i*(pw+gap); y0=34; new=i==3
    b.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="160" fill="#fff" stroke="{ACC if new else LINE}" stroke-width="{2 if new else 1}"/>')
    if i==0: rows(x0,y0,"check")
    if i==2:
        rows(x0,y0,"drag"); b.append(f'<path d="M{x0+pw-22} {y0+40} V{y0+118}" stroke="{INK}" stroke-width="1.5" marker-end="url(#ar)"/>')
    if i==1:
        b.append(f'<line x1="{x0+pw/2}" y1="{y0}" x2="{x0+pw/2}" y2="{y0+160}" stroke="{LINE}"/>')
        for r in range(6):
            yy=y0+18+r*22; on=r==2
            if on: b.append(f'<rect x="{x0+4}" y="{yy-4}" width="{pw/2-8}" height="20" fill="{ACC}" fill-opacity=".14"/>')
            b.append(f'<rect x="{x0+10}" y="{yy+3}" width="{40+(r*13)%22}" height="6" rx="3" fill="{INK if on else LINE}" fill-opacity="{.7 if on else 1}"/>')
        for k,(dx,dy) in enumerate(dots[:6]):
            px=x0+pw/2+8+(dx%(pw/2-16)); py=y0+16+dy
            on=k==2
            b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{ACC if on else "#fff"}" stroke="{"#fff" if on else INK}" stroke-width="1.3"/>')
            if on: cursor(px+2,py+2)
    if i==3:
        mapbg(x0,y0); bx,by,bw,bh=x0+30,y0+40,82,70
        for dx,dy in dots:
            px,py=x0+dx,y0+dy+8; sel=bx<px<bx+bw and by<py<by+bh
            b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{ACC if sel else "#fff"}" stroke="{"#fff" if sel else INK}" stroke-width="1.3"/>')
        b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{ACC}" fill-opacity=".1" stroke="{ACC}" stroke-width="1.6" stroke-dasharray="5 4"/>')
        cursor(bx+bw,by+bh)
    b.append(T(x0,y0+186,n,s=14,w=700,fill=ACC if new else INK))
    b.append(T(x0,y0+204,sub,s=12,op=.7))
b.append(T(20,22,"FOUR WAYS TO SELECT, ALL IN SYNC",s=11,w=600,op=.6,ls=1))
open('images/fig-select-modes.svg','w').write(svg(W,H,"Four ways to select in Google Earth: checkbox in the panel, click in the panel or on the map, drag in the panel, and the new marquee on the map",b))
print("ok")
