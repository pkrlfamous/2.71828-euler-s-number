"""
tangent_line_slope1.py — At x=0, e^x has slope exactly 1.

Shows e^x zoomed near the origin with tangent lines for 2^x, e^x, and 4^x,
each labeled with their exact slope ln(base).
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


BASES = [2, math.e, 4]
BASE_LABELS = ['$2^x$', '$e^x$', '$4^x$']
BASE_COLORS = [COLORS['e_blue'], COLORS['e_gold'], COLORS['e_purple']]
TANGENT_COLORS = [COLORS['e_cyan'], COLORS['e_red'], COLORS['e_pink']]


def main():
    apply_euler_style()

    x_zoom = np.linspace(-1.5, 1.5, 500)
    x_full = np.linspace(-2.5, 2.5, 600)

    fig = plt.figure(figsize=(15, 6))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # --- Left: zoomed near origin ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for base, label, bc, tc in zip(BASES, BASE_LABELS, BASE_COLORS, TANGENT_COLORS):
        slope = math.log(base)
        y_curve = base ** x_zoom
        y_tangent = 1 + slope * x_zoom   # tangent at (0, 1): y = 1 + slope*x

        ax1.plot(x_zoom, y_curve, color=bc, lw=2.5, label=label)
        ax1.plot(x_zoom, y_tangent, color=tc, lw=1.8, ls='--', alpha=0.85,
                 label=f'Tangent: slope $= \\ln {base:.3f} \\approx {slope:.4f}$')

    # Mark origin
    ax1.plot(0, 1, 'o', color='white', markersize=12, zorder=6)
    ax1.plot(0, 1, '*', color=COLORS['e_gold'], markersize=10, zorder=7)
    ax1.annotate('(0, 1) — all three\ncurves pass here',
                 xy=(0, 1), xytext=(0.3, 0.3),
                 arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=1),
                 color=COLORS['text'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_xlabel('$x$', color=COLORS['text'])
    ax1.set_ylabel('$a^x$', color=COLORS['text'])
    ax1.set_title('Zoomed Near Origin — Tangent Lines at $x=0$',
                  color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=8,
               loc='upper left')
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.axhline(0, color=COLORS['grid'], lw=0.8)
    ax1.axvline(0, color=COLORS['grid'], lw=0.8)

    # --- Right: slope magnitude bar chart ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    slopes = [math.log(b) for b in BASES]
    x_pos = np.arange(len(BASES))
    bars = ax2.bar(x_pos, slopes, color=BASE_COLORS, edgecolor=COLORS['grid'],
                   linewidth=1, zorder=3, width=0.55)

    ax2.axhline(1.0, color=COLORS['e_red'], lw=2.5, ls='--', zorder=4,
                label='Slope = 1 (the special value for $e$)')
    ax2.axhline(0.0, color=COLORS['grid'], lw=1, alpha=0.5)

    for bar, base, slope in zip(bars, BASES, slopes):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 slope + 0.02,
                 f'$\\ln({base:.3f})$\n$= {slope:.4f}$',
                 ha='center', va='bottom', fontsize=11,
                 color=COLORS['text'], fontweight='bold')

    # Highlight e's bar
    bars[1].set_edgecolor(COLORS['e_red'])
    bars[1].set_linewidth(3)

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(['$2^x$', '$e^x$', '$4^x$'], fontsize=14)
    ax2.set_ylabel('Slope of $a^x$ at $x = 0$ (= $\\ln a$)', color=COLORS['text'])
    ax2.set_title('Slope at $x=0$: Only $e^x$ Has Slope = 1',
                  color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax2.grid(True, axis='y', alpha=0.3, color=COLORS['grid'])
    ax2.set_ylim(0, 1.6)

    ax2.text(0.5, 0.12,
             r'$\left.\frac{d}{dx}a^x\right|_{x=0} = \ln a$' + '\n\n'
             r'$e$ is defined so that $\ln e = 1$',
             transform=ax2.transAxes, ha='center', fontsize=12,
             color=COLORS['e_green'],
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.85))

    fig.suptitle(r"Why $e$? — The Unique Base with Slope 1 at the Origin",
                 fontsize=17, color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'tangent_line_slope1', out_dir)
    plt.close(fig)
    print("Done: tangent_line_slope1")


if __name__ == '__main__':
    main()
