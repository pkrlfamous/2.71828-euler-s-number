"""
horn_growth.py — Ram horn growth as a thick logarithmic spiral.

Simulates a ram (bighorn sheep) horn cross-section:
  - Thick tube whose centerline follows r = e^(aθ)
  - Tube radius grows with r (thicker at base, tapering at tip)
  - Growth increments annotated at each quarter turn
  - Side panel shows radius vs. angle (exponential growth curve)
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import matplotlib.gridspec as gridspec
from matplotlib.collections import LineCollection
import matplotlib.cm as cm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

A_HORN = 0.22          # growth constant
THETA_MAX = 3.0 * math.pi


def horn_outline(a, theta, tube_fraction=0.18):
    """Compute outer and inner outline of a thick horn spiral."""
    r_center = np.exp(a * theta)
    # Tube radius is a fraction of center radius (horn thins at tip)
    r_tube = r_center * tube_fraction * (0.3 + 0.7 * theta / theta.max())

    # Tangent direction (for perpendicular offset)
    drdtheta = a * r_center
    # Perpendicular direction in Cartesian
    tx = np.cos(theta) - r_center * np.sin(theta)   # ∂x/∂θ (unnormalized)
    ty = np.sin(theta) + r_center * np.cos(theta)   # ∂y/∂θ
    t_len = np.sqrt(tx**2 + ty**2)
    nx = -ty / t_len   # normal (pointing inward)
    ny = tx / t_len

    x_c = r_center * np.cos(theta)
    y_c = r_center * np.sin(theta)

    x_outer = x_c + r_tube * nx
    y_outer = y_c + r_tube * ny
    x_inner = x_c - r_tube * nx
    y_inner = y_c - r_tube * ny

    return x_c, y_c, x_outer, y_outer, x_inner, y_inner, r_center


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(16, 8))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Ram Horn Growth — Logarithmic Spiral  $r = e^{a\theta}$',
        fontsize=18, fontweight='bold', color=COLORS['e_gold'], y=1.01,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.3, width_ratios=[1.4, 1])

    # ── Left: horn cross-section ──────────────────────────────────────────
    ax = fig.add_subplot(gs[0])
    ax.set_facecolor('#0d0d1a')

    theta_horn = np.linspace(0.15, THETA_MAX, 3000)
    x_c, y_c, x_out, y_out, x_in, y_in, r_ctr = horn_outline(A_HORN, theta_horn)

    # Horn body fill (keratin — dark brown with highlights)
    horn_color_map = matplotlib.colormaps['YlOrBr']
    t_norm = np.linspace(0, 1, len(theta_horn))

    # Fill outer shell with gradient (split into small polygons for gradient effect)
    step = 30
    for i in range(0, len(theta_horn) - step, step):
        seg_out_x = x_out[i:i+step+1]
        seg_out_y = y_out[i:i+step+1]
        seg_in_x = x_in[i:i+step+1]
        seg_in_y = y_in[i:i+step+1]
        patch_x = np.concatenate([seg_out_x, seg_in_x[::-1]])
        patch_y = np.concatenate([seg_out_y, seg_in_y[::-1]])
        color_t = (i / len(theta_horn)) * 0.7 + 0.1
        ax.fill(patch_x, patch_y, color=horn_color_map(color_t),
                alpha=0.88, zorder=3)

    # Highlight ridge along outer edge
    points = np.array([x_out, y_out]).T.reshape(-1, 1, 2)
    segs = np.concatenate([points[:-1], points[1:]], axis=1)
    hl_colors = matplotlib.colormaps['Wistia'](0.3 + 0.5 * t_norm[:-1])
    lc_hl = LineCollection(segs, colors=hl_colors, linewidth=2.5, alpha=0.7, zorder=5)
    ax.add_collection(lc_hl)

    # Inner shadow edge
    ax.plot(x_in, y_in, color='#3a1a00', lw=1.5, alpha=0.7, zorder=4)

    # Centerline (spiral)
    ax.plot(x_c, y_c, color=COLORS['e_gold'], lw=1.2, ls='--', alpha=0.5,
            zorder=6, label='Centerline r=e^(aθ)')

    # Quarter-turn growth annotations
    quarter_turns = [math.pi / 2 * k for k in range(1, 7)]
    prev_r = None
    for t_q in quarter_turns:
        if t_q > THETA_MAX:
            break
        r_q = math.exp(A_HORN * t_q)
        xq = r_q * math.cos(t_q)
        yq = r_q * math.sin(t_q)
        ax.plot(xq, yq, 'o', color=COLORS['e_cyan'], markersize=6, zorder=8)
        if prev_r is not None:
            ratio = r_q / prev_r
            ax.annotate(f'×{ratio:.3f}',
                        xy=(xq, yq), xytext=(xq + 0.2, yq + 0.3),
                        color=COLORS['e_cyan'], fontsize=8, zorder=9,
                        bbox=dict(boxstyle='round,pad=0.2',
                                  facecolor=COLORS['bg_dark'], alpha=0.7))
        prev_r = r_q

    # Formula annotation
    r_ann = math.exp(A_HORN * 2.0)
    ax.annotate(
        r'$r = e^{0.22\,\theta}$',
        xy=(r_ann * math.cos(2.0), r_ann * math.sin(2.0)),
        xytext=(-2.0, 2.5),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5),
        color=COLORS['e_gold'], fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                  edgecolor=COLORS['e_gold'], alpha=0.9),
        zorder=10,
    )

    ax.set_aspect('equal')
    ax.set_title('Ram Horn Cross-Section', color=COLORS['text'], fontsize=14)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.tick_params(colors=COLORS['text'])
    ax.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=9)
    ax.grid(True, alpha=0.1, color=COLORS['grid'])

    # ── Right: radius vs theta (exponential growth) ───────────────────────
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    theta_plot = np.linspace(0, THETA_MAX, 500)
    r_plot = np.exp(A_HORN * theta_plot)

    points2 = np.array([theta_plot, r_plot]).T.reshape(-1, 1, 2)
    segs2 = np.concatenate([points2[:-1], points2[1:]], axis=1)
    t_norm2 = np.linspace(0, 1, len(segs2))
    lc2 = LineCollection(segs2, colors=matplotlib.colormaps['YlOrBr'](0.2 + 0.7 * t_norm2),
                          linewidth=3, alpha=0.95, zorder=3)
    ax2.add_collection(lc2)

    # Mark quarter turns
    for t_q in quarter_turns:
        if t_q > THETA_MAX:
            break
        r_q = math.exp(A_HORN * t_q)
        ax2.plot(t_q, r_q, 'o', color=COLORS['e_cyan'], markersize=7, zorder=5)
        ax2.axvline(t_q, color=COLORS['grid'], lw=0.8, ls=':', alpha=0.5)

    # Exponential reference
    ax2.text(0.55, 0.15, r'$r(\theta) = e^{0.22\,\theta}$',
             transform=ax2.transAxes, color=COLORS['e_gold'], fontsize=12,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_gold'], alpha=0.9))

    ax2.autoscale()
    ax2.set_xlabel('θ (radians)', color=COLORS['text'])
    ax2.set_ylabel('r — horn radius', color=COLORS['text'])
    ax2.set_title('Radius vs. Angle\n(Exponential Growth)', color=COLORS['text'], fontsize=13)
    ax2.tick_params(colors=COLORS['text'])
    ax2.grid(True, alpha=0.25, color=COLORS['grid'])

    # Add π labels on x-axis
    pi_ticks = [k * math.pi / 2 for k in range(7) if k * math.pi / 2 <= THETA_MAX + 0.1]
    pi_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$', r'$5\pi/2$', r'$3\pi$']
    ax2.set_xticks(pi_ticks[:len(pi_labels)])
    ax2.set_xticklabels(pi_labels[:len(pi_ticks)], color=COLORS['text'])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'horn_growth', out_dir)
    plt.close(fig)
    print("Done: horn_growth")


if __name__ == '__main__':
    main()
