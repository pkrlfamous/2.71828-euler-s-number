"""
flower_petals.py — Fibonacci petal simulation using polar rose curves.

Shows flowers with n = 3, 5, 8, 13, 21 petals (Fibonacci numbers) drawn as
polar rose curves r = cos(n·θ) with coloring and shading.
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

FIBONACCI = [3, 5, 8, 13, 21]
CMAPS = ['RdPu', 'YlOrRd', 'BuGn', 'PuBu', 'OrRd']
PETAL_COLORS = [COLORS['e_pink'], COLORS['e_gold'], COLORS['e_green'],
                COLORS['e_cyan'], COLORS['e_orange']]


def main():
    apply_euler_style()

    fig, axes = plt.subplots(1, 5, figsize=(20, 5))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        'Fibonacci Flowers — Polar Rose Curves  $r = \\cos(n\\theta)$',
        fontsize=18, fontweight='bold', color=COLORS['e_gold'], y=1.04,
    )

    for ax, n, cmap_name, base_color in zip(axes, FIBONACCI, CMAPS, PETAL_COLORS):
        ax.set_facecolor(COLORS['bg_card'])

        # Dense theta for smooth petals; need 2π for even n, π for odd n
        theta = np.linspace(0, 2 * math.pi, 10000)
        r = np.cos(n * theta)

        # Only positive r (petals)
        r_pos = np.maximum(r, 0)
        x = r_pos * np.cos(theta)
        y = r_pos * np.sin(theta)

        # Gradient fill per petal loop
        # Split into petal segments where r > 0
        # Fill entire rose with gradient
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        t_norm = np.linspace(0, 1, len(segments))
        colors_arr = matplotlib.colormaps[cmap_name](0.4 + 0.6 * t_norm)
        lc = LineCollection(segments, colors=colors_arr, linewidth=1.5, alpha=0.8)
        ax.add_collection(lc)

        # Fill petals
        ax.fill(x, y, color=base_color, alpha=0.25)

        # Add circle at origin
        ax.plot(0, 0, 'o', color='white', markersize=4, zorder=5)

        # Draw individual petal outlines with varying alpha
        ax.plot(x, y, color=base_color, lw=1.2, alpha=0.7)

        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)
        ax.set_aspect('equal')
        ax.tick_params(colors=COLORS['text'], labelsize=7)
        ax.set_title(f'n = {n}\n({n} petals)', color=COLORS['text'], fontsize=12, pad=8)
        ax.set_xlabel('x', color=COLORS['text'], fontsize=9)
        ax.set_ylabel('y', color=COLORS['text'], fontsize=9)
        ax.grid(True, alpha=0.15, color=COLORS['grid'])

        # Fibonacci label
        ax.text(0.5, -0.15, f'Fib({FIBONACCI.index(n)+3}) = {n}',
                transform=ax.transAxes, ha='center', color=base_color,
                fontsize=9, fontweight='bold')

    # Footer
    fig.text(
        0.5, -0.05,
        r'Fibonacci sequence: 3, 5, 8, 13, 21, ...  — Nature favors these petal counts. '
        r'$r = \cos(n\theta)$ gives $n$ petals for odd $n$, $2n$ for even $n$.',
        ha='center', color=COLORS['text'], fontsize=9, style='italic',
    )

    plt.tight_layout()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'flower_petals', out_dir)
    plt.close(fig)
    print("Done: flower_petals")


if __name__ == '__main__':
    main()
