#!/usr/bin/env python3
"""Generates the multi-page static site from projects.json.
Run from anywhere:  python3 _tools/build.py   (output goes to the site root).
Edit projects.json to add/change a project, then re-run."""
import json, html, re, os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://swastiikgroup.com/"
E = html.escape
P = json.load(open(os.path.join(ROOT, "_tools", "projects.json"), encoding="utf-8"))
chrono = sorted(P, key=lambda p: (p["year"], p["status"] == "ongoing"))
ongoing = next(p for p in P if p["status"] == "ongoing")
done = [p for p in chrono if p["status"] != "ongoing"]
total_units = sum(sum(int(n) for n in re.findall(r"\d+", p["units"])) for p in done)
years = date.today().year - 2013
OFFICE = ("Swastiik Realty", "101, Rudramal Complex, Nr. Swastik Cross Road, Navrangpura, Ahmedabad.")
PHONE = "+91 98250 34030"
PHONE_HREF = "tel:+919825034030"
NAV = [("index.html", "Home"), ("about.html", "About"), ("projects.html", "Projects"),
       ("journey.html", "Journey"), ("photo.html", "Photos")]

def url(p): return f"project-{p['id']}.html"
def kind(p): return "commercial" if "Commercial" in p["type"] else "residential"
def ico(n, c=""): return f'<i data-lucide="{n}" class="{c}"></i>'
def tel(n):
    d = re.sub(r"\D", "", n)
    if len(d) > 10: d = d[-10:]
    return "tel:+91" + d
def phones(p): return [x.strip() for x in p["phone"].split("/")]
def short_addr(p): return ",".join(p["address"].split(",")[-3:]).strip()

def shell(file, title, desc, body, active, img="images/projects/shomes_hero.jpg", splash=False):
    links = "".join(f'<li><a href="{h}" class="nav-link{" active" if h == active else ""}">{t}</a></li>' for h, t in NAV)
    mlinks = "".join(f'<li><a href="{h}" class="mobile-nav-link{" active" if h == active else ""}">{t}</a></li>' for h, t in NAV)
    fprojects = "".join(f'<li><a href="{url(p)}">{E(p["name"])} <span>({p["year"]})</span></a></li>' for p in chrono)
    fnav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    sp = ('<div class="splash-screen" id="splashScreen"><div class="splash-mark"><div class="splash-ring"></div>'
          '<img src="images/logo.png" alt="Swastiik Group"></div><p class="splash-wordmark">SWASTIIK <span>GROUP</span></p>'
          '<p class="splash-sub">Building Since 2013</p></div>') if splash else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}{file}">
<link rel="icon" type="image/png" href="images/favicon.png">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{file}">
<meta property="og:image" content="{SITE}{img}">
<meta name="theme-color" content="#211f2e">
<script>document.documentElement.classList.add("js")</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="pages.css">
</head>
<body>
{sp}
<nav id="navbar" class="navbar">
 <div class="nav-container">
  <a href="index.html" class="nav-logo"><img src="images/logo.png" alt="Swastiik Group logo"><div class="logo-text"><span class="logo-name">SWASTIIK GROUP</span><span class="logo-sub">Real Estate</span></div></a>
  <ul class="nav-links">{links}</ul>
  <button class="hamburger" id="hamburger" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
 </div>
 <div class="mobile-menu" id="mobileMenu"><ul class="mobile-nav-links">{mlinks}</ul></div>
</nav>
{body}
<footer class="footer">
 <div class="footer-inner">
  <div class="footer-brand">
   <div class="footer-logo"><img src="images/logo.png" alt="Swastiik Group logo"><div class="logo-text"><span class="logo-name">SWASTIIK GROUP</span><span class="logo-sub">Real Estate</span></div></div>
   <p class="footer-tagline">Building homes and business spaces across Paldi &amp; Vasna, Ahmedabad since 2013.</p>
  </div>
  <div class="footer-col"><h4>Navigation</h4><ul>{fnav}</ul></div>
  <div class="footer-col"><h4>Projects</h4><ul>{fprojects}</ul></div>
  <div class="footer-col"><h4>Office &amp; Contact</h4><div class="footer-address-block"><strong>{OFFICE[0]}</strong>{OFFICE[1]}<br><br><a href="{PHONE_HREF}">{PHONE}</a><br><br>GCCI Member &ndash; 33036<br>CREDAI / GIHED &ndash; 1417</div></div>
 </div>
 <div class="footer-bottom"><p>&copy; {date.today().year} Swastiik Group. All Rights Reserved.</p>
  <div class="footer-legal"><span>Details on this site are indicative and sourced from official project brochures; not to be treated as legal documents.</span></div></div>
</footer>
<script src="site.js"></script>
</body>
</html>
'''

def banner(title_html, lead, crumbs, img=None, extra=""):
    bg = f'<div class="hero-media"><img src="{img}" alt=""></div><div class="hero-overlay"></div>' if img else ""
    cr = " <span>/</span> ".join(f'<a href="{h}">{t}</a>' if h else t for t, h in crumbs)
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<header class="page-hero">{bg}<div class="container"><p class="crumbs">{cr}</p><h1>{title_html}</h1>{ld}{extra}</div></header>'

def card(p, tags=True):
    t = f' data-tags="all {p["status"]} {kind(p)}"' if tags else ""
    badge = "badge-ongoing" if p["status"] == "ongoing" else "badge-completed"
    return (f'<a class="project-card reveal" href="{url(p)}"{t}><div class="project-card-media"><img src="{p["images"][0]}" alt="{E(p["name"])} elevation" loading="lazy" width="600" height="800">'
            f'<span class="project-year-tag">{E(p["yearLabel"])}</span></div><div class="project-card-body">'
            f'<span class="badge {badge}">{E(p["statusLabel"])}</span><h3>{E(p["name"])}</h3>'
            f'<p class="project-card-meta">{E(p["config"])} &middot; {E(p["units"])}</p>'
            f'<p class="project-card-loc">{ico("map-pin")} {E(short_addr(p))}</p>'
            f'<span class="project-card-link">View Details {ico("arrow-right")}</span></div></a>')

def head(eyebrow, title, desc="", light=False):
    cl = " section-title-light" if light else ""
    st = ' style="color:var(--color-saffron)"' if light else ""
    ds = f'<p class="section-desc"{" style=color:rgba(255,255,255,.6)" if light else ""}>{desc}</p>' if desc else ""
    return f'<div class="section-header"><p class="section-eyebrow"{st}>{eyebrow}</p><h2 class="section-title{cl}">{title}</h2>{ds}</div>'

WHY = [("map-pin", "Prime, Central Locations", "Every project sits close to Jamalpur, Paldi, Kalupur and the Sabarmati Riverfront — established, well-connected neighbourhoods, not the city's edge."),
       ("shield-check", "Earthquake-Resistant RCC Structure", "Every building, from 2013's Vimal Apartments to today's Scarlet Homes, is built on a quality-controlled, earthquake-resistant RCC frame."),
       ("car", "Real Allotted Parking", "At least one dedicated car parking space per unit on every residential project, with basement and stack parking on our larger developments."),
       ("video", "CCTV &amp; Video Door Security", "24x7 CCTV surveillance in common areas and video door phones in-flat are standard across our residences, not an upsell."),
       ("ruler", "13 ft. Ground Floor Height", "Our current project, Scarlet Homes, is built with a generous 13 ft. ground floor height for a more open, airy arrival experience."),
       ("users", "The Same Engineers, Project After Project", "Structural engineer Achal Parikh has worked across the majority of our developments since 2013 — consistency you can trace across a decade.")]
def why_section():
    cards = "".join(f'<div class="whyus-card reveal"><div class="whyus-icon">{ico(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in WHY)
    return (f'<section class="whyus-section"><div class="yantra-lines"></div><div style="position:relative;z-index:1">'
            + head("Why Choose Us", "What Every Swastiik<br><em>Address Gets Right.</em>", "Points our own site plans and brochures have always led with — what's actually built into every project.", True)
            + f'</div><div class="whyus-grid">{cards}</div></section>')

def timeline(items, compact=False):
    out = []
    for p in items:
        im = "" if compact else f'<img src="{p["images"][0]}" alt="{E(p["name"])}" loading="lazy">'
        out.append(f'<div class="tl-item reveal"><div class="tl-year">{p["year"]}</div><div class="tl-card">{im}<div class="tl-body">'
                   f'<h3>{E(p["name"])}</h3><p>{E(p["type"])} &middot; {E(p["config"])} &middot; {E(p["units"])}</p>'
                   f'<p>{E(short_addr(p))}</p><a class="project-card-link" href="{url(p)}">View project {ico("arrow-right")}</a></div></div></div>')
    return f'<div class="timeline{" compact" if compact else ""}">{"".join(out)}</div>'

def gallery_items(items, tags=False):
    out = []
    for p in items:
        for im in p["images"]:
            t = f' data-tags="all {p["id"]}"' if tags else ""
            out.append(f'<a class="gallery-item reveal" href="{im}" data-lb data-cap="{E(p["name"])} · {p["year"]}"{t}><img src="{im}" alt="{E(p["name"])}, {p["year"]}" loading="lazy"><div class="gallery-caption">{E(p["name"])} &middot; {p["year"]}</div></a>')
    return "".join(out)

def cta(title="Interested in a home or space with us?", text="Call the team about current availability, floor plans and site visits."):
    return f'<section class="cta-band"><div class="container reveal"><h2>{title}</h2><p>{text}</p><a class="btn" href="{PHONE_HREF}">Call {PHONE}</a></div></section>'

pages = {}

# ---------------- HOME ----------------
slides = [
    ("images/projects/shomes_hero.jpg", "Currently Under Construction", "Scarlet Homes.<br><em>28 elegant 3 BHK homes.</em>", "Rajnagar Char Rasta, behind NID, Paldi.", url(ongoing), "View Scarlet Homes"),
    ("images/projects/sbh_hero_night.jpg", "Commercial · 2015", "Scarlet Business Hub.<br><em>An address built for business.</em>", "75 offices and 24 showrooms on Mahalaxmi Cross Road, Paldi.", "project-scarlet-business-hub.html", "View project"),
    ("images/projects/kesariaji_aerial.jpg", "Completed · 2024", "Kesariaji Flats.<br><em>Back where the story began.</em>", "21 homes opposite Vimal Apartment, near Hirabaug Crossing.", "project-kesariaji.html", "View project"),
    ("images/projects/amarjyot_dusk.jpg", "Swastiik Group — Building Since 2013", "Eight Real Projects.<br><em>One Growing Legacy in Paldi.</em>", "Residential and commercial developments across Paldi and Vasna, Ahmedabad.", "projects.html", "Explore All Projects"),
]
sl = ""
for i, (im, ey, ti, sub, href, lab) in enumerate(slides):
    tag = "h1" if i == 0 else "h2"
    sl += (f'<div class="slide{" active" if i == 0 else ""}"><div class="hero-media"><img src="{im}" alt="" {"" if i == 0 else "loading=lazy"}></div><div class="hero-overlay"></div>'
           f'<div class="hero-content"><p class="hero-eyebrow">{ey}</p><{tag} class="hero-title">{ti}</{tag}><p class="hero-sub">{sub}</p>'
           f'<div class="hero-actions"><a href="{href}" class="btn btn-primary">{lab}</a><a href="{PHONE_HREF}" class="btn btn-outline">Call {PHONE}</a></div></div></div>')
o = ongoing
home = f'''<section class="hero" id="hero">{sl}
<button class="hero-arrow prev" aria-label="Previous slide">{ico("chev-l")}</button><button class="hero-arrow next" aria-label="Next slide">{ico("chev-r")}</button>
<div class="hero-dots"></div><div class="hero-scroll-indicator"><span>Scroll</span><div class="scroll-line"></div></div></section>
<section class="stats-section"><div class="stats-grid">
<div class="stat-item"><span class="stat-number" data-count="{years}">0</span><span class="stat-suffix">+</span><p class="stat-label">Years Building in Ahmedabad</p></div>
<div class="stat-item"><span class="stat-number" data-count="{len(P)}">0</span><p class="stat-label">Real Projects, 2013–2024</p></div>
<div class="stat-item"><span class="stat-number" data-count="{total_units}">0</span><span class="stat-suffix">+</span><p class="stat-label">Homes &amp; Spaces Delivered</p></div>
<div class="stat-item"><span class="stat-display">1</span><p class="stat-label">Project Currently Under Construction</p></div></div></section>
<section class="section"><div class="container split">
<div class="split-media reveal"><img src="images/projects/vimal_hero.jpg" alt="Vimal Apartments, our first project" loading="lazy"></div>
<div class="reveal"><p class="section-eyebrow">About Swastiik Group</p><h2 class="section-title">Building Paldi &amp; Vasna,<br><em>one address at a time.</em></h2>
<p>Swastiik Group has been building homes and commercial spaces in Ahmedabad since 2013. Our first project, Vimal Apartments, was a ground-up redevelopment of twenty-four 3 BHK homes on Sanjivani Hospital Road, Jain Nagar.</p>
<p>Since then we have delivered {len(done)} projects across Paldi and Vasna — and we are building Scarlet Homes behind NID today. Every page here is drawn from our official project brochures.</p>
<a class="btn btn-primary" href="about.html">Read Our Story</a></div></div></section>
<section class="spotlight-section"><div class="spotlight-inner">
<div class="spotlight-media reveal"><img src="{o["images"][0]}" alt="{E(o["name"])} elevation"><span class="spotlight-tag">{E(o["statusLabel"])}</span></div>
<div class="spotlight-content reveal"><p class="section-eyebrow">Currently Working On</p><h2 class="section-title">{E(o["name"])}<br><em>{E(o["config"])}</em></h2>
<p class="spotlight-desc">{E(o["description"])}</p>
<div class="spotlight-facts"><div class="spotlight-fact"><span>{E(o["units"])}</span><p>Units</p></div><div class="spotlight-fact"><span>{o["year"]}</span><p>Launch Year</p></div><div class="spotlight-fact"><span>{E(o["type"])}</span><p>Type</p></div></div>
<p class="spotlight-address">{ico("map-pin")} {E(o["address"])}</p><a class="btn btn-primary" href="{url(o)}">View Full Details</a></div></div></section>
<section class="section">{head("2013 — 2024", "Our Legacy,<br><em>Project by Project.</em>", "Seven completed developments, shown in the order they were built.")}
<div class="projects-grid">{"".join(card(p, False) for p in done[-4:])}</div>
<p class="center mt-2"><a class="btn btn-dark" href="projects.html">View All Projects</a></p></section>
{why_section()}
<section class="section alt">{head("Our Journey", "A decade of<br><em>steady building.</em>")}{timeline(chrono[:3], True)}<p class="center"><a class="btn btn-dark" href="journey.html">See the Full Journey</a></p></section>
<section class="section">{head("Real Projects, Real Photographs", "Across Every<br><em>Address We've Built.</em>", "Every image is taken from the official brochure of the project shown.")}
<div class="gallery-masonry">{gallery_items([chrono[i] for i in (7, 1, 6, 5)])}</div><p class="center mt-2"><a class="btn btn-dark" href="photo.html">View All Photos</a></p></section>
{cta()}'''
pages["index.html"] = shell("index.html", "Swastiik Group | Real Estate Developers in Paldi, Ahmedabad",
    "Swastiik Group has been building homes and commercial spaces across Paldi and Vasna, Ahmedabad since 2013 — from Vimal Apartments to the ongoing Scarlet Homes.", home, "index.html", splash=True)

# ---------------- ABOUT ----------------
rows = "".join(f'<tr><td><a href="{url(p)}">{E(p["name"])}</a></td><td>{p["year"]}</td><td>{E(p["developer"])}</td><td>{E(p["architect"])}</td><td>{E(p["structural"])}</td></tr>' for p in chrono)
about = banner("About <em>Swastiik Group</em>", "Real homes and business spaces in Paldi and Vasna, Ahmedabad — built since 2013.", [("Home", "index.html"), ("About", None)], "images/projects/sbh_hero_day.jpg") + f'''
<section class="section"><div class="container split"><div class="reveal"><p class="section-eyebrow">Our Story</p><h2 class="section-title">Where it started,<br><em>and where we are.</em></h2>
<p>In 2013 we redeveloped Vimal Apartments on Sanjivani Hospital Road, Jain Nagar — twenty-four 3 BHK homes with earthquake-resistant RCC framing, vitrified flooring and parking for every flat. That project set the template for the work that followed.</p>
<p>Our commercial landmark, Scarlet Business Hub, followed in 2015 on Mahalaxmi Cross Road. Residential projects at Suvidha, Shantivan, Vasna and Jain Nagar have followed since, and in 2024 Kesariaji Flats rose directly opposite Vimal Apartment.</p>
<p>Today we are building Scarlet Homes — 28 homes behind NID at Rajnagar Char Rasta, Paldi.</p></div>
<div class="split-media reveal"><img src="images/about.jpg" alt="Swastiik Group" loading="lazy" style="object-position:50% 18%"></div></div></section>
<section class="section alt">{head("Memberships", "Trusted <em>industry bodies.</em>")}<div class="container grid-3" style="max-width:820px;grid-template-columns:1fr 1fr"><div class="card reveal center"><h3>GCCI</h3><p class="lead-p" style="color:var(--color-ink-soft)">Member &ndash; <strong>33036</strong></p></div><div class="card reveal center"><h3>CREDAI / GIHED</h3><p class="lead-p" style="color:var(--color-ink-soft)">Member &ndash; <strong>1417</strong></p></div></div></section>
{why_section()}
<section class="section">{head("The Teams Behind Each Project", "Developers, architects &amp;<br><em>engineers.</em>", "Our projects have been delivered under several group entities, with a consistent structural engineering partner.")}
<div class="container"><div class="table-wrap reveal"><table class="data"><thead><tr><th>Project</th><th>Year</th><th>Developer</th><th>Architect</th><th>Structural Engineer</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
{cta()}'''
pages["about.html"] = shell("about.html", "About Us | Swastiik Group, Ahmedabad", "The story of Swastiik Group — residential and commercial real estate developers in Paldi and Vasna, Ahmedabad, since 2013.", about, "about.html", "images/projects/sbh_hero_day.jpg")

# ---------------- PROJECTS ----------------
chips = "".join(f'<button class="chip{" active" if f == "all" else ""}" data-filter="{f}">{l}</button>' for f, l in
                [("all", "All"), ("ongoing", "Ongoing"), ("completed", "Completed"), ("residential", "Residential"), ("commercial", "Commercial")])
pj = banner("Our <em>Projects</em>", "Eight developments across Paldi and Vasna — one under construction, seven completed.", [("Home", "index.html"), ("Projects", None)], "images/projects/shomes_terrace.jpg") + f'''
<section class="section"><div class="filters" data-filter-group="#pgrid">{chips}</div>
<div class="projects-grid" id="pgrid">{"".join(card(p) for p in reversed(chrono))}</div><p class="empty-note is-hidden">No projects in this category.</p></section>{cta()}'''
pages["projects.html"] = shell("projects.html", "Projects | Swastiik Group, Paldi & Vasna, Ahmedabad", "Browse all Swastiik Group residential and commercial projects in Paldi and Vasna, Ahmedabad — ongoing and completed.", pj, "projects.html")

# ---------------- JOURNEY ----------------
jr = banner("Our <em>Journey</em>", "Every project since 2013, in the order it was built.", [("Home", "index.html"), ("Journey", None)], "images/projects/vimal_hero.jpg") + f'<section class="section">{timeline(chrono)}</section>{cta()}'
pages["journey.html"] = shell("journey.html", "Our Journey 2013–2024 | Swastiik Group", "A timeline of every Swastiik Group project from Vimal Apartments (2013) to Scarlet Homes.", jr, "journey.html")

# ---------------- PHOTOS ----------------
pchips = '<button class="chip active" data-filter="all">All Photos</button>' + "".join(f'<button class="chip" data-filter="{p["id"]}">{E(p["name"])}</button>' for p in chrono)
ph = banner("Project <em>Photos</em>", "Every image is taken directly from the official brochure of the project shown.", [("Home", "index.html"), ("Photos", None)], "images/projects/amarjyot_dusk.jpg") + f'''
<section class="section"><div class="filters" data-filter-group="#ggrid">{pchips}</div><div class="gallery-masonry" id="ggrid">{gallery_items(chrono, True)}</div></section>{cta()}'''
pages["photo.html"] = shell("photo.html", "Photo Gallery | Swastiik Group", "Photographs of every Swastiik Group residential and commercial project in Ahmedabad.", ph, "photo.html")

# ---------------- PROJECT DETAIL PAGES ----------------
for i, p in enumerate(chrono):
    spec = [("Developer", p.get("developer")), ("Architect", p.get("architect")), ("Structural Engineer", p.get("structural")),
            ("Electrical Consultant", p.get("electrical")), ("Legal Advisor", p.get("legal")), ("RERA No.", p.get("rera")),
            ("Configuration", p["config"]), ("Units", p["units"]), ("Type", p["type"])]
    specs = "".join(f'<div class="spec-row"><span class="spec-label">{l}</span><span class="spec-value">{E(v)}</span></div>' for l, v in spec if v)
    am = "".join(f'<li>{ico("check-circle")} {E(a)}</li>' for a in p["amenities"])
    gl = "".join(f'<a href="{im}" data-lb data-cap="{E(p["name"])}"><img src="{im}" alt="{E(p["name"])} view {k + 1}" loading="lazy"></a>' for k, im in enumerate(p["images"]))
    ph_ = "".join(f'<div class="aside-row">{ico("phone")}<a href="{tel(x)}">{x}</a></div>' for x in phones(p))
    prev, nxt = chrono[i - 1] if i > 0 else None, chrono[i + 1] if i < len(chrono) - 1 else None
    pn = (f'<a href="{url(prev)}"><small>&larr; Previous</small><strong>{E(prev["name"])}</strong></a>' if prev else "<span></span>") + \
         (f'<a href="{url(nxt)}"><small>Next &rarr;</small><strong>{E(nxt["name"])}</strong></a>' if nxt else "<span></span>")
    badge = "badge-ongoing" if p["status"] == "ongoing" else "badge-completed"
    mp = "https://www.google.com/maps?q=" + re.sub(r"[^\w,]+", "+", p["address"]) + "&output=embed"
    meta = f'<div class="ph-meta"><span class="badge {badge}" style="background:rgba(255,255,255,.14);color:#fff">{E(p["statusLabel"])}</span><span>{E(p["yearLabel"])}</span><span>{E(p["config"])}</span><span>{E(p["units"])}</span></div>'
    body = banner(E(p["name"]), "", [("Home", "index.html"), ("Projects", "projects.html"), (E(p["name"]), None)], p["images"][0], meta) + f'''
<section class="section"><div class="container detail"><div>
<h2>About this project</h2><p class="lead-p">{E(p["description"])}</p>
<h2>Photographs</h2><div class="d-gallery">{gl}</div>
<h2>Amenities &amp; Features</h2><ul class="modal-amenities">{am}</ul>
<h2>Project Specifications</h2><div class="spec-grid">{specs}</div>
<h2>Location</h2><p class="aside-row">{ico("map-pin")} {E(p["address"])}</p><div class="map-box"><iframe src="{mp}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{E(p["name"])} location map"></iframe></div>
</div><aside><div class="aside-card"><h3>Contact</h3>{ph_}
<div class="aside-row">{ico("mail")}<a href="mailto:{p["email"]}">{p["email"]}</a></div><div class="aside-row">{ico("map-pin")}<span>{E(short_addr(p))}</span></div>
</div></aside></div></section>
<section class="section alt"><div class="container pn">{pn}</div></section>'''
    pages[url(p)] = shell(url(p), f'{p["name"]} | Swastiik Group', p["description"][:155].rsplit(" ", 1)[0] + "…", body, "projects.html", p["images"][0])

# ---------------- write ----------------
for f, c in pages.items():
    open(os.path.join(ROOT, f), "w", encoding="utf-8").write(c)
sm = "".join(f"<url><loc>{SITE}{f}</loc></url>" for f in pages)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
print(len(pages), "pages written;", total_units, "units;", years, "years")
