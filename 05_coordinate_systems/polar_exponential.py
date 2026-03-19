"""
polar_exponential.py — Logarithmic spiral r = e^(aθ) in polar coordinates.

Plots multiple spirals for a = 0.05, 0.1, 0.2, 0.3 over θ ∈ [0, 6π].
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

E = math.e


def main():
    apply_euler_style()

    a_values = [0.05, 0.1, 0.2, 0.3]
    palette = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_green'], COLORS['e_pink']]
    theta = np.linspace(0, 6 * math.pi, 2000)

    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])

    # Main polar plot
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor(COLORS['bg_card'])
    ax.grid(color=COLORS['grid'], alpha=0.4, linewidth=0.5)
    ax.tick_params(colors=COLORS['text'])

    for a, color in zip(a_values, palette):
        r = np.exp(a * theta)
        # Color gradient along the curve
        points = np.array([theta, r]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Convert to Cartesian for LineCollection (polar axes handle conversion internally)
        lc = LineCollection(segments, colors=color, linewidth=2.0, alpha=0.9)
        ax.add_collection(lc)

        # Label at the tip of the spiral
        tip_theta = theta[-1]
        tip_r = r[-1]
        ax.annotate(
            f'a = {a}',
            xy=(tip_theta, tip_r),
            xytext=(tip_theta + 0.3, tip_r * 1.05),
            color=color,
            fontsize=11,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8,
                      edgecolor=color),
        )

    # Equation annotation
    ax.set_title(
        r'Logarithmic Spiral:  $r = e^{a\theta}$',
        color=COLORS['e_gold'],
        fontsize=18,
        fontweight='bold',
        pad=20,
    )

    # Radial label
    ax.set_rlabel_position(135)
    ax.set_thetagrids(
        np.arange(0, 360, 45),
        labels=[r'$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$',
                r'$\pi$', r'$5\pi/4$', r'$3\pi/2$', r'$7\pi/4$'],
        color=COLORS['text'],
        fontsize=9,
    )

    # Legend
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color=c, linewidth=2.5, label=f'a = {a}')
               for a, c in zip(a_values, palette)]
    ax.legend(
        handles=handles,
        loc='lower left',
        bbox_to_anchor=(0.02, 0.02),
        facecolor=COLORS['bg_dark'],
        edgecolor=COLORS['grid'],
        fontsize=10,
        title='Growth rate a',
        title_fontsize=9,
    )

    # Subtitle
    fig.text(
        0.5, 0.02,
        r'θ ∈ [0, 6π]   —   Equal angle property: angle between tangent and radius is constant',
        ha='center', color=COLORS['text'], fontsize=10, style='italic',
    )

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'polar_exponential', out_dir)
    plt.close(fig)
    print("Done: polar_exponential")


if __name__ == '__main__':
    main()
