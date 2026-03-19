"""
Euler's Formula: e^(iθ) = cos(θ) + i·sin(θ)
Visualized as a 3D helix with projections onto three planes.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def main():
    apply_euler_style()

    theta = np.linspace(0, 4 * np.pi, 1000)
    x = np.cos(theta)   # real part
    y = np.sin(theta)   # imaginary part
    z = theta           # parameter

    fig = plt.figure(figsize=(18, 12))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"Euler's Formula:  $e^{i\theta} = \cos\theta + i\sin\theta$",
        fontsize=22, color=COLORS['e_gold'], fontweight='bold', y=0.98
    )

    # ── 3-D helix ────────────────────────────────────────────────────────────
    ax3d = fig.add_subplot(2, 2, (1, 3), projection='3d')
    ax3d.set_facecolor(COLORS['bg_card'])

    # Main helix
    ax3d.plot(x, y, z, color=COLORS['e_cyan'], lw=2.5, label=r'$e^{i\theta}$ helix', zorder=5)

    # Projection onto XY plane (unit circle) — z = 0
    ax3d.plot(x, y, zs=0, zdir='z', color=COLORS['e_gold'], lw=1.5,
              alpha=0.8, linestyle='--', label='Unit circle projection')

    # Projection onto XZ plane — cos(θ) vs θ
    ax3d.plot(x, z, zs=1, zdir='y', color=COLORS['e_blue'], lw=1.5,
              alpha=0.8, linestyle='--', label=r'$\cos\theta$ projection')

    # Projection onto YZ plane — sin(θ) vs θ
    ax3d.plot(y, z, zs=-1, zdir='x', color=COLORS['e_red'], lw=1.5,
              alpha=0.8, linestyle='--', label=r'$\sin\theta$ projection')

    # Vertical drop lines at key angles
    key_angles = np.linspace(0, 4 * np.pi, 9)[1:]
    for th in key_angles:
        xi, yi, zi = np.cos(th), np.sin(th), th
        ax3d.plot([xi, xi], [yi, yi], [0, zi], color=COLORS['grid'],
                  lw=0.6, alpha=0.5)

    ax3d.set_xlabel('Re (cos θ)', color=COLORS['e_blue'], labelpad=8)
    ax3d.set_ylabel('Im (sin θ)', color=COLORS['e_red'], labelpad=8)
    ax3d.set_zlabel('θ (radians)', color=COLORS['e_green'], labelpad=8)
    ax3d.set_title('3D Helix: e^(iθ)', color=COLORS['text'], pad=10)
    ax3d.tick_params(colors=COLORS['text'])
    ax3d.xaxis.pane.fill = False
    ax3d.yaxis.pane.fill = False
    ax3d.zaxis.pane.fill = False
    ax3d.xaxis.pane.set_edgecolor(COLORS['grid'])
    ax3d.yaxis.pane.set_edgecolor(COLORS['grid'])
    ax3d.zaxis.pane.set_edgecolor(COLORS['grid'])
    ax3d.set_zticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
    ax3d.set_zticklabels(['0', 'π', '2π', '3π', '4π'])
    ax3d.legend(loc='upper left', fontsize=9, facecolor=COLORS['bg_dark'],
                edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax3d.view_init(elev=20, azim=-50)

    # ── Unit circle (XY projection) ───────────────────────────────────────
    ax_xy = fig.add_subplot(2, 2, 2)
    ax_xy.set_facecolor(COLORS['bg_card'])
    circle_th = np.linspace(0, 2 * np.pi, 500)
    ax_xy.plot(np.cos(circle_th), np.sin(circle_th),
               color=COLORS['e_gold'], lw=2, label='Unit circle')

    # Highlight sample points
    sample_angles = np.linspace(0, 2 * np.pi, 9)[:-1]
    for a in sample_angles:
        ax_xy.plot(np.cos(a), np.sin(a), 'o',
                   color=COLORS['e_cyan'], markersize=8, zorder=5)
        ax_xy.plot([0, np.cos(a)], [0, np.sin(a)],
                   color=COLORS['e_cyan'], lw=0.8, alpha=0.5)

    ax_xy.axhline(0, color=COLORS['grid'], lw=0.7)
    ax_xy.axvline(0, color=COLORS['grid'], lw=0.7)
    ax_xy.set_xlim(-1.4, 1.4)
    ax_xy.set_ylim(-1.4, 1.4)
    ax_xy.set_aspect('equal')
    ax_xy.set_title('XY Projection: Unit Circle', color=COLORS['text'])
    ax_xy.set_xlabel('Re (cos θ)', color=COLORS['e_blue'])
    ax_xy.set_ylabel('Im (sin θ)', color=COLORS['e_red'])
    ax_xy.grid(True, alpha=0.25)
    ax_xy.text(0.04, 0.95, r'$|e^{i\theta}| = 1$  always',
               transform=ax_xy.transAxes, color=COLORS['e_gold'], fontsize=11)

    # ── cos and sin vs θ ─────────────────────────────────────────────────
    ax_cs = fig.add_subplot(2, 2, 4)
    ax_cs.set_facecolor(COLORS['bg_card'])
    th_plot = np.linspace(0, 4 * np.pi, 500)
    ax_cs.plot(th_plot, np.cos(th_plot), color=COLORS['e_blue'],
               lw=2.5, label=r'$\cos\theta = \mathrm{Re}(e^{i\theta})$')
    ax_cs.plot(th_plot, np.sin(th_plot), color=COLORS['e_red'],
               lw=2.5, label=r'$\sin\theta = \mathrm{Im}(e^{i\theta})$')
    ax_cs.axhline(0, color=COLORS['grid'], lw=0.7)
    ax_cs.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
    ax_cs.set_xticklabels(['0', 'π', '2π', '3π', '4π'])
    ax_cs.set_title('Real & Imaginary Parts vs θ', color=COLORS['text'])
    ax_cs.set_xlabel('θ', color=COLORS['text'])
    ax_cs.set_ylabel('Amplitude', color=COLORS['text'])
    ax_cs.legend(fontsize=10, facecolor=COLORS['bg_dark'],
                 edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax_cs.grid(True, alpha=0.25)
    ax_cs.set_ylim(-1.4, 1.4)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_plot(fig, 'euler_formula_3d', OUTPUT_DIR)
    plt.close(fig)
    print("euler_formula.py done.")


if __name__ == '__main__':
    main()
