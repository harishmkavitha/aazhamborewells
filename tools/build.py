#!/usr/bin/env python3
# =============================================================================
# Aazham Borewells — build.py  (V1)
# One source of truth for the shared shell (head / nav / footer) and every
# page's content. Run:  python3 tools/build.py
# It writes real, crawlable HTML into each page (nav + footer are baked in,
# not fetched at runtime) plus sitemap.xml.
# =============================================================================
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {
    "name": "Aazham Borewells",
    "domain": "https://www.aazhamborewells.com",
    "tel_display": "+91 98400 55123",     # DEMO number — replace before launch
    "tel_e164": "+919840055123",
    "wa": "919840055123",
    "email": "hello@aazhamborewells.com",
    "email2": "enquiry@aazhamborewells.com",
    "addr_line": "No. 88, Arcot Road, Vadapalani",
    "addr_city": "Chennai",
    "addr_region": "TN",
    "addr_pin": "600026",
    "lat": 13.0503, "lng": 80.2121,
    "since": "1979",
    "years": "45",
}

# ---- inline icons (currentColor, 24px line art) -----------------------------
IC = {
"drill": '<path d="M7 2h7l3 3v4l-4 2v3l-3 8-3-8V2z" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linejoin="round"/><path d="M7 6h7M7 10h9" stroke="currentColor" stroke-width="1.4"/>',
"rig": '<path d="M4 21h16M6 21 12 4l6 17M9 12h6M8 15h8" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
"hammer": '<path d="M12 3v6M8 6h8M11 9h2v5h-2z" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linejoin="round"/><path d="M10 14h4l-1 7h-2z" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linejoin="round"/>',
"compressor": '<rect x="3" y="9" width="12" height="9" rx="1.5" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M15 12h3l3-3v9l-3-3h-3M6 9V5h5v4" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linejoin="round"/>',
"rain": '<path d="M7 14a4 4 0 0 1-.5-7.97A5 5 0 0 1 16 6a3.5 3.5 0 0 1 1 6.9" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/><path d="M8 18l-1 2M12 18l-1 2M16 18l-1 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
"soil": '<path d="M3 7h18M3 12h18M3 17h18M3 4h18v16H3z" stroke="currentColor" stroke-width="1.4" fill="none"/><circle cx="8" cy="9.5" r="1" fill="currentColor"/><circle cx="15" cy="14.5" r="1" fill="currentColor"/>',
"pipe": '<path d="M4 8h9a3 3 0 0 1 3 3v9M4 6v4M2 8h4M16 20v-4M14 22h4" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
"gauge": '<path d="M4 20a8 8 0 1 1 16 0" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/><path d="M12 20l4-5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="20" r="1.4" fill="currentColor"/>',
"pebbles": '<circle cx="8" cy="9" r="3" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="16" cy="8" r="2.4" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="14" cy="15" r="3.2" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="7" cy="16" r="2.2" stroke="currentColor" stroke-width="1.5" fill="none"/>',
"wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5l-6 6 2.4 2.4 6-6a4 4 0 0 0 5-5.4l-2.3 2.3-2-2 2.3-2.3z" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linejoin="round"/>',
"flask": '<path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 17l-5-8V3" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linejoin="round"/><path d="M7.5 14h9" stroke="currentColor" stroke-width="1.5"/>',
"pin": '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.4" stroke="currentColor" stroke-width="1.5" fill="none"/>',
"pump": '<rect x="4" y="10" width="8" height="11" rx="1" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M8 10V6h6a4 4 0 0 1 4 4M6 14h4M6 17h4" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/>',
"waves": '<path d="M3 8c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 13c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 18c2-2 4-2 6 0s4 2 6 0 4-2 6 0" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>',
"drop": '<path d="M12 3c3 4 6 7 6 10.5a6 6 0 0 1-12 0C6 10 9 7 12 3z" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linejoin="round"/>',
"gear": '<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
"refresh": '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 8M20 4v4h-4M20 12a8 8 0 0 1-13.7 5.6L4 16M4 20v-4h4" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
"bolt": '<path d="M13 2 4 14h6l-1 8 9-12h-6z" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linejoin="round"/>',
"clock": '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
"phone": '<path d="M5 3h3l2 5-2 1.5a11 11 0 0 0 5 5L18 12l4 2v3a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 1-2z" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linejoin="round"/>',
"mail": '<rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="m4 7 8 6 8-6" stroke="currentColor" stroke-width="1.5" fill="none"/>',
"shield": '<path d="M12 3 5 6v5c0 4 3 7.5 7 10 4-2.5 7-6 7-10V6l-7-3z" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linejoin="round"/><path d="m9 12 2 2 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>',
}
def icon(name, cls="svc-card__icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" aria-hidden="true">{IC.get(name,"")}</svg>'

# ---- SVG "plate" graphics used instead of stock photos ----------------------
def plate_strata(ratio="plate"):
    return f'''<svg class="plate {ratio}" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration of a borewell cross-section through soil strata to the water table">
  <rect width="400" height="300" fill="#221e18"/>
  <rect y="0" width="400" height="70" fill="#bd5327"/><rect y="70" width="400" height="46" fill="#a8471f"/>
  <rect y="116" width="400" height="52" fill="#c9992f"/><rect y="168" width="400" height="60" fill="#8a6a24"/>
  <rect y="228" width="400" height="72" fill="#1a6560"/>
  <g opacity=".28" fill="#000"><circle cx="60" cy="140" r="4"/><circle cx="330" cy="95" r="5"/><circle cx="150" cy="190" r="4"/><circle cx="270" cy="250" r="5"/><circle cx="90" cy="255" r="4"/></g>
  <rect x="188" y="0" width="24" height="228" fill="#e7e5df"/>
  <rect x="192" y="0" width="16" height="228" fill="#f4f2ee"/>
  <path d="M200 300c-14 0-24-10-24-24 0-13 16-30 24-39 8 9 24 26 24 39 0 14-10 24-24 24z" fill="#eafffb"/>
  <g stroke="#f4f2ee" stroke-width="2" opacity=".5"><line x1="176" y1="60" x2="150" y2="60"/><line x1="224" y1="120" x2="252" y2="120"/><line x1="176" y1="180" x2="150" y2="180"/></g>
</svg>'''

def plate_rig(ratio="plate"):
    return f'''<svg class="plate {ratio}" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration of a truck-mounted borewell drilling rig at work">
  <rect width="400" height="300" fill="#221e18"/>
  <rect y="210" width="400" height="90" fill="#2c271f"/>
  <g stroke="#3d3830" stroke-width="1"><line x1="0" y1="235" x2="400" y2="235"/><line x1="0" y1="262" x2="400" y2="262"/></g>
  <g stroke="#bd5327" stroke-width="6" fill="none" stroke-linejoin="round">
    <path d="M150 210 200 40 250 210M170 150 230 150M160 180 240 180M180 110 220 110"/>
  </g>
  <rect x="196" y="40" width="8" height="220" fill="#c9992f"/>
  <rect x="60" y="150" width="120" height="60" rx="6" fill="#96401d"/>
  <circle cx="88" cy="215" r="20" fill="#171410" stroke="#3d3830" stroke-width="4"/>
  <circle cx="150" cy="215" r="20" fill="#171410" stroke="#3d3830" stroke-width="4"/>
  <rect x="196" y="255" width="10" height="45" fill="#1a6560"/>
</svg>'''

def plate_water(ratio="plate"):
    return f'''<svg class="plate {ratio}" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration of clean groundwater flow and testing">
  <rect width="400" height="300" fill="#0f3f3b"/>
  <rect y="0" width="400" height="120" fill="#1a6560"/>
  <g stroke="#3f9089" stroke-width="4" fill="none" opacity=".8">
    <path d="M0 150c40-30 80-30 120 0s80 30 120 0 80-30 120 0"/>
    <path d="M0 190c40-30 80-30 120 0s80 30 120 0 80-30 120 0"/>
    <path d="M0 230c40-30 80-30 120 0s80 30 120 0 80-30 120 0"/>
  </g>
  <path d="M200 60c26 34 44 56 44 86a44 44 0 0 1-88 0c0-30 18-52 44-86z" fill="#eafffb" opacity=".92"/>
  <rect x="150" y="255" width="100" height="8" fill="#c9992f"/>
</svg>'''

PLATES = {"strata": plate_strata, "rig": plate_rig, "water": plate_water}

# ---- navigation data --------------------------------------------------------
DRILLING = [
    ("borewell-drilling-services", "Borewell Drilling Services"),
    ("borewell-rig-drilling-services", "Rig Drilling Services"),
    ("galaxy-drilling-services", "Galaxy Drilling Services"),
    ("dth-method-drilling-services", "DTH Method Drilling"),
    ("borewell-compressor-drilling", "Compressor Drilling"),
    ("borewell-rain-harvesting", "Rain Water Harvesting"),
    ("borewell-soil-test-and-pile-test", "Soil Test & Pile Test"),
    ("borewell-plumbing", "Borewell Plumbing"),
    ("borewell-water-yield", "Water Yield Test"),
    ("borewell-pebbles", "Gravel & Pebble Packing"),
    ("borewell-repair-and-maintenance", "Repair & Maintenance"),
    ("borewell-water-quality-and-quantity", "Water Quality & Quantity"),
    ("domestic-borewell-point-survey", "Point Survey"),
    ("borewell-installation-of-pumps", "Pump Installation"),
    ("borewell-groundwater-survey", "Groundwater Survey"),
]
CLEANING = [
    ("borewell-cleaning", "Borewell Cleaning"),
    ("borewell-cleaning-methods", "Cleaning Methods"),
    ("borewell-cleaning-process", "Cleaning Process"),
    ("borewell-pipe-line-cleaning", "Pipe Line Cleaning"),
    ("borewell-motor-line-cleaning", "Motor Line Cleaning"),
]

def wa_link(text):
    from urllib.parse import quote
    return f'https://wa.me/{SITE["wa"]}?text={quote(text)}'

# ---- shared shell -----------------------------------------------------------
def head(title, desc, slug, jsonld=None):
    url = SITE["domain"] + "/" + ("" if slug == "index" else slug + ".html")
    og = SITE["domain"] + "/assets/img/og-default.jpg"
    ld = ""
    if jsonld:
        ld = '\n  <script type="application/ld+json">' + json.dumps(jsonld, separators=(",", ":")) + '</script>'
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/css/main.css">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#221e18">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="{og}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">{ld}
</head>
<body>'''

LOGO_SVG = '''<svg viewBox="0 0 48 48" aria-hidden="true"><defs><clipPath id="lg"><rect x="4" y="4" width="40" height="40" rx="9"/></clipPath></defs><g clip-path="url(#lg)"><rect x="4" y="4" width="40" height="40" fill="#221e18"/><rect x="4" y="4" width="40" height="12" fill="#bd5327"/><rect x="4" y="16" width="40" height="8" fill="#c9992f"/><rect x="4" y="24" width="40" height="12" fill="#1a6560"/><rect x="22.4" y="4" width="3.2" height="30" fill="#f4f2ee"/><path d="M24 40c-2.6 0-4.6-2-4.6-4.6 0-2.4 3-5.7 4.6-7.4 1.6 1.7 4.6 5 4.6 7.4C28.6 38 26.6 40 24 40Z" fill="#f4f2ee"/></g></svg>'''

def nav(active):
    def li(slug, label, top=False):
        href = "index.html" if slug == "index" else slug + ".html"
        cls = ' class="is-active"' if slug == active else ''
        return f'<li><a href="{href}"{cls}>{label}</a></li>'

    def mega(items, klass, hub_slug, hub_label):
        links = "".join(f'<a class="mega__link" href="{s}.html">{l}</a>' for s, l in items)
        return (f'<div class="mega {klass}">'
                f'<div class="mega__grid">{links}'
                f'<a class="mega__all" href="{hub_slug}.html">{hub_label} \u2192</a>'
                f'</div></div>')

    drill_active = ' is-active' if active in dict(DRILLING) or active == "drilling-services" else ''
    clean_active = ' is-active' if active in dict(CLEANING) or active == "cleaning-services" else ''

    return f'''
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="topbar">
    <div class="container topbar__inner">
      <div class="topbar__set topbar__set--meta">
        <span>Vadapalani, Chennai</span>
        <span>Open Mon\u2013Sat, 8am\u20138pm</span>
      </div>
      <div class="topbar__set">
        <a href="mailto:{SITE['email']}">{SITE['email']}</a>
        <a href="tel:{SITE['tel_e164']}">{SITE['tel_display']}</a>
      </div>
    </div>
  </div>
  <nav class="site-nav" aria-label="Main">
    <div class="container site-nav__inner">
      <a class="site-nav__logo" href="index.html" aria-label="Aazham Borewells home">
        {LOGO_SVG}
        <span><b>Aazham</b>Borewells</span>
      </a>
      <button class="site-nav__toggle" type="button" aria-expanded="false" aria-controls="nav-list">
        <span class="visually-hidden">Menu</span>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
      <ul class="nav-list" id="nav-list">
        {li("index","Home")}
        {li("about","About")}
        <li>
          <button class="nav-list__btn{drill_active}" type="button" aria-expanded="false">Drilling
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
          </button>
          {mega(DRILLING,"mega--drilling","drilling-services","All drilling services")}
        </li>
        <li>
          <button class="nav-list__btn{clean_active}" type="button" aria-expanded="false">Cleaning
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
          </button>
          {mega(CLEANING,"mega--cleaning","cleaning-services","All cleaning services")}
        </li>
        {li("gallery","Gallery")}
        {li("testimonial","Testimonials")}
        {li("contact","Contact")}
        <li><a class="nav-cta" href="tel:{SITE['tel_e164']}">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">{IC['phone']}</svg>Call now</a></li>
      </ul>
    </div>
  </nav>'''

def footer():
    dcols = "".join(f'<li><a href="{s}.html">{l}</a></li>' for s, l in DRILLING[:8])
    ccols = "".join(f'<li><a href="{s}.html">{l}</a></li>' for s, l in CLEANING)
    socials = {
        "Twitter": 'M18 4h3l-7 8 8 8h-6l-4-5-5 5H4l7-8L4 4h6l4 5z',
        "Facebook": 'M14 9h3V6h-3c-2 0-3 1-3 3v2H8v3h3v6h3v-6h3l1-3h-4V9z',
        "Instagram": 'M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm5 5a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm5-1h.01',
    }
    soc = "".join(
        f'<a href="#" aria-label="{n}" target="_blank" rel="noopener"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="{p}"/></svg></a>'
        for n, p in socials.items())
    return f'''
  <footer class="site-footer">
    <div class="container site-footer__top">
      <div class="site-footer__cols">
        <div class="site-footer__brand">
          {LOGO_SVG}
          <p>Borewell drilling, cleaning and groundwater specialists working across Chennai and Tamil Nadu since {SITE['since']}.</p>
          <div class="site-footer__social">{soc}</div>
        </div>
        <div>
          <h4>Drilling</h4>
          <ul>{dcols}<li><a href="drilling-services.html">View all \u2192</a></li></ul>
        </div>
        <div>
          <h4>Cleaning</h4>
          <ul>{ccols}<li><a href="cleaning-services.html">View all \u2192</a></li></ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul>
            <li><a href="tel:{SITE['tel_e164']}">{SITE['tel_display']}</a></li>
            <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
            <li><a href="{wa_link('Hi Aazham Borewells, I would like a free site visit and quote.')}" target="_blank" rel="noopener">WhatsApp us</a></li>
            <li>{SITE['addr_line']},<br>{SITE['addr_city']}, Tamil Nadu {SITE['addr_pin']}</li>
          </ul>
          <ul style="margin-top:1rem">
            <li><a href="about.html">About</a></li>
            <li><a href="gallery.html">Gallery</a></li>
            <li><a href="testimonial.html">Testimonials</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="container site-footer__legal">
      <span>&copy; <span data-year>2026</span> {SITE['name']}. All rights reserved. Demo replica for design purposes.</span>
      <span><a href="privacy.html">Privacy Policy</a> &nbsp;\u00b7&nbsp; <a href="terms.html">Terms of Use</a></span>
    </div>
  </footer>
  <a class="wa-float" href="{wa_link('Hi Aazham Borewells, I would like to know more about your services.')}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a13 13 0 0 1-5-4.4c-.4-.6-1-1.5-1-2.9 0-1.3.7-2 1-2.3.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.2-.3.3-.1.6.2.3.7 1.2 1.5 1.9 1 .9 1.8 1.2 2.1 1.3.3.1.4.1.6-.1l.8-1c.2-.2.3-.2.6-.1l2 1c.3.1.4.2.5.3.1.2.1.6-.1 1.1z"/></svg>
  </a>
  <script src="assets/js/main.js"></script>
</body>
</html>'''

def page(slug, title, desc, body, jsonld=None):
    doc = head(title, desc, slug, jsonld) + nav(slug) + '\n  <main id="main">\n' + body + '\n  </main>\n' + footer()
    with open(os.path.join(ROOT, ("index.html" if slug == "index" else slug + ".html")), "w") as f:
        f.write(doc)

# reusable CTA band
def cta_band(head_txt="Need a borewell? Let's get you water.",
             sub="Free site visit and a written, itemised quote across Chennai. Talk to a specialist today — no call-centre, no obligation.",
             wa_msg="Hi Aazham Borewells, I'd like a free site visit and quote."):
    return f'''
    <section class="cta-band">
      <div class="container cta-band__inner">
        <div class="stack">
          <h2>{head_txt}</h2>
          <p>{sub}</p>
        </div>
        <div class="cta-band__actions">
          <a class="btn btn--on-dark" href="tel:{SITE['tel_e164']}">Call {SITE['tel_display']}</a>
          <a class="btn btn--ghost-dark" href="{wa_link(wa_msg)}" target="_blank" rel="noopener">WhatsApp a photo</a>
        </div>
      </div>
    </section>'''

def strata_rule():
    return '<div class="strata" aria-hidden="true"><span></span><span></span><span></span><span></span></div>'

# =============================================================================
#  SERVICE CONTENT  (original copy — not taken from the source site)
# =============================================================================
# Each entry: cat, icon, plate, tag(card), lede(hero sub), intro[paras],
# includes[], steps[(title,desc)] OR bestfor[], faqs[(q,a)]
SERVICES = {
"borewell-drilling-services": dict(cat="drilling", icon="drill", plate="rig",
  tag="New borewells for homes, farms and industry — sunk to the right depth, cased for a long life.",
  lede="New borewells for homes, farms, apartments and industry across Chennai — surveyed, drilled and cased to last.",
  intro=["A borewell is only as good as the decisions made before the rig arrives. We start with a groundwater point survey, agree a target depth and casing plan with you in writing, then drill with the method that suits your soil and access.",
         "Every job is handled by our own crew and machines — no sub-contracting — so the person who quotes the work is the person accountable for it."],
  includes=["Groundwater point survey before drilling","Written depth, casing and cost estimate","6.5\" and 7\" borewell diameters","ISI-marked PVC or MS casing pipe","Clean site handover and debris removal","Yield check and flushing on completion"],
  steps=[("Survey the point","A geological point survey fixes the most promising spot on your plot and an expected depth band."),
         ("Agree the plan","You get a written estimate: diameter, casing depth, per-foot rate and what happens if water comes early or late."),
         ("Drill & case","The rig sinks the bore, casing pipe is set through the loose top strata, and the walls are stabilised."),
         ("Flush & handover","We develop the bore, confirm the yield, and hand over a clean site with a depth record.")],
  faqs=[("How deep will my borewell need to go in Chennai?","It varies by locality and season — many Chennai borewells strike usable water between 180 and 400 feet, but a point survey gives a realistic band for your plot before you commit."),
        ("Do you give a written estimate?","Yes. Every borewell is quoted in writing with the per-foot rate, casing plan and diameter so there are no surprises after drilling starts.")]),

"borewell-rig-drilling-services": dict(cat="drilling", icon="rig", plate="rig",
  tag="Truck-mounted rig drilling — the fast, deep-reaching option for open sites.",
  lede="Truck-mounted rotary rigs for deep, high-output borewells where the site has vehicle access.",
  intro=["Our lorry-mounted rigs are the workhorse for deep borewells on open plots, farmland and commercial sites. They reach greater depths faster than manual methods and set casing cleanly through unstable ground.",
         "We run both slow-speed and high-speed rigs, and match the machine to your soil so you get depth without needless vibration to neighbouring structures."],
  includes=["Slow-speed and high-speed rig options","Depths suited to deep aquifers","Stable casing through loose strata","Suited to open and semi-open sites","Trained operator and support crew","Site restored after drilling"],
  steps=[("Access check","We confirm the rig can reach and stand safely, and plan pipe and spoil handling."),
         ("Set up & centre","The mast is raised and centred exactly over the surveyed point."),
         ("Drill to target","The bore is sunk to the agreed depth, with casing set as the top strata are passed."),
         ("Develop & test","We flush the bore and measure the discharge before handover.")],
  faqs=[("What is the difference between slow-speed and high-speed rigs?","Slow-speed rigs give more control in mixed or rocky ground; high-speed rigs are quicker in consistent formations. We pick based on your soil report and site."),
        ("How much space does a lorry rig need?","Enough for the truck to stand and raise its mast — roughly a single-lorry width with clear overhead. On tight urban plots we may recommend a compressor or manual method instead.")]),

"galaxy-drilling-services": dict(cat="drilling", icon="gear", plate="rig",
  tag="Compact Galaxy (slow-rig) machines for tight urban plots and low-vibration work.",
  lede="Compact 'Galaxy' slow-rig drilling for narrow city plots, low headroom and vibration-sensitive sites.",
  intro=["The Galaxy slow-rig is our answer to Chennai's tight residential plots. It is smaller and gentler than a full lorry rig, so it reaches spots a truck cannot and keeps vibration away from adjoining walls.",
         "We also run oil-engine Galaxy units for locations without reliable power, so drilling isn't held up by supply cuts."],
  includes=["Fits narrow gates and compounds","Low vibration near existing structures","Oil-engine option for no-power sites","Good control in mixed soils","Ideal for homes and small commercial","Minimal disturbance to neighbours"],
  bestfor=["Independent houses on compact plots","Sites with restricted gate width or headroom","Locations close to existing buildings","Areas with unreliable power supply","Repeat borewells near an existing structure"],
  faqs=[("Why choose a Galaxy rig over a lorry rig?","When access is tight or you're drilling close to existing walls, the Galaxy's smaller footprint and lower vibration make it the safer, more practical choice."),
        ("What is an oil-engine Galaxy unit?","It's a Galaxy rig driven by its own diesel engine rather than mains power, so we can drill at sites with no supply or frequent cuts.")]),

"dth-method-drilling-services": dict(cat="drilling", icon="hammer", plate="rig",
  tag="Down-the-hole hammer drilling — straight, fast bores through hard rock.",
  lede="Down-the-Hole (DTH) hammer drilling for fast, straight borewells through Chennai's hard granite formations.",
  intro=["DTH drilling drives a pneumatic hammer at the base of the drill string, breaking rock directly at the face. It's the most effective method through the hard granite and gneiss common under much of Chennai.",
         "Because the hammer sits down the hole, bores stay straight and true even at depth — which matters for pump installation and long-term casing life."],
  includes=["Efficient through hard rock","Straight, plumb bores at depth","Higher penetration rates","Lorry-mounted DTH available","Clean cuttings removal by air","Suited to deep, high-yield borewells"],
  steps=[("Assess the formation","We confirm rock type and depth so the hammer and bit are matched to the ground."),
         ("Position the rig","The DTH rig is set and centred over the surveyed point."),
         ("Hammer to depth","Compressed air drives the hammer; cuttings are lifted clear as the bore advances."),
         ("Case & develop","Casing is set through the top soil and the bore is flushed and yield-checked.")],
  faqs=[("Is DTH suitable for rocky Chennai soil?","Yes — DTH is the standard method for the hard rock found across much of Chennai and generally the fastest way through granite."),
        ("Does DTH keep the borehole straight?","Because the hammer works at the bottom of the hole, DTH bores stay notably straighter than some rotary methods, which helps pump alignment later.")]),

"borewell-compressor-drilling": dict(cat="drilling", icon="compressor", plate="rig",
  tag="Compressor-powered drilling for controlled, precise borewells — slow and high options.",
  lede="Compressor-based borewell drilling — precise, controlled sinking with slow and high-pressure options.",
  intro=["Compressor drilling uses high-pressure air to power the drill and lift cuttings, giving a clean, controlled bore. It's a versatile method that adapts well to both soft and hard strata.",
         "We offer slow-compressor drilling for careful work near structures and high-compressor drilling where speed and depth are the priority."],
  includes=["Slow and high compressor options","Clean cuttings evacuation","Good control in variable ground","Suited to homes and industry","Efficient in mixed formations","Consistent bore diameter"],
  bestfor=["Sites needing a clean, controlled bore","Mixed soft-and-hard strata","Homes where dust must be contained","Faster deep drilling (high compressor)","Careful work near existing borewells"],
  faqs=[("What decides slow versus high compressor drilling?","Ground conditions and how close you are to existing structures. Slow gives control; high gives speed and depth. We recommend based on your site."),
        ("Is compressor drilling dust-free?","No method is fully dust-free, but compressor drilling evacuates cuttings efficiently and we take steps to contain dust on residential sites.")]),

"borewell-rain-harvesting": dict(cat="drilling", icon="rain", plate="water",
  tag="Recharge structures that put rainwater back into your borewell and the water table.",
  lede="Rainwater harvesting and borewell recharge for homes, apartments, farms and industry across Chennai.",
  intro=["A borewell only lasts as long as the aquifer feeding it. Rainwater harvesting captures roof and surface runoff and channels it back into the ground — often directly to your borewell — instead of letting it drain to the street.",
         "In a city that swings between flood and drought, a well-built recharge pit is the single best thing you can do for the long-term yield of your borewell."],
  includes=["Rooftop and surface runoff capture","Recharge pits and recharge wells","Direct borewell recharge structures","Filter media and silt traps","Solutions for homes, apartments and farms","CMWSSB-aware design guidance"],
  bestfor=["Homes wanting a reliable borewell year-round","Apartments meeting harvesting rules","Farms recharging irrigation borewells","Industrial units managing large roof areas","Areas with falling water tables"],
  faqs=[("Will rainwater harvesting improve my borewell yield?","Over time, yes. Recharge structures raise the local water table and can noticeably improve a borewell's yield and reliability across seasons."),
        ("Is rainwater harvesting mandatory in Chennai?","Tamil Nadu requires rainwater harvesting for buildings. We design structures that both meet the requirement and actually recharge your borewell.")]),

"borewell-soil-test-and-pile-test": dict(cat="drilling", icon="soil", plate="strata",
  tag="Geotechnical soil investigation and pile load testing before you build.",
  lede="Soil investigation and pile load testing to give your structure a foundation you can trust.",
  intro=["Before a foundation is designed, you need to know what's under it. We carry out geotechnical soil testing — boring, sampling and analysis — to establish bearing capacity, water table and soil profile.",
         "For piled foundations we conduct pile load tests to confirm the pile performs to the design load, giving your engineer the data to sign off with confidence."],
  includes=["Soil boring and sampling","Bearing-capacity assessment","Water-table and strata logging","Pile load testing to design load","Reports for structural design","Home, commercial and industrial sites"],
  bestfor=["New home and villa construction","Apartment and commercial foundations","Industrial sheds and heavy plant","Compound and retaining structures","Any build needing a soil report"],
  faqs=[("Why do I need a soil test before building?","Foundation design depends on the soil's bearing capacity and water table. A soil test prevents costly settlement problems and lets your engineer design safely."),
        ("What is a pile load test?","It applies a controlled load to a test pile and measures settlement, confirming the pile can safely carry the load your structure will place on it.")]),

"borewell-plumbing": dict(cat="drilling", icon="pipe", plate="strata",
  tag="Leak-proof borewell plumbing — delivery lines, connections and fittings done right.",
  lede="Complete borewell plumbing — delivery lines, connections and fittings, built leak-proof and to last.",
  intro=["Getting water out of the ground is only half the job; getting it to your tank without leaks or pressure loss is the other half. We handle the full plumbing run from the borewell head to your storage.",
         "Good fittings, correct pipe sizing and clean joints are what separate a system that runs quietly for years from one that's forever being patched."],
  includes=["Delivery and suction line plumbing","Correct pipe sizing for your pump","Leak-proof, pressure-tested joints","Head assembly and control connections","Home, commercial and agricultural runs","Neat, accessible pipe routing"],
  bestfor=["New borewell connections","Homes upgrading old pipe runs","Farm irrigation delivery lines","Commercial and apartment systems","Fixing recurring leaks and pressure loss"],
  faqs=[("Can you connect my new borewell to my existing tank?","Yes — we plan and run the delivery line to your sump or overhead tank, size it for your pump, and pressure-test the joints before handover."),
        ("Do you fix leaking or low-pressure borewell plumbing?","We do. We trace the cause — undersized pipe, bad joints or a failing fitting — and rebuild the affected run properly rather than just patching it.")]),

"borewell-water-yield": dict(cat="drilling", icon="gauge", plate="water",
  tag="Yield and discharge testing so you know exactly how much water your borewell gives.",
  lede="Water yield and discharge testing — measured, documented figures for your borewell's real capacity.",
  intro=["Before you size a pump or plan an irrigation schedule, you need to know what your borewell actually delivers. We measure discharge over a controlled pumping test and record how the yield holds up over time.",
         "The result is a clear figure in litres per hour and a picture of whether the borewell sustains that rate or draws down — the data you need to invest sensibly."],
  includes=["Controlled continuous pumping test","Discharge measured in LPH","Drawdown and recovery observation","Aquifer performance assessment","Reports for pump sizing","Home, farm and industrial testing"],
  bestfor=["Choosing the right pump size","Planning farm irrigation","Buying or valuing a property","Diagnosing a weakening borewell","Industrial water-supply planning"],
  faqs=[("How is borewell yield measured?","We run a controlled pumping test, measure the steady discharge rate, and watch how the water level draws down and recovers to judge whether the yield is sustainable."),
        ("Why test yield before buying a pump?","An oversized pump on a low-yield borewell runs dry and burns out. A measured yield lets us match the pump to what the bore can actually sustain.")]),

"borewell-pebbles": dict(cat="drilling", icon="pebbles", plate="strata",
  tag="Gravel and pebble packing that filters silt and protects your casing.",
  lede="Gravel and pebble packing around your casing — a filter layer that keeps silt out and yield up.",
  intro=["Packing graded pebbles in the annulus around the casing does two quiet but important jobs: it filters fine sand and silt before they reach the pump, and it stabilises the borewell wall.",
         "Done with the right grade and quantity, gravel packing extends casing life, protects the pump, and keeps the water coming clean."],
  includes=["Graded, washed pebble media","Correct annulus packing depth","Silt and fine-sand filtration","Casing stabilisation","Home, commercial and industrial bores","Supplied and placed by our crew"],
  bestfor=["New borewells in sandy strata","Bores drawing silty or sandy water","Protecting a new submersible pump","Deep high-yield borewells","Any bore prone to sand ingress"],
  faqs=[("What do pebbles do in a borewell?","Graded pebbles packed around the casing act as a filter — they hold back sand and silt while letting water through — and they support the borewell wall."),
        ("Will gravel packing stop sandy water?","In sand-prone strata it makes a real difference, filtering fines before they reach your pump. We match the pebble grade to your soil for the best result.")]),

"borewell-repair-and-maintenance": dict(cat="drilling", icon="wrench", plate="rig",
  tag="Repairs and annual maintenance that keep drilling and cleaning equipment reliable.",
  lede="Borewell repair and annual maintenance — diagnose the fault, fix it properly, keep it running.",
  intro=["Borewells and their equipment don't fail on a convenient day. When yield drops, the pump trips or the line clogs, we diagnose the real cause rather than swapping parts and hoping.",
         "Our annual maintenance plans catch small problems — a worn fitting, a silting bore — before they become an expensive, waterless emergency."],
  includes=["Fault diagnosis and honest advice","Drilling equipment repair","Cleaning equipment servicing","Annual maintenance contracts","Priority response for AMC clients","Repairs to casing, head and lines"],
  bestfor=["Sudden drops in water supply","Pumps that trip or run dry","Bores that have started silting","Ageing borewells needing a check-up","Anyone wanting predictable upkeep"],
  faqs=[("My borewell yield suddenly dropped — what's wrong?","It could be silting, a falling water table, or a pump fault. We test the bore and the pump to find the actual cause before recommending any work."),
        ("What does an annual maintenance contract cover?","A scheduled inspection of the bore, pump and lines, priority response when something goes wrong, and early warning of problems while they're still cheap to fix.")]),

"borewell-water-quality-and-quantity": dict(cat="drilling", icon="flask", plate="water",
  tag="Lab water testing plus yield checks — is your water safe, and is there enough?",
  lede="Water quality and quantity testing — lab analysis for safety, yield checks for sufficiency.",
  intro=["Two questions decide whether a borewell is fit for use: is the water safe, and is there enough of it? We answer both. Lab analysis covers the chemical and bacterial quality; a yield test confirms the quantity.",
         "You get a clear report — what's in the water, whether it's fit to drink or needs treatment, and how much the bore reliably delivers."],
  includes=["Chemical water analysis","Bacterial / potability testing","TDS, hardness and pH checks","Discharge and yield measurement","Plain-language report and advice","Treatment recommendations if needed"],
  bestfor=["New borewells before first use","Drinking-water safety checks","Diagnosing taste, colour or odour","Property purchase due diligence","Industrial and food-grade supply"],
  faqs=[("How do I know if my borewell water is safe to drink?","Only a lab test can tell you for certain. We test for the chemical and bacterial parameters that matter and advise whether the water is potable or needs treatment."),
        ("Can you test both quality and quantity together?","Yes — we combine a lab water analysis with a yield test so you know in one visit both what's in the water and how much the bore gives.")]),

"domestic-borewell-point-survey": dict(cat="drilling", icon="pin", plate="strata",
  tag="Point surveys that find the best spot to drill — before you spend on a rig.",
  lede="Groundwater point surveys that locate the most promising drilling spot on your plot.",
  intro=["Where you drill decides what you get. Our point survey combines traditional water divining with scientific resistivity readings to identify the spot on your plot most likely to yield water — and at roughly what depth.",
         "Spending a little on a survey before drilling is the cheapest insurance there is against a dry or low-yield bore."],
  includes=["Traditional and scientific survey","Best drilling point marked on site","Likely depth band indicated","Survey for drilling and cleaning","Clear, on-the-spot guidance","Home and commercial plots"],
  bestfor=["Before drilling any new borewell","Plots where a previous bore failed","Deciding between two possible spots","Planning a cleaning or recharge point","Getting a realistic depth expectation"],
  faqs=[("Is a point survey really worth it?","A survey costs a fraction of a borewell. Drilling in the wrong spot can waste far more, so a survey is usually money well spent before you commit a rig."),
        ("What methods do you use for the survey?","We combine traditional divining with scientific resistivity readings, so the recommended point is backed by more than one method.")]),

"borewell-installation-of-pumps": dict(cat="drilling", icon="pump", plate="rig",
  tag="Submersible pump supply and installation, sized to your borewell's real yield.",
  lede="Submersible pump supply and installation — sized to your borewell, wired safely, set to last.",
  intro=["The wrong pump is the most common reason a good borewell disappoints. We size the pump to your bore's measured yield and depth, install it correctly, and wire the controls safely.",
         "From a single-phase home pump to a large industrial submersible, we supply, lower, connect and commission the whole system."],
  includes=["Pump sizing to measured yield","Quality submersible pumps","Correct cable and control panel","Safe lowering and connection","Commissioning and flow check","Home, commercial and industrial"],
  bestfor=["New borewells needing a pump","Replacing a failed or wrong-size pump","Upgrading to a higher-yield bore","Industrial and agricultural supply","Anyone with a pump that runs dry"],
  faqs=[("How do you choose the right pump for my borewell?","We base it on the bore's measured yield and depth, not guesswork. Matching the pump to what the bore sustains protects both the pump and your bill."),
        ("Do you supply the pump or just install it?","Either — we can supply a quality submersible matched to your bore, or install a pump you already have, wired and commissioned properly.")]),

"borewell-groundwater-survey": dict(cat="drilling", icon="waves", plate="strata",
  tag="Geophysical resistivity surveys that map groundwater before you drill.",
  lede="Scientific groundwater surveys using electrical resistivity to map water-bearing strata.",
  intro=["A groundwater survey reads the ground before you disturb it. Using electrical resistivity, we map the sub-surface layers and identify where water-bearing strata are most likely to sit — and how deep.",
         "It's the scientific backbone to a good drilling decision, giving you a depth expectation and the confidence to drill in the right place."],
  includes=["Electrical resistivity survey","Sub-surface strata mapping","Water-bearing zone identification","Depth expectation guidance","Home, farm and industrial plots","Report to guide drilling"],
  bestfor=["Large plots and farmland","Sites where drilling failed before","Industrial water-supply planning","Anyone wanting data before drilling","Comparing several possible spots"],
  faqs=[("How is a groundwater survey different from a point survey?","A point survey marks the best single spot to drill; a resistivity groundwater survey maps the strata across an area, which is valuable on larger or difficult plots."),
        ("Can a survey guarantee water?","No survey can promise water — nature has the final say — but a scientific survey markedly improves the odds and gives a realistic depth expectation.")]),

# ---------------------------------- CLEANING ---------------------------------
"borewell-cleaning": dict(cat="cleaning", icon="drop", plate="water",
  tag="Flushing that clears silt, mud, sand and yellow water to restore your yield.",
  lede="Borewell flushing and cleaning that clears silt, mud, sand and discoloured water — and brings the yield back.",
  intro=["When a borewell's flow drops or the water turns cloudy or yellow, the bore usually needs cleaning, not replacing. High-pressure flushing lifts out the silt, mud, dust and sand that have built up over the years.",
         "We handle slit, mud, yellow-water and dust cleaning — restoring flow and water quality for a fraction of the cost of a new borewell."],
  includes=["High-pressure compressor flushing","Slit, mud and sand removal","Yellow-water clearing","Dust and debris removal","Yield check after cleaning","Home, commercial and farm bores"],
  bestfor=["Borewells with a dropping yield","Cloudy, yellow or sandy water","Bores unused for a long time","Silted or muddy older borewells","Restoring flow before buying a new pump"],
  faqs=[("Can cleaning bring back a borewell that stopped giving water?","Often, yes. If the drop is from silting or blockage rather than a fallen water table, flushing frequently restores usable flow far more cheaply than a new bore."),
        ("Why has my borewell water turned yellow?","Usually silt, iron or fine sediment stirred into the water. Flushing clears the accumulated material; if it persists we test the water and advise on treatment.")]),

"borewell-cleaning-methods": dict(cat="cleaning", icon="gear", plate="water",
  tag="Hand, Galaxy and DTH cleaning methods — matched to your bore's condition.",
  lede="Three cleaning methods — hand, Galaxy slow-rig and DTH power-rig — matched to your borewell's condition.",
  intro=["Not every borewell needs the same treatment. A lightly silted home bore and a deep, badly blocked industrial one call for different tools. We run three methods and choose the right one for your bore.",
         "Hand (manual) cleaning for shallow, light work; Galaxy slow-rig for controlled mid-depth cleaning; and DTH power-rig for deep or stubborn blockages."],
  includes=["Hand / manual method cleaning","Galaxy slow-rig cleaning","DTH power-rig cleaning","Method matched to your bore","Depth-appropriate equipment","Yield check after every clean"],
  bestfor=["Shallow home bores (hand method)","Mid-depth controlled cleaning (Galaxy)","Deep or badly blocked bores (DTH)","Sites sensitive to vibration","Bores where a previous clean failed"],
  faqs=[("Which cleaning method does my borewell need?","It depends on depth and how badly it's blocked. We inspect first, then recommend hand, Galaxy or DTH cleaning — you're never sold more machine than the job needs."),
        ("Is DTH cleaning safe for an old borewell?","On a sound casing, yes — DTH clears deep, stubborn blockages. If we're concerned about the casing's condition, we'll tell you and suggest a gentler method.")]),

"borewell-cleaning-process": dict(cat="cleaning", icon="refresh", plate="water",
  tag="A clear step-by-step process for cleaning both old and new borewells.",
  lede="A clear cleaning process for both old and new borewells — inspect, flush, verify.",
  intro=["Whether it's a decades-old borewell that's slowed to a trickle or a new one that's throwing sand, our cleaning process follows the same disciplined sequence: understand the bore, clean it correctly, and prove the result.",
         "Old borewells often need patient de-silting and care around ageing casing; new borewells usually need developing and sand clearing. We handle both."],
  includes=["Inspection of bore and casing","Old-borewell de-silting","New-borewell development","Staged high-pressure flushing","Before-and-after yield check","Advice on keeping it clean"],
  steps=[("Inspect","We check depth, water level and casing condition to understand what we're dealing with."),
         ("Plan the clean","Old or new, silted or sandy — the bore's condition decides the method and the care needed."),
         ("Flush in stages","Staged high-pressure flushing lifts out silt, sand and debris without stressing the casing."),
         ("Verify & advise","We measure the restored yield and advise on how to keep the bore clean longer.")],
  faqs=[("Is cleaning an old borewell risky?","Old casings need care, which is exactly why we inspect first and choose a method that clears the bore without stressing ageing pipe."),
        ("Why does a new borewell need cleaning?","New bores often throw fine sand until they're properly developed. Developing and flushing settles this so your pump draws clean water.")]),

"borewell-pipe-line-cleaning": dict(cat="cleaning", icon="pipe", plate="water",
  tag="Pipeline flushing that clears sand, rust, algae and scale for full flow.",
  lede="Borewell pipeline cleaning that clears sand, silt, rust, algae and scale — for homes, farms, industry and metro lines.",
  intro=["Over time, delivery and supply lines fur up with sand, silt, rust, algae and mineral scale — quietly strangling your flow and pressure. Cleaning the pipeline restores the full bore of the pipe and the flow you're paying to pump.",
         "We clean home, commercial, agricultural, domestic, industrial and large metro pipelines, sizing the method to the run."],
  includes=["Sand, silt and rust removal","Algae and biofilm clearing","Mineral-scale descaling","Restored flow and pressure","Home to large metro pipelines","Minimal disruption to supply"],
  bestfor=["Dropping pressure at the tap","Discoloured water from the line","Long agricultural delivery runs","Apartment and commercial risers","Municipal and metro pipelines"],
  faqs=[("My pressure has dropped but the pump is fine — why?","Often the pipeline itself is the problem: scale, rust or algae narrowing the pipe. Cleaning the line restores the flow without touching the pump or bore."),
        ("Do you clean large agricultural and metro lines?","Yes — we scale the method and equipment to the run, from a home delivery pipe up to long agricultural and metro pipelines.")]),

"borewell-motor-line-cleaning": dict(cat="cleaning", icon="bolt", plate="water",
  tag="Suction and delivery line cleaning to protect your motor and keep flow strong.",
  lede="Motor suction and delivery line cleaning — clear the blockages that starve and strain your pump.",
  intro=["A borewell motor is only as healthy as the lines feeding and leaving it. A clogged suction line makes the pump work dry and hot; a scaled delivery line throttles its output. Cleaning both protects the motor and restores flow.",
         "We clear the suction and delivery lines so your pump runs cool, efficient and long."],
  includes=["Suction line cleaning","Delivery line cleaning","Blockage and scale removal","Reduced strain on the motor","Restored flow and efficiency","Home, commercial and farm pumps"],
  bestfor=["Motors that overheat or trip","Pumps drawing poorly","Scaled or clogged delivery lines","Older pump installations","Before fitting a replacement motor"],
  faqs=[("Can a dirty line damage my motor?","Yes — a blocked suction line can make a pump run dry and overheat, while a scaled delivery line overworks it. Cleaning the lines protects the motor and your bill."),
        ("How do I know the line and not the pump is the problem?","We test both. If the pump is sound but flow is poor, the suction or delivery line is usually the culprit — and cleaning it is far cheaper than a new pump.")]),
}

# =============================================================================
#  RENDERERS
# =============================================================================
def crumb(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
        if i < len(items) - 1:
            parts.append('<span aria-hidden="true">/</span>')
    return '<nav class="crumb" aria-label="Breadcrumb">' + "".join(parts) + '</nav>'

def related_grid(cat, exclude):
    src = DRILLING if cat == "drilling" else CLEANING
    picks = [(s, l) for s, l in src if s != exclude][:3]
    cards = ""
    for s, l in picks:
        d = SERVICES[s]
        cls = "svc-card--clean" if cat == "cleaning" else ""
        cards += f'''
        <a class="svc-card {cls}" href="{s}.html">
          {icon(d["icon"])}
          <h3 class="svc-card__title">{l}</h3>
          <p>{d["tag"]}</p>
          <span class="svc-card__more">Learn more \u2192</span>
        </a>'''
    return cards

def render_service(slug, label):
    d = SERVICES[slug]
    cat = d["cat"]
    clean = cat == "cleaning"
    hub = ("cleaning-services.html", "Cleaning Services") if clean else ("drilling-services.html", "Drilling Services")
    tickcls = "tick tick--aquifer" if clean else "tick"
    herocls = "page-hero page-hero--clean" if clean else "page-hero"
    title = f"{label} in Chennai | {SITE['name']}"
    desc = d["tag"] + f" {SITE['name']}, Chennai."
    desc = (desc[:154]).rsplit(" ", 1)[0] if len(desc) > 155 else desc

    intro = "".join(f"<p>{p}</p>" for p in d["intro"])
    includes = "".join(f"<li>{x}</li>" for x in d["includes"])
    plate = PLATES[d["plate"]]("plate")

    # steps or best-for block
    if d.get("steps"):
        items = "".join(f"<li><h4>{t}</h4><p>{x}</p></li>" for t, x in d["steps"])
        mid = f'''
    <section>
      <div class="container">
        <p class="{tickcls}">How the work runs</p>
        <h2 style="margin:.6rem 0 2rem">A clear process, start to finish</h2>
        <ol class="steps">{items}</ol>
      </div>
    </section>'''
    else:
        items = "".join(f"<li>{x}</li>" for x in d["bestfor"])
        mid = f'''
    <section>
      <div class="container">
        <p class="{tickcls}">When it's the right call</p>
        <h2 style="margin:.6rem 0 2rem">Best suited for</h2>
        <ul class="checks two-col">{items}</ul>
      </div>
    </section>'''

    faqs = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in d["faqs"])
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]}
    svc_ld = {"@context": "https://schema.org", "@type": "Service",
              "name": label, "areaServed": "Chennai, Tamil Nadu",
              "provider": {"@type": "LocalBusiness", "name": SITE["name"], "telephone": SITE["tel_e164"]},
              "description": d["lede"]}

    body = f'''
    <section class="{herocls}">
      <div class="container stack">
        {crumb([("Home","index.html"),(hub[1],hub[0]),(label,None)])}
        <p class="{tickcls}">{'Cleaning service' if clean else 'Drilling service'}</p>
        <h1>{label} in Chennai</h1>
        <p>{d["lede"]}</p>
        <div class="hero__actions" style="margin-top:1.5rem">
          <a class="btn" href="tel:{SITE['tel_e164']}">Call {SITE['tel_display']}</a>
          <a class="btn btn--ghost" href="{wa_link('Hi Aazham Borewells, I am enquiring about ' + label + '.')}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
        </div>
      </div>
    </section>
    {strata_rule()}

    <section>
      <div class="container">
        <div class="split{'' if clean else ' '}">
          <div class="stack">
            <p class="{tickcls}">Overview</p>
            <h2>What we do</h2>
            {intro}
          </div>
          <div class="split__media">{plate}</div>
        </div>
      </div>
    </section>

    <section class="logband is-flush">
      <div class="container" style="padding-block:var(--space-6)">
        <p class="{tickcls}">What's included</p>
        <h2 style="margin:.6rem 0 2rem">Every {label.lower()} job covers</h2>
        <ul class="checks two-col">{includes}</ul>
      </div>
    </section>
    {mid}

    <section class="is-flush" style="padding-block:var(--space-section)">
      <div class="container container--narrow">
        <p class="{tickcls}">Questions</p>
        <h2 style="margin:.6rem 0 1.5rem">Frequently asked</h2>
        <div class="faq">{faqs}</div>
      </div>
    </section>

    <section>
      <div class="container">
        <p class="{tickcls}">Related services</p>
        <h2 style="margin:.6rem 0 2rem">You might also need</h2>
        <div class="grid grid--3">{related_grid(cat, slug)}</div>
      </div>
    </section>
    {cta_band(wa_msg='Hi Aazham Borewells, I am enquiring about ' + label + '.')}'''
    page(slug, title, desc, body, jsonld={"@graph": [svc_ld, faq_ld]})

def render_hub(cat):
    clean = cat == "cleaning"
    src = CLEANING if clean else DRILLING
    slug = "cleaning-services" if clean else "drilling-services"
    name = "Cleaning Services" if clean else "Drilling Services"
    tickcls = "tick tick--aquifer" if clean else "tick"
    herocls = "page-hero page-hero--clean" if clean else "page-hero"
    lede = ("Flushing, method cleaning, pipeline and motor-line work to bring tired borewells back to full flow."
            if clean else
            "New borewells, surveys, pumps, harvesting and testing — the full drilling side of Aazham Borewells.")
    title = f"All Borewell {name} in Chennai | {SITE['name']}"
    desc = (f"Complete borewell {name.lower()} in Chennai from {SITE['name']}: "
            + ", ".join(l for _, l in src[:4]).lower() + " and more.")
    desc = desc[:154]
    cards = ""
    for s, l in src:
        d = SERVICES[s]
        cls = "svc-card--clean" if clean else ""
        cards += f'''
        <a class="svc-card {cls}" href="{s}.html">
          {icon(d["icon"])}
          <h3 class="svc-card__title">{l}</h3>
          <p>{d["tag"]}</p>
          <span class="svc-card__more">Learn more \u2192</span>
        </a>'''
    intro = ("A blocked or slow borewell is rarely a dead borewell. Our cleaning side clears the silt, sand, scale and blockages that throttle flow — and proves the result with a yield check."
             if clean else
             "From the first survey to the final pump connection, our drilling side handles the whole life of a borewell. Every job is done by our own crews and machines, quoted in writing, and built to last.")
    body = f'''
    <section class="{herocls}">
      <div class="container stack">
        {crumb([("Home","index.html"),(name,None)])}
        <p class="{tickcls}">{'Cleaning' if clean else 'Drilling'}</p>
        <h1>Borewell {name} in Chennai</h1>
        <p>{lede}</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container stack-lg">
        <div class="stack" style="max-width:60ch">
          <p class="{tickcls}">Overview</p>
          <h2>{'Bring your borewell back to life' if clean else 'Everything a borewell needs'}</h2>
          <p class="lede">{intro}</p>
        </div>
        <div class="grid grid--3">{cards}</div>
      </div>
    </section>
    {cta_band()}'''
    page(slug, title, desc, body,
         jsonld={"@context": "https://schema.org", "@type": "Service",
                 "name": f"Borewell {name}", "areaServed": "Chennai",
                 "provider": {"@type": "LocalBusiness", "name": SITE["name"]}})

# ---- LocalBusiness JSON-LD (home + contact) ---------------------------------
def local_business_ld():
    return {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
            "name": SITE["name"], "url": SITE["domain"] + "/",
            "telephone": SITE["tel_e164"], "email": SITE["email"],
            "image": SITE["domain"] + "/assets/img/og-default.jpg",
            "priceRange": "\u20b9\u20b9",
            "address": {"@type": "PostalAddress", "streetAddress": SITE["addr_line"],
                        "addressLocality": SITE["addr_city"], "addressRegion": SITE["addr_region"],
                        "postalCode": SITE["addr_pin"], "addressCountry": "IN"},
            "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
            "openingHours": "Mo-Sa 08:00-20:00",
            "areaServed": "Chennai, Tamil Nadu"}

def home_service_cards(src, clean=False):
    cards = ""
    for s, l in src:
        d = SERVICES[s]
        cls = "svc-card--clean" if clean else ""
        cards += f'''
        <a class="svc-card {cls}" href="{s}.html">
          {icon(d["icon"])}
          <h3 class="svc-card__title">{l}</h3>
          <p>{d["tag"]}</p>
          <span class="svc-card__more">Learn more \u2192</span>
        </a>'''
    return cards

def render_home():
    title = f"{SITE['name']} | Borewell Drilling & Cleaning in Chennai"
    desc = ("Aazham Borewells drills, cleans and maintains borewells across Chennai since 1979 — "
            "surveys, DTH & rig drilling, pumps, recharge and cleaning.")
    ruler_marks = [("0 m", ""), ("60 m", ""), ("120 m", ""), ("180 m", " ruler__mark--water"),
                   ("240 m", ""), ("300 m", "")]
    marks = "".join(f'<span class="ruler__mark{c}">{t}</span>' for t, c in ruler_marks)

    testimonial_teaser = '''
        <div class="grid grid--3">
          <figure class="quote"><div class="quote__stars" aria-label="5 out of 5">\u2605\u2605\u2605\u2605\u2605</div>
            <p>"They surveyed first, told us honestly it would be a deep bore, and hit water at 280 feet exactly as promised. No inflated bill afterwards."</p>
            <figcaption class="quote__who">Ramesh K.<span>Homeowner, Ashok Nagar</span></figcaption></figure>
          <figure class="quote"><div class="quote__stars" aria-label="5 out of 5">\u2605\u2605\u2605\u2605\u2605</div>
            <p>"Our apartment borewell had slowed to a trickle. Their cleaning crew flushed it and the flow came back the same day. Saved us a new borewell."</p>
            <figcaption class="quote__who">Lakshmi S.<span>Secretary, Velachery</span></figcaption></figure>
          <figure class="quote"><div class="quote__stars" aria-label="5 out of 5">\u2605\u2605\u2605\u2605\u2605</div>
            <p>"Professional from survey to pump. The written estimate matched the final bill to the rupee, which almost never happens with borewell work."</p>
            <figcaption class="quote__who">Arun P.<span>Builder, Porur</span></figcaption></figure>
        </div>'''

    body = f'''
    <section class="hero">
      <div class="container">
        <div class="hero__grid">
          <div>
            <p class="tick hero__eyebrow">Borewell specialists \u00b7 Chennai \u00b7 since {SITE['since']}</p>
            <h1>We go down until we find <em>water</em>.</h1>
            <p class="hero__lede">Surveying, drilling, cleaning and maintaining borewells across Chennai for {SITE['years']} years \u2014 with our own crews, our own machines, and a written quote you can hold us to.</p>
            <div class="hero__actions">
              <a class="btn btn--on-dark" href="tel:{SITE['tel_e164']}">Call {SITE['tel_display']}</a>
              <a class="btn btn--ghost-dark" href="drilling-services.html">Explore services</a>
            </div>
          </div>
          <div class="ruler" aria-hidden="true">
            <div class="ruler__fill"></div>
            {marks}
          </div>
        </div>
      </div>
    </section>

    <section class="logband is-flush">
      <div class="container">
        <div class="logband__grid">
          <div class="logstat"><b>{SITE['years']}<i>+</i></b><span>years drilling Chennai's ground</span></div>
          <div class="logstat"><b>9,000<i>+</i></b><span>borewells sunk and serviced</span></div>
          <div class="logstat"><b>20</b><span>drilling &amp; cleaning services</span></div>
          <div class="logstat"><b>1<i>-day</i></b><span>typical response for cleaning</span></div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="split">
          <div class="split__media about-figure">
            {PLATES['strata']('plate--tall')}
            <div class="about-figure__badge"><b>{SITE['since']}</b><span>drilling since</span></div>
          </div>
          <div class="stack">
            <p class="tick">Who we are</p>
            <h2>Two generations of getting Chennai its water</h2>
            <p>Aazham Borewells began in {SITE['since']} with a single rig and a simple promise: survey honestly, drill properly, and stand behind the result. Three decades on, that hasn't changed \u2014 we've just gone deeper, added cleaning and pump work, and kept every job in-house.</p>
            <p>The word <em>aazham</em> means <em>depth</em> in Tamil. It's what we're named for and what we're good at: reading the ground, choosing the right method, and going down until the water's there.</p>
            <p><a class="btn btn--ghost" href="about.html">More about us</a></p>
          </div>
        </div>
      </div>
    </section>

    {strata_rule()}
    <section>
      <div class="container stack-lg">
        <div class="stack" style="max-width:56ch">
          <p class="tick">Drilling</p>
          <h2>New borewells, done from survey to pump</h2>
          <p class="lede">Point surveys, rig, DTH and compressor drilling, pumps, recharge, testing and repair \u2014 the full drilling side.</p>
        </div>
        <div class="grid grid--3">{home_service_cards(DRILLING[:6])}</div>
        <p><a class="btn btn--ghost" href="drilling-services.html">View all 15 drilling services \u2192</a></p>
      </div>
    </section>

    <section class="logband is-flush" style="padding-block:var(--space-section)">
      <div class="container stack-lg">
        <div class="stack" style="max-width:56ch">
          <p class="tick tick--aquifer">Cleaning</p>
          <h2>Slow flow? Yellow water? Often it's just blocked</h2>
          <p class="lede">Before you pay for a new borewell, let us clean the one you have \u2014 flushing, pipeline and motor-line work that brings the yield back.</p>
        </div>
        <div class="grid grid--3">{home_service_cards(CLEANING, clean=True)}</div>
      </div>
    </section>

    <section>
      <div class="container">
        <p class="tick">How we work</p>
        <h2 style="margin:.6rem 0 2rem">Survey first. Quote in writing. Then drill.</h2>
        <ol class="steps grid grid--2" style="gap:2rem">
          <li><h4>Survey the ground</h4><p>A point survey fixes the best spot and a realistic depth before any machine moves.</p></li>
          <li><h4>Quote in writing</h4><p>Diameter, casing, per-foot rate and terms \u2014 agreed on paper, no surprises later.</p></li>
          <li><h4>Drill with the right method</h4><p>Rig, DTH, compressor or Galaxy, matched to your soil and access.</p></li>
          <li><h4>Test &amp; hand over clean</h4><p>We flush, check the yield, clear the site and leave you a depth record.</p></li>
        </ol>
      </div>
    </section>

    <section class="band-dark">
      <div class="container">
        <div class="split">
          <div class="stack">
            <p class="tick tick--light">Why Aazham</p>
            <h2>The reasons customers call us back</h2>
            <ul class="checks" style="margin-top:1rem">
              <li>Our own crews and machines \u2014 never sub-contracted</li>
              <li>Honest surveys: we'll tell you if a spot is poor</li>
              <li>Written estimates that match the final bill</li>
              <li>Both drilling and cleaning under one roof</li>
              <li>Fast response across Chennai, six days a week</li>
            </ul>
          </div>
          <div class="split__media">{PLATES['rig']('plate')}</div>
        </div>
      </div>
    </section>

    <section>
      <div class="container stack-lg">
        <div class="stack" style="max-width:56ch">
          <p class="tick tick--light">In their words</p>
          <h2>Trusted across the city</h2>
        </div>
        {testimonial_teaser}
        <p><a class="btn btn--ghost" href="testimonial.html">Read more reviews \u2192</a></p>
      </div>
    </section>
    {cta_band()}'''
    page("index", title, desc, body, jsonld=local_business_ld())

def render_about():
    title = f"About {SITE['name']} | Borewell Contractors in Chennai"
    desc = ("Aazham Borewells has drilled, cleaned and maintained borewells across Chennai since 1979 "
            "with in-house crews, honest surveys and written quotes.")
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        {crumb([("Home","index.html"),("About",None)])}
        <p class="tick">Since {SITE['since']}</p>
        <h1>Reading Chennai's ground for {SITE['years']} years</h1>
        <p>What started with one rig in {SITE['since']} is now a full borewell service \u2014 drilling, cleaning, pumps and recharge \u2014 still run the same honest way.</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container">
        <div class="split">
          <div class="stack">
            <p class="tick">Our story</p>
            <h2>Named for depth, built on trust</h2>
            <p>Aazham Borewells was founded in {SITE['since']} by a family that believed borewell work should be done honestly: survey before you drill, tell the customer the truth about their ground, and put the estimate in writing.</p>
            <p>Over {SITE['years']} years we've drilled through every kind of strata Chennai can throw at a bit \u2014 soft coastal sand, stubborn granite, mixed rock \u2014 and added the machines and methods to match: lorry rigs, DTH hammers, compressors and compact Galaxy units for tight city plots.</p>
            <p>Today we handle the whole life of a borewell, from the first survey to cleaning one that's decades old. Every job is done by our own people, because that's the only way to stand behind it.</p>
          </div>
          <div class="split__media">{PLATES['strata']('plate')}</div>
        </div>
      </div>
    </section>
    <section class="logband is-flush">
      <div class="container">
        <div class="logband__grid">
          <div class="logstat"><b>{SITE['years']}<i>+</i></b><span>years in the trade</span></div>
          <div class="logstat"><b>9,000<i>+</i></b><span>borewells drilled &amp; serviced</span></div>
          <div class="logstat"><b>100<i>%</i></b><span>work done in-house</span></div>
          <div class="logstat"><b>6</b><span>days a week across Chennai</span></div>
        </div>
      </div>
    </section>
    <section>
      <div class="container stack-lg">
        <div class="stack" style="max-width:56ch">
          <p class="tick">What we value</p>
          <h2>How we've stayed in business for {SITE['years']} years</h2>
        </div>
        <div class="grid grid--3">
          <article class="svc-card">{icon('pin')}<h3 class="svc-card__title">Survey before we sell</h3><p>We'd rather lose a job than drill a spot we don't believe in. The survey comes first, always.</p></article>
          <article class="svc-card">{icon('shield')}<h3 class="svc-card__title">Written, honest quotes</h3><p>The estimate you sign is the bill you pay. No mid-job surprises, no padded footage.</p></article>
          <article class="svc-card">{icon('wrench')}<h3 class="svc-card__title">Our own crews</h3><p>The person who quotes the work runs the work. Nothing is sub-contracted to strangers.</p></article>
          <article class="svc-card svc-card--clean">{icon('drop')}<h3 class="svc-card__title">Clean and cleaning</h3><p>We leave your site tidy \u2014 and we clean old borewells so you don't needlessly drill new ones.</p></article>
          <article class="svc-card">{icon('gauge')}<h3 class="svc-card__title">We prove the result</h3><p>Every borewell is flushed and yield-checked, so you know what you're getting before we leave.</p></article>
          <article class="svc-card">{icon('clock')}<h3 class="svc-card__title">We answer the phone</h3><p>A real person, fast response, six days a week. When your water stops, that matters.</p></article>
        </div>
      </div>
    </section>
    {cta_band()}'''
    page("about", title, desc, body, jsonld=local_business_ld())

def render_contact():
    title = f"Contact {SITE['name']} | Borewell Enquiries in Chennai"
    desc = (f"Contact Aazham Borewells in Vadapalani, Chennai for borewell drilling, cleaning and pump work. "
            f"Call {SITE['tel_display']}, WhatsApp, or send an enquiry.")
    maps_q = "Vadapalani,Chennai"
    all_services = [("", "Select a service\u2026")] + [(l, l) for _, l in DRILLING] + [(l, l) for _, l in CLEANING]
    opts = "".join(f'<option value="{html.escape(v)}"{" disabled selected" if v=="" else ""}>{l}</option>' for v, l in all_services)
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        {crumb([("Home","index.html"),("Contact",None)])}
        <p class="tick">Get in touch</p>
        <h1>Let's get you water</h1>
        <p>Free site visit and a written quote anywhere in Chennai. Call or WhatsApp for the fastest response, or send the form and we'll call you back.</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container">
        <div class="contact-grid">
          <div class="stack">
            <div class="info-row"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true">{IC['phone']}</svg>
              <div><b>Phone</b><a href="tel:{SITE['tel_e164']}">{SITE['tel_display']}</a><br><span style="color:var(--c-ink-soft);font-size:var(--t-sm)">Mon\u2013Sat, 8am\u20138pm</span></div></div>
            <div class="info-row"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true">{IC['drop']}</svg>
              <div><b>WhatsApp</b><a href="{wa_link('Hi Aazham Borewells, I would like a free site visit and quote.')}" target="_blank" rel="noopener">Message us a photo of your site</a></div></div>
            <div class="info-row"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true">{IC['mail']}</svg>
              <div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a><br><a href="mailto:{SITE['email2']}">{SITE['email2']}</a></div></div>
            <div class="info-row"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true">{IC['pin']}</svg>
              <div><b>Visit</b>{SITE['addr_line']},<br>{SITE['addr_city']}, Tamil Nadu {SITE['addr_pin']}</div></div>
            <div class="map-embed" style="margin-top:1.5rem">
              <iframe title="Map to Aazham Borewells, Vadapalani" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                src="https://maps.google.com/maps?q={maps_q}&t=&z=14&ie=UTF8&iwloc=&output=embed"></iframe>
            </div>
          </div>
          <div class="stack">
            <h2>Send an enquiry</h2>
            <p style="color:var(--c-ink-soft)">Tell us what you need and we'll call you back, usually the same day.</p>
            <form data-ajax-form action="https://example.com/your-form-endpoint" method="post" novalidate>
              <div class="form-row">
                <label class="field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>
                <label class="field"><span>Phone</span><input type="tel" name="phone" autocomplete="tel" required></label>
              </div>
              <label class="field"><span>Service needed</span><select name="service">{opts}</select></label>
              <label class="field"><span>Your locality in Chennai</span><input type="text" name="area" placeholder="e.g. Velachery, Porur, Anna Nagar"></label>
              <label class="field"><span>Message</span><textarea name="message" rows="4" placeholder="Depth needed, current problem, plot access\u2026"></textarea></label>
              <button class="btn" type="submit">Send enquiry</button>
              <p class="form-status" role="status" aria-live="polite"></p>
              <p style="font-size:var(--t-xs);color:var(--c-ink-soft)">By sending this form you agree to be contacted about your enquiry. See our <a href="privacy.html">Privacy Policy</a>.</p>
            </form>
          </div>
        </div>
      </div>
    </section>
    {cta_band(head_txt="Water trouble that can't wait?", sub="For emergencies \u2014 a borewell that's stopped, a pump that's failed \u2014 call us directly and we'll get a crew to you fast.")}'''
    page("contact", title, desc, body, jsonld=local_business_ld())

def render_gallery():
    title = f"Gallery | {SITE['name']} Borewell Work in Chennai"
    desc = ("See Aazham Borewells at work across Chennai \u2014 rig and DTH drilling, borewell cleaning, "
            "pump installation, recharge structures and more.")
    items = [
        ("rig", "Truck-mounted rig drilling a new borewell, Porur"),
        ("strata", "Reading the strata log during a point survey"),
        ("water", "Borewell flushed clean \u2014 clear water restored"),
        ("rig", "DTH hammer drilling through granite, Tambaram"),
        ("strata", "Casing pipe set through the loose top strata"),
        ("water", "Recharge pit feeding a home borewell, Adyar"),
        ("rig", "Submersible pump lowered and commissioned"),
        ("water", "Pipeline descaled and back to full flow"),
        ("strata", "Gravel packing graded and ready to place"),
    ]
    figs = ""
    for plate, cap in items:
        figs += f'<figure class="gallery-item">{PLATES[plate]("plate--wide")}<figcaption>{cap}</figcaption></figure>'
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        {crumb([("Home","index.html"),("Gallery",None)])}
        <p class="tick">On site</p>
        <h1>Our work around Chennai</h1>
        <p>A look at the drilling, cleaning and pump work we do week in, week out across the city and its outskirts.</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container stack-lg">
        <div class="gallery-grid">{figs}</div>
        <p style="font-size:var(--t-sm);color:var(--c-ink-soft);border-left:3px solid var(--c-ochre);padding-left:1rem">
          Note for launch: these are illustrated placeholders in the site's house style. Swap them for real, compressed WebP photos of your own jobs \u2014 same captions, real sites.</p>
      </div>
    </section>
    {cta_band()}'''
    page("gallery", title, desc, body)

def render_testimonials():
    title = f"Testimonials | {SITE['name']} Reviews in Chennai"
    desc = ("Read what Chennai homeowners, builders and businesses say about Aazham Borewells' drilling, "
            "cleaning and pump work.")
    reviews = [
        ("Ramesh K.", "Homeowner, Ashok Nagar", "They surveyed first, told us honestly it would be a deep bore, and hit water at 280 feet exactly as promised. The written estimate matched the final bill. Rare and refreshing."),
        ("Lakshmi S.", "Association Secretary, Velachery", "Our apartment borewell had slowed to a trickle. Their cleaning crew flushed it and the flow came back the same day. It saved the association the cost of a whole new borewell."),
        ("Arun P.", "Builder, Porur", "I've worked with a lot of borewell contractors. Aazham is the one I call back \u2014 own crews, on time, and they don't disappear when there's a problem."),
        ("Fathima R.", "Homeowner, Adyar", "The point survey was worth every rupee. A previous contractor drilled a dry hole nearby; Aazham found water on the first try with a proper survey."),
        ("Venkatesh M.", "Farm owner, Tiruvallur", "They fixed our irrigation yield with a good clean and the right pump. Water where we needed it, and honest advice on the recharge pit."),
        ("Priya D.", "Restaurant owner, T. Nagar", "Water quality test, cleaning and a new pump \u2014 all handled in two visits. Clear reports, clear pricing, and the water's been perfect since."),
        ("Suresh B.", "Homeowner, Tambaram", "DTH drilling through hard rock that another crew gave up on. Aazham's rig went straight down and we finally have a reliable borewell."),
        ("Meenakshi V.", "Apartment resident, Anna Nagar", "Booked a cleaning on WhatsApp in the morning, crew came the same afternoon. Professional, tidy, and the yellow water is gone."),
    ]
    cards = ""
    for who, role, txt in reviews:
        cards += f'''<figure class="quote"><div class="quote__stars" aria-label="5 out of 5">\u2605\u2605\u2605\u2605\u2605</div>
          <p>"{txt}"</p><figcaption class="quote__who">{who}<span>{role}</span></figcaption></figure>'''
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        {crumb([("Home","index.html"),("Testimonials",None)])}
        <p class="tick">In their words</p>
        <h1>What Chennai says about us</h1>
        <p>Homeowners, builders, farms and businesses \u2014 here's what people tell us after the water's flowing.</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container">
        <div class="grid grid--3">{cards}</div>
      </div>
    </section>
    {cta_band(head_txt="Ready to join them?", sub="Book a free site visit and see why Chennai has trusted us with its borewells for over four decades.")}'''
    page("testimonial", title, desc, body)

def render_privacy():
    title = f"Privacy Policy | {SITE['name']}"
    desc = "How Aazham Borewells collects, uses and protects the personal data you share through this website, in line with India's DPDP Act, 2023."
    updated = "August 2026"
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        {crumb([("Home","index.html"),("Privacy Policy",None)])}
        <p class="tick">Legal</p>
        <h1>Privacy Policy</h1>
        <p>How we handle the personal information you share with us. Last updated {updated}.</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container container--narrow stack">
        <p style="border-left:3px solid var(--c-ochre);padding-left:1rem;color:var(--c-ink-soft);font-size:var(--t-sm)">
          This is a starting-draft policy for a demo site. Before you publish, have it reviewed against the Digital Personal Data Protection Act, 2023, and insert your real grievance officer's name and contact details.</p>
        <h2>What we collect</h2>
        <p>When you use this site we may collect: your name, phone number, email address and message when you submit the enquiry form; and standard analytics identifiers (such as your approximate location and the pages you view) if analytics is enabled.</p>
        <h2>Why we collect it</h2>
        <p>We use your contact details only to respond to your enquiry, provide a quote, and arrange a site visit or service. Analytics data, where collected, helps us understand which services people look for so we can improve the site.</p>
        <h2>Your consent</h2>
        <p>By submitting the enquiry form you consent to us contacting you about your request. Consent is the basis on which we process your personal data, and you may withdraw it at any time by contacting us \u2014 we will then stop processing your data and delete it unless we are required to keep it.</p>
        <h2>Your rights</h2>
        <p>Under the Digital Personal Data Protection Act, 2023, you have the right to access the personal data we hold about you, to have it corrected or completed, to have it erased, to grievance redressal, and to nominate another person to exercise your rights in the event of death or incapacity.</p>
        <h2>How long we keep it</h2>
        <p>We keep enquiry details only as long as needed to serve you and to maintain a basic record of the work, after which they are deleted. We do not sell your data.</p>
        <h2>Who else sees it</h2>
        <p>Your data may be handled by the form-delivery service that carries your enquiry to us and, if enabled, an analytics provider. We share it with no one else for marketing.</p>
        <h2>Grievance officer</h2>
        <p>For any privacy question or complaint, contact our grievance officer:<br>
        <strong>[Insert name]</strong>, {SITE['name']}<br>
        {SITE['addr_line']}, {SITE['addr_city']}, Tamil Nadu {SITE['addr_pin']}<br>
        <a href="mailto:{SITE['email']}">{SITE['email']}</a> \u00b7 <a href="tel:{SITE['tel_e164']}">{SITE['tel_display']}</a></p>
        <h2>Changes</h2>
        <p>We may update this policy from time to time. The date at the top shows when it was last revised.</p>
      </div>
    </section>'''
    page("privacy", title, desc, body)

def render_terms():
    title = f"Terms of Use | {SITE['name']}"
    desc = "The terms on which Aazham Borewells provides this website and its borewell drilling, cleaning and related services."
    updated = "August 2026"
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        {crumb([("Home","index.html"),("Terms of Use",None)])}
        <p class="tick">Legal</p>
        <h1>Terms of Use</h1>
        <p>The terms on which we offer this website and our services. Last updated {updated}.</p>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container container--narrow stack">
        <p style="border-left:3px solid var(--c-ochre);padding-left:1rem;color:var(--c-ink-soft);font-size:var(--t-sm)">
          Demo starting-draft terms. Have them reviewed by a professional and tailored to your actual services and warranties before publishing.</p>
        <h2>About this website</h2>
        <p>This website provides information about the borewell drilling, cleaning, pump and related services offered by {SITE['name']}, based in {SITE['addr_city']}. By using the site you accept these terms.</p>
        <h2>Information, not a guarantee</h2>
        <p>Depths, yields, timelines and prices mentioned on this site are general guidance. Groundwater is variable by its nature: no borewell contractor can guarantee that water will be found at a particular depth, or at all. Firm terms for any job are set out in the written estimate we give you.</p>
        <h2>Quotes and work</h2>
        <p>Any quotation we provide is based on the site information available at the time and the method agreed. If ground conditions differ materially once work begins, we will discuss and agree any change with you before proceeding.</p>
        <h2>Your responsibilities</h2>
        <p>You are responsible for providing safe site access, confirming plot boundaries and the drilling location, and disclosing any underground cables, pipes or structures known to you before work begins.</p>
        <h2>Enquiries</h2>
        <p>Enquiries submitted through this site are handled in line with our <a href="privacy.html">Privacy Policy</a>. Submitting an enquiry does not by itself create a contract for work.</p>
        <h2>Intellectual property</h2>
        <p>The design, text and graphics on this website belong to {SITE['name']} and may not be copied or reused without permission.</p>
        <h2>Contact</h2>
        <p>Questions about these terms? Reach us at <a href="mailto:{SITE['email']}">{SITE['email']}</a> or <a href="tel:{SITE['tel_e164']}">{SITE['tel_display']}</a>.</p>
      </div>
    </section>'''
    page("terms", title, desc, body)

def render_404():
    title = f"Page not found | {SITE['name']}"
    desc = "The page you were looking for could not be found. Explore our borewell drilling and cleaning services or get in touch."
    body = f'''
    <section class="page-hero">
      <div class="container stack">
        <p class="tick">Error 404</p>
        <h1>This bore came up dry</h1>
        <p>The page you were looking for isn't here \u2014 it may have moved or the link may be mistyped. Let's get you back to water.</p>
        <div class="hero__actions" style="margin-top:1rem">
          <a class="btn btn--on-dark" href="index.html">Back to home</a>
          <a class="btn btn--ghost-dark" href="contact.html">Contact us</a>
        </div>
      </div>
    </section>
    {strata_rule()}
    <section>
      <div class="container stack-lg">
        <div class="stack" style="max-width:56ch">
          <p class="tick">Popular services</p>
          <h2>Try one of these instead</h2>
        </div>
        <div class="grid grid--3">
          {home_service_cards(DRILLING[:3])}
          {home_service_cards(CLEANING[:0])}
        </div>
        <div class="grid grid--3">
          <a class="svc-card" href="drilling-services.html">{icon('rig')}<h3 class="svc-card__title">All drilling services</h3><p>New borewells, surveys, pumps, recharge and testing.</p><span class="svc-card__more">Browse \u2192</span></a>
          <a class="svc-card svc-card--clean" href="cleaning-services.html">{icon('drop')}<h3 class="svc-card__title">All cleaning services</h3><p>Flushing, pipeline and motor-line cleaning.</p><span class="svc-card__more">Browse \u2192</span></a>
          <a class="svc-card" href="contact.html">{icon('phone')}<h3 class="svc-card__title">Talk to us</h3><p>Free site visit and a written quote across Chennai.</p><span class="svc-card__more">Contact \u2192</span></a>
        </div>
      </div>
    </section>'''
    page("404", title, desc, body)

# ---- sitemap ----------------------------------------------------------------
def write_sitemap(slugs):
    from datetime import date
    today = date.today().isoformat()
    urls = ""
    for s in slugs:
        loc = SITE["domain"] + "/" + ("" if s == "index" else s + ".html")
        pri = "1.0" if s == "index" else ("0.9" if s in ("drilling-services", "cleaning-services") else "0.7")
        urls += f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>\n'
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'.replace("sitemap.org", "sitemaps.org")
           + urls + '</urlset>\n')
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(xml)

# =============================================================================
#  RUN
# =============================================================================
def main():
    written = []
    # core
    render_home();        written.append("index")
    render_about();       written.append("about")
    render_gallery();     written.append("gallery")
    render_testimonials();written.append("testimonial")
    render_contact();     written.append("contact")
    render_privacy();     written.append("privacy")
    render_terms();       written.append("terms")
    # hubs
    render_hub("drilling"); written.append("drilling-services")
    render_hub("cleaning"); written.append("cleaning-services")
    # services
    for s, l in DRILLING + CLEANING:
        render_service(s, l); written.append(s)
    # 404 (not in sitemap)
    render_404()
    # sitemap uses public pages only, home first
    write_sitemap(written)
    print(f"Generated {len(written)+1} HTML pages (+ sitemap.xml).")
    print("Pages:", ", ".join(written))

if __name__ == "__main__":
    main()
