#!/usr/bin/env python3
# prepare_images.py (V1) — pick, resize, recompress and rename the client's
# photos into assets/img/photos/, and write image_manifest.json for build.py.
import os, glob, json
from PIL import Image

SRC = "/home/claude/imgsrc/aazhamborewells_images"
PROJ = "/home/claude/aazham-borewells"
OUT = os.path.join(PROJ, "assets/img/photos")
os.makedirs(OUT, exist_ok=True)

def fit_save(src, dst, max_w, q=82):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > max_w:
        h = int(h * max_w / w); w = max_w
        im = im.resize((w, h), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q, method=6)
    return w, h

def biggest(folder):
    """largest-area non-logo webp in a source folder"""
    best, area = None, -1
    for f in glob.glob(os.path.join(SRC, folder, "*.webp")):
        if "logo1_1" in f:
            continue
        try:
            w, h = Image.open(f).size
        except Exception:
            continue
        if w * h > area:
            best, area = f, w * h
    return best

# slug -> (source folder, explicit lead file or None=auto)
SVC_FOLDER = {
 "borewell-drilling-services": ("03_BOREWELL_DRILLING_SERVICES", None),
 "borewell-rig-drilling-services": ("06_BOREWELL_RIG_DRILLING_SERVICES", None),
 "galaxy-drilling-services": ("09_GALAXY_DRILLING_SERVICES", None),
 "dth-method-drilling-services": ("11_DTH_METHOD_DRILLING_SERVICES", None),
 "borewell-compressor-drilling": ("13_BOREWELL_COMPRESSOR_DRILLING", None),
 "borewell-rain-harvesting": ("16_BOREWELL_RAIN_HARVESTING", None),
 "borewell-soil-test-and-pile-test": ("21_BOREWELL_SOIL_TEST_&_PILE_TEST", None),
 "borewell-plumbing": ("26_BOREWELL_PLUMBING", None),
 "borewell-water-yield": ("31_BOREWELL_WATER_YIELD_TEST", None),
 "borewell-pebbles": ("36_BOREWELL_PEBBLES", None),
 "borewell-repair-and-maintenance": ("41_BOREWELL_REPAIR_&_MAINTENANCE", None),
 "borewell-water-quality-and-quantity": ("44_BOREWELL_WATER_QUALITY_&_QUANTITY", None),
 "domestic-borewell-point-survey": ("49_DOMESTIC_BOREWELL_POINT_SURVEY", None),
 "borewell-installation-of-pumps": ("52_BOREWELL_INSTALLATION_OF_PUMPS", None),
 "borewell-groundwater-survey": ("57_BOREWELL_GROUNDWATER_SURVEY", None),
 "borewell-cleaning": ("62_BOREWELL_CLEANING", None),
 "borewell-cleaning-methods": ("67_BOREWELL_CLEANING_METHODS", None),
 "borewell-cleaning-process": ("71_BOREWELL_CLEANING_PROCESS", None),
 "borewell-pipe-line-cleaning": ("74_BOREWELL_PIPE_LINE_CLEANING", None),
 "borewell-motor-line-cleaning": ("81_BOREWELL_MOTOR_LINE_CLEANING", None),
}
LABELS = {
 "borewell-drilling-services":"Borewell drilling services","borewell-rig-drilling-services":"Borewell rig drilling",
 "galaxy-drilling-services":"Galaxy rig drilling","dth-method-drilling-services":"DTH method drilling",
 "borewell-compressor-drilling":"Borewell compressor drilling","borewell-rain-harvesting":"Rainwater harvesting",
 "borewell-soil-test-and-pile-test":"Soil test and pile test","borewell-plumbing":"Borewell plumbing",
 "borewell-water-yield":"Borewell water yield test","borewell-pebbles":"Gravel and pebble packing",
 "borewell-repair-and-maintenance":"Borewell repair and maintenance","borewell-water-quality-and-quantity":"Water quality and quantity testing",
 "domestic-borewell-point-survey":"Borewell point survey","borewell-installation-of-pumps":"Borewell pump installation",
 "borewell-groundwater-survey":"Groundwater survey","borewell-cleaning":"Borewell cleaning",
 "borewell-cleaning-methods":"Borewell cleaning methods","borewell-cleaning-process":"Borewell cleaning process",
 "borewell-pipe-line-cleaning":"Borewell pipe line cleaning","borewell-motor-line-cleaning":"Borewell motor line cleaning",
}

manifest = {"services": {}, "home": {}, "hubs": {}, "gallery": [], "core": {}}

# --- services: lead (1400w) + thumb (640w) ---
for slug, (folder, explicit) in SVC_FOLDER.items():
    src = os.path.join(SRC, folder, explicit) if explicit else biggest(folder)
    lead = f"svc-{slug}.webp"; thumb = f"svc-{slug}-thumb.webp"
    w, h = fit_save(src, os.path.join(OUT, lead), 1400, 82)
    tw, th = fit_save(src, os.path.join(OUT, thumb), 640, 80)
    alt = f"{LABELS[slug]} in Chennai by Aazham Borewells"
    manifest["services"][slug] = {"lead": {"src": f"assets/img/photos/{lead}", "w": w, "h": h, "alt": alt},
                                   "thumb": {"src": f"assets/img/photos/{thumb}", "w": tw, "h": th, "alt": alt}}

# --- home hero / about / why ---
home_map = {
 "hero": ("01_Home/ChatGPT_Image_Feb_11_2026_05_01_44_PM.webp", 1600, "Borewell drilling rig striking water at a Chennai site"),
 "about": ("01_Home/about1.webp", 1200, "Aazham Borewells crew working on a borewell"),
 "why": ("01_Home/ChatGPT_Image_Feb_11_2026_12_53_20_PM.webp", 1200, "Borewell drilling rig and crew on site in Chennai"),
}
for key, (rel, mw, alt) in home_map.items():
    dst = f"home-{key}.webp"; w, h = fit_save(os.path.join(SRC, rel), os.path.join(OUT, dst), mw, 82)
    manifest["home"][key] = {"src": f"assets/img/photos/{dst}", "w": w, "h": h, "alt": alt}

# --- about page + contact side ---
core_map = {
 "about-story": ("02_About/about3.webp", 1200, "Aazham Borewells drilling rig at work"),
 "about-banner": ("02_About/banner1.webp", 1400, "Borewell drilling site managed by Aazham Borewells"),
 "contact": ("85_Contact/" + os.path.basename(biggest("85_Contact")), 1200, "Get in touch with Aazham Borewells, Chennai"),
}
for key, (rel, mw, alt) in core_map.items():
    src = os.path.join(SRC, rel)
    if not os.path.exists(src):
        src = biggest(rel.split("/")[0])
    dst = f"{key}.webp"; w, h = fit_save(src, os.path.join(OUT, dst), mw, 82)
    manifest["core"][key] = {"src": f"assets/img/photos/{dst}", "w": w, "h": h, "alt": alt}

# --- hubs ---
hub_map = {
 "drilling": ("06_BOREWELL_RIG_DRILLING_SERVICES/ChatGPT_Image_Feb_11_2026_12_59_52_PM.webp", 1400, "Borewell drilling services in Chennai"),
 "cleaning": (None, 1400, "Borewell cleaning services in Chennai"),
}
for key, (rel, mw, alt) in hub_map.items():
    src = os.path.join(SRC, rel) if rel else biggest("62_BOREWELL_CLEANING")
    if rel and not os.path.exists(src):
        src = biggest("06_BOREWELL_RIG_DRILLING_SERVICES")
    dst = f"hub-{key}.webp"; w, h = fit_save(src, os.path.join(OUT, dst), mw, 82)
    manifest["hubs"][key] = {"src": f"assets/img/photos/{dst}", "w": w, "h": h, "alt": alt}

# --- gallery: pick a diverse 12 spread across the folder ---
gal = sorted(f for f in glob.glob(os.path.join(SRC, "84_Gallery", "*.webp")) if "logo1_1" not in f)
pick = [gal[i] for i in range(0, len(gal), max(1, len(gal)//12))][:12]
caps = ["Rig drilling a new borewell on a city plot","Casing pipe set through the top strata",
        "Truck-mounted rig at a residential site","Borewell crew at work in a Chennai street",
        "Deep drilling in progress","Setting up the drilling mast",
        "Fresh borewell being developed","Compressor drilling on a compact plot",
        "New borewell point being drilled","Rig and support crew on site",
        "Borewell casing and pit work","Completed borewell handover"]
for i, src in enumerate(pick):
    dst = f"gallery-{i+1:02d}.webp"; w, h = fit_save(src, os.path.join(OUT, dst), 1000, 80)
    manifest["gallery"].append({"src": f"assets/img/photos/{dst}", "w": w, "h": h,
                                "alt": caps[i] + " — Aazham Borewells", "cap": caps[i]})

# --- OG image: crop hero to 1200x630 jpg ---
hero_src = os.path.join(SRC, "01_Home/ChatGPT_Image_Feb_11_2026_05_01_44_PM.webp")
im = Image.open(hero_src).convert("RGB")
tw, th = 1200, 630
r = max(tw/im.width, th/im.height)
im2 = im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)
left = (im2.width-tw)//2; top = (im2.height-th)//2
im2.crop((left, top, left+tw, top+th)).save(os.path.join(PROJ, "assets/img/og-default.jpg"), "JPEG", quality=86)

with open(os.path.join(PROJ, "tools/image_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)

# report
n = len(glob.glob(os.path.join(OUT, "*.webp")))
tot = sum(os.path.getsize(p) for p in glob.glob(os.path.join(OUT, "*.webp")))
print(f"Wrote {n} photos to assets/img/photos ({tot/1024/1024:.1f} MB) + og-default.jpg")
print("services:", len(manifest["services"]), "gallery:", len(manifest["gallery"]))
