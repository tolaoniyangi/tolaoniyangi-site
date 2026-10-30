INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{INK}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'

# ---- Elections: pipeline ----
W,H=720,440
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Diagram: hundreds of local election offices feed one verified dataset, which powers a voter guide used by more than 5 million voters">']
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
# column 1: many offices
cx0,cy0=40,70
for r in range(10):
    for c in range(6):
        o.append(f'<rect x="{cx0+c*24}" y="{cy0+r*28}" width="18" height="20" fill="#fff" stroke="{INK}" stroke-width="1"/><rect x="{cx0+c*24+4}" y="{cy0+r*28+5}" width="10" height="2" fill="{INK}" fill-opacity=".5"/><rect x="{cx0+c*24+4}" y="{cy0+r*28+10}" width="7" height="2" fill="{INK}" fill-opacity=".3"/>')
o.append(T(cx0,48,"Local election offices",w=700))
o.append(T(cx0,cy0+10*28+24,"Hundreds of sources, each",s=11,op=.7))
o.append(T(cx0,cy0+10*28+40,"publishing in its own format",s=11,op=.7))
# arrows
def arrow(x1,y1,x2,y2):
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2-8}" y2="{y2}" stroke="{INK}" stroke-width="1.5"/><path d="M{x2} {y2} l-10 -5 v10 z" fill="{INK}"/>')
for yy in (110,200,290):
    o.append(f'<line x1="186" y1="{yy}" x2="262" y2="{215}" stroke="{INK}" stroke-width="1" stroke-opacity=".35"/>')
arrow(262,215,286,215)
# column 2: verified table
tx,ty,tw=292,120,180
o.append(T(tx,96,"One verified dataset",w=700))
o.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="200" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
o.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="26" fill="{INK}"/>')
for i,hd in enumerate(["Location","Hours","Type"]):
    o.append(f'<text x="{tx+10+i*60}" y="{ty+17}" {F} font-size="11" font-weight="600" fill="#fff">{hd}</text>')
for r in range(7):
    y=ty+26+r*24.8
    o.append(f'<line x1="{tx}" y1="{y}" x2="{tx+tw}" y2="{y}" stroke="{LINE}"/>')
    for i,wd in enumerate([42,34,30]):
        o.append(f'<rect x="{tx+10+i*60}" y="{y+9}" width="{wd-(r*7+i*11)%14}" height="6" rx="3" fill="{INK}" fill-opacity=".25"/>')
    o.append(f'<path d="M{tx+tw-20} {y+12} l4 4 l7 -8" stroke="{ACC}" stroke-width="2" fill="none"/>')
o.append(T(tx,ty+224,"Early voting, absentee and",s=11,op=.7))
o.append(T(tx,ty+240,"polling places, checked by hand",s=11,op=.7))
arrow(tx+tw+8,215,tx+tw+44,215)
# column 3: phone
px,py=548,96
o.append(T(px,78,"Voter guide",w=700))
o.append(f'<rect x="{px}" y="{py}" width="128" height="240" rx="16" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
o.append(f'<rect x="{px+14}" y="{py+22}" width="100" height="70" fill="#EAE6DE"/>')
o.append(f'<circle cx="{px+64}" cy="{py+57}" r="9" fill="{ACC}"/>')
for i in range(4):
    o.append(f'<rect x="{px+14}" y="{py+106+i*22}" width="{100-i*14}" height="8" rx="4" fill="{INK}" fill-opacity=".25"/>')
o.append(f'<rect x="{px+14}" y="{py+196}" width="100" height="26" rx="13" fill="{ACC}"/>')
o.append(f'<text x="{px+64}" y="{py+213}" text-anchor="middle" {F} font-size="11" font-weight="600" fill="#fff">Find my polling place</text>'.replace('font-size="11"','font-size="9"'))
o.append(T(px+64,py+268,"5M+",a="middle",s=30,w=800))
o.append(T(px+64,py+288,"voters in 2020",a="middle",s=11,op=.7))
o.append('</svg>')
open('images/fig-elections.svg','w').write("\n".join(o))
print("ok")

# ---- Traffic: calmer version ----
W,H=720,440
cols={"A":"#FBF4EA","C":"#EE8A55","F":"#B5381B"}
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Street grid where each intersection is colored by its A to F delay grade; one busy corridor stands out, and one intersection’s grade is shown across the day">']
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
gx=[70,160,250,340,430]; gy=[70,150,230,310]
for x in gx: o.append(f'<line x1="{x}" y1="30" x2="{x}" y2="350" stroke="#fff" stroke-width="8"/>')
for y in gy: o.append(f'<line x1="30" y1="{y}" x2="470" y2="{y}" stroke="#fff" stroke-width="8"/>')
o.append(f'<line x1="30" y1="150" x2="470" y2="150" stroke="#fff" stroke-width="16"/>')
hot={(160,150):"F",(250,150):"F",(340,150):"C",(70,150):"C",(250,70):"C",(250,230):"C"}
hl=(250,150)
for x in gx:
    for y in gy:
        g=hot.get((x,y),"A")
        if (x,y)==hl:
            o.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{cols[g]}" stroke="{INK}" stroke-width="2.5"/>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{cols[g]}" stroke="#8A857B" stroke-width="1.5"/>')
o.append(T(30,130,"Main street",s=11,op=.6))
# legend: gradient bar A..F
o.append(f'<defs><linearGradient id="gr"><stop offset="0" stop-color="{cols["A"]}"/><stop offset=".5" stop-color="{cols["C"]}"/><stop offset="1" stop-color="{cols["F"]}"/></linearGradient></defs>')
o.append(T(520,62,"Delay grade",w=700))
o.append(f'<rect x="520" y="74" width="160" height="12" fill="url(#gr)"/>')
o.append(T(520,104,"A: short waits",s=11,op=.75))
o.append(T(680,104,"F: long waits",a="end",s=11,op=.75))
o.append(f'<line x1="{hl[0]+15}" y1="{hl[1]}" x2="514" y2="196" stroke="{INK}" stroke-width="1"/>')
o.append(T(520,200,"Follow one intersection",w=600))
o.append(T(520,216,"through the day ↓",w=600))
# day strip: 3 colors, peaks
hours=list(range(6,23)); prof="AACFCAAAAACCFFCAA"
sx,sy=40,382; cw=(680-40)/len(hours)
o.append(T(sx,sy-10,"The circled intersection, 06:00 to 22:00",s=11,w=600))
for i,(h,g) in enumerate(zip(hours,prof)):
    o.append(f'<rect x="{sx+i*cw:.1f}" y="{sy}" width="{cw-2:.1f}" height="20" fill="{cols[g]}"/>')
o.append(T(sx,sy+38,"06:00",s=10,op=.7)); o.append(T(680,sy+38,"22:00",a="end",s=10,op=.7))
o.append('</svg>')
open('images/fig-traffic.svg','w').write("\n".join(o))
print("traffic ok")
