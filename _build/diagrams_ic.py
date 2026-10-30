# Intelligent City: line -> generated building -> floor plans -> data + dashboard (one diagram).
import math
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
W,H=720,380; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
pw,ph,py=160,230,50; xs=[10,190,370,550]
for x in xs: b.append(f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" fill="#fff" stroke="{LINE}" stroke-width=".6"/>')
P=[(0,0),(50,0),(50,32),(92,32),(92,74)]      # four-segment line, plan units
wbar=17
L=[math.dist(P[i],P[i+1]) for i in range(4)]; tot=sum(L)

# 1. the line
s1=1.25; ox,oy=xs[0]+22,py+52
pts=" ".join(f"{ox+x*s1:.1f},{oy+y*s1:.1f}" for x,y in P)
b.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.2"/>')
for x,y in P: b.append(f'<rect x="{ox+x*s1-2.5:.1f}" y="{oy+y*s1-2.5:.1f}" width="5" height="5" fill="#fff" stroke="{ACC}" stroke-width=".7"/>')
b.append(T(xs[0]+14,py+ph-14,"Four segments, drawn in Rhino",s=10,op=.6))

# 2. generated building (isometric), height rising along the line
def iso(x,y,z,ox,oy,s=0.82): return (ox+(x-y)*0.866*s, oy+(x+y)*0.5*s - z*s)
ox2,oy2=xs[1]+74,py+118
faces=[]; acc=0
for i in range(4):
    (ax,ay),(bx_,by_)=P[i],P[i+1]
    dx,dy=bx_-ax,by_-ay; n=math.hypot(dx,dy); nx,ny=-dy/n*wbar,dx/n*wbar
    za=20+(1-acc/tot)*120; acc+=L[i]; zb=20+(1-acc/tot)*120
    q=[(ax,ay,za),(bx_,by_,zb),(bx_+nx,by_+ny,zb),(ax+nx,ay+ny,za)]
    depth=max(p[0]+p[1] for p in q)
    sides=[]
    for k in range(4):
        p1,p2=q[k],q[(k+1)%4]
        ex,ey=p2[0]-p1[0],p2[1]-p1[1]; onx,ony=ey,-ex   # outward for this winding
        cx=sum(p[0] for p in q)/4; cy=sum(p[1] for p in q)/4
        mx,my=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2
        if (mx-cx)*onx+(my-cy)*ony<0: onx,ony=-onx,-ony
        if onx+ony>0: sides.append((p1,p2,onx))
    faces.append((depth,q,sides))
faces.sort(key=lambda f:f[0])
for depth,q,sides in faces:
    for p1,p2,onx in sides:
        poly=[iso(p1[0],p1[1],0,ox2,oy2),iso(p2[0],p2[1],0,ox2,oy2),iso(p2[0],p2[1],p2[2],ox2,oy2),iso(p1[0],p1[1],p1[2],ox2,oy2)]
        shade="#F6F4EF" if onx>0 else "#E9E5DD"
        b.append(f'<path d="M'+" L".join(f"{x:.1f} {y:.1f}" for x,y in poly)+f' Z" fill="{shade}" stroke="{INK}" stroke-width=".7"/>')
        for z in range(9,150,9):
            h1,h2=p1[2],p2[2]
            if z>max(h1,h2): break
            t0=0 if h1>=z else (z-h1)/(h2-h1); t1=1 if h2>=z else (z-h1)/(h2-h1)
            xa,ya=p1[0]+(p2[0]-p1[0])*t0,p1[1]+(p2[1]-p1[1])*t0
            xb,yb=p1[0]+(p2[0]-p1[0])*t1,p1[1]+(p2[1]-p1[1])*t1
            (u1,v1),(u2,v2)=iso(xa,ya,z,ox2,oy2),iso(xb,yb,z,ox2,oy2)
            b.append(f'<line x1="{u1:.1f}" y1="{v1:.1f}" x2="{u2:.1f}" y2="{v2:.1f}" stroke="{INK}" stroke-width=".4" stroke-opacity=".55"/>')
    top=[iso(x,y,z,ox2,oy2) for x,y,z in q]
    b.append(f'<path d="M'+" L".join(f"{x:.1f} {y:.1f}" for x,y in top)+f' Z" fill="#fff" stroke="{INK}" stroke-width=".7"/>')
b.append(T(xs[1]+14,py+ph-14,"Stepping down along the line",s=10,op=.6))

# 3. a typical floor, laid out: corridor + units from the panel system
s3=1.3; ox3,oy3=xs[2]+18,py+48
for i in range(4):
    (ax,ay),(bx_,by_)=P[i],P[i+1]
    dx,dy=bx_-ax,by_-ay; n=math.hypot(dx,dy); ux,uy=dx/n,dy/n; nx,ny=-uy*wbar,ux*wbar
    corners=[(ax,ay),(bx_,by_),(bx_+nx,by_+ny),(ax+nx,ay+ny)]
    b.append(f'<path d="M'+" L".join(f"{ox3+x*s3:.1f} {oy3+y*s3:.1f}" for x,y in corners)+f' Z" fill="#F6F4EF" stroke="{INK}" stroke-width=".8"/>')
    mx0,my0=ax+nx/2,ay+ny/2; mx1,my1=bx_+nx/2,by_+ny/2
    b.append(f'<line x1="{ox3+mx0*s3:.1f}" y1="{oy3+my0*s3:.1f}" x2="{ox3+mx1*s3:.1f}" y2="{oy3+my1*s3:.1f}" stroke="{INK}" stroke-width=".4" stroke-dasharray="2 2"/>')
    k=1
    while k*8<n:
        px,py_=ax+ux*k*8,ay+uy*k*8
        b.append(f'<line x1="{ox3+px*s3:.1f}" y1="{oy3+py_*s3:.1f}" x2="{ox3+(px+nx)*s3:.1f}" y2="{oy3+(py_+ny)*s3:.1f}" stroke="{INK}" stroke-width=".4" stroke-opacity=".7"/>')
        k+=1
    if i==1:
        px,py_=ax+ux*8,ay+uy*8
        u=[(px,py_),(px+ux*8,py_+uy*8),(px+ux*8+nx/2,py_+uy*8+ny/2),(px+nx/2,py_+ny/2)]
        b.append(f'<path d="M'+" L".join(f"{ox3+x*s3:.1f} {oy3+y*s3:.1f}" for x,y in u)+f' Z" fill="{ACC}" fill-opacity=".5"/>')
b.append(T(xs[2]+14,py+ph-14,"Units from the set panel system",s=10,op=.6))

# 4. data + dashboard
x4=xs[3]
for j,(t,sub) in enumerate([("Building data","Areas, units, materials"),("Other data","Costs, carbon factors")]):
    yy=py+16+j*42
    b.append(f'<rect x="{x4+12}" y="{yy}" width="{pw-24}" height="32" fill="#F6F4EF" stroke="{LINE}" stroke-width=".6"/>')
    b.append(T(x4+20,yy+14,t,s=10,w=700)); b.append(T(x4+20,yy+26,sub,s=9,op=.6))
b.append(T(x4+pw/2,py+108,"+",a="middle",s=12,op=.6) if False else "")
b.append(f'<line x1="{x4+pw/2}" y1="{py+100}" x2="{x4+pw/2}" y2="{py+114}" stroke="{INK}" stroke-width=".7"/><path d="M{x4+pw/2} {py+120} l-3.5 -7 h7 z" fill="{INK}"/>')
dy0=py+124
b.append(f'<rect x="{x4+12}" y="{dy0}" width="{pw-24}" height="92" fill="#fff" stroke="{INK}" stroke-width=".7"/>')
b.append(T(x4+20,dy0+14,"Dashboard",s=10,w=700))
b.append(T(x4+20,dy0+30,"Embodied carbon",s=8,op=.7))
for k,(wd,o) in enumerate([(40,.35),(64,.55),(24,.8)]):
    b.append(f'<rect x="{x4+20+sum([40,64,24][:k])}" y="{dy0+34}" width="{wd}" height="7" fill="{ACC}" fill-opacity="{o}"/>')
b.append(T(x4+20,dy0+54,"Cost",s=8,op=.7))
cx,cy,r=x4+44,dy0+72,12
b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="5"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-opacity=".6" stroke-width="5" stroke-dasharray="{2*math.pi*r*.62:.1f} 200" transform="rotate(-90 {cx} {cy})"/>')
for k in range(3):
    b.append(f'<rect x="{x4+68}" y="{dy0+62+k*8}" width="{50-k*12}" height="4" fill="{INK}" fill-opacity=".3"/>')
# stage titles + arrows
titles=[("1. Draw a line",""),("2. Generate the building","Parametric building generation"),("3. Floor plans, laid out","Fully resolved, floor by floor"),("4. Extract the data","Into a carbon and cost dashboard")]
titles[0]=("1. Draw a line","A quick gesture, not a plan")
for x,(t,sub) in zip(xs,titles):
    b.append(T(x,py+ph+28,t,s=12,w=700)); b.append(T(x,py+ph+45,sub,s=10,op=.7))
for x in xs[:3]:
    a=x+pw+4; c=x+pw+16
    b.append(f'<line x1="{a}" y1="{py+ph/2}" x2="{c-5}" y2="{py+ph/2}" stroke="{INK}" stroke-width=".7"/><path d="M{c} {py+ph/2} l-6 -3 v6 z" fill="{INK}"/>')
b.append(T(10,32,"FROM ONE LINE TO A COSTED BUILDING",s=11,w=600,op=.6,ls=1))
svg=f'<svg data-thinned="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Diagram in four steps: a line with four segments is drawn; the generator turns it into a building whose height rises along the line; each floor plan is laid out with units from the panel system; the building data and other data feed a carbon and cost dashboard">'+"\n".join(b)+'</svg>'
open('images/fig-ic.svg','w').write(svg); print("ok")
