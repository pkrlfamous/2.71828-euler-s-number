"""
fractal_trees.py — Fractal tree with exponential branch scaling.

Each branch is scaled by e^(-0.3) ≈ 0.7408 (the e-based contraction ratio).
Two panels:
  Left:  symmetric tree (branching angle ±25°)
  Right: asymmetric tree (branching angles +20°, -35°) with e^(-0.3) scaling

Color codes branches by depth (gold→green→cyan→blue).
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.cm as cm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

SCALE = math.exp(-0.3)   # ≈ 0.7408
MAX_DEPTH = 11


def draw_tree(ax, x, y, angle, length, depth, max_depth,
              left_angle, right_angle, lines, depths):
    """Recursively build branch line segments."""
    if depth > max_depth or length < 0.005:
        return
    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)
    lines.append([(x, y), (x2, y2)])
    depths.append(depth)

    draw_tree(ax, x2, y2, angle + math.radians(left_angle),
              length * SCALE, depth + 1, max_depth, left_angle, right_angle, lines, depths)
    draw_tree(ax, x2, y2, angle - math.radians(right_angle),
              length * SCALE, depth + 1, max_depth, left_angle, right_angle, lines, depths)


def render_tree(ax, left_angle, right_angle, title_str):
    ax.set_facecolor(COLORS['bg_card'])
    lines = []
    depths = []
    draw_tree(ax, 0, 0, math.pi / 2, 1.0, 0, MAX_DEPTH,
              left_angle, right_angle, lines, depths)

    depths_arr = np.array(depths, dtype=float)
    norm_depths = depths_arr / MAX_DEPTH

    # Line widths decrease with depth
    lw_arr = np.clip(3.5 - depths_arr * 0.28, 0.3, 3.5)

    # Color by depth: gold (trunk) → cyan (tips)
    color_arr = matplotlib.colormaps['YlGnBu'](norm_depths)

    lc = LineCollection(lines, colors=color_arr,
                        linewidths=lw_arr, alpha=0.92, capstyle='round')
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect('equal')
    ax.set_title(title_str, color=COLORS['text'], fontsize=13, pad=10)
    ax.tick_params(colors=COLORS['text'])
    ax.grid(False)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])


def main():
    apply_euler_style()

    fig, axes = plt.subplots(1, 2, figsize=(16, 12))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Fractal Trees — Branch Scaling by $e^{-0.3} \approx 0.7408$',
        fontsize=18, fontweight='bold', color=COLORS['e_gold'], y=0.99,
    )

    render_tree(
        axes[0], 25, 25,
        f'Symmetric Tree (±25°)\nScale factor: e⁻⁰·³ ≈ {SCALE:.4f}',
    )
    render_tree(
        axes[1], 20, 35,
        f'Asymmetric Tree (+20°/−35°)\nScale factor: e⁻⁰·³ ≈ {SCALE:.4f}',
    )

    # Info box
    info_text = (
        r'$\ell_{n+1} = \ell_n \cdot e^{-0.3}$'
        '\n'
        r'After $n$ branchings: $\ell_n = \ell_0 \cdot e^{-0.3n}$'
        '\n'
        r'Total branch count at depth $d$: $2^d$'
        '\n'
        r'Scale = $e^{-3/10}$ → each branch $\approx74\%$ of parent'
    )
    fig.text(0.5, 0.01, info_text,
             ha='center', color=COLORS['e_cyan'], fontsize=10,
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_cyan'], alpha=0.9))

    plt.tight_layout(rect=[0, 0.07, 1, 0.97])
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'fractal_trees', out_dir)
    plt.close(fig)
    print("Done: fractal_trees")


if __name__ == '__main__':
    main()
