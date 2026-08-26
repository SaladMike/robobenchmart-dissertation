"""Redraw the dissertation's result figures from tools/data/*.json.

Outputs into assets/figures/retail-vla-benchmark/:
    mesh_timing.pdf, asset_pareto.pdf,
    failure_by_scenario.pdf, failure_by_task.pdf
"""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

OUT = "assets/figures/retail-vla-benchmark/"
INK, MUTE, GRID = "#1f2933", "#8d99a6", "#eceff2"
MODELC = {"Octo": "#5b8db8", "SmolVLA": "#c0504d",
          "pi0": "#e08a3c", "pi05": "#2e6f5e"}
MODELL = {"Octo": "Octo", "SmolVLA": "SmolVLA",
          "pi0": r"$\pi_0$", "pi05": r"$\pi_{0.5}$"}

def clean(ax, keep=("bottom", "left")):
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(s in keep)
        if s in keep: ax.spines[s].set_color("#b8c2cc")
    ax.tick_params(colors=INK, labelsize=8)

# --------------------------------------------------------------- 1. mesh timing
d = json.load(open("tools/data/mesh_timing.json"))
fig, ax = plt.subplots(figsize=(6.1, 3.5))
for key, col, lab, mk in [("original", "#c0504d", "original meshes", "o"),
                          ("optimised", "#5b8db8", "simplified background meshes", "s")]:
    xs = [p[0] for p in d[key]]; ys = [p[1] for p in d[key]]
    ax.plot(xs, ys, mk + "-", color=col, lw=1.6, ms=5.5, label=lab, zorder=3)
ax.annotate("no measurement beyond\nfour units at full detail",
            xy=(4, 4.494), xytext=(7.5, 3.05), fontsize=7.8, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTE, lw=.9,
                            connectionstyle="arc3,rad=-.25"))
for x, y in d["optimised"]:
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=7.2, color=MUTE)
for x, y in d["original"]:
    dy = 8 if y > 2 else -14
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                xytext=(0, dy), ha="center", fontsize=7.2, color=MUTE)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xticks([1, 2, 4, 8, 20, 118]); ax.set_xticklabels(["1","2","4","8","20","118"])
ax.set_yticks([0.6, 1, 2, 4]); ax.set_yticklabels(["0.6","1","2","4"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("stocked shelving units in the scene", fontsize=9, color=INK)
ax.set_ylabel("seconds per 50 simulation steps", fontsize=9, color=INK)
ax.grid(color=GRID, lw=.8, which="major"); ax.set_axisbelow(True)
clean(ax); ax.legend(fontsize=8, frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(OUT + "mesh_timing.pdf"); plt.close(fig)

# --------------------------------------------------------------- 2. pareto
p = json.load(open("tools/data/pareto.json"))
fig, ax = plt.subplots(figsize=(5.0, 4.2))
vx = [q[0] for q in p["variants"]]; vy = [q[1] for q in p["variants"]]
fx = [q[0] for q in p["front"]];    fy = [q[1] for q in p["front"]]
bx, by = p["best"][0]
ax.scatter(vx, vy, s=26, c="#c9ced4", ec="none", zorder=2, label="candidate mesh")
order = sorted(zip(fx, fy))
ax.plot([q[0] for q in order], [q[1] for q in order], "-", color="#5b8db8",
        lw=1.3, zorder=3, label="non-dominated frontier")
ax.scatter(fx, fy, s=30, c="#5b8db8", ec="none", zorder=4)
ax.scatter([bx], [by], s=130, marker="*", c="#c0504d", ec="none", zorder=5,
           label="selected variant")
ax.annotate(f"({bx:.2f}, {by:.2f})", (bx, by), textcoords="offset points",
            xytext=(12, 4), fontsize=8, color=INK)
ax.set_xlabel("normalised geometric distance to source", fontsize=9, color=INK)
ax.set_ylabel("normalised triangle count", fontsize=9, color=INK)
ax.set_xlim(-.04, 1.04); ax.set_ylim(-.04, 1.06)
ax.grid(color=GRID, lw=.8); ax.set_axisbelow(True); clean(ax)
ax.legend(fontsize=8, frameon=False, loc="upper right")
fig.tight_layout(); fig.savefig(OUT + "asset_pareto.pdf"); plt.close(fig)
print("wrote 2 figures")
