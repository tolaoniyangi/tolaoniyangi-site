# Sidewalk Labs use-case research: data sources -> planning analyses (redrawn from the original GIF,
# keeping its per-source colours, the * on a less certain use and the + joining housing to demographics).
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
sources=[("Weather","Historical, real-time, forecasts"),("Buildings","Occupancy, geometry, type, rent"),("Land use","Current and historical"),
         ("Parcels","Units, tax lots, zoning"),("Boundaries","Admin, political, social, economic"),
         ("Census","Income, housing, commute"),("Roads","Intersections, curbs, lanes"),
         ("Bike data","Racks, paths, suggested routes"),("Transit","Parking, stations, schedules"),("Traffic","Congestion, accidents, live flow")]
uses=[("Shadow analysis","Sun and weather on buildings"),("Shading","Glare, views, daylight"),("Environment","Emissions, watersheds, pollution"),
      ("Economic conditions","Scenarios like a new BID"),("Land use","Past patterns, zoning impacts"),("Political modeling","Voting districts and access"),
      ("Demographic analysis","Who a decision affects"),("Population","Change over time"),
      ("Transportation","Does supply meet demand?"),("Traffic flow","Least disruptive times"),("Accidents","Safer intersections")]
links={"Weather":["Shadow analysis"],"Buildings":["Shadow analysis","Shading","Environment","Economic conditions","Land use"],
       "Land use":["Land use","Economic conditions"],"Parcels":["Economic conditions","Land use","Political modeling","Demographic analysis"],
       "Boundaries":["Political modeling","Demographic analysis","Economic conditions","Population"],
       "Census":["Demographic analysis","Population","Political modeling"],"Roads":["Transportation","Traffic flow"],
       "Bike data":["Transportation"],"Transit":["Transportation","Traffic flow"],"Traffic":["Traffic flow","Accidents"]}
col={"Weather":"#8A857B","Buildings":"#D29A12","Land use":"#D29A12","Parcels":"#E2512B","Boundaries":"#C7356B",
     "Census":"#6E9E2E","Roads":"#1597AC","Bike data":"#2E78C8","Transit":"#5B4FC4","Traffic":"#8C3BAE"}
# Drawn at the size it is shown (660 wide), so the text stays readable
W=660; top=60; row=40; H=top+len(uses)*row+34
b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
lx,lw=16,176; rx,rw=300,176
ys={n:top+i*(len(uses)*row/len(sources))+6 for i,(n,_) in enumerate(sources)}
yu={n:top+i*row+4 for i,(n,_) in enumerate(uses)}
for s_,targets in links.items():
    for t_ in targets:
        y1=ys[s_]+16; y2=yu[t_]+16
        b.append(f'<path d="M{lx+lw} {y1:.1f} C {lx+lw+60} {y1:.1f}, {rx-60} {y2:.1f}, {rx} {y2:.1f}" fill="none" stroke="{col[s_]}" stroke-width=".8" stroke-opacity=".7"/>')
for n,sub in sources:
    y=ys[n]; c=col[n]
    b.append(f'<rect x="{lx}" y="{y}" width="{lw}" height="32" rx="4" fill="#fff" stroke="{c}" stroke-width=".9"/>')
    b.append(T(lx+10,y+14,n,s=11,w=700,fill=c)); b.append(T(lx+10,y+26,sub,s=9,op=.65))
for n,sub in uses:
    y=yu[n]
    b.append(f'<rect x="{rx}" y="{y}" width="{rw}" height="32" rx="16" fill="#fff" stroke="{INK}" stroke-width=".6"/>')
    b.append(T(rx+14,y+14,n,s=11,w=700)); b.append(T(rx+14,y+26,sub,s=9,op=.65))
# * marks a less certain use; + joins housing to demographic analysis, as in the original
ye=yu["Environment"]; b.append(T(rx+rw+8,ye+26,"*",s=20,w=400))
yd=yu["Demographic analysis"]; hx=rx+rw+34
b.append(T(rx+rw+11,yd+23,"+",s=20,w=400))
b.append(f'<rect x="{hx}" y="{yd}" width="{W-hx-16}" height="32" rx="16" fill="#fff" stroke="{INK}" stroke-width=".6"/>')
b.append(T(hx+14,yd+14,"Housing",s=11,w=700)); b.append(T(hx+14,yd+26,"Occupancy, affordability",s=9,op=.65))
b.append(T(rx,H-14,"* Possible use, less certain",s=9,op=.65)); b.append(T(rx+140,H-14,"+ Builds on demographic analysis",s=9,op=.65))
b.append(T(lx,36,"DATA SOURCES",s=11,w=600,op=.6,ls=1)); b.append(T(rx,36,"WHAT PLANNERS COULD DO",s=11,w=600,op=.6,ls=1))

open('images/fig-ped-research.svg','w').write(f'<svg data-thinned="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Flowchart: ten urban data sources, such as weather, buildings, parcels, census, roads and transit, linked to twelve planning analyses, from shadow studies and demographic analysis to transportation, traffic flow and accidents">'+"\n".join(b)+'</svg>')
print("ok",H)
