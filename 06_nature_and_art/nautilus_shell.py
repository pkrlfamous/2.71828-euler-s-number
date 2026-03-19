"""
nautilus_shell.py — Nautilus cross-section as a logarithmic spiral.

Simulates the characteristic chambered nautilus by:
  - Drawing multiple logarithmic spirals rotated by 90° increments
  - Filling each chamber with a distinct color gradient
  - Adding radial chamber dividers
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.cm as cm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

A = 0.18   # nautilus growth constant


def log_spiral(a, theta_start, theta_end, n=600, phase=0.0):
    theta = np.linspace(theta_start, theta_end, n)
    r = np.exp(a * theta)
    x = r * np.cos(theta + phase)
    y = r * np.sin(theta + phase)
    return x, y


def main():
    apply_euler_style()

    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    ax.set_facecolor('#0a0a1a')
    ax.set_aspect('equal')

    # Chamber colors — pearlescent palette
    chamber_colors = [
        '#f5deb3', '#deb887', '#cd853f', '#d2691e',
        '#a0522d', '#8b4513', '#6b3410', '#4a2408',
    ]
    n_chambers = 8
    theta_step = math.pi / 2  # quarter turn per chamber

    # Outer and inner spiral boundaries
    theta_full_out = np.linspace(0, n_chambers * theta_step, 3000)
    r_out = np.exp(A * theta_full_out)
    x_out = r_out * np.cos(theta_full_out)
    y_out = r_out * np.sin(theta_full_out)

    # Draw chambers
    for k in range(n_chambers):
        t_start = k * theta_step
        t_end = (k + 1) * theta_step

        # Outer arc of this chamber
        theta_arc = np.linspace(t_start, t_end, 200)
        r_outer = np.exp(A * theta_arc)
        x_o = r_outer * np.cos(theta_arc)
        y_o = r_outer * np.sin(theta_arc)

        # Inner arc (one full turn back)
        r_inner = np.exp(A * (theta_arc - 2 * math.pi))
        x_i = r_inner * np.cos(theta_arc)
        y_i = r_inner * np.sin(theta_arc)

        # Fill chamber
        x_patch = np.concatenate([x_o, x_i[::-1]])
        y_patch = np.concatenate([y_o, y_i[::-1]])
        alpha_val = 0.7 - k * 0.04
        ax.fill(x_patch, y_patch,
                color=chamber_colors[k % len(chamber_colors)],
                alpha=max(0.35, alpha_val), zorder=2)

        # Chamber wall (septa)
        r_sep_start = math.exp(A * t_end - 2 * A * math.pi)
        r_sep_end = math.exp(A * t_end)
        x_s = [r_sep_start * math.cos(t_end), r_sep_end * math.cos(t_end)]
        y_s = [r_sep_start * math.sin(t_end), r_sep_end * math.sin(t_end)]
        ax.plot(x_s, y_s, color='#fff8dc', lw=1.0, alpha=0.7, zorder=4)

    # Outer spiral outline
    ax.plot(x_out, y_out, color=COLORS['e_gold'], lw=2.5, zorder=5,
            label=r'$r = e^{0.18\,\theta}$')

    # Inner spiral outline (one full rotation back)
    theta_inner = np.linspace(0, n_chambers * theta_step, 3000)
    r_in_line = np.exp(A * (theta_inner - 2 * math.pi))
    mask_in = r_in_line > 0.05
    x_in_l = r_in_line[mask_in] * np.cos(theta_inner[mask_in])
    y_in_l = r_in_line[mask_in] * np.sin(theta_inner[mask_in])
    ax.plot(x_in_l, y_in_l, color=COLORS['e_gold'], lw=1.5, alpha=0.6, zorder=5)

    # Siphuncle (central tube) — small central spiral
    theta_sip = np.linspace(0, 6 * math.pi, 1000)
    r_sip = 0.02 * np.exp(A * theta_sip)
    x_sip = r_sip * np.cos(theta_sip)
    y_sip = r_sip * np.sin(theta_sip)
    ax.plot(x_sip, y_sip, color=COLORS['e_cyan'], lw=1.5, alpha=0.8,
            label='Siphuncle', zorder=6)

    # Annotations
    r_ann = math.exp(A * 3 * math.pi)
    ax.annotate(
        r'$r = e^{a\theta}$' + '\n' + r'$a = 0.18$',
        xy=(r_ann * math.cos(3 * math.pi), r_ann * math.sin(3 * math.pi)),
        xytext=(r_ann * 0.4, r_ann * 0.6),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5),
        color=COLORS['e_gold'], fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                  edgecolor=COLORS['e_gold'], alpha=0.9),
        zorder=8,
    )

    # Growth ratio annotation
    r1 = math.exp(A * math.pi / 2)
    r2 = math.exp(A * math.pi)
    ax.annotate(
        f'Growth ratio\nper 90°: {r2/r1:.3f}×',
        xy=(r1 * math.cos(math.pi / 2), r1 * math.sin(math.pi / 2)),
        xytext=(-r1 * 1.4, r1 * 1.4),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.2),
        color=COLORS['e_cyan'], fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85),
        zorder=8,
    )

    ax.set_title(
        'Nautilus Shell — Chambered Logarithmic Spiral',
        color=COLORS['e_gold'], fontsize=17, fontweight='bold', pad=14,
    )
    ax.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=11, loc='lower right')
    ax.tick_params(colors=COLORS['text'])
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.1, color=COLORS['grid'])

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'nautilus_shell', out_dir)
    plt.close(fig)
    print("Done: nautilus_shell")


if __name__ == '__main__':
    main()
