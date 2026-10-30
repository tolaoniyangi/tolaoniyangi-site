# Animated traffic diagram: intersections change grade through the day.
INK="#141413"; PAPER="#EAE6DE"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
cols=["#F1E6DA","#F2C9A8","#EE9E73","#B5381B"]   # A, B, C-D, E-F
hours=list(range(6,23)); N=len(hours); DUR=10   # seconds per day
rush=[0.15,0.55,1.0,0.7,0.4,0.3,0.3,0.35,0.35,0.4,0.5,0.75,1.0,0.8,0.45,0.25,0.15]
gx=[70,160,250,340,430]; gy=[70,150,230,310]
def base(x,y):
    b=0.25
    if y==150: b=1.0                         # main street
    if x==250: b=max(b,0.65)                 # cross street
    return b
def level(v): return 0 if v<0.2 else 1 if v<0.42 else 2 if v<0.7 else 3
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 440" role="img" aria-label="Animation: a street grid through one day. Intersections on the main street turn from A to F during the morning and evening rush.">']
css=["svg *{animation-duration:%ds;animation-iteration-count:infinite;animation-timing-function:steps(1,end)}"%DUR]
body=[]
body.append(f'<rect width="720" height="440" fill="{PAPER}"/>')
for x in gx: body.append(f'<line x1="{x}" y1="30" x2="{x}" y2="350" stroke="#fff" stroke-width="8"/>')
for y in gy: body.append(f'<line x1="30" y1="{y}" x2="470" y2="{y}" stroke="#fff" stroke-width="8"/>')
body.append(f'<line x1="30" y1="150" x2="470" y2="150" stroke="#fff" stroke-width="16"/>')
body.append(f'<text x="470" y="140" text-anchor="end" {F} font-size="11" fill="{INK}" fill-opacity=".6">Main street</text>')
k=0
for x in gx:
    for y in gy:
        seq=[level(base(x,y)*r*1.05) for r in rush]
        frames=" ".join(f"{i*100/N:.3f}%{{fill:{cols[s]}}}" for i,s in enumerate(seq))
        css.append(f"@keyframes c{k}{{{frames}}} .c{k}{{animation-name:c{k};fill:{cols[seq[2]]}}}")
        body.append(f'<circle class="c{k}" cx="{x}" cy="{y}" r="12" stroke="#fff" stroke-width="2"/>')
        k+=1
# clock: one text per hour, shown in its slot
for i,h in enumerate(hours):
    frames=" ".join(f"{j*100/N:.3f}%{{opacity:{1 if j==i else 0}}}" for j in range(N))
    css.append(f"@keyframes t{i}{{{frames}}} .t{i}{{animation-name:t{i};opacity:{1 if i==2 else 0}}}")
    lab="Morning rush" if 7<=h<=9 else "Evening rush" if 17<=h<=19 else "&#160;"
    body.append(f'<g class="t{i}"><text x="520" y="120" {F} font-size="56" font-weight="800" fill="{INK}" letter-spacing="-1">{h:02d}:00</text><text x="522" y="148" {F} font-size="13" font-weight="600" fill="{INK}" fill-opacity=".7">{lab}</text></g>')
# legend
body.append(f'<text x="520" y="214" {F} font-size="12" font-weight="700" fill="{INK}">Delay grade</text>')
for i,(g,c) in enumerate(zip(["A","B","C–D","E–F"],cols)):
    body.append(f'<circle cx="{530+i*40}" cy="236" r="9" fill="{c}" stroke="#fff" stroke-width="1.5"/><text x="{530+i*40}" y="262" text-anchor="middle" {F} font-size="11" font-weight="600" fill="{INK}">{g}</text>')
# day strip with moving marker
sx,sy,sw=40,384,640
body.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="4" fill="#fff"/>')
for h,lab in ((6,"06:00"),(12,"12:00"),(18,"18:00"),(22,"22:00")):
    xx=sx+(h-6)/(N-1)*sw
    body.append(f'<text x="{xx:.0f}" y="{sy+26}" text-anchor="middle" {F} font-size="10" fill="{INK}" fill-opacity=".6">{lab}</text>')
frames=" ".join(f"{i*100/N:.3f}%{{transform:translateX({i/(N-1)*sw:.1f}px)}}" for i in range(N))
css.append(f"@keyframes m{{{frames}}} .m{{animation-name:m;transform:translateX({2/(N-1)*sw:.1f}px)}}")
body.append(f'<g class="m"><circle cx="{sx}" cy="{sy+2}" r="7" fill="{INK}"/></g>')
css.append("@media (prefers-reduced-motion:reduce){svg *{animation:none!important}}")
o.append("<style>"+"\n".join(css)+"</style>")
o+=body; o.append("</svg>")
open('images/fig-traffic-anim.svg','w').write("\n".join(o))
print("ok")
