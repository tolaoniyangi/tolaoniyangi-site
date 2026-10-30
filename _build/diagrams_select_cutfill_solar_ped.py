import math, random
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
def svg(W,H,label,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'+"\n".join(body)+'</svg>'

# ---------- 1. Four ways to select ----------
W,H=720,300; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
pw=156; gap=(W-40-4*pw)/3
random.seed(3); dots=[]
while len(dots)<13:
    p=(random.uniform(14,pw-14),random.uniform(14,130))
    if all((p[0]-a)**2+(p[1]-c)**2>22**2 for a,c in dots): dots.append(p)
names=[("Checkbox","in the panel"),("Drag","in the panel"),("Click","on the map"),("Marquee","on the map · new")]
for i,(n,sub) in enumerate(names):
    x0=20+i*(pw+gap); y0=34; new=i==3
    b.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="160" fill="#fff" stroke="{ACC if new else LINE}" stroke-width="{2 if new else 1}"/>')
    if i<2:
        for r in range(6):
            yy=y0+18+r*22; on=(r in (1,2) if i==0 else 1<=r<=4)
            b.append(f'<rect x="{x0+14}" y="{yy}" width="12" height="12" rx="2" fill="{ACC if on else "#fff"}" stroke="{ACC if on else MUTED}" stroke-width="1.3"/>')
            b.append(f'<rect x="{x0+34}" y="{yy+3}" width="{70+(r*23)%40}" height="6" rx="3" fill="{INK if on else LINE}" fill-opacity="{.7 if on else 1}"/>')
        if i==1:
            b.append(f'<path d="M{x0+pw-22} {y0+44} V{y0+122}" stroke="{INK}" stroke-width="1.5" marker-end="url(#ar)"/>')
    else:
        b.append(f'<g stroke="{LINE}" stroke-width="1">'+"".join(f'<line x1="{x0+xx}" y1="{y0}" x2="{x0+xx}" y2="{y0+160}"/>' for xx in range(26,pw,32))+"".join(f'<line x1="{x0}" y1="{y0+yy}" x2="{x0+pw}" y2="{y0+yy}"/>' for yy in range(24,160,32))+'</g>')
        bx,by,bw,bh=x0+30,y0+40,82,70
        for dx,dy in dots:
            px,py=x0+dx,y0+dy+8
            sel=(i==2 and abs(px-(x0+78))<1 and False) or (i==3 and bx<px<bx+bw and by<py<by+bh)
            b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{ACC if sel else "#fff"}" stroke="{"#fff" if sel else INK}" stroke-width="1.3"/>')
        if i==2:
            px,py=x0+dots[5][0],y0+dots[5][1]+8
            b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{ACC}" stroke="#fff" stroke-width="1.3"/>')
            b.append(f'<path d="M{px+2:.0f} {py+2:.0f} l0 16 l4 -4 l4 8 l3 -1.5 l-4 -8 l6 0 z" fill="{INK}" stroke="#fff" stroke-width="1"/>')
        else:
            b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{ACC}" fill-opacity=".1" stroke="{ACC}" stroke-width="1.6" stroke-dasharray="5 4"/>')
            b.append(f'<path d="M{bx+bw} {by+bh} l0 16 l4 -4 l4 8 l3 -1.5 l-4 -8 l6 0 z" fill="{INK}" stroke="#fff" stroke-width="1"/>')
    b.append(T(x0,y0+186,n,s=14,w=700,fill=ACC if new else INK))
    b.append(T(x0,y0+204,sub,s=12,op=.7))
b.insert(1,f'<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>')
b.append(T(20,22,"FOUR WAYS TO SELECT, ALL IN SYNC",s=11,w=600,op=.6,ls=1))
open('images/fig-select-modes.svg','w').write(svg(W,H,"Four ways to select in Google Earth: checkbox and drag in the panel, click and the new marquee on the map",b))

# ---------- 2. Cut and fill, plan view ----------
W,H=720,420; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
b.append(f'<defs><pattern id="h2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1.2"/></pattern><clipPath id="sheet"><rect width="560" height="420"/></clipPath><clipPath id="site"><path id="sp" d="M120 90 L430 60 L500 250 L380 360 L140 330 Z"/></clipPath></defs>')
# contours across whole sheet
for k in range(-6,9):
    pts=" ".join(f"{x},{180+k*34+28*math.sin(x/110)+12*math.sin(x/37):.1f}" for x in range(0,561,10))
    b.append(f'<polyline clip-path="url(#sheet)" points="{pts}" fill="none" stroke="{MUTED}" stroke-width="{1.4 if k%4==0 else .7}" stroke-opacity=".7"/>')
# inside site: split cut (upper-left, high ground) vs fill
b.append(f'<g clip-path="url(#site)"><path d="M0 0 H560 V0 L560 120 C 460 160, 380 140, 300 210 S 140 300, 0 260 Z" fill="{ACC}" fill-opacity=".85"/><path d="M560 120 C 460 160, 380 140, 300 210 S 140 300, 0 260 V420 H560 Z" fill="url(#h2)"/></g>')
b.append(f'<path d="M120 90 L430 60 L500 250 L380 360 L140 330 Z" fill="none" stroke="{INK}" stroke-width="2.5"/>')
for x,y in [(120,90),(430,60),(500,250),(380,360),(140,330)]:
    b.append(f'<rect x="{x-4}" y="{y-4}" width="8" height="8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
b.append(T(220,150,"CUT",s=15,w=800,ls=1.5,fill="#fff"))
b.append(T(330,300,"FILL",s=15,w=800,ls=1.5))
# legend
lx=580
b.append(T(lx,96,"Site boundary",w=600)); b.append(f'<line x1="{lx}" y1="106" x2="{lx+40}" y2="106" stroke="{INK}" stroke-width="2.5"/>')
b.append(T(lx,146,"Cut",w=600)); b.append(f'<rect x="{lx}" y="154" width="40" height="18" fill="{ACC}" fill-opacity=".85"/>')
b.append(T(lx,196,"Fill",w=600)); b.append(f'<rect x="{lx}" y="204" width="40" height="18" fill="url(#h2)" stroke="{INK}" stroke-width=".5"/>')
b.append(T(lx,246,"Contours",w=600)); b.append(f'<line x1="{lx}" y1="258" x2="{lx+40}" y2="258" stroke="{MUTED}" stroke-width="1.4"/>')
b.append(T(20,H-16,"PLAN · NOT TO SCALE",s=11,op=.6,ls=1))
open('images/fig-cutfill-plan.svg','w').write(svg(W,H,"Plan view: a drawn site boundary over contour lines, split into an area to cut and an area to fill",b))

# ---------- 3. Solar: gable roof, colored by sun, setback + HVAC only ----------
W,H=720,440; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
b.append(f'<defs><pattern id="h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{MUTED}" stroke-width="1"/></pattern></defs>')
x0,y0,x1,y1=80,60,540,380; sb=24; ry=(y0+y1)//2
b.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#F6F4EF" stroke="{INK}" stroke-width="2"/>')
b.append(f'<path d="M{x0} {y0}H{x1}V{y1}H{x0}Z M{x0+sb} {y0+sb}V{y1-sb}H{x1-sb}V{y0+sb}Z" fill="url(#h)" fill-rule="evenodd"/>')
b.append(f'<line x1="{x0}" y1="{ry}" x2="{x1}" y2="{ry}" stroke="{INK}" stroke-width="1.5"/>')
hv=[(350,ry+30,74,54),(170,ry-100,56,44)]; buf=10
for x,y,w,h in hv:
    b.append(f'<rect x="{x-buf}" y="{y-buf}" width="{w+2*buf}" height="{h+2*buf}" fill="none" stroke="{MUTED}" stroke-dasharray="3 3"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width="1.5"/><line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="{INK}"/><line x1="{x+w}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{INK}"/>')
pw,ph,g=36,20,4
def ok(x,y):
    if not(x0+sb+4<=x and x+pw<=x1-sb-4 and y0+sb+4<=y and y+ph<=y1-sb-4): return False
    if not (y+ph<ry-4 or y>ry+4): return False
    for hx,hy,hw,hh in hv:
        if x<hx+hw+buf and x+pw>hx-buf and y<hy+hh+buf and y+ph>hy-buf: return False
    return True
for y in list(range(ry+8,y1,ph+g))+list(range(ry-8-ph,y0,-(ph+g))):
    for x in range(x0+sb+6,x1,pw+g):
        if ok(x,y):
            sunny=y>ry
            b.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="{ACC}" fill-opacity="{1 if sunny else .45}" stroke="#fff" stroke-width="1"/>')
def call(px,py,tx,ty,t):
    b.append(f'<line x1="{px}" y1="{py}" x2="{tx-6}" y2="{ty-4}" stroke="{INK}" stroke-width="1"/><circle cx="{px}" cy="{py}" r="2.5" fill="{INK}"/>')
    b.append(T(tx,ty,t,w=600))
call(x1-sb/2,y0+70,572,110,"Fire-code setback")
call(424,ry+57,572,250,"HVAC clearance")
b.append(T(572,316,"Panels",w=600))
b.append(f'<rect x="572" y="326" width="36" height="20" fill="{ACC}"/><rect x="614" y="326" width="36" height="20" fill="{ACC}" fill-opacity=".45"/>')
b.append(T(572,366,"Sunnier",s=11,op=.7)); b.append(T(614,366,"Shadier",s=11,op=.7))
b.append(T(20,H-16,"ROOF PLAN · NOT TO SCALE",s=11,op=.6,ls=1))
open('images/fig-solar.svg','w').write(svg(W,H,"Roof plan: panels fill both roof planes, darker on the sunnier side, keeping clear of the fire-code setback and HVAC units",b))

# ---------- 4. Pedestrian method: block group -> buildings -> street ----------
W,H=720,320; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
random.seed(5)
blds=[(30+c*34+random.uniform(0,6),70+r*34+random.uniform(0,6),random.choice([20,24,26]),random.choice([18,22,26]),random.random()) for r in range(4) for c in range(4)]
def panel(ox,title,sub,mode):
    b.append(f'<g transform="translate({ox} 0)">')
    b.append(f'<rect x="20" y="60" width="160" height="150" fill="#fff" stroke="{LINE}"/>')
    if mode==0:
        b.append(f'<rect x="20" y="60" width="160" height="150" fill="{ACC}" fill-opacity=".35"/>')
        b.append(T(100,142,"1,840",a="middle",s=22,w=800)); b.append(T(100,160,"people",a="middle",s=11,op=.7))
    for (x,y,w,h,v) in blds:
        if mode==0: b.append(f'<rect x="{x-10}" y="{y-10}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-opacity=".25"/>')
        if mode==1: b.append(f'<rect x="{x-10}" y="{y-10}" width="{w}" height="{h}" fill="{ACC}" fill-opacity="{.15+.8*v:.2f}" stroke="{INK}" stroke-width=".8"/>')
        if mode==2: b.append(f'<rect x="{x-10}" y="{y-10}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-opacity=".4"/>')
    if mode==2:
        for k,(yy) in enumerate([84,118,152,186]):
            b.append(f'<line x1="20" y1="{yy}" x2="180" y2="{yy}" stroke="{ACC}" stroke-width="{2+((k*7)%5)*1.4}" stroke-opacity=".8"/>')
        for k,xx in enumerate([48,82,116,150]):
            b.append(f'<line x1="{xx}" y1="60" x2="{xx}" y2="210" stroke="{ACC}" stroke-width="{1.5+((k*3)%4)*1.2}" stroke-opacity=".6"/>')
    b.append(T(20,240,title,s=14,w=700)); b.append(T(20,258,sub,s=12,op=.7))
    b.append('</g>')
panel(0,"Census block group","One count for the whole area",0)
panel(250,"Split to buildings","By size and use",1)
panel(500,"Activity on the street","The “buzz metric”",2)
for ax in (200,450):
    b.append(f'<line x1="{ax+6}" y1="135" x2="{ax+56}" y2="135" stroke="{INK}" stroke-width="1.5"/><path d="M{ax+64} 135 l-10 -5 v10 z" fill="{INK}"/>')
b.append(T(20,34,"FROM CENSUS COUNTS TO STREET-LEVEL ACTIVITY",s=11,w=600,op=.6,ls=1))
b.append(T(20,H-14,"Illustrative numbers",s=10,op=.5))
open('images/fig-ped.svg','w').write(svg(W,H,"Diagram: one census count for an area is split across its buildings, then turned into estimated activity on each street",b))
print("ok")
