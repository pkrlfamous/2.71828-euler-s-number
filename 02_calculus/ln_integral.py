"""
ln_integral.py — ∫₁ᵉ (1/t) dt = 1

Plots 1/t from t = 0.1 to 4, shades the area from 1 to e,
and annotates that the shaded area equals exactly 1 — which defines ln and e.
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
from utils.math_helpers import numerical_integral

E = math.e


def main():
    apply_euler_style()

    x_full = np.linspace(0.1, 4.5, 600)
    y_full = 1.0 / x_full

    x_fill = np.linspace(1.0, E, 400)
    y_fill = 1.0 / x_fill

    exact_val = math.log(E) - math.log(1)   # = 1
    numerical_val = numerical_integral(lambda t: 1.0 / t, 1.0, E)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    ax.set_facecolor(COLORS['bg_card'])

    # Main curve
    ax.plot(x_full, y_full, color=COLORS['e_gold'], lw=3, label=r'$f(t) = 1/t$', zorder=4)

    # Shaded integral region
    ax.fill_between(x_fill, y_fill, alpha=0.45, color=COLORS['e_green'],
                    label=r'$\int_1^e \frac{1}{t}\,dt = 1$', zorder=2)
    ax.fill_between(x_fill, y_fill, alpha=0.2, color=COLORS['e_cyan'], zorder=2)

    # Boundary verticals
    ax.axvline(1.0, color=COLORS['e_red'], lw=2, ls='--', alpha=0.9, label='$t = 1$')
    ax.axvline(E, color=COLORS['e_blue'], lw=2, ls='--', alpha=0.9,
               label=f'$t = e \\approx {E:.5f}$')
    ax.axhline(0, color=COLORS['grid'], lw=0.8, alpha=0.5)

    # Shaded area label
    mid_x = (1.0 + E) / 2
    mid_y = 1.0 / mid_x * 0.55
    ax.text(mid_x, mid_y,
            r'Area $= 1$' + '\n' + r'exactly!',
            ha='center', va='center', fontsize=16,
            color='white', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['e_green'],
                      alpha=0.85, edgecolor='white'))

    # Point annotations
    ax.plot(1.0, 1.0, 'o', color=COLORS['e_red'], markersize=10, zorder=6)
    ax.annotate('$(1,\\ 1)$', xy=(1.0, 1.0), xytext=(1.15, 1.15),
                color=COLORS['e_red'], fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['e_red'], lw=1))

    ax.plot(E, 1.0 / E, 'o', color=COLORS['e_blue'], markersize=10, zorder=6)
    ax.annotate(f'$(e,\\ 1/e) \\approx ({E:.3f},\\ {1/E:.3f})$',
                xy=(E, 1.0 / E), xytext=(E + 0.3, 1.0 / E + 0.15),
                color=COLORS['e_blue'], fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['e_blue'], lw=1))

    # Definition box
    ax.text(0.55, 0.87,
            r'$\ln x \equiv \int_1^x \frac{1}{t}\,dt$' + '\n\n'
            r'$e$ is the unique number where' + '\n'
            r'$\int_1^e \frac{1}{t}\,dt = 1$',
            transform=ax.transAxes, fontsize=12, verticalalignment='top',
            color=COLORS['e_gold'],
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.9))

    ax.text(0.02, 0.97,
            f'Exact value: $\\ln e = {exact_val:.1f}$\n'
            f'Numerical (Simpson): {numerical_val:.8f}',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            color=COLORS['e_cyan'],
            bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax.set_xlabel('$t$', color=COLORS['text'], fontsize=13)
    ax.set_ylabel('$1/t$', color=COLORS['text'], fontsize=13)
    ax.set_title(r"$\int_1^e \frac{1}{t}\,dt = 1$ — The Integral Definition of $e$",
                 color=COLORS['text'], fontsize=14, pad=12)
    ax.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=11,
              loc='upper right')
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.2, 3.5)

    fig.suptitle(r"$e$ Defined by the Integral: $\int_1^e \frac{1}{t}\,dt = 1$",
                 fontsize=17, color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'ln_integral', out_dir)
    plt.close(fig)
    print("Done: ln_integral")


if __name__ == '__main__':
    main()
