"""Create the 'How It Works' workflow diagram (white background, professional)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------- palette ----------
NAVY = "#0E3A53"
TEAL = "#1B7F8E"
LIGHT = "#EAF4F6"
TEXT = "#1A1A1A"
ARROW = "#4A5568"

steps = [
    ("1", "Satellite Data &\nGeospatial Layers",
     "Landsat 8/9 LST \u00b7 Sentinel-2 NDVI/NDBI \u00b7 SRTM \u00b7 WorldPop"),
    ("2", "Feature Engineering",
     "NDVI \u00b7 NDBI \u00b7 Elevation \u00b7 Population \u00b7 Land Cover"),
    ("3", "LST Prediction \u2014 XGBoost",
     "Machine-learning model predicts\nland surface temperature"),
    ("4", "Spatial Cross-Validation",
     "Block CV reduces spatial leakage\nin model evaluation"),
    ("5", "SHAP Explainability",
     "Feature contribution analysis\nfor every prediction"),
    ("6", "Hotspot & Vulnerability\nAnalysis",
     "Heat hazard + population exposure\n= Heat Vulnerability Index"),
    ("7", "Cooling Intervention\nSimulation",
     "Urban greening \u00b7 cool roofs\npermeable surfaces"),
    ("8", "Priority Zones &\nInteractive Dashboard",
     "Ranked zones for planners &\ndecision-makers"),
]

fig, ax = plt.subplots(figsize=(12.6, 4.1), dpi=200)
ax.set_xlim(0, 126)
ax.set_ylim(0, 41)
ax.axis("off")

box_w, box_h = 28.5, 17.0
top_y = 22.5
bot_y = 1.5

def box(x, y, num, title, sub):
    ax.add_patch(FancyBboxPatch(
        (x, y), box_w, box_h,
        boxstyle="round,pad=0.6,rounding_size=1.6",
        linewidth=1.4, edgecolor=NAVY, facecolor=LIGHT))
    ax.add_patch(plt.Circle((x + 3.0, y + box_h - 3.0), 2.9,
                            facecolor=TEAL, edgecolor=NAVY, linewidth=1.0, zorder=5))
    ax.text(x + 3.0, y + box_h - 3.0, num, color="white", fontsize=11.5,
            fontweight="bold", ha="center", va="center", zorder=6)
    ax.text(x + 7.2, y + box_h - 4.2, title, fontsize=10.6, fontweight="bold",
            color=NAVY, va="top", ha="left")
    ax.text(x + 7.2, y + box_h - 10.2, sub, fontsize=8.2, color=TEXT,
            va="top", ha="left", linespacing=1.35)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=16,
                 linewidth=2.0, color=ARROW, shrinkA=0, shrinkB=0))

# Top row: 1 -> 2 -> 3 -> 4 (left to right)
x_top = [1.0, 32.5, 64.0, 95.5]
for i, (x, step) in enumerate(zip(x_top, steps[:4])):
    box(x, top_y, step[0], step[1], step[2])
    if i < 3:
        arrow(x + box_w + 0.5, top_y + box_h / 2, x_top[i + 1] - 0.5, top_y + box_h / 2)

# Connector down between col 4 and col 5
arrow(95.5 + box_w / 2, top_y - 0.5, 95.5 + box_w / 2, bot_y + box_h + 0.5)

# Bottom row: 5 -> 6 -> 7 -> 8 (right to left)
x_bot = [95.5, 64.0, 32.5, 1.0]
for i, (x, step) in enumerate(zip(x_bot, steps[4:])):
    box(x, bot_y, str(i + 5), step[1], step[2])
    if i < 3:
        arrow(x - 0.5, bot_y + box_h / 2, x_bot[i + 1] + box_w + 0.5, bot_y + box_h / 2)

ax.text(63, 39.2, "Decision-Support Workflow \u2014 How the System Works",
        fontsize=15, fontweight="bold", color=NAVY, ha="center", va="center")
plt.tight_layout(pad=0.4)
plt.savefig("workflow_diagram.png", dpi=200, facecolor="white", bbox_inches="tight")
print("saved workflow_diagram.png")
