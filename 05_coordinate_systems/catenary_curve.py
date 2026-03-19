"""
catenary_curve.py — The catenary: y = a·cosh(x/a)

Plots catenary curves for a = 0.5, 1, 2, 3 alongside a parabola,
shows the hanging-chain interpretation, and annotates key properties.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS


def catenary(x, a):
    return a * np.cosh(x / a)


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"The Catenary:  $y = a\cosh\!\left(\frac{x}{a}\right) = \frac{a}{2}\!\left(e^{x/a}+e^{-x/a}\right)$",
        fontsize=18, fontweight='bold', color=COLORS['e_gold'], y=0.98,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    a_values = [0.5, 1.0, 2.0, 3.0]
    palette = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_green'], COLORS['e_pink']]

    # ── Left: multiple catenaries ─────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    x = np.linspace(-6, 6, 1000)

    for a, color in zip(a_values, palette):
        y = catenary(x, a)
        mask = y < 15  # clip tall catenaries
        ax1.plot(x[mask], y[mask], color=color, lw=2.5, label=f'a = {a}')
        # Mark the vertex (lowest point)
        ax1.plot(0, a, 'o', color=color, markersize=7, zorder=5)

    # Parabola for comparison
    y_para = x**2 / 2 + 1
    mask_p = y_para < 15
    ax1.plot(x[mask_p], y_para[mask_p], color=COLORS['e_red'],
             lw=2, ls='--', label=r'Parabola $y=x^2/2+1$')

    ax1.set_xlim(-6, 6)
    ax1.set_ylim(0, 14)
    ax1.set_xlabel('x', color=COLORS['text'], fontsize=13)
    ax1.set_ylabel('y', color=COLORS['text'], fontsize=13)
    ax1.set_title('Catenary Curves for Various a', color=COLORS['text'], fontsize=14)
    ax1.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.25, color=COLORS['grid'])
    ax1.tick_params(colors=COLORS['text'])

    # Annotation: vertex is at (0, a)
    ax1.annotate('Vertex (0, a)\nlowest point',
                 xy=(0, 1.0), xytext=(1.5, 1.8),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5),
                 color=COLORS['e_gold'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    # ── Right: hanging-chain illustration ─────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    a_chain = 1.5
    x_chain = np.linspace(-4, 4, 500)
    y_chain = catenary(x_chain, a_chain)
    # Shift so the chain hangs from y=0
    y_hang = y_chain - catenary(np.array([4.0]), a_chain)[0]

    ax2.plot(x_chain, y_hang, color=COLORS['e_cyan'], lw=3.5, label=f'Catenary a={a_chain}')

    # Support poles
    pole_height = 0.5
    for xp in [-4, 4]:
        yp = catenary(np.array([xp]), a_chain)[0] - catenary(np.array([4.0]), a_chain)[0]
        ax2.plot([xp, xp], [yp - pole_height, yp + pole_height],
                 color=COLORS['e_orange'], lw=6, solid_capstyle='round', zorder=5)
        ax2.plot(xp, yp, 'o', color=COLORS['e_gold'], markersize=10, zorder=6)

    # Weight/tension force arrows
    n_arrows = 7
    x_arr = np.linspace(-3, 3, n_arrows)
    for xa in x_arr:
        ya = catenary(np.array([xa]), a_chain)[0] - catenary(np.array([4.0]), a_chain)[0]
        ax2.annotate('', xy=(xa, ya - 0.5), xytext=(xa, ya),
                     arrowprops=dict(arrowstyle='->', color=COLORS['e_purple'],
                                     lw=1.5, mutation_scale=12))

    # Tension direction indicator at one point
    x_t = 2.0
    y_t = catenary(np.array([x_t]), a_chain)[0] - catenary(np.array([4.0]), a_chain)[0]
    slope = math.sinh(x_t / a_chain)
    tangent = np.array([1, slope]) / math.sqrt(1 + slope**2) * 1.2
    ax2.annotate('Tension\nalong tangent',
                 xy=(x_t + tangent[0], y_t + tangent[1]),
                 xytext=(x_t + 1.5, y_t + 1.5),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5),
                 color=COLORS['e_gold'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    # Formula box
    ax2.text(0, y_hang.max() * 0.55,
             r'$y = a\cosh\!\left(\dfrac{x}{a}\right)$'
             '\n\n'
             r'$= \dfrac{a}{2}\!\left(e^{x/a}+e^{-x/a}\right)$',
             ha='center', va='center', color=COLORS['e_cyan'],
             fontsize=13,
             bbox=dict(boxstyle='round,pad=0.6', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_cyan'], alpha=0.9))

    ax2.set_title('Hanging Chain — Catenary in Nature', color=COLORS['text'], fontsize=14)
    ax2.set_xlabel('x', color=COLORS['text'], fontsize=13)
    ax2.set_ylabel('y', color=COLORS['text'], fontsize=13)
    ax2.grid(True, alpha=0.25, color=COLORS['grid'])
    ax2.tick_params(colors=COLORS['text'])
    ax2.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=10)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'catenary_curve', out_dir)
    plt.close(fig)
    print("Done: catenary_curve")


if __name__ == '__main__':
    main()
