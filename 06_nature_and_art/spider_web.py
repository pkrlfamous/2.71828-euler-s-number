"""
spider_web.py — Logarithmic spiral in spider webs.

Draws a realistic orb-weaver web:
  - 12 radial threads from center to frame
  - A logarithmic spiral connecting thread spiraling outward
  - A cross-connecting auxiliary spiral (inner zone)
  - Dew drop highlights on the spiral thread
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

N_RADIALS = 16
A_WEB = 0.12
R_MAX = math.exp(A_WEB * 3.5 * math.pi)
RNG = np.random.default_rng(7)


def main():
    apply_euler_style()

    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#050510')
    ax.set_facecolor('#050510')
    ax.set_aspect('equal')

    # ── Radial threads ────────────────────────────────────────────────────
    for k in range(N_RADIALS):
        angle = k * 2 * math.pi / N_RADIALS
        x_end = R_MAX * 1.05 * math.cos(angle)
        y_end = R_MAX * 1.05 * math.sin(angle)
        ax.plot([0, x_end], [0, y_end],
                color='#C8C8DC', lw=0.8, alpha=0.55, zorder=2)

    # ── Outer frame (polygon) ─────────────────────────────────────────────
    frame_angles = np.linspace(0, 2 * math.pi, N_RADIALS + 1)
    frame_x = R_MAX * 1.05 * np.cos(frame_angles)
    frame_y = R_MAX * 1.05 * np.sin(frame_angles)
    ax.plot(frame_x, frame_y, color='#A0A0C0', lw=1.2, alpha=0.6, zorder=2)

    # ── Logarithmic spiral (capture spiral) ───────────────────────────────
    theta_spiral = np.linspace(0.3, 3.5 * math.pi, 6000)
    r_spiral = np.exp(A_WEB * theta_spiral)
    x_spiral = r_spiral * np.cos(theta_spiral)
    y_spiral = r_spiral * np.sin(theta_spiral)

    # Gradient: inner = cyan, outer = gold
    points = np.array([x_spiral, y_spiral]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    t_norm = np.linspace(0, 1, len(segments))
    spiral_colors = matplotlib.colormaps['winter'](t_norm)
    lc_spiral = LineCollection(segments, colors=spiral_colors,
                                linewidth=1.6, alpha=0.85, zorder=3)
    ax.add_collection(lc_spiral)

    # ── Inner auxiliary spiral (different growth rate) ────────────────────
    theta_aux = np.linspace(0.1, 2 * math.pi, 3000)
    r_aux = 0.3 * np.exp(0.08 * theta_aux)
    x_aux = r_aux * np.cos(theta_aux)
    y_aux = r_aux * np.sin(theta_aux)
    ax.plot(x_aux, y_aux, color=COLORS['e_cyan'], lw=1.0, alpha=0.5,
            ls='--', zorder=3, label='Auxiliary spiral')

    # ── Dew drops along the spiral ────────────────────────────────────────
    dew_indices = np.arange(0, len(theta_spiral), 80)
    dew_x = x_spiral[dew_indices]
    dew_y = y_spiral[dew_indices]
    dew_r = r_spiral[dew_indices]
    dew_sizes = np.clip(dew_r * 6, 8, 55)
    ax.scatter(dew_x, dew_y, s=dew_sizes, color='#E8F4FD',
               alpha=0.75, zorder=5, edgecolors='#87CEEB', linewidths=0.5)

    # Glint on each dew drop
    ax.scatter(dew_x + dew_r * 0.03, dew_y + dew_r * 0.03,
               s=dew_sizes * 0.12, color='white', alpha=0.9, zorder=6)

    # ── Hub (center) ──────────────────────────────────────────────────────
    hub_theta = np.linspace(0, 2 * math.pi, 200)
    hub_r = 0.12
    ax.fill(hub_r * np.cos(hub_theta), hub_r * np.sin(hub_theta),
            color='#C8C8DC', alpha=0.4, zorder=7)
    ax.plot(hub_r * np.cos(hub_theta), hub_r * np.sin(hub_theta),
            color='#C8C8DC', lw=1.5, alpha=0.7, zorder=7)

    # Hub zone (free zone / sticky spiral start)
    hub_z_r = math.exp(A_WEB * 0.3)
    ax.plot(hub_z_r * np.cos(hub_theta), hub_z_r * np.sin(hub_theta),
            color=COLORS['grid'], lw=0.8, ls=':', alpha=0.4, zorder=4)

    # ── Annotations ───────────────────────────────────────────────────────
    ann_t = 2.2 * math.pi
    ann_r = math.exp(A_WEB * ann_t)
    ax.annotate(
        r'$r = e^{0.12\,\theta}$' + '\nCapture spiral',
        xy=(ann_r * math.cos(ann_t), ann_r * math.sin(ann_t)),
        xytext=(ann_r * 0.4, ann_r * 0.8),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5),
        color=COLORS['e_gold'], fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#050510',
                  edgecolor=COLORS['e_gold'], alpha=0.9),
        zorder=9,
    )

    ax.annotate(
        'Dew drops\n(surface tension)',
        xy=(dew_x[4], dew_y[4]),
        xytext=(-R_MAX * 0.5, -R_MAX * 0.6),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.2),
        color=COLORS['e_cyan'], fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#050510', alpha=0.85),
        zorder=9,
    )

    ax.set_title(
        "Spider Web — Logarithmic Spiral Architecture",
        color=COLORS['e_gold'], fontsize=16, fontweight='bold', pad=14,
    )
    ax.tick_params(colors=COLORS['text'])
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.legend(facecolor='#050510', edgecolor=COLORS['grid'], fontsize=9)
    ax.grid(False)

    lim = R_MAX * 1.15
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'spider_web', out_dir)
    plt.close(fig)
    print("Done: spider_web")


if __name__ == '__main__':
    main()
