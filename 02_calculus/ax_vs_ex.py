"""
ax_vs_ex.py — Wikipedia-style graph of 2^x, e^x, 4^x with tangent at origin.

Reproduces the classic comparison showing e^x as the unique exponential whose
tangent at the origin has slope exactly 1.
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

X_MIN, X_MAX = -2.5, 1.5
Y_MIN, Y_MAX = -0.5, 4.0


def main():
    apply_euler_style()

    x = np.linspace(X_MIN, X_MAX, 600)

    y2 = 2 ** x
    ye = np.e ** x
    y4 = 4 ** x
    tangent = x + 1          # y = x + 1 (slope 1 through (0,1))

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    ax.set_facecolor(COLORS['bg_card'])

    # All three exponentials in blue shades (Wikipedia style), then our accent
    ax.plot(x, y2, color=COLORS['e_blue'], lw=2.5, ls=':', label=r'$y = 2^x$')
    ax.plot(x, ye, color=COLORS['e_blue'], lw=3.0, ls='-', label=r'$y = e^x$')
    ax.plot(x, y4, color=COLORS['e_blue'], lw=2.5, ls='--', label=r'$y = 4^x$')

    # Red tangent line
    ax.plot(x, tangent, color=COLORS['e_red'], lw=2.5, ls='-',
            label=r'$y = x + 1$ (tangent at origin)')

    # Mark the origin point (0, 1)
    ax.plot(0, 1, 'o', color='white', markersize=10, zorder=6)
    ax.plot(0, 1, 'o', color=COLORS['e_red'], markersize=6, zorder=7)
    ax.annotate(r'$(0,\,1)$', xy=(0, 1), xytext=(0.12, 1.35),
                color=COLORS['text'], fontsize=13, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['e_red'], lw=1.2))

    # Label each curve at right edge
    label_x = 1.4
    for base, y_arr, label_str in [(2, y2, '$2^x$'), (math.e, ye, '$e^x$'), (4, y4, '$4^x$')]:
        y_val = base ** label_x
        if Y_MIN < y_val < Y_MAX:
            ax.text(label_x + 0.02, y_val, label_str, color=COLORS['e_blue'],
                    fontsize=13, va='center', fontweight='bold')

    ax.text(X_MIN + 0.05, X_MIN + 1 + 0.15, '$y = x+1$',
            color=COLORS['e_red'], fontsize=12)

    # Slope callouts
    slope_e = math.e ** 0 * math.log(math.e)   # = 1
    slope_2 = 2 ** 0 * math.log(2)
    slope_4 = 4 ** 0 * math.log(4)
    ax.text(0.03, 0.30,
            f"Slopes at $x=0$:\n"
            f"  $2^x$: $\\ln 2 \\approx {slope_2:.4f}$\n"
            f"  $e^x$: $\\ln e = {slope_e:.4f}$ ← exactly 1!\n"
            f"  $4^x$: $\\ln 4 \\approx {slope_4:.4f}$",
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            color=COLORS['e_gold'],
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.9))

    ax.set_xlim(X_MIN, X_MAX + 0.2)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_xlabel('$x$', color=COLORS['text'], fontsize=13)
    ax.set_ylabel('$y$', color=COLORS['text'], fontsize=13)
    ax.set_title(r'$2^x$, $e^x$, and $4^x$ — Only $e^x$ Has Slope 1 at the Origin',
                 color=COLORS['text'], fontsize=14, pad=12)
    ax.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'],
              fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    ax.axhline(0, color=COLORS['grid'], lw=1, alpha=0.5)
    ax.axvline(0, color=COLORS['grid'], lw=1, alpha=0.5)

    fig.suptitle(r"$a^x$ vs $e^x$ — Wikipedia Graph Reproduction",
                 fontsize=17, color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'ax_vs_ex_wikipedia', out_dir)
    plt.close(fig)
    print("Done: ax_vs_ex_wikipedia")


if __name__ == '__main__':
    main()
