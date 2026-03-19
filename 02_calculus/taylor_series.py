"""
taylor_series.py — Taylor polynomial approximations to e^x.

Static multi-panel figure showing polynomials with n = 1, 2, 3, 5, 8, 12 terms
alongside the exact e^x curve.
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

# Number of terms to show (each panel shows one approximation)
TERM_COUNTS = [1, 2, 3, 5, 8, 12]
X_RANGE = (-4, 4)
Y_LIM = (-2, 20)

PANEL_COLORS = [
    COLORS['e_red'],
    COLORS['e_orange'],
    COLORS['e_gold'],
    COLORS['e_green'],
    COLORS['e_cyan'],
    COLORS['e_purple'],
]


def taylor_exp(x, n_terms):
    """Taylor polynomial of e^x up to n_terms terms: Σ x^k/k! for k=0..n_terms-1."""
    result = np.zeros_like(x, dtype=float)
    for k in range(n_terms):
        result += x ** k / math.factorial(k)
    return result


def main():
    apply_euler_style()

    x = np.linspace(X_RANGE[0], X_RANGE[1], 600)
    y_exact = np.exp(x)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    axes = axes.flatten()

    for idx, (n, color, ax) in enumerate(zip(TERM_COUNTS, PANEL_COLORS, axes)):
        ax.set_facecolor(COLORS['bg_card'])

        y_approx = taylor_exp(x, n)
        # Clip to keep y-axis sane
        y_approx_clipped = np.clip(y_approx, Y_LIM[0] - 5, Y_LIM[1] + 5)

        ax.plot(x, y_exact, color=COLORS['e_gold'], lw=2.5, label=r'$e^x$ (exact)', zorder=4)
        ax.plot(x, y_approx_clipped, color=color, lw=2, ls='--',
                label=f'$P_{{{n}}}(x)$ ({n} term{"s" if n > 1 else ""})', zorder=3)

        # Shaded error region
        err_region = np.abs(y_exact - y_approx_clipped)
        ax.fill_between(x,
                        np.clip(y_exact, Y_LIM[0], Y_LIM[1]),
                        np.clip(y_approx_clipped, Y_LIM[0], Y_LIM[1]),
                        alpha=0.15, color=color)

        ax.set_ylim(Y_LIM)
        ax.set_xlim(X_RANGE)
        ax.set_xlabel('$x$', color=COLORS['text'], fontsize=10)
        ax.set_ylabel('$y$', color=COLORS['text'], fontsize=10)
        ax.set_title(
            r'$P_{' + str(n) + r'}(x) = \sum_{k=0}^{' + str(n - 1) + r'} \frac{x^k}{k!}$',
            color=COLORS['text'], fontsize=12, pad=8)
        ax.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
        ax.grid(True, alpha=0.3, color=COLORS['grid'])
        ax.axhline(0, color=COLORS['grid'], lw=0.8, alpha=0.5)
        ax.axvline(0, color=COLORS['grid'], lw=0.8, alpha=0.5)

        # Quality range annotation: find where |approx - exact| < 0.01
        good = np.where(np.abs(y_exact - y_approx) < 0.05)[0]
        if len(good) > 0:
            x_min_good = x[good[0]]
            x_max_good = x[good[-1]]
            ax.axvspan(x_min_good, x_max_good, alpha=0.08, color=color, zorder=1)
            ax.text(0.5, 0.04,
                    f'Good approx: [{x_min_good:.1f}, {x_max_good:.1f}]',
                    transform=ax.transAxes, ha='center', fontsize=8,
                    color=color, alpha=0.9)

    fig.suptitle(r"Taylor Series Approximations to $e^x = \sum_{k=0}^\infty \frac{x^k}{k!}$",
                 fontsize=18, color=COLORS['e_gold'], y=1.01, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'taylor_series', out_dir)
    plt.close(fig)
    print("Done: taylor_series")


if __name__ == '__main__':
    main()
