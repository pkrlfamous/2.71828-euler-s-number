"""
logarithmic_spiral.py — r = e^(aθ): the self-similar logarithmic spiral.

Three panels comparing tight (a=0.1), nautilus-like (a=0.2), and loose (a=0.3)
spirals, with annotations for the constant-angle (equiangular) property.
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


def draw_spiral(ax, a, theta_max, color, title, cmap_name='plasma'):
    """Draw a single logarithmic spiral with self-similarity arrows."""
    ax.set_facecolor(COLORS['bg_card'])
    theta = np.linspace(0, theta_max, 4000)
    r = np.exp(a * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Gradient line collection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    colors_arr = matplotlib.colormaps[cmap_name](np.linspace(0, 1, len(segments)))
    lc = LineCollection(segments, colors=colors_arr, linewidth=2.5, alpha=0.95)
    ax.add_collection(lc)

    # Self-similar growth arrows at 90° intervals
    angles_arrow = [math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi,
                    5 * math.pi / 2, 3 * math.pi]
    for ang in angles_arrow:
        if ang > theta_max:
            break
        r_a = math.exp(a * ang)
        r_b = math.exp(a * (ang + 0.3))
        x_a, y_a = r_a * math.cos(ang), r_a * math.sin(ang)
        dx = (r_b * math.cos(ang + 0.3) - x_a) * 0.4
        dy = (r_b * math.sin(ang + 0.3) - y_a) * 0.4
        ax.annotate('', xy=(x_a + dx, y_a + dy), xytext=(x_a, y_a),
                    arrowprops=dict(arrowstyle='->', color='white',
                                    lw=1.2, mutation_scale=12))

    # Constant-angle annotation at one point
    t_ann = 2.5
    r_ann = math.exp(a * t_ann)
    x_ann, y_ann = r_ann * math.cos(t_ann), r_ann * math.sin(t_ann)
    alpha_deg = math.degrees(math.atan(1.0 / a)) if a != 0 else 90
    ax.annotate(
        f'α ≈ {alpha_deg:.1f}°\n(constant)',
        xy=(x_ann, y_ann), xytext=(x_ann + 1.5, y_ann + 1.0),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.2),
        color=COLORS['e_gold'], fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85),
    )

    ax.autoscale()
    ax.set_aspect('equal')
    ax.set_title(f'{title}\na = {a}', color=COLORS['text'], fontsize=13)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.2, color=COLORS['grid'])
    ax.tick_params(colors=COLORS['text'])

    # Label origin
    ax.plot(0, 0, '+', color='white', markersize=10, markeredgewidth=1.5, zorder=5)


def main():
    apply_euler_style()

    configs = [
        (0.1, 6 * math.pi, 'Tight Spiral',        'cool'),
        (0.2, 5 * math.pi, 'Nautilus-like Spiral', 'plasma'),
        (0.3, 4 * math.pi, 'Loose Spiral',         'spring'),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Logarithmic Spiral  $r = e^{a\theta}$  — Self-Similar Growth',
        fontsize=20, fontweight='bold', color=COLORS['e_gold'], y=1.01,
    )

    colors = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_pink']]
    for ax, (a, theta_max, title, cmap) in zip(axes, configs):
        draw_spiral(ax, a, theta_max, colors[configs.index((a, theta_max, title, cmap))],
                    title, cmap)

    # Shared description
    fig.text(
        0.5, -0.02,
        r'Equal-angle property: the angle between the tangent and radius vector is $\alpha = \arctan(1/a)$ — constant everywhere on the spiral.',
        ha='center', color=COLORS['text'], fontsize=10, style='italic',
    )

    plt.tight_layout()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'logarithmic_spiral', out_dir)
    plt.close(fig)
    print("Done: logarithmic_spiral")


if __name__ == '__main__':
    main()
