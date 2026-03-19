"""
derivative_equals_self.py — d/dx(e^x) = e^x

Left:  overlay e^x and its numerical derivative (they match perfectly).
Right: error |e^x - numerical_derivative(e^x)| showing near-zero residual.
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
from utils.math_helpers import numerical_derivative


def main():
    apply_euler_style()

    x = np.linspace(-3, 3, 500)
    f = np.exp(x)

    # Vectorised central difference
    h = 1e-6
    df_numerical = (np.exp(x + h) - np.exp(x - h)) / (2 * h)
    error = np.abs(f - df_numerical)

    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # --- Left: overlay ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    ax1.plot(x, f, color=COLORS['e_gold'], lw=3, label=r'$e^x$ (exact)', zorder=3)
    ax1.plot(x, df_numerical, color=COLORS['e_cyan'], lw=2, ls='--',
             label=r"$\frac{d}{dx}e^x$ (numerical)", zorder=4)

    # Highlight a specific point
    x0 = 1.0
    y0 = np.exp(x0)
    slope = np.exp(x0)
    tangent_x = np.linspace(x0 - 0.8, x0 + 0.8, 50)
    tangent_y = y0 + slope * (tangent_x - x0)
    ax1.plot(tangent_x, tangent_y, color=COLORS['e_orange'], lw=2, ls=':',
             label=f'Tangent at $x=1$: slope $= e^1 \\approx {np.e:.3f}$')
    ax1.plot(x0, y0, 'o', color=COLORS['e_red'], markersize=10, zorder=5)

    ax1.set_xlabel('$x$', color=COLORS['text'])
    ax1.set_ylabel('$y$', color=COLORS['text'])
    ax1.set_title(r'$\frac{d}{dx}e^x = e^x$ — Function Equals Its Derivative',
                  color=COLORS['text'], pad=12)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_ylim(-1, 22)

    # Annotation box
    ax1.text(0.03, 0.97,
             r'$e^x$ is the unique function satisfying:' + '\n'
             r'$f\'(x) = f(x)$, $f(0) = 1$',
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             color=COLORS['e_green'],
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    # --- Right: error plot ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    ax2.semilogy(x, error + 1e-20, color=COLORS['e_purple'], lw=2,
                 label=r'$|e^x - \hat{f}\'(x)|$')
    ax2.set_xlabel('$x$', color=COLORS['text'])
    ax2.set_ylabel('Absolute Error  (log scale)', color=COLORS['text'])
    ax2.set_title('Numerical Differentiation Error\n(Central Difference, $h=10^{-6}$)',
                  color=COLORS['text'], pad=12)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])

    ax2.text(0.05, 0.95,
             f'Max error: {error.max():.2e}\n(floating-point rounding only)',
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             color=COLORS['e_orange'],
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    fig.suptitle(r"$\frac{d}{dx}e^x = e^x$ — The Self-Replicating Derivative",
                 fontsize=18, color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'derivative_equals_self', out_dir)
    plt.close(fig)
    print("Done: derivative_equals_self")


if __name__ == '__main__':
    main()
