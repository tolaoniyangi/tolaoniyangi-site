# Intelligent City: line -> continuous generated building -> floor plan -> data + dashboard.
import math
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
W,H=720,380; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
pw,ph,py=160,230,50; xs=[10,190,370,550]
for x in xs: b.append(f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" fill="#fff" stroke="{LINE}" stroke-width=".6"/>')

P=[(0,6),(34,40),(76,52),(112,36),(126,0)]       # four segments, gentle bends; the convex front faces the viewer
wbar=16
def offset(P,w):
    """Left offset of a polyline with mitered joints."""
    out=[]
    for i,(x,y) in enumerate(P):
        ns=[]
        for j in (i-1,i):
            if 0<=j<len(P)-1:
                (ax,ay),(bx,by)=P[j],P[j+1]; L=math.hypot(bx-ax,by-ay); ns.append((-(by-ay)/L,(bx-ax)/L))
        nx=sum(n[0] for n in ns); ny=sum(n[1] for n in ns); m=math.hypot(nx,ny); nx,ny=nx/m,ny/m
        cos=nx*ns[0][0]+ny*ns[0][1]
        out.append((x+nx*w/cos,y+ny*w/cos))
    return out
R=P; Lf=offset(P,wbar)

# 1. the line
s1=1.0; ox,oy=xs[0]+16,py+46
b.append('<polyline points="'+" ".join(f"{ox+x*s1:.1f},{oy+y*s1:.1f}" for x,y in P)+f'" fill="none" stroke="{ACC}" stroke-width="1.2"/>')
for x,y in P: b.append(f'<rect x="{ox+x*s1-2.5:.1f}" y="{oy+y*s1-2.5:.1f}" width="5" height="5" fill="#fff" stroke="{ACC}" stroke-width=".7"/>')

# 2. continuous building, extruded from the mitered footprint
def iso(x,y,z,ox,oy,s=0.66): return (ox+(x-y)*0.866*s, oy+(x+y)*0.5*s - z*s)
ox2,oy2=xs[1]+44,py+128
nf=9; gfh=12; fh=8.5; hgt=gfh+(nf-1)*fh
foot=R+Lf[::-1]                                   # closed outline
edges=[]
for k in range(len(foot)):
    p1,p2=foot[k],foot[(k+1)%len(foot)]
    edges.append((p1,p2))
cx=sum(p[0] for p in foot)/len(foot); cy=sum(p[1] for p in foot)/len(foot)
area=sum(foot[k][0]*foot[(k+1)%len(foot)][1]-foot[(k+1)%len(foot)][0]*foot[k][1] for k in range(len(foot)))
vis=[]
for p1,p2 in edges:
    ex,ey=p2[0]-p1[0],p2[1]-p1[1]
    onx,ony=(ey,-ex) if area>0 else (-ey,ex)        # outward normal for this winding
    if onx+ony>0: vis.append((p1,p2,onx,ony))
vis.sort(key=lambda e:(e[0][0]+e[0][1]+e[1][0]+e[1][1]))
def P2(pts): return "M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+" Z"
for p1,p2,onx,ony in vis:
    q=[iso(*p1,0,ox2,oy2),iso(*p2,0,ox2,oy2),iso(*p2,hgt,ox2,oy2),iso(*p1,hgt,ox2,oy2)]
    b.append(f'<path d="{P2(q)}" fill="{"#F8F6F2" if onx>ony else "#ECE8E1"}" stroke="{INK}" stroke-width=".6"/>')
    g=[iso(*p1,0,ox2,oy2),iso(*p2,0,ox2,oy2),iso(*p2,gfh,ox2,oy2),iso(*p1,gfh,ox2,oy2)]
    b.append(f'<path d="{P2(g)}" fill="{INK}" fill-opacity=".22"/>')
    (u1,v1),(u2,v2)=iso(*p1,hgt-3,ox2,oy2),iso(*p2,hgt-3,ox2,oy2)
    b.append(f'<line x1="{u1:.1f}" y1="{v1:.1f}" x2="{u2:.1f}" y2="{v2:.1f}" stroke="{INK}" stroke-width=".4" stroke-opacity=".7"/>')
    for f_ in range(1,nf-1):
        (u1,v1),(u2,v2)=iso(*p1,gfh+f_*fh,ox2,oy2),iso(*p2,gfh+f_*fh,ox2,oy2)
        b.append(f'<line x1="{u1:.1f}" y1="{v1:.1f}" x2="{u2:.1f}" y2="{v2:.1f}" stroke="{INK}" stroke-width=".3" stroke-opacity=".4"/>')
    L_=math.hypot(p2[0]-p1[0],p2[1]-p1[1]); steps=max(1,int(L_/9))
    for t in range(1,steps):
        xx,yy=p1[0]+(p2[0]-p1[0])*t/steps,p1[1]+(p2[1]-p1[1])*t/steps
        (u1,v1),(u2,v2)=iso(xx,yy,gfh,ox2,oy2),iso(xx,yy,hgt,ox2,oy2)
        b.append(f'<line x1="{u1:.1f}" y1="{v1:.1f}" x2="{u2:.1f}" y2="{v2:.1f}" stroke="{INK}" stroke-width=".3" stroke-opacity=".45"/>')
b.append(f'<path d="{P2([iso(x,y,hgt,ox2,oy2) for x,y in foot])}" fill="#fff" stroke="{INK}" stroke-width=".7"/>')

# 3. a typical floor: same footprint, corridor and units
s3=1.0; ox3,oy3=xs[2]+16,py+46
b.append(f'<path d="{P2([(ox3+x*s3,oy3+y*s3) for x,y in foot])}" fill="#F6F4EF" stroke="{INK}" stroke-width=".8"/>')
mid=offset(P,wbar/2)
b.append('<polyline points="'+" ".join(f"{ox3+x*s3:.1f},{oy3+y*s3:.1f}" for x,y in mid)+f'" fill="none" stroke="{INK}" stroke-width=".4" stroke-dasharray="2 2"/>')
for i in range(4):
    (ax,ay),(bx_,by_)=R[i],R[i+1]; (lax,lay),(lbx,lby)=Lf[i],Lf[i+1]
    n=max(1,int(math.hypot(bx_-ax,by_-ay)/8))
    for k in range(1,n):
        t=k/n
        x1,y1=ax+(bx_-ax)*t,ay+(by_-ay)*t; x2,y2=lax+(lbx-lax)*t,lay+(lby-lay)*t
        b.append(f'<line x1="{ox3+x1*s3:.1f}" y1="{oy3+y1*s3:.1f}" x2="{ox3+x2*s3:.1f}" y2="{oy3+y2*s3:.1f}" stroke="{INK}" stroke-width=".4" stroke-opacity=".7"/>')
        for cxp,cyp in ((x1,y1),(x2,y2)):
            b.append(f'<rect x="{ox3+cxp*s3-1.6:.1f}" y="{oy3+cyp*s3-1.6:.1f}" width="3.2" height="3.2" fill="{INK}"/>')
    if i==1:
        t0,t1=1/n,2/n
        u=[(ax+(bx_-ax)*t0,ay+(by_-ay)*t0),(ax+(bx_-ax)*t1,ay+(by_-ay)*t1)]
        m=[(mid[i][0]+(mid[i+1][0]-mid[i][0])*t1,mid[i][1]+(mid[i+1][1]-mid[i][1])*t1),(mid[i][0]+(mid[i+1][0]-mid[i][0])*t0,mid[i][1]+(mid[i+1][1]-mid[i][1])*t0)]
        b.append(f'<path d="{P2([(ox3+x*s3,oy3+y*s3) for x,y in u+m])}" fill="{ACC}" fill-opacity=".5"/>')
# stair and elevator core at the second joint
(jx,jy),(lx_,ly_)=R[2],Lf[2]
core=[(jx-4,jy+1),(jx+5,jy+2),(lx_+5,ly_+2),(lx_-4,ly_+1)]
b.append(f'<path d="{P2([(ox3+x*s3,oy3+y*s3) for x,y in core])}" fill="{INK}" fill-opacity=".55"/>')
# legend
lg=py+150
b.append(f'<rect x="{xs[2]+16}" y="{lg}" width="3.2" height="3.2" fill="{INK}"/>'+T(xs[2]+26,lg+4,"Timber columns",s=9,op=.75))
b.append(f'<rect x="{xs[2]+15}" y="{lg+12}" width="6" height="5" fill="{INK}" fill-opacity=".55"/>'+T(xs[2]+26,lg+17,"Stair and elevator core",s=9,op=.75))
b.append(f'<rect x="{xs[2]+15}" y="{lg+25}" width="6" height="5" fill="{ACC}" fill-opacity=".5"/>'+T(xs[2]+26,lg+30,"One unit, from standard panels",s=9,op=.75))


# 4. data + dashboard
x4=xs[3]
for j,(t,sub) in enumerate([("Building data","Areas, units, materials"),("Other data","Costs, carbon factors")]):
    yy=py+16+j*42
    b.append(f'<rect x="{x4+12}" y="{yy}" width="{pw-24}" height="32" fill="#F6F4EF" stroke="{LINE}" stroke-width=".6"/>')
    b.append(T(x4+20,yy+14,t,s=10,w=700)); b.append(T(x4+20,yy+26,sub,s=9,op=.6))
b.append(f'<line x1="{x4+pw/2}" y1="{py+100}" x2="{x4+pw/2}" y2="{py+114}" stroke="{INK}" stroke-width=".7"/><path d="M{x4+pw/2} {py+120} l-3.5 -7 h7 z" fill="{INK}"/>')
dy0=py+124
b.append(f'<rect x="{x4+12}" y="{dy0}" width="{pw-24}" height="92" fill="#fff" stroke="{INK}" stroke-width=".7"/>')
b.append(T(x4+20,dy0+14,"Dashboard",s=10,w=700))
b.append(T(x4+20,dy0+30,"Embodied carbon",s=8,op=.7))
for k,(wd,o) in enumerate([(40,.35),(64,.55),(24,.8)]):
    b.append(f'<rect x="{x4+20+sum([40,64,24][:k])}" y="{dy0+34}" width="{wd}" height="7" fill="{ACC}" fill-opacity="{o}"/>')
b.append(T(x4+20,dy0+54,"Cost",s=8,op=.7))
cx_,cy_,r=x4+44,dy0+72,12
b.append(f'<circle cx="{cx_}" cy="{cy_}" r="{r}" fill="none" stroke="{LINE}" stroke-width="5"/>')
b.append(f'<circle cx="{cx_}" cy="{cy_}" r="{r}" fill="none" stroke="{INK}" stroke-opacity=".6" stroke-width="5" stroke-dasharray="{2*math.pi*r*.62:.1f} 200" transform="rotate(-90 {cx_} {cy_})"/>')
for k in range(3):
    b.append(f'<rect x="{x4+68}" y="{dy0+62+k*8}" width="{50-k*12}" height="4" fill="{INK}" fill-opacity=".3"/>')
titles=[("1. Draw a line","A quick gesture, not a plan"),("2. Generate the building","Parametric building generation"),("3. Floor plans, laid out","Structure and cores factored in"),("4. Extract the data","Into a carbon and cost dashboard")]
for x,(t,sub) in zip(xs,titles):
    b.append(T(x,py+ph+28,t,s=12,w=700)); b.append(T(x,py+ph+45,sub,s=10,op=.7))
for x in xs[:3]:
    a=x+pw+4; c=x+pw+16
    b.append(f'<line x1="{a}" y1="{py+ph/2}" x2="{c-5}" y2="{py+ph/2}" stroke="{INK}" stroke-width=".7"/><path d="M{c} {py+ph/2} l-6 -3 v6 z" fill="{INK}"/>')
b.append(T(10,32,"FROM ONE LINE TO A COSTED BUILDING",s=11,w=600,op=.6,ls=1))
open('images/fig-ic.svg','w').write(f'<svg data-thinned="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Diagram in four steps: a line with four segments is drawn; the generator extrudes it into one continuous nine-storey building that follows the line; each floor plan is laid out with units from the panel system; the building data and other data feed a carbon and cost dashboard">'+"\n".join(b)+'</svg>')
print("ok")
