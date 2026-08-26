"""Regenerate the store-generation figure from the benchmark's own layout algorithm.

Faithful re-implementation of dsynth/scene_gen/layouts/tensor_field.py using the
parameters in conf/ds_continuous/config.yaml:
    store 24 x 15 m, tf_blending_decay 12, passage_width 2.0,
    inactive_shelvings_occupancy_width 1.0, skip prob 0.1, axis gate thresh 0.2.

Output: assets/figures/retail-vla-benchmark/layout_pipeline.pdf
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib.lines import Line2D
import random

SIZE_X, SIZE_Y = 24.0, 15.0
DECAY = 12.0
PASSAGE = 2.0
OCC = 1.0
SKIP = 0.1
THRESH = 0.2                       # 1-|cos| < 0.2  ->  within ~36.9 deg
SHELF_L, SHELF_W = 1.55, 0.6

INK   = "#1f2933"
ACC_H = "#2f6f9f"                  # gate admits a horizontal shelf
ACC_V = "#c2703a"                  # gate admits a vertical shelf
REJ   = "#c9ced4"                  # outside the band: nothing may be placed
OBST  = "#8d99a6"
SHELF = "#dbe4ec"

# ----------------------------------------------------------------- tensor field
class TensorField:
    def __init__(self, decay=DECAY):
        self.decay = decay
        self.origins, self.tensors = [], []

    def add_grid_basis(self, direction, origin):
        l = np.linalg.norm(direction)
        angle = np.arctan(direction[1] / (direction[0] + 1e-4))   # as in the source
        self.origins.append(np.asarray(origin, float))
        self.tensors.append(l * np.array([[np.cos(2*angle),  np.sin(2*angle)],
                                          [np.sin(2*angle), -np.cos(2*angle)]]))

    def add_line(self, line, closed=False, sample_step=None):
        line = np.asarray(line, float); n = len(line)
        for i in range(n):
            cur = line[i]
            if i == n - 1:
                if not closed: break
                nxt = line[0]
            else:
                nxt = line[i + 1]
            vec = nxt - cur
            self.add_grid_basis(vec, cur)
            if sample_step:
                while np.linalg.norm(vec) > sample_step:
                    cur = cur + vec / np.linalg.norm(vec) * sample_step
                    vec = nxt - cur
                    self.add_grid_basis(vec, cur)

    def add_boundary(self):
        self.add_line([[0,0],[0,SIZE_Y],[SIZE_X,SIZE_Y],[SIZE_X,0]],
                      closed=True, sample_step=1.0)

    def add_rects(self, rects):
        for r in rects:
            self.add_line(r.polygon(), closed=True, sample_step=0.5)

    def major(self, p):
        p = np.asarray(p, float)
        O = np.asarray(self.origins); T = np.asarray(self.tensors)
        w = np.exp(-self.decay * np.linalg.norm(O - p, axis=1))
        F = (T * w[:, None, None]).sum(0)
        vals, vecs = np.linalg.eig(F)
        return vecs.T[np.argsort(vals)[::-1]][0]

# ----------------------------------------------------------------- fixtures
class Rect:
    def __init__(self, x, y, l=SHELF_L, w=SHELF_W, vertical=False, occ=OCC, kind="shelf"):
        self.x, self.y, self.l, self.w = x, y, l, w
        self.vertical, self.occ, self.kind = vertical, occ, kind

    def half(self):
        return (self.w/2, self.l/2) if self.vertical else (self.l/2, self.w/2)

    def polygon(self):
        hx, hy = self.half()
        return [[self.x-hx, self.y-hy], [self.x+hx, self.y-hy],
                [self.x+hx, self.y+hy], [self.x-hx, self.y+hy]]

    def bounds(self, inflate=False):
        hx, hy = self.half()
        if inflate:
            if self.vertical: hx += self.occ
            else:             hy += self.occ
        return self.x-hx, self.y-hy, self.x+hx, self.y+hy

    def valid(self):
        x0, y0, x1, y1 = self.bounds(inflate=True)
        return x0 >= 0 and y0 >= 0 and x1 <= SIZE_X and y1 <= SIZE_Y

def overlap(a, b):
    ax0, ay0, ax1, ay1 = a.bounds(); bx0, by0, bx1, by1 = b.bounds(inflate=True)
    if not (bx1 < ax0 or ax1 < bx0 or by1 < ay0 or ay1 < by0): return True
    ax0, ay0, ax1, ay1 = a.bounds(inflate=True); bx0, by0, bx1, by1 = b.bounds()
    if not (bx1 < ax0 or ax1 < bx0 or by1 < ay0 or ay1 < by0): return True
    if a.vertical != b.vertical:
        ax0, ay0, ax1, ay1 = a.bounds(inflate=True); bx0, by0, bx1, by1 = b.bounds(inflate=True)
        if not (bx1 < ax0 or ax1 < bx0 or by1 < ay0 or ay1 < by0): return True
    return False

def collides(r, others): return any(overlap(r, o) for o in others)

def gate(vec):
    u = vec / np.linalg.norm(vec)
    if 1 - abs(np.dot(u, [1, 0])) < THRESH: return "h"
    if 1 - abs(np.dot(u, [0, 1])) < THRESH: return "v"
    return None

def sweep(tf, existing, rng):
    placed = []
    for vertical in (False, True):
        cur = np.array([1.0, 1.0]); first = True
        while True:
            g = gate(tf.major(cur))
            want = "v" if vertical else "h"
            if g == want and rng.random() > SKIP:
                r = Rect(cur[0], cur[1], vertical=vertical)
                if r.valid() and not collides(r, placed + existing):
                    placed.append(r); first = False
            if vertical:
                dy, dx = (0.1, 0.1) if first else (SHELF_L + 1e-2, SHELF_W + PASSAGE)
                if cur[1] + dy < SIZE_Y: cur[1] += dy
                elif cur[0] + dx < SIZE_X: cur[1] = 1.0; cur[0] += dx
                else: break
            else:
                dx, dy = (0.1, 0.1) if first else (SHELF_L + 1e-2, SHELF_W + PASSAGE)
                if cur[0] + dx < SIZE_X: cur[0] += dx
                elif cur[1] + dy < SIZE_Y: cur[0] = 1.0; cur[1] += dy
                else: break
    return placed

# ----------------------------------------------------------------- build a store
rng = random.Random(56)
obstacles = [Rect(SIZE_X, SIZE_Y-2, l=2, w=2, occ=0.0, kind="service")]
for (l, w) in [(2.2, 1.1), (1.8, 1.2), (2.0, 0.9)]:
    for _ in range(40):
        c = Rect(rng.uniform(2, SIZE_X-2), rng.uniform(2, SIZE_Y-2), l=l, w=w,
                 vertical=rng.random() < .5, occ=0.2, kind="obstacle")
        if c.valid() and not collides(c, obstacles): obstacles.append(c); break

tf = TensorField(); tf.add_boundary(); tf.add_rects(obstacles)
shelves = sweep(tf, obstacles, rng)
print(f"placed {len(shelves)} shelving units "
      f"({sum(not s.vertical for s in shelves)} horizontal, "
      f"{sum(s.vertical for s in shelves)} vertical)")

# ----------------------------------------------------------------- draw
fig, axes = plt.subplots(1, 3, figsize=(13.6, 3.05))
for ax in axes:
    ax.set_xlim(-.4, SIZE_X+.4); ax.set_ylim(-.4, SIZE_Y+.4)
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0,0), SIZE_X, SIZE_Y, fc="none", ec=INK, lw=1.1))

def draw_obstacles(ax):
    for o in obstacles:
        x0, y0, x1, y1 = o.bounds()
        ax.add_patch(Rectangle((x0,y0), x1-x0, y1-y0, fc=OBST, ec=INK, lw=.7, alpha=.85))

# (a) the field as a gate
step = 0.80
for gx in np.arange(step, SIZE_X, step):
    for gy in np.arange(step, SIZE_Y, step):
        v = tf.major([gx, gy]); g = gate(v)
        col = {"h": ACC_H, "v": ACC_V, None: REJ}[g]
        u = v / np.linalg.norm(v) * (0.26 if g else 0.20)
        axes[0].plot([gx-u[0], gx+u[0]], [gy-u[1], gy+u[1]],
                     color=col, lw=1.6 if g else 1.3, solid_capstyle="round",
                     zorder=2 if g else 3)
draw_obstacles(axes[0])
axes[0].set_title("(a)  orientation field, read as a gate", fontsize=9.5, color=INK, pad=6)

# (b) accepted plan
for s in shelves:
    x0, y0, x1, y1 = s.bounds(inflate=True)
    axes[1].add_patch(Rectangle((x0,y0), x1-x0, y1-y0, fc="none", ec=ACC_H,
                                lw=.6, ls=(0,(2.2,1.8)), alpha=.55))
for s in shelves:
    x0, y0, x1, y1 = s.bounds()
    axes[1].add_patch(Rectangle((x0,y0), x1-x0, y1-y0, fc=SHELF,
                                ec=ACC_H if not s.vertical else ACC_V, lw=1.0))
draw_obstacles(axes[1])
axes[1].set_title("(b)  accepted fixtures and clearance", fontsize=9.5, color=INK, pad=6)

# (c) what one episode actually occupies
for s in shelves:
    x0, y0, x1, y1 = s.bounds()
    axes[2].add_patch(Rectangle((x0,y0), x1-x0, y1-y0, fc="#eef2f6", ec="#b8c2cc", lw=.8))
draw_obstacles(axes[2])
interior = [s for s in shelves if not s.vertical
            and 3 < s.x < SIZE_X-3 and 3.5 < s.y < SIZE_Y-3.5]
active = sorted(interior, key=lambda s: (abs(s.x-9.5) + abs(s.y-8.5)))[0]
ax0, ay0, ax1, ay1 = active.bounds()
rx, ry = active.x, active.y - active.w/2 - 1.4
# the footprint a single episode actually visits
axes[2].add_patch(plt.Circle(((active.x+rx)/2, (active.y+ry)/2), 1.85,
                             fc="#f2c8a8", ec="none", alpha=.35, zorder=2))
axes[2].add_patch(Rectangle((ax0,ay0), ax1-ax0, ay1-ay0, fc="#f7d9c4", ec=ACC_V, lw=1.4, zorder=4))
axes[2].add_patch(plt.Circle((rx, ry), 0.36, fc="#ffffff", ec=INK, lw=1.2, zorder=6))
axes[2].add_patch(FancyArrow(rx, ry+0.42, 0, 0.62, width=.05, head_width=.30, head_length=.26,
                             length_includes_head=True, fc=INK, ec=INK, zorder=7))
axes[2].annotate("", xy=(rx-1.35, active.y-active.w/2), xytext=(rx-1.35, ry),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=.9, shrinkA=0, shrinkB=0))
axes[2].text(rx-1.60, (ry + active.y-active.w/2)/2, "1.4 m", fontsize=8.4, color=INK,
             va="center", ha="right")
axes[2].set_title("(c)  the region a single episode occupies", fontsize=9.5, color=INK, pad=6)

handles = [Line2D([0],[0], color=ACC_H, lw=2, label="admits a horizontal unit"),
           Line2D([0],[0], color=ACC_V, lw=2, label="admits a vertical unit"),
           Line2D([0],[0], color=REJ,   lw=2, label="outside the band, no placement")]
axes[0].legend(handles=handles, loc="upper center", bbox_to_anchor=(.5,-.02),
               frameon=False, fontsize=7.6, ncol=1, handlelength=1.5, labelspacing=.25)

fig.subplots_adjust(left=.01, right=.99, top=.90, bottom=.02, wspace=.03)
out = "assets/figures/retail-vla-benchmark/layout_pipeline.pdf"
fig.savefig(out, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
