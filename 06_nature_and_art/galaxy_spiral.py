"""
galaxy_spiral.py — Spiral galaxy simulation using logarithmic arms.

Components:
  - Central bulge: dense cluster of stars drawn from a 2D Gaussian
  - 4 spiral arms: logarithmic spirals with scattered stars + dust
  - Background stars: faint random scatter
  - Color coding: blue for young arm stars, yellow/white for bulge stars
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

RNG = np.random.default_rng(42)
A_GAL = 0.25          # spiral arm growth constant
N_ARM_STARS = 1800    # stars per arm
N_BULGE_STARS = 4000
N_BG_STARS = 800
N_ARMS = 4


def arm_stars(phase_offset, a=A_GAL, n=N_ARM_STARS, spread=0.18):
    """Generate star positions along one logarithmic spiral arm."""
    # Theta distributed along arm; bias toward outer regions
    theta = np.linspace(0.5, 5 * math.pi, n) + RNG.normal(0, spread * 0.3, n)
    r_base = np.exp(a * theta)
    # Add perpendicular scatter (increases with r for flocculent appearance)
    r_scatter = RNG.normal(0, spread, n) * (1 + 0.15 * theta)
    r = r_base + r_scatter
    x = r * np.cos(theta + phase_offset)
    y = r * np.sin(theta + phase_offset)
    # Age proxy: outer = younger (bluer)
    age = 1 - theta / theta.max()
    return x, y, age


def main():
    apply_euler_style()

    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#000005')
    ax.set_facecolor('#000005')
    ax.set_aspect('equal')

    # ── Background stars ─────────────────────────────────────────────────
    bg_r = RNG.exponential(120, N_BG_STARS)
    bg_theta = RNG.uniform(0, 2 * math.pi, N_BG_STARS)
    bg_x = bg_r * np.cos(bg_theta)
    bg_y = bg_r * np.sin(bg_theta)
    bg_brightness = RNG.uniform(0.05, 0.3, N_BG_STARS)
    ax.scatter(bg_x, bg_y, s=RNG.uniform(0.2, 1.5, N_BG_STARS),
               c=[[b, b, b] for b in bg_brightness], alpha=0.5, zorder=1)

    # ── Spiral arms ───────────────────────────────────────────────────────
    # Custom colormap: old (red/orange) → young (blue/white)
    arm_cmap = LinearSegmentedColormap.from_list(
        'arm',
        [(0, '#FF6B35'), (0.3, '#FFD700'), (0.65, '#87CEEB'), (1.0, '#FFFFFF')],
    )

    for k in range(N_ARMS):
        phase = k * math.pi / 2
        x_arm, y_arm, age = arm_stars(phase)

        sizes = RNG.uniform(1, 18, len(x_arm)) * (0.4 + 0.8 * age)
        alphas = np.clip(0.35 + 0.55 * age + RNG.uniform(-0.1, 0.1, len(x_arm)), 0.2, 1.0)

        sc = ax.scatter(x_arm, y_arm, s=sizes, c=age, cmap=arm_cmap,
                        alpha=None, linewidths=0, zorder=3)
        sc.set_alpha(alphas)

        # Arm outline (faint logarithmic spiral)
        theta_line = np.linspace(0.5, 5 * math.pi, 2000)
        r_line = np.exp(A_GAL * theta_line)
        xL = r_line * np.cos(theta_line + phase)
        yL = r_line * np.sin(theta_line + phase)
        t_norm = (theta_line - theta_line.min()) / theta_line.ptp()
        for i in range(len(xL) - 1):
            ax.plot(xL[i:i+2], yL[i:i+2],
                    color=cm.cool(t_norm[i]), lw=0.7, alpha=0.25, zorder=2)

    # ── Central bulge ────────────────────────────────────────────────────
    bulge_r = np.abs(RNG.normal(0, 12, N_BULGE_STARS))
    bulge_theta = RNG.uniform(0, 2 * math.pi, N_BULGE_STARS)
    b_x = bulge_r * np.cos(bulge_theta)
    b_y = bulge_r * np.sin(bulge_theta)
    bulge_temp = RNG.uniform(0.4, 1.0, N_BULGE_STARS)   # 0=reddish, 1=white
    bulge_cmap = LinearSegmentedColormap.from_list(
        'bulge', [(0, '#FF8C00'), (0.5, '#FFD700'), (1, '#FFFAF0')]
    )
    ax.scatter(b_x, b_y, s=RNG.uniform(0.5, 20, N_BULGE_STARS),
               c=bulge_temp, cmap=bulge_cmap,
               alpha=0.7, linewidths=0, zorder=4)

    # Bright galactic core
    core_x = RNG.normal(0, 3, 300)
    core_y = RNG.normal(0, 3, 300)
    ax.scatter(core_x, core_y, s=RNG.uniform(5, 80, 300),
               color='white', alpha=0.9, linewidths=0, zorder=5)

    # Glow effect around core
    for glow_r, alpha in [(8, 0.06), (15, 0.04), (25, 0.025)]:
        circle = plt.Circle((0, 0), glow_r, color='#FFD700', alpha=alpha, zorder=3)
        ax.add_patch(circle)

    # ── Annotations ───────────────────────────────────────────────────────
    r_ann = math.exp(A_GAL * 4)
    ax.annotate(
        r'Arm: $r = e^{0.25\,\theta}$',
        xy=(r_ann * math.cos(4), r_ann * math.sin(4)),
        xytext=(r_ann * 0.5, -r_ann * 0.7),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5),
        color=COLORS['e_gold'], fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#000010',
                  edgecolor=COLORS['e_gold'], alpha=0.9),
        zorder=10,
    )

    ax.set_title(
        'Spiral Galaxy — Logarithmic Arm Structure',
        color=COLORS['e_gold'], fontsize=17, fontweight='bold', pad=14,
    )
    ax.tick_params(colors=COLORS['text'])
    ax.set_xlabel('kpc', color=COLORS['text'])
    ax.set_ylabel('kpc', color=COLORS['text'])

    r_max = math.exp(A_GAL * 5 * math.pi) * 1.3
    ax.set_xlim(-r_max, r_max)
    ax.set_ylim(-r_max, r_max)
    ax.grid(False)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'galaxy_spiral', out_dir)
    plt.close(fig)
    print("Done: galaxy_spiral")


if __name__ == '__main__':
    main()
