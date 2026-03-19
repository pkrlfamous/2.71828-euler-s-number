"""
Static multi-frame view of e^(iθ) on the unit circle.
Shows 8 positions with horizontal (cos) and vertical (sin) components.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

FRAME_ANGLES = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4,
                np.pi, 5 * np.pi / 4, 3 * np.pi / 2, 7 * np.pi / 4]
ANGLE_LABELS = ['0', 'π/4', 'π/2', '3π/4', 'π', '5π/4', '3π/2', '7π/4']
FRAME_COLORS = [
    COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_purple'],
    COLORS['e_red'], COLORS['e_orange'], COLORS['e_pink'], COLORS['e_blue']
]


def draw_frame(ax, theta, color, label):
    """Draw unit circle, the point e^(iθ), and its cos/sin components."""
    circ_th = np.linspace(0, 2 * np.pi, 360)
    ax.plot(np.cos(circ_th), np.sin(circ_th),
            color=COLORS['e_cyan'], lw=1.4, alpha=0.5)

    cx, sy = np.cos(theta), np.sin(theta)

    # Radius vector
    ax.annotate('', xy=(cx, sy), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.2))

    # Cosine (horizontal) component
    ax.plot([0, cx], [0, 0], color=COLORS['e_blue'], lw=2,
            linestyle='-', solid_capstyle='round')
    ax.plot([cx, cx], [0, sy], color=COLORS['e_red'], lw=2,
            linestyle='-', solid_capstyle='round')

    # Dashed drop lines to axes
    ax.plot([cx, cx], [sy, 0], color=COLORS['e_blue'], lw=0.8,
            linestyle=':', alpha=0.5)
    ax.plot([0, cx], [sy, sy], color=COLORS['e_red'], lw=0.8,
            linestyle=':', alpha=0.5)

    # Point on circle
    ax.plot(cx, sy, 'o', color=color, markersize=10, zorder=6,
            markeredgecolor='white', markeredgewidth=0.8)

    # Cos / sin values on axes
    ax.plot(cx, 0, 's', color=COLORS['e_blue'], markersize=7, zorder=5)
    ax.plot(0, sy, 's', color=COLORS['e_red'], markersize=7, zorder=5)

    ax.axhline(0, color=COLORS['grid'], lw=0.7, alpha=0.6)
    ax.axvline(0, color=COLORS['grid'], lw=0.7, alpha=0.6)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal')
    ax.set_facecolor(COLORS['bg_card'])
    ax.grid(True, alpha=0.15)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.tick_params(labelsize=7)

    ax.set_title(
        rf'$\theta = {label}$' + '\n'
        rf'$\cos={cx:.3f}$,  $\sin={sy:.3f}$',
        color=color, fontsize=9, pad=4
    )


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Unit Circle: 8 Positions of $e^{i\theta}$  with cos and sin Components',
        fontsize=20, color=COLORS['e_gold'], fontweight='bold', y=0.99
    )

    gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.45, wspace=0.35)

    for idx, (theta, label, color) in enumerate(
            zip(FRAME_ANGLES, ANGLE_LABELS, FRAME_COLORS)):
        row, col = divmod(idx, 4)
        ax = fig.add_subplot(gs[row, col])
        draw_frame(ax, theta, color, label)

    # Legend panel at bottom
    legend_ax = fig.add_axes([0.1, 0.01, 0.8, 0.04])
    legend_ax.set_facecolor(COLORS['bg_dark'])
    legend_ax.axis('off')

    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], color=COLORS['e_cyan'], lw=2, label='Unit circle'),
        Line2D([0], [0], color=COLORS['e_gold'], lw=2.5,
               marker='o', markersize=8, label=r'$e^{i\theta}$ point'),
        Line2D([0], [0], color=COLORS['e_blue'], lw=2, label=r'cos(θ) component'),
        Line2D([0], [0], color=COLORS['e_red'], lw=2, label=r'sin(θ) component'),
    ]
    legend_ax.legend(handles=handles, loc='center', ncol=4, fontsize=11,
                     facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'],
                     labelcolor=COLORS['text'])

    save_plot(fig, 'unit_circle_frames', OUTPUT_DIR)
    plt.close(fig)
    print("unit_circle_animation.py done.")


if __name__ == '__main__':
    main()
