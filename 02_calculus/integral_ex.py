"""
integral_ex.py — ∫e^x dx = e^x + C

Plots e^x with a shaded area under the curve from a = -1 to b = 2,
and annotates the exact integral value e^2 - e^(-1).
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

A, B = -1.0, 2.0
E = math.e


def main():
    apply_euler_style()

    x_full = np.linspace(-2.5, 3.0, 600)
    y_full = np.exp(x_full)

    x_fill = np.linspace(A, B, 400)
    y_fill = np.exp(x_fill)

    exact_integral = E ** B - E ** A
    numerical = numerical_integral(np.exp, A, B)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    ax.set_facecolor(COLORS['bg_card'])

    # Main curve
    ax.plot(x_full, y_full, color=COLORS['e_gold'], lw=3, label=r'$f(x) = e^x$', zorder=4)

    # Shaded region
    ax.fill_between(x_fill, y_fill, alpha=0.35, color=COLORS['e_blue'],
                    label=f'Area from $a={A}$ to $b={B}$', zorder=2)
    ax.fill_between(x_fill, y_fill, alpha=0.15, color=COLORS['e_cyan'], zorder=2)

    # Vertical boundary lines
    ax.axvline(A, color=COLORS['e_red'], lw=1.8, ls='--', alpha=0.8)
    ax.axvline(B, color=COLORS['e_red'], lw=1.8, ls='--', alpha=0.8)
    ax.axhline(0, color=COLORS['grid'], lw=1, alpha=0.5)

    # Annotations
    ax.annotate(f'$x = {A}$\n$e^{{{A}}} = {E**A:.4f}$',
                xy=(A, E**A), xytext=(A + 0.4, E**A + 1.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.2),
                color=COLORS['e_cyan'], fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax.annotate(f'$x = {B}$\n$e^{{{B}}} \\approx {E**B:.4f}$',
                xy=(B, E**B), xytext=(B - 1.5, E**B + 0.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.2),
                color=COLORS['e_cyan'], fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    # Integral value box
    mid_x = (A + B) / 2
    mid_y = np.exp(mid_x) * 0.5
    ax.text(mid_x, mid_y,
            f'$\\int_{{{A}}}^{{{B}}} e^x\\,dx$\n'
            f'$= e^{{{B}}} - e^{{{A}}}$\n'
            f'$\\approx {exact_integral:.6f}$',
            ha='center', va='center', fontsize=13,
            color=COLORS['text'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.9))

    # Antiderivative reminder
    ax.text(0.02, 0.97,
            r'$\int e^x\,dx = e^x + C$' + '\n\n'
            r'$e^x$ is its own antiderivative!',
            transform=ax.transAxes, fontsize=12, verticalalignment='top',
            color=COLORS['e_green'],
            bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax.text(0.98, 0.03,
            f'Numerical (Simpson): {numerical:.8f}\nExact: {exact_integral:.8f}',
            transform=ax.transAxes, fontsize=10,
            ha='right', va='bottom', color=COLORS['e_orange'],
            bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax.set_xlabel('$x$', color=COLORS['text'], fontsize=13)
    ax.set_ylabel('$e^x$', color=COLORS['text'], fontsize=13)
    ax.set_title(r'$\int e^x\,dx = e^x + C$ — Area Under the Exponential Curve',
                 color=COLORS['text'], fontsize=15, pad=12)
    ax.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=11)
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    ax.set_ylim(-0.5, 10)
    ax.set_xlim(-2.5, 3.0)

    fig.suptitle(r"The Integral of $e^x$ — Self-Replicating Under Integration",
                 fontsize=17, color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'integral_ex', out_dir)
    plt.close(fig)
    print("Done: integral_ex")


if __name__ == '__main__':
    main()
