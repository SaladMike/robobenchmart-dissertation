"""Schematic of the demonstration collector, drawn from dsynth/planning/."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

INK="#1f2933"; MUTE="#8d99a6"
BLUE="#5b8db8"; RED="#c0504d"; GREEN="#2e6f5e"; PALE="#eef2f6"

fig, ax = plt.subplots(figsize=(12.2, 3.5))
ax.set_xlim(0, 122); ax.set_ylim(0, 38); ax.axis("off")

def box(x, y, w, h, text, fc=PALE, ec=BLUE, fs=8.2, lw=1.1, tc=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs,
            color=tc, zorder=4, linespacing=1.45)

def arrow(x1, y1, x2, y2, style="-|>", col=INK, rad=0.0, lw=1.0, ls="-"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle=style, color=col,
                                 lw=lw, linestyle=ls, mutation_scale=11, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=1.5, shrinkB=1.5))

# --- top row: per-segment planning
box(1, 19, 17, 9, "task anchors\nsampled around\ntrue target state", ec=GREEN)
box(22, 19, 15, 9, "segment needs\nbase motion?")
box(41, 24.5, 20, 6.5, "task-specific\napproach planner", ec=GREEN)
box(41, 15.5, 20, 6.5, "screw motion\n(attempted twice,\nidentical arguments)")
box(65, 15.5, 15, 6.5, "collision\nvalid?")
box(65, 5.5, 15, 6.5, "RRT-Connect\nfallback", ec=RED)
box(84, 19, 16, 9, "execute the full\ncandidate rollout\nin simulation")
box(104, 19, 17, 9, "task predicate\nsatisfied?")

arrow(18.5, 23.5, 21.5, 23.5)
arrow(37.5, 25.5, 40.5, 27.0); ax.text(38.4, 27.6, "yes", fontsize=7.2, color=MUTE)
arrow(37.5, 21.5, 40.5, 19.5); ax.text(38.4, 17.9, "no", fontsize=7.2, color=MUTE)
arrow(61.5, 18.7, 64.5, 18.7)
arrow(61.5, 27.7, 84.0, 25.5, rad=-0.12)
arrow(72.5, 15.0, 72.5, 12.5, col=RED); ax.text(73.4, 13.4, "no", fontsize=7.2, color=RED)
arrow(80.5, 9.0, 92.0, 18.5, rad=-0.22, col=RED)
arrow(80.5, 18.7, 83.5, 21.0); ax.text(79.8, 21.4, "yes", fontsize=7.2, color=MUTE, ha="right")
arrow(100.5, 23.5, 103.5, 23.5)

box(104, 5.5, 17, 6.5, "keep: 248 per triplet", fc="#e6f0ea", ec=GREEN, tc=GREEN)
arrow(112.5, 18.5, 112.5, 12.5, col=GREEN)
ax.text(113.4, 15.0, "yes", fontsize=7.2, color=GREEN)

# discard loop
arrow(112.5, 28.6, 9.5, 34.4, rad=0.05, col=RED, ls=(0,(4,2.5)))
ax.text(114.2, 29.8, "no", fontsize=7.2, color=RED)
ax.text(60, 35.6, "discard the episode, reset the environment, resample anchors",
        fontsize=7.8, color=RED, ha="center")

ax.text(1, 1.2, "Successful rollouts only. Planning failures, collisions and unmet predicates leave no trace in the corpus, "
                "so the demonstrations show completion and never recovery.",
        fontsize=7.9, color=MUTE, ha="left")
fig.tight_layout(pad=0.2)
fig.savefig("assets/figures/retail-vla-benchmark/collector_pipeline.pdf",
            bbox_inches="tight", pad_inches=0.03)
print("wrote collector_pipeline.pdf")
