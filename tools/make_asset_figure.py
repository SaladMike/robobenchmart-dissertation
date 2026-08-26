"""Regenerate the asset-library figure from conf/assets/assets_preprocessed.yaml.

Panel (a): products per category in the released library.
Panel (b): the eight products that ever served as a task target, and their role
           in each pick-and-place task.

Output: assets/figures/retail-vla-benchmark/asset_library.pdf
"""
import re, collections, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

YAML = "213/conf/assets/assets_preprocessed.yaml"

INK    = "#1f2933"
USED   = "#2f6f9f"
UNUSED = "#c9ced4"
TRAIN  = "#2f6f9f"
TEST   = "#c2703a"
DISTR  = "#e3e8ed"

# ------------------------------------------------------------------ read library
path, leaves = [], []
for line in open(YAML):
    if not line.strip() or line.strip().startswith("#"):
        continue
    m = re.match(r"^(\s*)([A-Za-z_][\w]*):\s*(.*)$", line)
    if not m:
        continue
    ind, key = len(m.group(1)), m.group(2)
    path = path[: ind // 2] + [key]
    if key == "asset_file_path" and len(path) >= 4 and path[0] == "products_hierarchy":
        leaves.append((path[2], path[3]))          # (category, product)

legacy = {"grocery", "drinks", "dairy_products"}
counts = collections.Counter(c for c, _ in leaves if c not in legacy)
prod2cat = {p: c for c, p in leaves}

# ------------------------------------------------------------------ experiment slice
targets = {
    "NiveaBodyMilk": "Nivea Body Milk",
    "NestleHoneyStars": "Honey Stars",
    "FantaSaborNaranja2L": "Fanta 2L",
    "NestleFitnessChocolateCereals": "Nestle Fitness",
    "SlamLuncheonMeat": "SLAM luncheon",
    "HeinzBeansInARichTomatoSauce": "Heinz Beans",
    "DuffBeerCan": "Duff Beer",
    "VanishStainRemover": "Vanish",
}
used_cats = {prod2cat[k] for k in targets if k in prod2cat}

# role per task: 1 = trained target, 2 = held-out target, 0 = on the shelf only
TASKS = ["Basket", "Board", "Floor"]
ROLE = {
    "Nivea Body Milk":  [1, 2, 0],
    "Honey Stars":      [1, 0, 0],
    "Fanta 2L":         [1, 2, 2],
    "Nestle Fitness":   [2, 1, 0],
    "Duff Beer":        [0, 1, 2],
    "Vanish":           [0, 1, 2],
    "Heinz Beans":      [0, 0, 1],
    "SLAM luncheon":    [2, 0, 1],
}
order = ["Nivea Body Milk", "Honey Stars", "Fanta 2L", "Nestle Fitness",
         "Duff Beer", "Vanish", "Heinz Beans", "SLAM luncheon"]

print(f"{sum(counts.values())} products in {len(counts)} categories; "
      f"{len(targets)} ever a target, drawn from {len(used_cats)} categories")

# ------------------------------------------------------------------ draw
fig = plt.figure(figsize=(12.6, 4.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.42, 1.0], wspace=0.34)

# (a) library composition
axa = fig.add_subplot(gs[0, 0])
cats = [c for c, _ in counts.most_common()]
vals = [counts[c] for c in cats]
ypos = range(len(cats))[::-1]
for y, c, v in zip(ypos, cats, vals):
    hit = c in used_cats
    axa.barh(y, v, height=.68, color=USED if hit else UNUSED,
             ec="none", zorder=3)
    axa.text(v + 0.8, y, str(v), va="center", fontsize=7.4,
             color=INK if hit else "#8d99a6", zorder=4)
axa.set_yticks(list(ypos))
axa.set_yticklabels([c.replace("_", " ").title() for c in cats], fontsize=7.6, color=INK)
axa.set_xlabel("product assets in the released library", fontsize=8.6, color=INK)
axa.set_xlim(0, max(vals) * 1.13)
axa.tick_params(axis="x", labelsize=7.6, colors=INK)
for s in ("top", "right", "left"):
    axa.spines[s].set_visible(False)
axa.spines["bottom"].set_color("#b8c2cc")
axa.grid(axis="x", color="#eceff2", zorder=0)
axa.set_axisbelow(True)
axa.set_title("(a)  371 assets across 21 categories", fontsize=9.6, color=INK, pad=8, loc="left")
axa.legend(handles=[Rectangle((0,0),1,1, fc=USED, ec="none"),
                    Rectangle((0,0),1,1, fc=UNUSED, ec="none")],
           labels=["contains a product used as a target", "never supplies a target"],
           fontsize=7.4, frameon=False, loc="lower right", handlelength=1.1)

# (b) the experimental slice
axb = fig.add_subplot(gs[0, 1])
axb.set_xlim(-.5, len(TASKS)-.5); axb.set_ylim(-1.45, len(order)-.45)
axb.invert_yaxis(); axb.axis("off")
for j, tname in enumerate(TASKS):
    axb.text(j, -0.78, tname, ha="center", va="bottom", fontsize=8.4, color=INK)
for i, name in enumerate(order):
    axb.text(-.62, i, name, ha="right", va="center", fontsize=8.0, color=INK)
    for j, role in enumerate(ROLE[name]):
        fc = {0: DISTR, 1: TRAIN, 2: TEST}[role]
        axb.add_patch(Rectangle((j-.40, i-.34), .80, .68, fc=fc, ec="none"))
axb.set_title("(b)  every product the benchmark ever names", fontsize=9.6,
              color=INK, pad=8, loc="left")
axb.plot([-.5, len(TASKS)-.5], [-.62, -.62], color="#c9ced4", lw=.8, clip_on=False)
axb.legend(handles=[Rectangle((0,0),1,1, fc=TRAIN, ec="none"),
                    Rectangle((0,0),1,1, fc=TEST, ec="none"),
                    Rectangle((0,0),1,1, fc=DISTR, ec="#c9ced4")],
           labels=["demonstrated on this task",
                   "held out as a Pairing target, still on the shelf",
                   "on the shelf, never named"],
           fontsize=7.4, frameon=False, loc="upper center",
           bbox_to_anchor=(.42, -.02), handlelength=1.1, labelspacing=.35)

fig.subplots_adjust(left=.13, right=.98, top=.88, bottom=.20)
out = "assets/figures/retail-vla-benchmark/asset_library.pdf"
fig.savefig(out, bbox_inches="tight", pad_inches=0.03)
print("wrote", out)
