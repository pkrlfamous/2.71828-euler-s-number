"""
limit_definition_plot.py — Visual showing WHY (1 + 1/n)^n → e.

For n = 1, 2, 5, 10, 100 shows:
  - The compound interest curves (1 + r/n)^(nt) for r=1
  - A number-line panel showing convergence to e
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

E = math.e
N_VALUES = [1, 2, 5, 10, 100]
PANEL_COLORS = [
    COLORS['e_red'],
    COLORS['e_orange'],
    COLORS['e_gold'],
    COLORS['e_green'],
    COLORS['e_cyan'],
]


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(15, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 1, figure=fig, hspace=0.45,
                           height_ratios=[3, 1])

    # ------------------------------------------------------------------ #
    # Top panel: compound growth curves (1 + 1/n)^(n*t) for t in [0, 1]  #
    # ------------------------------------------------------------------ #
    ax_top = fig.add_subplot(gs[0])
    ax_top.set_facecolor(COLORS['bg_card'])

    t = np.linspace(0, 1, 400)

    for n, color in zip(N_VALUES, PANEL_COLORS):
        # At time t: (1 + 1/n)^(n*t) — compound interest analogy
        y = (1 + 1.0 / n) ** (n * t)
        label = f'$n = {n}$: final $\\approx {(1+1/n)**n:.5f}$'
        ax_top.plot(t, y, color=color, lw=2.5, label=label)

    # True e^t (continuous compounding)
    ax_top.plot(t, np.exp(t), color='white', lw=2, ls='-.',
                label=r'$e^t$ (continuous, $n \to \infty$)', zorder=5)
    ax_top.plot(1, E, '*', color=COLORS['e_gold'], markersize=18, zorder=6)

    ax_top.set_xlabel('Time $t$ (normalised to [0, 1])', color=COLORS['text'], fontsize=12)
    ax_top.set_ylabel(r'$(1 + 1/n)^{nt}$', color=COLORS['text'], fontsize=12)
    ax_top.set_title(
        r'Compound Interest Analogy: $(1+1/n)^{nt}$ vs $e^t$ for Various $n$',
        color=COLORS['text'], fontsize=14, pad=10)
    ax_top.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'],
                  fontsize=10, loc='upper left')
    ax_top.grid(True, alpha=0.3, color=COLORS['grid'])

    # Explanation text
    ax_top.text(0.55, 0.12,
                r'$\$1$ invested at 100\% annual interest,' + '\n'
                r'compounded $n$ times/year' + '\n'
                r'grows to $(1+1/n)^n$ after 1 year' + '\n'
                r'As $n\to\infty$: grows to exactly $e$',
                transform=ax_top.transAxes, fontsize=11, verticalalignment='bottom',
                color=COLORS['e_gold'],
                bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.9))

    # ------------------------------------------------------------------ #
    # Bottom panel: number line showing convergence to e                  #
    # ------------------------------------------------------------------ #
    ax_bot = fig.add_subplot(gs[1])
    ax_bot.set_facecolor(COLORS['bg_card'])
    ax_bot.set_xlim(2.5, 2.75)
    ax_bot.set_ylim(-0.5, 1.5)
    ax_bot.set_yticks([])

    # Draw number line
    ax_bot.axhline(0, color=COLORS['text'], lw=2, alpha=0.8)

    # Mark e
    ax_bot.axvline(E, color=COLORS['e_red'], lw=3, ymin=0.1, ymax=0.9, zorder=5)
    ax_bot.text(E, 1.1, f'$e = {E:.8f}...$',
                ha='center', va='bottom', fontsize=12,
                color=COLORS['e_red'], fontweight='bold')

    # Mark each approximation
    approx_vals = [(1 + 1.0 / n) ** n for n in N_VALUES]
    y_levels = [0.25, 0.4, 0.55, 0.7, 0.85]
    for n, approx, color, ylevel in zip(N_VALUES, approx_vals, PANEL_COLORS, y_levels):
        ax_bot.plot(approx, 0, 'o', color=color, markersize=10, zorder=4)
        ax_bot.annotate(f'$n={n}$\n$\\approx{approx:.5f}$',
                        xy=(approx, 0),
                        xytext=(approx - 0.003, ylevel),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1),
                        color=color, fontsize=9, ha='center',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax_bot.set_xlabel('Value', color=COLORS['text'], fontsize=11)
    ax_bot.set_title(r'Number Line: $(1+1/n)^n \to e$ as $n$ Increases',
                     color=COLORS['text'], fontsize=13, pad=8)
    ax_bot.grid(True, axis='x', alpha=0.3, color=COLORS['grid'])

    fig.suptitle(r"Why $(1+1/n)^n \to e$ — A Visual Explanation",
                 fontsize=18, color=COLORS['e_gold'], y=1.01, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'limit_definition_plot', out_dir)
    plt.close(fig)
    print("Done: limit_definition_plot")


if __name__ == '__main__':
    main()
