# Sidewalk Labs use-case research: data sources -> planning analyses (redrawn from the original GIF).
INK="#141413"; MUTED="#8A857B"; LINE="#CFCAC0"; PAPER="#EAE6DE"; ACC="#E2512B"
F='font-family="Archivo, Helvetica, Arial, sans-serif"'
def T(x,y,t,a="start",s=12,w=400,op=1,ls=0,fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{a}" {F} font-size="{s}" font-weight="{w}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{t}</text>'
sources=[("Weather","Historical, real-time, forecasts"),("Buildings","Occupancy, geometry, type, rent"),("Land use",""),
         ("Parcels","Units, tax lots, zoning"),("Boundaries","Administrative, political, social, economic"),
         ("Census","Income, housing, education, commute"),("Roads","Intersections, curbs, road types, lanes"),
         ("Bike data","Racks, paths, suggested routes"),("Transit","Parking, stations, schedules"),("Traffic","Congestion, accidents, live flow")]
uses=[("Shadow analysis","Sun and weather on buildings"),("Shading","Glare, views, daylight"),("Environment","Emissions, watersheds, pollution"),
      ("Economic conditions","Scenarios like a new BID"),("Land use","Past patterns, zoning impacts"),("Political modeling","Voting districts and access"),
      ("Demographic analysis","Who a decision affects"),("Housing","Occupancy, type, affordability"),("Population","Change over time"),
      ("Transportation","Does supply meet demand?"),("Traffic flow","Least disruptive times"),("Accidents","Safer intersections")]
links={"Weather":["Shadow analysis"],"Buildings":["Shadow analysis","Shading","Environment","Economic conditions","Land use","Housing"],
       "Land use":["Land use","Economic conditions"],"Parcels":["Economic conditions","Land use","Political modeling","Demographic analysis"],
       "Boundaries":["Political modeling","Demographic analysis","Economic conditions","Population"],
       "Census":["Demographic analysis","Population","Political modeling","Housing"],"Roads":["Transportation","Traffic flow"],
       "Bike data":["Transportation"],"Transit":["Transportation","Traffic flow"],"Traffic":["Traffic flow","Accidents"]}
focus=set()
W=720; top=64; row=46; H=top+len(uses)*row+40
b=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
lx,lw=20,230; rx,rw=470,230
ys={n:top+i*(len(uses)*row/len(sources))+6 for i,(n,_) in enumerate(sources)}
yu={n:top+i*row+4 for i,(n,_) in enumerate(uses)}
for s_,targets in links.items():
    for t_ in targets:
        y1=ys[s_]+18; y2=yu[t_]+17
        on=s_ in focus
        b.append(f'<path d="M{lx+lw} {y1:.1f} C {lx+lw+110} {y1:.1f}, {rx-110} {y2:.1f}, {rx} {y2:.1f}" fill="none" stroke="{ACC if on else MUTED}" stroke-width="{.9 if on else .6}" stroke-opacity="{.75 if on else .5}"/>')
for n,sub in sources:
    y=ys[n]; on=n in focus
    b.append(f'<rect x="{lx}" y="{y}" width="{lw}" height="36" rx="4" fill="#fff" stroke="{ACC if on else LINE}" stroke-width="{1 if on else .6}"/>')
    b.append(T(lx+10,y+15,n,s=11,w=700,fill=ACC if on else INK)); b.append(T(lx+10,y+29,sub,s=9,op=.65))
for n,sub in uses:
    y=yu[n]
    b.append(f'<rect x="{rx}" y="{y}" width="{rw}" height="34" rx="17" fill="#fff" stroke="{INK}" stroke-width=".6"/>')
    b.append(T(rx+14,y+15,n,s=11,w=700)); b.append(T(rx+14,y+27,sub,s=9,op=.65))
b.append(T(lx,40,"DATA SOURCES",s=11,w=600,op=.6,ls=1)); b.append(T(rx,40,"WHAT PLANNERS COULD DO",s=11,w=600,op=.6,ls=1))

open('images/fig-ped-research.svg','w').write(f'<svg data-thinned="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Flowchart: ten urban data sources, such as weather, buildings, parcels, census, roads and transit, linked to twelve planning analyses, from shadow studies and demographic analysis to transportation, traffic flow and accidents">'+"\n".join(b)+'</svg>')
print("ok",H)
