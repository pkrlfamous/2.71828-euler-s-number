"""
De Moivre's Theorem: (e^(iθ))^n = e^(inθ) = cos(nθ) + i·sin(nθ)
Visualized as regular polygons inscribed in the unit circle.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def nth_roots_of_unity(n):
    """Return the n-th roots of unity as (x, y) arrays."""
    k = np.arange(n)
    angles = 2 * np.pi * k / n
    return np.cos(angles), np.sin(angles)


def main():
    apply_euler_style()

    ns = [3, 4, 5, 6, 8, 12]
    palette = [
        COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_red'],
        COLORS['e_green'], COLORS['e_purple'], COLORS['e_orange']
    ]
    polygon_names = {
        3: 'Triangle', 4: 'Square', 5: 'Pentagon',
        6: 'Hexagon', 8: 'Octagon', 12: 'Dodecagon'
    }

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"De Moivre's Theorem: $(e^{i\theta})^n = e^{in\theta}$  —  Regular Polygons",
        fontsize=20, color=COLORS['e_gold'], fontweight='bold', y=0.99
    )

    circle_th = np.linspace(0, 2 * np.pi, 400)

    for ax, n, color in zip(axes.flat, ns, palette):
        ax.set_facecolor(COLORS['bg_card'])

        # Unit circle
        ax.plot(np.cos(circle_th), np.sin(circle_th),
                color=COLORS['grid'], lw=1.2, alpha=0.6)

        # Vertices: e^(i·2πk/n)
        vx, vy = nth_roots_of_unity(n)

        # Draw polygon edges
        vx_closed = np.append(vx, vx[0])
        vy_closed = np.append(vy, vy[0])
        ax.fill(vx, vy, alpha=0.15, color=color)
        ax.plot(vx_closed, vy_closed, color=color, lw=2.5, zorder=4)

        # Draw radii from origin
        for k in range(n):
            ax.plot([0, vx[k]], [0, vy[k]], color=color,
                    lw=1, alpha=0.5, linestyle='--')

        # Mark vertices
        ax.scatter(vx, vy, color=color, s=80, zorder=5, edgecolors='white', lw=0.8)

        # Label each vertex with e^(i·2πk/n)
        for k in range(n):
            angle = 2 * np.pi * k / n
            offset = 1.22
            ax.text(offset * np.cos(angle), offset * np.sin(angle),
                    rf'$k={k}$', ha='center', va='center',
                    color=color, fontsize=7.5)

        # Axes
        ax.axhline(0, color=COLORS['grid'], lw=0.6, alpha=0.5)
        ax.axvline(0, color=COLORS['grid'], lw=0.6, alpha=0.5)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_title(
            f'n={n}: {polygon_names[n]}\n'
            r'$e^{i \cdot 2\pi k/' + str(n) + r'}$, $k=0,\ldots,' + str(n - 1) + r'$',
            color=color, fontsize=11
        )
        ax.grid(True, alpha=0.15)

        # Show the theorem at bottom
        side_len = 2 * math.sin(math.pi / n)
        ax.text(0, -1.38, f'Side length = {side_len:.4f}',
                ha='center', color=COLORS['text'], fontsize=8.5)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    save_plot(fig, 'de_moivre', OUTPUT_DIR)
    plt.close(fig)
    print("de_moivre.py done.")


if __name__ == '__main__':
    main()
