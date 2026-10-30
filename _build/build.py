"""Builds index.html and every project page from one data source."""
import os, re, subprocess, html, json
ROOT = "/Users/tolaoniyangi/Documents/tolaoniyangi-site"
BASE = "https://tolaoniyangi.github.io/tolaoniyangi-site/"  # change to https://tolaoniyangi.com/ when the domain moves
NAME = "Shakira “Tola” Oniyangi"
TAGLINE = "Senior UX Engineer and Computational Designer"
RESUME = "https://docs.google.com/document/d/1PsYkoxXYiOl4ZxGXRmqG97AJ3HAt2X0ppgQ0ddp8kbU/export?format=pdf"
EMAIL = "tolaoniyangi@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/tolaoniyangi"

def dims(f):
    p = f"{ROOT}/images/{f}"
    if f.endswith(".svg"):
        return re.search(r'viewBox="0 0 (\d+) (\d+)"', open(p).read()).groups()
    o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p], capture_output=True, text=True).stdout
    return re.findall(r"pixel\w+: (\d+)", o)

class Figs:
    def __init__(self, pre="../"): self.n = 0; self.pre = pre
    def fig(self, src, alt, cap, cls="", lazy=True):
        self.n += 1; w, h = dims(src)
        c = f' class="{cls}"' if cls else ""
        ld = ' loading="lazy"' if lazy else ""
        return f'<figure{c}><img src="{self.pre}images/{src}" alt="{html.escape(alt)}" width="{w}" height="{h}"{ld}><figcaption><b>Fig. {self.n}</b>{cap}</figcaption></figure>'
    def video(self, src, poster, label, cap):
        self.n += 1; w, h = dims(poster)
        return f'<figure><video src="{self.pre}images/{src}" poster="{self.pre}images/{poster}" muted loop playsinline preload="none" width="{w}" height="{h}" aria-label="{label}"></video><figcaption><b>Fig. {self.n}</b>{cap}</figcaption></figure>'

def head(title, desc, url, pre, extra=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="{NAME}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}images/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F3F1EC">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}styles.css">{extra}
</head>
<body>

<header class="top" id="top">
  <div class="top-in">
    <a class="name" href="{pre or './'}">{NAME}</a>
    <nav aria-label="Primary">
      <a class="hide-xs" href="{pre}#work">Work</a>
      <a class="hide-sm" href="{pre}#about">About</a>
      <a class="hide-sm" href="{RESUME}">Resume</a>
      <a class="hello-btn" href="#hello">Say hello</a>
    </nav>
  </div>
</header>
'''

def foot(pre):
    return f'''
  <section class="hello" id="hello">
    <div class="wrap">
      <h2 class="display">Say hello.</h2>
      <p>Working on something for the built environment? I’d love to hear about it.</p>
      <div class="ctas">
        <button class="btn primary" type="button" data-copy="{EMAIL}">Copy email address</button>
        <a class="btn" href="{LINKEDIN}">LinkedIn</a>
        <a class="btn" href="{RESUME}">Resume (PDF)</a>
      </div>
      <div class="foot"><span>© 2026 {NAME}</span><a href="#top">Back to top ↑</a></div>
    </div>
  </section>
</main>

<script src="{pre}site.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- projects
P = []
def project(**k): P.append(k); return Figs()

# 01 Drag to select
f = project(slug="drag-to-select", num="01", title="Drag to select", thumb="fig-select.svg", contain=True,
    eyebrow="Google Earth · Interaction design, front end", card_label="Google Earth · Design, front end",
    card="Draw a box on the map to select as many places as you want at once. Before this, Google Earth only let you pick places one at a time.",
    dek="Draw a box on the map, select every place inside it, and style them all at once. Before this, places on the map could only be picked one at a time.",
    meta=[("Role", "Interaction design and front-end engineering, sole engineer"), ("Product", "Google Earth, web"), ("Status", "Live"),
          ("Links", '<a href="https://developers.google.com/maps/documentation/earth/style-your-places#bulk_styling">Bulk styling docs ↗</a>')])
P[-1]["lead"] = f.fig("fig-select.svg", "Diagram: a dashed box dragged over map points selects them, and the same items appear checked in the project panel",
    "Drag a box on the map. Everything inside is selected, and the project panel’s checkboxes update to match.", lazy=False)
P[-1]["chapters"] = [
    ("<p>Places could be selected one at a time on the map, or several at once from the project panel. It was slow and unintuitive, and a real limit for power users and complex work.</p>"
     "<p>Google Earth also needed a temporary drawing state for features on the way. Drag to select would be the first to use it, so it had to set the pattern.</p>"),
    ("<p>Selection already worked three ways: checkboxes, dragging in the panel, and clicking items. The new gesture had to fit with all of them, across:</p>"
     "<ul><li><strong>Web and mobile.</strong> One idea, two very different kinds of input.</li>"
     "<li><strong>Streamlined and productivity layouts.</strong> Simple by default, fast for power users.</li>"
     "<li><strong>Screen-centered drawing tools.</strong> Other tools also claim the middle of the map, so the gestures can’t collide.</li></ul>"
     "<p>Each of these was worked out by prototyping, testing and iterating closely with a UX designer and a PM. All of the implementation was one engineer.</p>"),
    ("<p>Drag to select is live in Google Earth on the web, and it’s the first feature built on Earth’s new drawing state.</p>"),
]

# 02 Cut and fill
f = project(slug="cut-and-fill", num="02", title="Cut and fill", thumb="fig-cutfill.svg", contain=True,
    eyebrow="Google Earth · Back-end design, engineering", card_label="Google Earth · Back end",
    card="Draw a site and see how much earth has to be dug out or brought in to level it, and where. One of four terrain analysis tools in Google Earth.",
    dek="An earthwork estimate in Google Earth. Draw a site and see how much soil has to be dug out or brought in to level it, and where.",
    meta=[("Role", "Back-end design and engineering"), ("Product", "Google Earth terrain analysis"), ("Status", "Live"),
          ("Links", '<a href="https://mapsplatform.google.com/resources/blog/a-field-guide-to-terrain-analysis-tools-in-google-earth/">Field guide ↗</a><br><a href="https://developers.google.com/maps/documentation/earth/terrain-analysis">Docs ↗</a>')])
P[-1]["lead"] = f.fig("fig-cutfill.svg", "Section diagram: soil above the dashed target level is cut, the gap below it is filled",
    "The idea in one section. Soil above the target level gets dug out, and hollows below it get built up.", lazy=False)
P[-1]["chapters"] = [
    ("<p>Before a site can be graded, someone has to estimate how much soil comes out and how much goes back in. It’s one of the first numbers on any construction project, and getting it usually means survey data and CAD software.</p>"),
    ("<p>The back end calculates cut and fill volumes for a site and produces the map of where earth has to move. It can find the elevation where cut equals fill, or calculate the volumes for any target elevation a user sets.</p>"
     f'<div class="figs">{f.video("cut-and-fill.mp4", "cutfill-poster.jpg", "Screen recording of the cut and fill tool in Google Earth", "The tool in Google Earth: choose a site, set a target elevation, get the volumes.")}</div>'),
    ("<p>Cut and fill is live in Google Earth, one of four terrain analysis tools alongside elevation contours, slope and aspect.</p>"),
]

# 03 Traffic
f = project(slug="1p-research-data-layers", num="03", title="Traffic signal level of service", thumb="fig-traffic.svg", contain=True,
    eyebrow="Google Earth · 2025 · Data product, UI", card_label="Google Earth · Data product, UI",
    card="Google Research’s vehicle-delay data, turned into an A–F grade for every signalized intersection, hour by hour. Part of a launch that signed up 470+ paying professional users.",
    dek="Google Research measured how long vehicles wait at traffic lights. This data layer turns that research into an A–F grade for every signalized intersection, hour by hour.",
    meta=[("Role", "Visualization strategy and UI design"), ("Product", "Google Earth data layers"), ("Status", "Live"), ("Timeline", "Q1–Q2 2025")])
P[-1]["lead"] = f.fig("fig-traffic.svg", "Street grid where each intersection is colored by its A to F delay grade, with one intersection's grade shown across the day",
    "How the layer reads. Each intersection gets a grade from A (little delay) to F (long waits). Pick one to see its grade through the day.", lazy=False)
P[-1]["chapters"] = [
    ("<p>The research was rigorous and hard to read. Traffic engineers and planners needed to act on it in seconds, and the research team needed it shown accurately.</p>"),
    ("<ul><li><strong>A–F grading</strong> designed so a dense dataset reads at a glance.</li>"
     "<li><strong>An hour-by-hour view</strong> from 06:00 to 22:00, so congestion can be followed through the day.</li>"
     "<li><strong>One agreed plan.</strong> The work sat between research scientists and product engineering, getting both to sign off on a visualization that was accurate and easy to read.</li></ul>"
     f'<div class="figs two"><div class="wide">{f.fig("traffic-seattle.jpg", "Seattle intersections colored by delay grade in Google Earth", "Seattle in Google Earth, every signalized intersection graded.")}</div>'
     f'{f.fig("traffic-detail.jpg", "One intersection selected with its grade and hourly breakdown", "One intersection’s grade, percentile and hourly scores.")}'
     f'{f.fig("traffic-layers.jpg", "The data layers catalog in Google Earth", "The layer sits alongside Earth’s other professional data layers.")}</div>'),
    ('<div class="stat"><div><b>470+</b><span>paying professional users</span></div><div><b>10%</b><span>conversion in the first two weeks</span></div></div>'
     "<p>It set the template for bringing more Google research into Earth as data layers, including inundation history, which started from these initial designs.</p>"),
]

# 04 Solar
f = project(slug="solar-assessment", num="04", title="Solar layouts and potential", thumb="fig-solar.svg", contain=True,
    eyebrow="Google Earth · 2023–24 · Computational design lead", card_label="Google Earth · Computational design lead",
    card="Estimate a site’s solar potential in minutes, with a panel layout for any building or parking lot that keeps clear of HVAC units and fire-code setbacks.",
    dek="Estimate a site’s solar potential in minutes: a panel layout for any building or parking lot, with expected output and cost.",
    meta=[("Role", "Computational design lead"), ("Product", "Google Earth solar studies"), ("Status", "Live"),
          ("Links", '<a href="https://medium.com/google-earth/evaluate-building-and-solar-design-options-in-minutes-with-google-earth-6b5bc5734351">Launch post ↗</a>')])
P[-1]["lead"] = f.fig("fig-solar.svg", "Roof plan: solar panels fill the roof while keeping clear of the fire-code setback and HVAC units",
    "What the layouts work around: a fire-code setback at the roof edge, and HVAC units with clearance around them.", lazy=False)
P[-1]["chapters"] = [
    ("<p>Planners and developers want to know whether solar makes sense on a site before they hire anyone. A useful estimate needs a layout that could actually be built.</p>"),
    ("<ul><li><strong>Solar API integration.</strong> The first in Google Earth, for residential and small commercial roofs up to 500 m².</li>"
     "<li><strong>Placement logic</strong> that keeps panels clear of HVAC units and fire-code setbacks.</li>"
     "<li><strong>Panel types by building size</strong>, residential or commercial, so output estimates stay realistic.</li>"
     "<li><strong>Beyond rooftops.</strong> Design logic for solar canopies, and production code for carports.</li></ul>"
     f'<div class="figs two">{f.fig("solar-before.jpg", "Solar layout before the Solar API integration", "Before the Solar API integration")}{f.fig("solar-after.jpg", "Solar layout after the Solar API integration", "After")}</div>'),
    ("<p>Solar studies are live in Google Earth for rooftops and parking lots, with three carport options and expected output, savings and payback for each design.</p>"
     f'<div class="figs">{f.fig("solar-carports.jpg", "Carport solar design with financials in Google Earth", "A carport design with output, savings and payback.")}</div>'),
]

# 05 Intelligent City
f = project(slug="computational-design", num="05", title="Mass-timber buildings, generated", thumb="intelligent-city.jpg", contain=True,
    eyebrow="Intelligent City · 2021–22 · Computational design", card_label="Intelligent City · Computational design",
    card="Software that generates mass-timber housing a factory can build, and measures the materials, cost and emissions of every design.",
    dek="Intelligent City designs and manufactures mass-timber housing. Its parametric generator produces buildings the factory can make, and every design is measured for materials, cost and emissions.",
    meta=[("Role", "Computational designer"), ("Product", "Parametric building platform"), ("Status", "2021–22, Vancouver"),
          ("Links", '<a href="https://intelligent-city.com">Intelligent City ↗</a>')])
P[-1]["lead"] = f.fig("intelligent-city.jpg", "Intelligent City's technology stack, from design and data to parametric software, automated manufacturing and on-site assembly",
    "From design to factory to site. This work sat in the parametric software and the data.", lazy=False)
P[-1]["chapters"] = [
    ("<p>The range of buildings the generator could produce limited what the company could evaluate and optimize. Pulling data out of each design, like material quantities, was manual.</p>"),
    ("<ul><li><strong>A bigger generator.</strong> New building forms, all compatible with the mass-timber manufacturing system.</li>"
     "<li><strong>Automatic data extraction</strong> from every design, down to material quantities, joined with outside data sources.</li>"
     "<li><strong>A client-facing dashboard</strong>, designed and built solo, that turns each design into cost and emissions estimates.</li></ul>"
     f'<div class="figs">{f.fig("intelligent-city-process.jpg", "Diagram of parametric generation, data extraction and dashboard creation", "Generate the building, extract its data, show it to the client.")}</div>'),
    ('<div class="stat"><div><b>200%</b><span>more building forms the generator can produce</span></div></div>'
     "<p>That range became the base for the company’s design evaluation and optimization, and every design now comes with instant cost and emissions estimates.</p>"),
]

# 06 Pedestrians
f = project(slug="estimating-pedestrian-activity", num="06", title="Estimating pedestrian activity", thumb="ped-buzz.jpg",
    eyebrow="Sidewalk Labs · 2019 · Computational design", card_label="Sidewalk Labs · Computational design",
    card="A pipeline that estimates street-level foot traffic from census data and feeds it straight into generative design tools.",
    dek="Generative design tools need good data about streets. This pipeline estimates street-level foot traffic and feeds it straight in.",
    meta=[("Role", "Computational design summer associate"), ("Product", "Generative design tools"), ("Status", "Summer 2019"), ("Team", "Generative Design, Sidewalk Labs")])
P[-1]["lead"] = f.fig("ped-buzz.jpg", "3D site model with pedestrian activity colored by intensity",
    "The “buzz metric”: estimated pedestrian activity from residents and workers around a site.", lazy=False)
P[-1]["chapters"] = [
    ("<p>Getting geospatial data into generative design was slow and manual, which kept the tools stuck on narrow test cases. The first step was research into which use cases mattered most, and which standard datasets, like pedestrian activity and transit access, they needed.</p>"
     f'<div class="figs">{f.fig("ped-research.gif", "Animated diagram of use-case research", "Mapping use cases to the data they need.")}</div>'),
    ("<p>An automated pipeline pulls the data in. Census population and workforce counts are then split down to individual buildings to estimate activity at street level.</p>"
     f'<div class="figs two">{f.fig("ped-site.jpg", "Map of New York with the test site highlighted", "The test site.")}{f.fig("ped-volume.jpg", "Buildings colored by estimated population volume", "Population split down to each building.")}</div>'),
    ("<p>Built on a test site, then confirmed in other cities and over larger areas. Generative design can now draw on building-level population, workforce and land use, plus a “buzz metric” for pedestrian activity.</p>"
     f'<div class="figs">{f.fig("ped-mockup.gif", "Animated mockup of choosing a place and loading its data", "Pick a place and its data loads automatically.")}</div>'),
]

# Earlier work with their own pages
f = project(slug="beyond-the-blue-dot", num=None, title="Beyond the Blue Dot", thumb="bluedot.jpg", year="2020", kind="Urban planning capstone",
    eyebrow="Columbia GSAPP · 2020 · Urban planning capstone",
    card="A web tool that turns census data into short stories about the people who live and work in a place.",
    dek="Who lives here? Who works here? A web tool that turns census data into short stories about the people in a place.",
    meta=[("Role", "UX, visual design, prototyping, code"), ("Product", "Web prototype"), ("Status", "Capstone, Spring 2020"), ("Advisors", "Anthony Vanky. Reader: Violet Whitney")])
P[-1]["lead"] = f.fig("bluedot.jpg", "Beyond the Blue Dot landing page with a map of New York", "Choose a place and a type of person, and read their story.", lazy=False)
P[-1]["chapters"] = [
    ("<p>A planner working on a transit project wants to disrupt people’s days as little as possible, so they need to know who lives and works nearby, how they get around and what they earn.</p>"
     "<p>Getting that from GIS takes days. Community meetings help, but they don’t represent everyone. There was no quick way to see a place at the scale of one person.</p>"),
    ("<p>Pick a location and a profile, and the tool builds a narrative about a typical or outlier resident or worker from national data, so it works anywhere in the US. The flow was shaped by interviews with practicing planners.</p>"
     f'<div class="figs">{f.fig("bluedot-persona.jpg", "User persona for an urban planner", "The persona, from conversations with planners.")}{f.fig("bluedot-flow.jpg", "User flow from location to persona to narrative", "A deliberately short flow: location, person, story.")}</div>'),
    ("<p>A working prototype and the capstone for the MS in Urban Planning. The name plays on the blue dot that stands for you in Google Maps. Here, the dot is a person.</p>"),
]

f = project(slug="data-storytelling", num=None, title="Election data for 5M voters", thumb="fig-elections.svg", contain=True, year="2020", kind="Data visualization",
    eyebrow="BallotReady · 2020 · Data visualization internship",
    card="Polling places checked and ballot trends charted for a nonpartisan voter guide.",
    dek="BallotReady is a nonpartisan voter guide used by more than 5 million people in 2020. Its data had to say exactly where and when people could vote.",
    meta=[("Role", "Elections intern, data team"), ("Product", "BallotReady voter guide"), ("Status", "Fall 2020"), ("Links", '<a href="https://www.ballotready.org">BallotReady ↗</a>')])
P[-1]["lead"] = f.fig("fig-elections.svg", "Diagram: hundreds of local election offices feed one verified dataset, which powers a voter guide used by more than 5 million voters",
    "Hundreds of local sources, one verified dataset, more than 5 million voters.", lazy=False)
P[-1]["chapters"] = [
    ("<p>Every local election office publishes voting locations and hours its own way. A voter guide has to turn all of it into one dataset people can trust.</p>"),
    ("<ul><li><strong>Verification</strong> of hundreds of early voting, absentee and polling place locations and hours for the 2020 general election.</li>"
     '<li><strong>Charts</strong> for BallotReady’s reporting: <a href="https://medium.com/@BallotReady/what-are-candidates-talking-about-this-year-2a9a9463ca50">top issues by state</a>, <a href="https://medium.com/@BallotReady/whats-on-the-ballot-75da87973a50">what’s on the ballot</a>, and <a href="https://medium.com/@BallotReady/today-is-the-day-but-what-happens-next-ff73b3bf9a4e">how people could vote</a>.</li></ul>'
     f'<div class="figs">{f.fig("elections-issues.jpg", "Maps comparing top state issues in 2018 and 2020", "Top issues by state, 2018 vs 2020.")}{f.fig("elections-numbers.jpg", "Map of candidates per seat by US state", "97,475 candidates for 71,210 seats.")}</div>'),
    ('<div class="stat"><div><b>5M+</b><span>voters used the guide in 2020</span></div></div>'),
]

# Earlier work that still lives on Adobe
EARLY_ADOBE = [
    ("https://tolaoniyangi.com/12", "wastespace.jpg", "wastespace", "A recycling hub that creates jobs for women in Vieques, Puerto Rico.", "Architecture · 2019"),
    ("https://tolaoniyangi.com/library", "library.jpg", "design for who?", "A Dumbo library designed around who can walk to it.", "Architecture, mapping · 2018"),
    ("https://tolaoniyangi.com/citi-bike-access", "citibike.jpg", "Citi Bike access", "Who Citi Bike reaches, and who it leaves out.", "GIS · 2017"),
    ("https://tolaoniyangi.com/airbnb-analysis", "airbnb.jpg", "Airbnb analysis", "How hosts and guests describe the same neighborhoods differently.", "Data visualization · 2017"),
    ("https://tolaoniyangi.com/predicting-urban-sprawl", "sprawl.jpg", "Predicting urban sprawl", "A model trained on satellite images of Cairo, Dubai and Wuhan.", "Machine learning · 2016"),
]

SELECTED = [p for p in P if p["num"]]
EARLIER = [p for p in P if not p["num"]]

def project_page(p, nxt):
    f = Figs()
    meta = "".join(f'<div><dt class="label">{k}</dt><dd>{v}</dd></div>' for k, v in p["meta"])
    names = ["The problem", "The work", "The result"]
    chapters = "\n    ".join(
        f'<section class="chapter"><h2><span class="num">{i+1:02d}</span>{names[i]}</h2><div class="prose">{body}</div></section>'
        for i, body in enumerate(p["chapters"]))
    num = f'<span class="num">{p["num"]}</span>' if p["num"] else '<span class="num">Earlier work</span>'
    nc = " contain" if nxt.get("contain") else ""
    w, h = dims(nxt["thumb"])
    url = f'{BASE}{p["slug"]}/'
    desc = re.sub("<[^>]+>", "", p["dek"])
    return head(f'{p["title"]} · {NAME}', desc, url, "../") + f'''
<main>
  <div class="wrap">
    <section class="p-hero">
      <a class="back" href="../#work">← All work</a>
      <div class="eyebrow">{num}<span class="label">{p["eyebrow"]}</span></div>
      <h1 class="display">{p["title"]}</h1>
      <p class="dek">{p["dek"]}</p>
    </section>

    <dl class="meta">{meta}</dl>

    <div class="lead">{p["lead"]}</div>

    {chapters}

    <a class="next" href="../{nxt["slug"]}/">
      <div><span class="label">Next project</span><h2 class="display">{nxt["title"]}</h2></div>
      <div class="pic{nc}"><img src="../images/{nxt["thumb"]}" alt="" width="{w}" height="{h}" loading="lazy"></div>
    </a>
  </div>
''' + foot("../")

def card(p):
    w, h = dims(p["thumb"])
    c = " contain" if p.get("contain") else ""
    return f'''        <a class="card" href="{p["slug"]}/">
          <div class="pic{c}"><img src="images/{p["thumb"]}" alt="" width="{w}" height="{h}" loading="lazy"></div>
          <div class="card-text"><span class="num">{p["num"]}</span><h3 class="display">{p["title"]}</h3><p>{p["card"]}</p><span class="label">{p["card_label"]}</span></div>
        </a>'''

def early_row(href, img, title, line, when):
    w, h = dims(img)
    return f'''        <tr>
          <td class="thumb"><a href="{href}" tabindex="-1" aria-hidden="true"><img src="images/{img}" alt="" loading="lazy" width="{w}" height="{h}"></a></td>
          <td><h3><a href="{href}">{title}</a></h3><p>{line}</p></td>
          <td class="when label">{when}</td>
        </tr>'''

person = {
    "@context": "https://schema.org", "@type": "Person",
    "name": "Shakira Oniyangi", "alternateName": ["Tola Oniyangi", "Shakirat Ibitola Oniyangi"],
    "jobTitle": TAGLINE, "worksFor": {"@type": "Organization", "name": "Google"},
    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Columbia University Graduate School of Architecture, Planning and Preservation"},
                 {"@type": "CollegeOrUniversity", "name": "Barnard College"}],
    "knowsAbout": ["UX engineering", "Computational design", "Architecture", "Urban planning", "GIS", "Geospatial data visualization"],
    "url": BASE, "sameAs": [LINKEDIN],
}

def home():
    cards = "\n".join(card(p) for p in SELECTED)
    rows = "\n".join([early_row(f'{p["slug"]}/', p["thumb"] if not p["thumb"].endswith("svg") else "elections-numbers.jpg", p["title"], p["card"], f'{p["kind"]} · {p["year"]}') for p in EARLIER]
                     + [early_row(*r) for r in EARLY_ADOBE])
    desc = f"{NAME} is a senior UX engineer and computational designer on Google Earth, with a background in architecture and urban planning from Columbia GSAPP."
    ld = f'\n<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>'
    return head(f"{NAME} · {TAGLINE}", desc, BASE, "", ld).replace('<a class="name" href="./">', '<a class="name" href="./">') + f'''
<main>
  <div class="wrap">
    <section class="hero">
      <h1 class="display">I design and build software for the <em>built environment.</em></h1>
      <div class="hero-foot">
        <p>I’m a senior UX engineer and computational designer on Google Earth. Before software, I studied architecture and urban planning at Columbia. Now I build the tools that planners, architects and builders use to understand a site before they change it.</p>
        <div class="ctas">
          <a class="btn primary" href="#hello">Say hello</a>
          <a class="btn" href="#work">See the work ↓</a>
        </div>
      </div>
    </section>

    <section id="work" class="block">
      <div class="sec-head"><h2 class="label">Selected work</h2><span class="label">2019–2026</span></div>
      <div class="index">
{cards}
      </div>
    </section>

    <section class="block" aria-labelledby="earlier">
      <div class="sec-head"><h2 class="label" id="earlier">Earlier work</h2><span class="label">Columbia GSAPP and internships, 2016–20</span></div>
      <table class="early">
{rows}
      </table>
    </section>

    <section class="about block" id="about">
      <div class="sec-head" style="grid-column:1/-1;margin-bottom:0"><h2 class="label">About</h2></div>
      <div></div>
      <div>
        <p class="big">I came to software from architecture and urban planning, and the built environment is still what I care about most. I want my tools to keep getting closer to the people who design and construct it.</p>

        <h3 class="label">Experience</h3>
        <ul class="list">
          <li><span>Google, Senior Computational Designer (UX Engineer)<small>Google Earth. Designing and building map interactions, data layers and site analysis tools, from front end to back end.</small></span><span class="label">2022–now</span></li>
          <li><span>Intelligent City, Computational Designer<small>Vancouver. Parametric design and data for mass-timber housing.</small></span><span class="label">2021–22</span></li>
          <li><span>Columbia GSAPP, Graduate Researcher and Teaching Assistant<small>Center for Spatial Research. GIS teaching assistant for the whole school, and Urban Analytics teaching assistant in the planning program.</small></span><span class="label">2017–20</span></li>
          <li><span>Buell Center, Columbia GSAPP, Research Assistant<small>Research for the exhibition <em>Living in America</em>.</small></span><span class="label">2016–17</span></li>
        </ul>

        <h3 class="label">Education</h3>
        <ul class="list">
          <li><span>Columbia GSAPP, Master of Architecture and MS Urban Planning</span><span class="label">2020</span></li>
          <li><span>Barnard College, Columbia University, BA Architecture</span><span class="label">2016</span></li>
        </ul>

        <h3 class="label">Teaching and mentoring</h3>
        <ul class="list">
          <li><span>Mentorship Program, Columbia GSAPP<small>Mentor to an MS Urban Planning student, class of 2027</small></span><span class="label">2026–27</span></li>
          <li><span>Guest Lecturer, Columbia GSAPP<small><em>Prototyping in Urban Tech</em>, taught by James Piacentini</small></span><span class="label">2026</span></li>
        </ul>

        <h3 class="label">Recognition</h3>
        <ul class="list">
          <li><span>Honorable Mention, Analytics, Geo Makers Hackathon at Google<small>Came up with the idea and built the prototype with two teammates</small></span><span class="label">2025</span></li>
        </ul>

        <h3 class="label">Mentions</h3>
        <ul class="list">
          <li><a href="https://news.columbia.edu/news/tola-oniyangi-graduates-dual-degree-architecture-urban-planning">Three degrees later, this graduate is ready to move on</a><span class="label">Columbia News · 2020</span></li>
          <li><a href="https://www.civilbeat.org/2020/01/can-fixing-our-parking-rules-make-honolulu-more-affordable/">Can fixing parking rules make Honolulu more affordable?</a><span class="label">Civil Beat · 2020</span></li>
          <li><span>Researcher, <a href="https://c4sr.columbia.edu/projects/homophily-urban-history-algorithm"><em>Homophily: The Urban History of an Algorithm</em></a></span><span class="label">Chicago Architecture Biennial · 2019</span></li>
          <li><a href="https://blogs.ei.columbia.edu/2019/12/06/proposals-resilience-vieques-puerto-rico/">13 proposals to boost resilience in Vieques, Puerto Rico</a><span class="label">Columbia Climate School · 2019</span></li>
          <li><span>Researcher, <a href="https://buellcenter.columbia.edu/projects/3c803455-dbd0-4491-9c68-dec1004d1b30/"><em>Living in America: Frank Lloyd Wright, Harlem &amp; Modern Housing</em></a></span><span class="label">Buell Center · 2017</span></li>
        </ul>
      </div>
    </section>
  </div>
''' + foot("")

ALL = SELECTED + EARLIER
for i, p in enumerate(ALL):
    nxt = ALL[(i + 1) % len(ALL)]
    os.makedirs(f"{ROOT}/{p['slug']}", exist_ok=True)
    open(f"{ROOT}/{p['slug']}/index.html", "w").write(project_page(p, nxt))
open(f"{ROOT}/index.html", "w").write(home())
print("built", len(ALL), "pages + home")
