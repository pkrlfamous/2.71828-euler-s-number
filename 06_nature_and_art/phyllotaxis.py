"""
phyllotaxis.py — Sunflower seed packing and the golden angle.

Three panels, each with 2000 seeds placed at angle φ_n from origin:
  Left:   golden angle ≈ 137.508° → optimal packing, no gaps
  Middle: slightly off  137.600° → subtle gaps / parastichy drift
  Right:  rational angle 2π/7 rad ≈ 51.43° → clear radial spokes
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))   # ≈ 2.39996 rad ≈ 137.508°
N_SEEDS = 2000
C = 1.5   # scaling constant: r = c * sqrt(n)


def make_seeds(angle_rad, n=N_SEEDS, c=C):
    ns = np.arange(n)
    r = c * np.sqrt(ns)
    theta = ns * angle_rad
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def main():
    apply_euler_style()

    configs = [
        (GOLDEN_ANGLE, 'YlOrBr',
         f'Golden Angle ≈ {math.degrees(GOLDEN_ANGLE):.3f}°\n(optimal packing)'),
        (math.radians(137.6), 'Blues',
         'Slightly Off  137.600°\n(gaps emerge)'),
        (2 * math.pi / 7, 'Reds',
         f'Rational  2π/7 ≈ {math.degrees(2*math.pi/7):.2f}°\n(visible spokes)'),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        'Phyllotaxis — Sunflower Seed Packing and the Golden Angle',
        fontsize=18, fontweight='bold', color=COLORS['e_gold'], y=1.01,
    )

    for ax, (angle, cmap, title) in zip(axes, configs):
        ax.set_facecolor(COLORS['bg_card'])
        x, y = make_seeds(angle)
        colors_arr = np.arange(N_SEEDS)  # color by index

        sc = ax.scatter(x, y, c=colors_arr, cmap=cmap, s=4.5, alpha=0.85,
                        linewidths=0)
        ax.set_aspect('equal')
        ax.set_title(title, color=COLORS['text'], fontsize=12, pad=10)
        ax.tick_params(colors=COLORS['text'])
        ax.set_xlabel('x', color=COLORS['text'])
        ax.set_ylabel('y', color=COLORS['text'])
        ax.grid(False)

        lim = C * math.sqrt(N_SEEDS) * 1.05
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

    # Annotation on golden angle panel
    axes[0].text(
        0.5, -0.09,
        r'$\theta_n = n \cdot \frac{2\pi}{\phi^2}$,  $r_n = c\sqrt{n}$'
        '\n'
        r'Fibonacci spirals emerge from irrational $\phi$-based spacing',
        transform=axes[0].transAxes, ha='center',
        color=COLORS['e_gold'], fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85),
    )

    plt.tight_layout()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'phyllotaxis', out_dir)
    plt.close(fig)
    print("Done: phyllotaxis")


if __name__ == '__main__':
    main()
