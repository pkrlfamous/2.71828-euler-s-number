"""
natural_log_derivative.py — d/dx(ln x) = 1/x

Left:  ln(x) with tangent lines showing the slope equals 1/x.
Right: 1/x function alongside the numerical derivative of ln(x).
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


def main():
    apply_euler_style()

    x = np.linspace(0.05, 5.0, 600)
    y_ln = np.log(x)
    y_inv = 1.0 / x

    # Numerical derivative of ln(x)
    h = 1e-6
    x_nd = np.linspace(0.1, 5.0, 500)
    y_deriv_num = (np.log(x_nd + h) - np.log(x_nd - h)) / (2 * h)
    y_inv_nd = 1.0 / x_nd

    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # --- Left: ln(x) with tangent lines ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    ax1.plot(x, y_ln, color=COLORS['e_gold'], lw=3, label=r'$f(x) = \ln x$', zorder=4)
    ax1.axhline(0, color=COLORS['grid'], lw=0.8, alpha=0.5)
    ax1.axvline(1, color=COLORS['e_green'], lw=1.5, ls=':', alpha=0.7)

    # Mark special points and draw tangents
    tangent_points = [0.5, 1.0, 2.0, 3.5]
    tangent_colors = [COLORS['e_red'], COLORS['e_cyan'], COLORS['e_purple'], COLORS['e_orange']]
    for xp, tc in zip(tangent_points, tangent_colors):
        slope = 1.0 / xp
        y_pt = np.log(xp)
        span = 0.6
        tx = np.linspace(xp - span, xp + span, 50)
        ty = y_pt + slope * (tx - xp)
        ax1.plot(tx, ty, color=tc, lw=1.8, ls='--', alpha=0.8)
        ax1.plot(xp, y_pt, 'o', color=tc, markersize=8, zorder=5)
        ax1.annotate(f'slope $= 1/{xp} = {slope:.2f}$',
                     xy=(xp, y_pt), xytext=(xp + 0.2, y_pt - 0.4),
                     fontsize=8, color=tc,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7))

    ax1.text(0.03, 0.97,
             r'$\frac{d}{dx}\ln x = \frac{1}{x}$',
             transform=ax1.transAxes, fontsize=15, verticalalignment='top',
             color=COLORS['e_green'], fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax1.set_xlabel('$x$', color=COLORS['text'])
    ax1.set_ylabel('$\\ln x$', color=COLORS['text'])
    ax1.set_title(r'$\ln x$ — Tangent Slopes Equal $1/x$',
                  color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, 5.2)
    ax1.set_ylim(-3, 2.5)

    # --- Right: 1/x vs numerical derivative ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    ax2.plot(x_nd, y_inv_nd, color=COLORS['e_blue'], lw=3, label=r'$1/x$ (exact derivative)',
             zorder=4)
    ax2.plot(x_nd, y_deriv_num, color=COLORS['e_pink'], lw=2, ls='--',
             label=r'Numerical $\frac{d}{dx}\ln x$', zorder=3)

    # Error inset (tiny text)
    err = np.abs(y_inv_nd - y_deriv_num)
    ax2.text(0.55, 0.95,
             f'Max error: {err.max():.2e}\n(floating-point only)',
             transform=ax2.transAxes, fontsize=9, verticalalignment='top',
             color=COLORS['e_orange'],
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.axhline(0, color=COLORS['grid'], lw=0.8, alpha=0.5)
    ax2.set_xlabel('$x$', color=COLORS['text'])
    ax2.set_ylabel('$1/x$', color=COLORS['text'])
    ax2.set_title(r"$1/x$ = Derivative of $\ln x$ (Confirmed Numerically)",
                  color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_xlim(0.1, 5.0)
    ax2.set_ylim(-0.2, 5)

    # Fundamental theorem note
    ax2.text(0.03, 0.97,
             r'$\int_1^e \frac{1}{t}\,dt = 1$' + '\n' + r'(defines $\ln$ and $e$!)',
             transform=ax2.transAxes, fontsize=11, verticalalignment='top',
             color=COLORS['e_gold'],
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    fig.suptitle(r"$\frac{d}{dx}\ln x = \frac{1}{x}$ — The Natural Logarithm Derivative",
                 fontsize=17, color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'natural_log_derivative', out_dir)
    plt.close(fig)
    print("Done: natural_log_derivative")


if __name__ == '__main__':
    main()
