# Buzz metric: one 3x3 block grid, numbers carried through all three steps.
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
W,H=720,360; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
people=[[60,180,40],[120,420,90],[30,150,110]]     # per block, sums to 1,200
tot=sum(map(sum,people))
cell,st=44,10        # block size, street width
def panel(ox,oy,mode):
    size=3*cell+4*st
    b.append(f'<rect x="{ox}" y="{oy}" width="{size}" height="{size}" fill="#fff" stroke="{LINE}" stroke-width=".6"/>')
    # streets
    for k in range(4):
        p=ox+k*(cell+st)
        b.append(f'<rect x="{p}" y="{oy}" width="{st}" height="{size}" fill="#F1EEE8"/>')
        b.append(f'<rect x="{ox}" y="{oy+k*(cell+st)}" width="{size}" height="{st}" fill="#F1EEE8"/>')
    if mode==2:
        # street activity = neighbors' people; draw each street segment
        def seg(x1,y1,x2,y2,v):
            o=min(1,v/700)
            b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACC}" stroke-width="{st-3}" stroke-opacity="{.12+.8*o:.2f}"/>')
        for r in range(3):
            for k in range(4):   # vertical street segments beside row r
                v=sum(people[r][c] for c in (k-1,k) if 0<=c<3)
                x=ox+k*(cell+st)+st/2; y1=oy+st+r*(cell+st); seg(x,y1,x,y1+cell,v)
        for c in range(3):
            for k in range(4):   # horizontal segments beside column c
                v=sum(people[r][c] for r in (k-1,k) if 0<=r<3)
                y=oy+k*(cell+st)+st/2; x1=ox+st+c*(cell+st); seg(x1,y,x1+cell,y,v)
    for r in range(3):
        for c in range(3):
            x=ox+st+c*(cell+st); y=oy+st+r*(cell+st); v=people[r][c]
            if mode==0:
                b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="none" stroke="{INK}" stroke-width=".5" stroke-opacity=".35"/>')
            elif mode==1:
                b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{ACC}" fill-opacity="{.08+.6*v/420:.2f}" stroke="{INK}" stroke-width=".5" stroke-opacity=".5"/>')
                b.append(T(x+cell/2,y+cell/2+4,str(v),a="middle",s=11,w=600))
            else:
                b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="#fff" stroke="{INK}" stroke-width=".5" stroke-opacity=".35"/>')
    if mode==0:
        b.append(f'<rect x="{ox+4}" y="{oy+4}" width="{size-8}" height="{size-8}" fill="none" stroke="{ACC}" stroke-width="1" stroke-dasharray="5 3"/>')
        b.append(f'<rect x="{ox+size/2-44}" y="{oy+size/2-18}" width="88" height="36" fill="#fff" stroke="{ACC}" stroke-width=".8"/>')
        b.append(T(ox+size/2,oy+size/2-1,f"{tot:,}",a="middle",s=14,w=700,fill=ACC))
        b.append(T(ox+size/2,oy+size/2+12,"people, one area",a="middle",s=9,op=.7))
    return size
xs=[30,270,510]; oy=60
for i,x in enumerate(xs): size=panel(x,oy,i)
titles=[("1. One census count",f"{tot:,} residents and workers for the whole area"),
        ("2. Split to buildings","The numbers still add up"),
        ("3. Estimate foot traffic","From the residents and workers in each building")]
for x,(t,sub) in zip(xs,titles):
    b.append(T(x,oy+size+28,t,s=13,w=700)); b.append(T(x,oy+size+45,sub,s=10,op=.7))
for x in xs[:2]:
    a=x+size+14; c=x+240-14
    b.append(f'<line x1="{a}" y1="{oy+size/2}" x2="{c-6}" y2="{oy+size/2}" stroke="{INK}" stroke-width=".7"/><path d="M{c} {oy+size/2} l-7 -3.5 v7 z" fill="{INK}"/>')
b.append(f'<defs><linearGradient id="bz"><stop offset="0" stop-color="{ACC}" stop-opacity=".12"/><stop offset="1" stop-color="{ACC}" stop-opacity=".92"/></linearGradient></defs>')
b.append(f'<rect x="{xs[2]}" y="{oy+size+58}" width="100" height="6" fill="url(#bz)"/>')
b.append(T(xs[2],oy+size+78,"Quiet",s=9,op=.6)); b.append(T(xs[2]+100,oy+size+78,"Busy",a="end",s=9,op=.6))
b.append(T(30,34,"THE BUZZ METRIC: FROM CENSUS COUNTS TO AN ESTIMATE OF PEDESTRIAN ACTIVITY",s=11,w=600,op=.6,ls=1))
b.append(T(30,H-12,"Illustrative numbers",s=9,op=.5))
open('images/fig-ped.svg','w').write(f'<svg data-thinned="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Diagram in three steps: one census count of 1,200 people for an area is split across nine blocks, then each street segment is shaded by the people in the blocks beside it">'+"\n".join(b)+'</svg>')
print("ok")
