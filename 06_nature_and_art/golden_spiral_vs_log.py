"""
golden_spiral_vs_log.py — Golden spiral (φ-based) vs e-based logarithmic spiral.

Left:  r = φ^(2θ/π)  — the golden spiral (quarter-turn growth factor = φ)
Right: r = e^(0.3063·θ)  — e-based spiral with identical growth rate

They are virtually indistinguishable, illustrating the deep connection
between the golden ratio and the exponential function.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.cm as cm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

PHI = (1 + math.sqrt(5)) / 2          # ≈ 1.6180
# ln(φ) / (π/2) so that each quarter turn the radius grows by φ
A_E  = math.log(PHI) / (math.pi / 2)  # ≈ 0.3063


def spiral_xy(r_func, theta):
    r = r_func(theta)
    return r * np.cos(theta), r * np.sin(theta)


def gradient_lc(x, y, cmap_name, lw=2.8):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    colors = matplotlib.colormaps[cmap_name](np.linspace(0, 1, len(segments)))
    return LineCollection(segments, colors=colors, linewidth=lw, alpha=0.95)


def annotate_growth(ax, theta_vals, r_func, color, label_prefix):
    """Mark quarter-turn growth points and annotate radius ratio."""
    prev_r = None
    for t in theta_vals:
        r = r_func(t)
        xp, yp = r * math.cos(t), r * math.sin(t)
        ax.plot(xp, yp, 'o', color=color, markersize=7, zorder=6)
        if prev_r is not None:
            ratio = r / prev_r
            ax.annotate(f'×{ratio:.4f}',
                        xy=(xp, yp), xytext=(xp + 0.3, yp + 0.3),
                        color=color, fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7))
        prev_r = r


def main():
    apply_euler_style()

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Golden Spiral vs $e$-based Logarithmic Spiral',
        fontsize=20, fontweight='bold', color=COLORS['e_gold'], y=1.01,
    )

    theta = np.linspace(0, 5 * math.pi, 6000)
    quarter_turns = [math.pi / 2 * k for k in range(1, 9)]

    # ── Left: Golden spiral r = φ^(2θ/π) ──────────────────────────────────
    ax = axes[0]
    ax.set_facecolor(COLORS['bg_card'])

    phi_r = lambda t: PHI ** (2 * t / math.pi)
    x_phi, y_phi = spiral_xy(phi_r, theta)
    lc_phi = gradient_lc(x_phi, y_phi, 'YlOrBr')
    ax.add_collection(lc_phi)
    ax.autoscale()

    annotate_growth(ax, quarter_turns[:6], phi_r, COLORS['e_gold'], 'φ')

    ax.set_title(
        r'Golden Spiral: $r = \varphi^{\,2\theta/\pi}$'
        '\n'
        r'($\varphi \approx 1.6180$, growth per ¼-turn = φ)',
        color=COLORS['text'], fontsize=13,
    )
    ax.set_aspect('equal')
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.2, color=COLORS['grid'])
    ax.tick_params(colors=COLORS['text'])

    # Info box
    ax.text(0.03, 0.97,
            f'φ = {PHI:.6f}\na_e equivalent = {A_E:.6f}\n'
            r'$r_{n+1}/r_n = \varphi$ per ¼ turn',
            transform=ax.transAxes, va='top',
            color=COLORS['e_gold'], fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                      edgecolor=COLORS['e_gold'], alpha=0.9))

    # ── Right: e-based spiral r = e^(a·θ) with a = ln(φ)/(π/2) ────────────
    ax2 = axes[1]
    ax2.set_facecolor(COLORS['bg_card'])

    e_r = lambda t: np.exp(A_E * t)
    x_e, y_e = spiral_xy(e_r, theta)
    lc_e = gradient_lc(x_e, y_e, 'cool')
    ax2.add_collection(lc_e)
    ax2.autoscale()

    annotate_growth(ax2, quarter_turns[:6], lambda t: math.exp(A_E * t),
                    COLORS['e_cyan'], 'e')

    ax2.set_title(
        r'$e$-based Spiral: $r = e^{a\theta}$'
        '\n'
        rf'$a = \ln\varphi\,/\,(\pi/2) \approx {A_E:.4f}$',
        color=COLORS['text'], fontsize=13,
    )
    ax2.set_aspect('equal')
    ax2.set_xlabel('x', color=COLORS['text'])
    ax2.set_ylabel('y', color=COLORS['text'])
    ax2.grid(True, alpha=0.2, color=COLORS['grid'])
    ax2.tick_params(colors=COLORS['text'])

    # Difference overlay
    ax2.text(0.03, 0.97,
             r'$a = \ln\varphi\,/\,(\pi/2)$' + '\n'
             r'Identical growth rate!' + '\n'
             r'$e^{a \cdot \pi/2} = \varphi$',
             transform=ax2.transAxes, va='top',
             color=COLORS['e_cyan'], fontsize=9,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_cyan'], alpha=0.9))

    # Comparison note at bottom
    fig.text(
        0.5, -0.02,
        f'Both spirals grow by a factor of φ ≈ {PHI:.4f} per quarter turn.  '
        f'They are geometrically identical — only the base differs.',
        ha='center', color=COLORS['text'], fontsize=10, style='italic',
    )

    plt.tight_layout()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'golden_spiral_vs_log', out_dir)
    plt.close(fig)
    print("Done: golden_spiral_vs_log")


if __name__ == '__main__':
    main()
