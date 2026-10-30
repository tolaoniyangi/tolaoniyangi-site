# Airbnb analysis: two voices -> five themes -> compared borough by borough.
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"; BLUE="#4E7A99"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
W,H=720,400; b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
def arrow(x1,y,x2): b.append(f'<line x1="{x1}" y1="{y}" x2="{x2-7}" y2="{y}" stroke="{INK}" stroke-width=".7"/><path d="M{x2} {y} l-8 -3.5 v7 z" fill="{INK}"/>')
# 1. two sources, as stacked cards
for j,(lab,col,y0) in enumerate([("Host listings",ACC,70),("Guest reviews",BLUE,200)]):
    for k in range(3):
        b.append(f'<rect x="{24+k*5}" y="{y0+k*5}" width="130" height="78" fill="#fff" stroke="{LINE}" stroke-width=".6"/>')
    x,y=34,y0+10
    b.append(f'<rect x="{x}" y="{y+2}" width="8" height="8" fill="{col}"/>')
    for r,wd in enumerate([96,84,100,70]):
        b.append(f'<rect x="{x}" y="{y+18+r*12}" width="{wd}" height="4" rx="2" fill="{INK}" fill-opacity=".2"/>')
    b.append(T(24,y0-10,lab,s=12,w=700))
b.append(T(24,315,"Same platform, same",s=10,op=.6)); b.append(T(24,329,"neighborhoods, two voices",s=10,op=.6))
arrow(176,180,214)
# 2. five themes
themes=["Price","Interior","Identity","Neighborhood","Pace"]
b.append(T(222,60,"Words, sorted by theme",s=12,w=700))
for i,t in enumerate(themes):
    y=78+i*44
    b.append(f'<rect x="222" y="{y}" width="150" height="32" rx="16" fill="#fff" stroke="{INK}" stroke-width=".6"/>')
    b.append(T(297,y+20,t,a="middle",s=12,w=600))
arrow(386,180,424)
# 3. boroughs: paired bars per borough, abstract
b.append(T(432,60,"Compared, borough by borough",s=12,w=700))
bors=["Manhattan","Brooklyn","Queens","Bronx","Staten Island"]
pairs=[(70,52),(58,74),(40,30),(22,34),(14,10)]
for i,(bn,(h,g)) in enumerate(zip(bors,pairs)):
    y=86+i*44
    b.append(T(432,y+14,bn,s=11,op=.8))
    b.append(f'<rect x="540" y="{y+2}" width="{h*1.9:.0f}" height="8" fill="{ACC}" fill-opacity=".8"/>')
    b.append(f'<rect x="540" y="{y+14}" width="{g*1.9:.0f}" height="8" fill="{BLUE}" fill-opacity=".8"/>')
b.append(f'<rect x="432" y="318" width="10" height="10" fill="{ACC}" fill-opacity=".8"/>'+T(448,327,"Hosts",s=10,op=.75))
b.append(f'<rect x="500" y="318" width="10" height="10" fill="{BLUE}" fill-opacity=".8"/>'+T(516,327,"Guests",s=10,op=.75))
b.append(T(24,30,"HOW HOSTS AND GUESTS DESCRIBE THE SAME CITY",s=11,w=600,op=.6,ls=1))
b.append(T(24,H-14,"Method diagram · illustrative bars",s=9,op=.5))
open('images/fig-airbnb.svg','w').write(f'<svg data-thinned="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Diagram: host listings and guest reviews are mined for words, sorted into five themes (price, interior, identity, neighborhood, pace), then compared borough by borough for hosts and guests">'+"\n".join(b)+'</svg>')
print("ok")
