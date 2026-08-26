"""Redraw the dissertation's result figures from tools/data/*.json.

Outputs into assets/figures/retail-vla-benchmark/:
    mesh_timing.pdf, asset_pareto.pdf, failure_rates.pdf,
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

# --------------------------------------------------------------- 3. failure rate
fr = json.load(open("tools/data/failure_rates.json"))
CONDS = ["Seeds", "Pose", "Layout", "Pairing"]
KEY = {"Seeds":"Train","Pose":"ID","Layout":"US","Pairing":"US&I"}
fig, ax = plt.subplots(figsize=(6.9, 3.3))
w = .19
for i, m in enumerate(["Octo", "SmolVLA", "pi0", "pi05"]):
    xs = [j + (i - 1.5) * w for j in range(4)]
    ys = [fr[m][KEY[c]] for c in CONDS]
    ax.bar(xs, ys, width=w * .92, color=MODELC[m], ec="none",
           label=MODELL[m], zorder=3)
    for x, y in zip(xs, ys):
        ax.text(x, y + 1.6, f"{y:.0f}", ha="center", fontsize=6.6, color=MUTE)
ax.set_xticks(range(4)); ax.set_xticklabels(CONDS, fontsize=9, color=INK)
ax.set_ylabel("episodes failed (%)", fontsize=9, color=INK)
ax.set_ylim(0, 112); ax.set_yticks([0, 25, 50, 75, 100])
ax.grid(axis="y", color=GRID, lw=.8); ax.set_axisbelow(True); clean(ax)
ax.legend(fontsize=8, frameon=False, ncol=4, loc="upper left",
          bbox_to_anchor=(0, 1.14), columnspacing=1.4, handlelength=1.1)
fig.tight_layout(); fig.savefig(OUT + "failure_rates.pdf"); plt.close(fig)

# --------------------------------------------------------------- 4/5. taxonomy
TAGS = ["task","target","move","pregrasp","grasp","drop","displace",
        "preplace","place-coord","place","partial"]
# grouped by stage of the execution chain rather than an arbitrary palette
TAGC = {"task":"#7d3c4a","target":"#c0504d",
        "move":"#e0a03c","pregrasp":"#f0cd8a",
        "grasp":"#2f6f9f","drop":"#8fb8d6",
        "displace":"#7b6ca8",
        "preplace":"#b7d3b0","place-coord":"#6fa86b","place":"#2e6f5e",
        "partial":"#b8c2cc"}
STAGES = [("grounding", ["task","target"]), ("approach", ["move","pregrasp"]),
          ("contact", ["grasp","drop"]), ("side effect", ["displace"]),
          ("placement", ["preplace","place-coord","place"]),
          ("articulation", ["partial"])]

TAGKEY = {"Seeds":"Train","Pose":"ID","Layout":"US","Pairing":"US&I",
          "move-board":"move-board","door":"door","pick-floor":"pick-floor","pick-basket":"pick-basket"}
def taxonomy(block, cols, fname, width):
    fig, axes = plt.subplots(1, 4, figsize=(width, 4.0), sharey=True)
    for ax, m in zip(axes, ["Octo", "SmolVLA", "pi0", "pi05"]):
        bottom = [0.0] * len(cols)
        for t in TAGS:
            vals = [block[m][TAGKEY[c]][t] for c in cols]
            ax.bar(range(len(cols)), vals, bottom=bottom, width=.66,
                   color=TAGC[t], ec="white", lw=.4, zorder=3)
            bottom = [b + v for b, v in zip(bottom, vals)]
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels(cols, fontsize=7.6, color=INK,
                           rotation=0 if len(cols[0]) < 6 else 26,
                           ha="center" if len(cols[0]) < 6 else "right")
        ax.set_title(MODELL[m], fontsize=9.5, color=INK, pad=6)
        ax.set_ylim(0, 100); ax.set_yticks([0, 25, 50, 75, 100])
        clean(ax, keep=("left",)); ax.tick_params(axis="x", length=0)
        ax.grid(axis="y", color=GRID, lw=.7); ax.set_axisbelow(True)
    axes[0].set_ylabel("share of failed episodes (%)", fontsize=9, color=INK)
    handles, labels = [], []
    for stage, ts in STAGES:
        for t in ts:
            handles.append(Rectangle((0,0),1,1, fc=TAGC[t], ec="none"))
            labels.append(f"{t}")
    fig.legend(handles, labels, fontsize=7.8, frameon=False, ncol=6,
               loc="lower center", bbox_to_anchor=(.5, .004),
               handlelength=1.0, columnspacing=1.5, handletextpad=.5)
    fig.tight_layout(rect=(0, .135, 1, 1))
    fig.savefig(OUT + fname); plt.close(fig)

tg = json.load(open("tools/data/tag_data.json"))
taxonomy(tg["by_scenario"], ["Seeds","Pose","Layout","Pairing"], "failure_by_scenario.pdf", 10.2)
taxonomy(tg["by_task"], ["move-board","door","pick-floor","pick-basket"],
         "failure_by_task.pdf", 10.2)
print("wrote 5 figures")
