"""Build a 5-slide professional PPT (Times New Roman, white background)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# ---------- palette ----------
NAVY = RGBColor(0x0E, 0x3A, 0x53)
TEAL = RGBColor(0x1B, 0x7F, 0x8E)
LIGHT = RGBColor(0xEA, 0xF4, 0xF6)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x5A, 0x5A, 0x5A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Times New Roman"

SW, SH = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]

# ---------- helpers ----------
def add_slide():
    return prs.slides.add_slide(BLANK)

def rect(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp

def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tb, tf

def set_run(r, text, size, bold=False, color=DARK, italic=False, name=FONT):
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = name
    rPr = r.font._rPr
    if rPr is not None:
        rPr.set("typeface", name)
    return r

def para(tf, first=False):
    if first and not tf.paragraphs[0].runs:
        return tf.paragraphs[0]
    return tf.add_paragraph()

def add_text(slide, x, y, w, h, lines, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT,
             space_after=4, line_spacing=1.0):
    tb, tf = textbox(slide, x, y, w, h, anchor)
    first = True
    for ln in lines:
        p = para(tf, first)
        first = False
        p.alignment = ln.get("align", align)
        p.space_after = Pt(ln.get("space_after", space_after))
        p.space_before = Pt(ln.get("space_before", 0))
        p.line_spacing = ln.get("line_spacing", line_spacing)
        r = p.add_run()
        set_run(r, ln["text"], ln.get("size", 18), ln.get("bold", False),
                ln.get("color", DARK), ln.get("italic", False))
    return tb

def add_bullets(slide, x, y, w, h, items, size=16, color=DARK, gap=6,
                line_spacing=1.05, bullet="\u2022  ", bcolor=TEAL):
    tb, tf = textbox(slide, x, y, w, h)
    first = True
    for it in items:
        p = para(tf, first)
        first = False
        p.space_after = Pt(gap)
        p.line_spacing = line_spacing
        r1 = p.add_run(); set_run(r1, bullet, size, True, bcolor)
        if isinstance(it, tuple):
            r2 = p.add_run(); set_run(r2, it[0], size, True, color)
            r3 = p.add_run(); set_run(r3, it[1], size, False, color)
        else:
            r2 = p.add_run(); set_run(r2, it, size, False, color)
    return tb

def style_cell(cell, text, size=12, bold=False, color=DARK, fill=None,
               align=PP_ALIGN.LEFT):
    cell.margin_left = Inches(0.08)
    cell.margin_right = Inches(0.08)
    cell.margin_top = Inches(0.03)
    cell.margin_bottom = Inches(0.03)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.fill.solid(); cell.fill.fore_color.rgb = fill if fill is not None else WHITE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run(); set_run(r, text, size, bold, color)

def header(slide, kicker, title, num):
    rect(slide, 0, 0, SW, Inches(0.16), TEAL)
    rect(slide, 0, Inches(0.16), Inches(0.16), Inches(0.62), NAVY)
    tb, tf = textbox(slide, Inches(0.55), Inches(0.42), SW - Inches(1.1), Inches(0.5))
    p = tf.paragraphs[0]
    r = p.add_run(); set_run(r, kicker.upper(), 12, True, TEAL)
    tb2, tf2 = textbox(slide, Inches(0.55), Inches(0.86), SW - Inches(1.1), Inches(0.85))
    p2 = tf2.paragraphs[0]
    r2 = p2.add_run(); set_run(r2, title, 30, True, NAVY)
    rect(slide, Inches(0.55), Inches(7.06), SW - Inches(1.1), Pt(1.2), LIGHT)
    tb3, tf3 = textbox(slide, Inches(0.55), Inches(7.12), Inches(9), Inches(0.3))
    p3 = tf3.paragraphs[0]
    r3 = p3.add_run(); set_run(r3, "Team AstroByte  \u2022  Bharatiya Antariksh Hackathon 2026  \u2022  Problem Statement PS-01", 10, False, GREY)
    tb4, tf4 = textbox(slide, SW - Inches(1.0), Inches(7.12), Inches(0.6), Inches(0.3))
    p4 = tf4.paragraphs[0]; p4.alignment = PP_ALIGN.RIGHT
    r4 = p4.add_run(); set_run(r4, str(num), 10, False, GREY)

def pic_fit(slide, path, x, y, h):
    """place picture keeping aspect, centred horizontally in a cell of width handled by caller"""
    im = Image.open(path)
    ar = im.size[0] / im.size[1]
    w = h * ar
    return slide.shapes.add_picture(path, x, y, height=h, width=w)

# =========================================================
# SLIDE 1 — Introduction
# =========================================================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
rect(s, 0, 0, Inches(0.22), SH, TEAL)
rect(s, Inches(0.22), 0, Inches(0.06), SH, NAVY)

tb, tf = textbox(s, Inches(0.9), Inches(1.1), Inches(11.4), Inches(1.9), MSO_ANCHOR.MIDDLE)
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "URBAN HEAT STRESS HOTSPOT DETECTION", 40, True, NAVY)
p2 = tf.add_paragraph(); p2.space_before = Pt(10)
r2 = p2.add_run(); set_run(r2, "AI/ML-Powered Geospatial Decision-Support & Cooling Strategy Optimization", 20, False, TEAL, True)

tb, tf = textbox(s, Inches(0.9), Inches(3.02), Inches(11.4), Inches(0.75))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "A satellite-driven machine-learning framework that detects urban heat-stress hotspots, "
                            "predicts land surface temperature (LST), explains heat drivers, and prioritises "
                            "cooling interventions for planners and decision-makers.", 15, False, DARK)
p.line_spacing = 1.15

info = [
    ("STUDY AREA", "Chhatrapati Sambhajinagar (Aurangabad), Maharashtra, India"),
    ("HACKATHON", "Bharatiya Antariksh Hackathon 2026 \u2014 Problem Statement PS-01"),
    ("TEAM", "AstroByte  (Srushti Bawaskar \u00b7 Priyal Deshmukh \u00b7 Rishika Deshmukh)"),
    ("PLATFORM", "Deployed Streamlit decision-support dashboard"),
]
y = 4.02
for k, v in info:
    tb, tf = textbox(s, Inches(0.9), Inches(y), Inches(1.9), Inches(0.4))
    p = tf.paragraphs[0]
    r = p.add_run(); set_run(r, k, 12.5, True, TEAL)
    tb, tf = textbox(s, Inches(2.95), Inches(y), Inches(9.35), Inches(0.4))
    p = tf.paragraphs[0]
    r = p.add_run(); set_run(r, v, 13, False, DARK)
    y += 0.52

tb, tf = textbox(s, Inches(0.9), Inches(6.35), Inches(11.4), Inches(0.6))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Objective:  address urban heat as a planning and decision-support problem \u2014 from detection to intervention prioritisation.", 13, True, NAVY)

# =========================================================
# SLIDE 2 — Working (How It Works)
# =========================================================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
header(s, "Working", "How the System Works", 2)

s.shapes.add_picture("workflow_diagram.png", Inches(0.45), Inches(1.72), width=Inches(12.45))

tb, tf = textbox(s, Inches(0.55), Inches(6.05), SW - Inches(1.1), Inches(0.95))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Workflow in brief:  satellite-derived indicators (Landsat 8/9 LST, Sentinel-2 NDVI/NDBI, SRTM elevation, "
                            "WorldPop population) are engineered into physical features; an XGBoost model predicts LST using "
                            "spatial block cross-validation; SHAP explains each prediction; hotspots and population-aware "
                            "vulnerability are mapped; cooling scenarios (greening, cool/permeable surfaces) are simulated, "
                            "and priority zones are delivered through an interactive dashboard.", 12.5, False, DARK)
p.line_spacing = 1.12

# =========================================================
# SLIDE 3 — Tech Stack, Technologies & Datasets
# =========================================================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
header(s, "Tech Stack & Technologies", "Technology Stack & Datasets", 3)

tb, tf = textbox(s, Inches(0.55), Inches(1.52), Inches(4.0), Inches(0.4))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Technology Stack", 16, True, NAVY)

logos = [
    ("image-search/python-programming-language-logo-icon-pn-1.png", "Python"),
    ("image-search/pandas-library-logo-icon-png-2.jpg", "Pandas"),
    ("image-search/xgboost-logo-icon-png-2.png", "XGBoost"),
    ("image-search/scikit-learn-logo-icon-png-3.png", "Scikit-learn"),
    ("image-search/google-earth-engine-logo-icon-png-2.png", "Google Earth Engine"),
    ("image-search/shap-explainable-ai-logo-icon-png-2.png", "SHAP"),
    ("image-search/streamlit-logo-icon-png-1.png", "Streamlit"),
    ("image-search/fastapi-logo-icon-png-2.png", "FastAPI"),
    ("image-search/qgis-logo-icon-png-2.png", "QGIS"),
]
cell_w, cell_h = Inches(2.78), Inches(1.5)
gx, gy = Inches(0.55), Inches(2.0)
logo_h = Inches(0.85)
for i, (path, label) in enumerate(logos):
    col, row = i % 3, i // 3
    x = gx + col * (cell_w + Inches(0.13))
    y = gy + row * (cell_h + Inches(0.08))
    rect(s, x, y, cell_w, cell_h, LIGHT)
    im = Image.open(path)
    ar = im.size[0] / im.size[1]
    lw = min(logo_h * ar, cell_w - Inches(0.25))
    lh = lw / ar
    lx = x + (cell_w - lw) / 2
    ly = y + (cell_h - lh) / 2
    pic_fit(s, path, lx, ly, lh)
    tb, tf = textbox(s, x, y + Inches(1.06), cell_w, Inches(0.4), MSO_ANCHOR.TOP)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); set_run(r, label, 11, True, NAVY)

tb, tf = textbox(s, Inches(9.35), Inches(1.52), Inches(3.95), Inches(0.4))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Datasets Used", 16, True, NAVY)

rows, cols = 7, 4
tbl_shape = s.shapes.add_table(rows, cols, Inches(9.35), Inches(2.0), Inches(3.95), Inches(3.3))
table = tbl_shape.table
table.columns[0].width = Inches(1.20)
table.columns[1].width = Inches(1.20)
table.columns[2].width = Inches(0.75)
table.columns[3].width = Inches(0.80)
headers = ["Parameter", "Dataset", "Resolution", "Purpose"]
data = [
    ("Land Surface Temp.", "Landsat 8/9 C2 L2", "30 m", "Surface heat & hotspots"),
    ("Vegetation", "Sentinel-2 SR", "10 m", "NDVI / cooling"),
    ("Built-up", "Sentinel-2 SR", "10\u201320 m", "NDBI / built-up"),
    ("Elevation", "SRTM", "30 m", "Terrain influence"),
    ("Population", "WorldPop India 2020", "100 m", "Exposure & vulnerability"),
    ("Land Cover", "Derived classification", "Variable", "Surface characterisation"),
]
for j, htext in enumerate(headers):
    style_cell(table.cell(0, j), htext, size=10.5, bold=True, color=WHITE, fill=NAVY)
for i, row in enumerate(data, start=1):
    fill = LIGHT if i % 2 == 0 else WHITE
    for j, val in enumerate(row):
        style_cell(table.cell(i, j), val, size=9.5, bold=(j == 0), fill=fill,
                   color=NAVY if j == 0 else DARK)

tb, tf = textbox(s, Inches(9.35), Inches(5.45), Inches(3.95), Inches(1.15))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Working dataset: ~9,900 sampled locations across the study area. "
                            "Lat/long used only for mapping \u2014 excluded from model inputs "
                            "to prevent location memorisation.", 10.5, False, DARK)
p.line_spacing = 1.08

tb, tf = textbox(s, Inches(0.55), Inches(6.72), Inches(6.6), Inches(0.3))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Also used:  NumPy \u00b7 Matplotlib \u00b7 Plotly \u00b7 Folium \u00b7 Joblib", 11.5, False, GREY, True)

# =========================================================
# SLIDE 4 — Impact, Benefits & Other Things
# =========================================================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
header(s, "Impact & Benefits", "Impact, Benefits & Outlook", 4)

cards = [
    ("R\u00b2 \u2248 0.51", "XGBoost model accuracy (spatial block CV)"),
    ("\u2248 1.78 \u00b0C", "Mean Absolute Error in LST prediction"),
    ("\u2248 2.26 \u00b0C", "Root Mean Squared Error"),
    ("Up to 0.84 \u00b0C", "Zone-level cooling potential under greening"),
    ("Top 10 / 96", "Priority heat-stress zones ranked for action"),
    ("~9,900", "Sampled locations analysed across the city"),
]
cw, ch = Inches(4.0), Inches(1.28)
for i, (big, small) in enumerate(cards):
    col, row = i % 3, i // 3
    x = Inches(0.55) + col * (cw + Inches(0.17))
    y = Inches(1.7) + row * (ch + Inches(0.14))
    rect(s, x, y, cw, ch, LIGHT)
    rect(s, x, y, Inches(0.07), ch, TEAL)
    tb, tf = textbox(s, x + Inches(0.22), y + Inches(0.12), cw - Inches(0.35), Inches(0.5))
    p = tf.paragraphs[0]
    r = p.add_run(); set_run(r, big, 19, True, NAVY)
    tb, tf = textbox(s, x + Inches(0.22), y + Inches(0.6), cw - Inches(0.35), Inches(0.62), MSO_ANCHOR.TOP)
    p = tf.paragraphs[0]
    r = p.add_run(); set_run(r, small, 10.5, False, DARK)
    p.line_spacing = 1.05

tb, tf = textbox(s, Inches(0.55), Inches(5.58), Inches(6.0), Inches(0.4))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Key Benefits", 15, True, NAVY)
add_bullets(s, Inches(0.55), Inches(6.0), Inches(6.0), Inches(1.0), [
    "Detects & ranks urban heat-stress hotspots across the city",
    "Identifies physical drivers of heat using SHAP explainability",
    "Distinguishes hottest zones from most vulnerable (population-aware) zones",
    "Simulates cooling scenarios and recommends interventions per zone",
], size=11.5, gap=3)

tb, tf = textbox(s, Inches(6.95), Inches(5.58), Inches(5.85), Inches(0.4))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Other Things", 15, True, NAVY)
add_bullets(s, Inches(6.95), Inches(6.0), Inches(5.85), Inches(1.0), [
    "Aligned with ISRO/Indian EO \u2014 Bhuvan, NRSC LULC, MOSDAC, TRISHNA-ready",
    "Deployed interactive Streamlit dashboard for planners & researchers",
    "Limitations: LST \u2260 air temperature; scenario values are model estimates",
    "Future scope: more cities, socio-economic indicators, cost & feasibility scoring",
], size=11.5, gap=3)

# =========================================================
# SLIDE 5 — References
# =========================================================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
header(s, "References", "References & Data Sources", 5)

refs = [
    "Landsat 8/9 Collection 2 Level-2 Land Surface Temperature product \u2014 USGS / NASA Earthdata.",
    "Sentinel-2 Surface Reflectance Harmonized \u2014 ESA Copernicus Programme (NDVI, NDBI).",
    "Shuttle Radar Topography Mission (SRTM) Digital Elevation Model \u2014 NASA / USGS.",
    "WorldPop India 2020 population dataset \u2014 University of Southampton (100 m resolution).",
    "Bhuvan / NRSC Land Use-Land Cover layers and MOSDAC meteorological datasets \u2014 ISRO, India (future integration references).",
    "TRISHNA thermal-infrared mission concept \u2014 ISRO / CNES for high-resolution urban thermal monitoring.",
    "Bharatiya Antariksh Hackathon 2026, Problem Statement PS-01 \u2014 Optimizing Urban Heat Mitigation and Cooling Strategies via AI/ML.",
    "Source code & outputs \u2014 github.com/priyaldeshmukh2005/urban-heat-stress-hotspot-detection.",
    "Live dashboard \u2014 https://urban-heat-stress-hotspot-detection-hxyycd4fe98eq67h3raq8u.streamlit.app/.",
]
tb, tf = textbox(s, Inches(0.55), Inches(1.55), Inches(12.25), Inches(5.1))
first = True
for i, ref in enumerate(refs, start=1):
    p = para(tf, first); first = False
    p.space_after = Pt(8)
    p.line_spacing = 1.0
    r1 = p.add_run(); set_run(r1, f"[{i}]  ", 11.5, True, TEAL)
    r2 = p.add_run(); set_run(r2, ref, 11.5, False, DARK)

tb, tf = textbox(s, Inches(0.55), Inches(6.78), Inches(12.25), Inches(0.3))
p = tf.paragraphs[0]
r = p.add_run(); set_run(r, "Prepared by Team AstroByte \u2014 Chhatrapati Sambhajinagar, Maharashtra, India", 11, False, GREY, True)

OUT = "Urban_Heat_Stress_Hotspot_Detection_Presentation.pptx"
prs.save(OUT)
print("saved", OUT)