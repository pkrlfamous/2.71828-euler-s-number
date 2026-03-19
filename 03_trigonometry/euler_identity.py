"""
Euler's Identity: e^(iπ) + 1 = 0
Often called "the most beautiful equation in mathematics."
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def main():
    apply_euler_style()

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(18, 9))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"Euler's Identity:  $e^{i\pi} + 1 = 0$",
        fontsize=26, color=COLORS['e_gold'], fontweight='bold', y=0.98
    )

    # ── Left panel: Complex plane with unit circle ────────────────────────
    ax = ax_left
    ax.set_facecolor(COLORS['bg_card'])

    # Unit circle
    th = np.linspace(0, 2 * np.pi, 600)
    ax.plot(np.cos(th), np.sin(th), color=COLORS['e_cyan'], lw=2, alpha=0.8,
            label='Unit circle $|e^{i\\theta}|=1$')

    # Arc from 0 to π with arrow
    arc_th = np.linspace(0, np.pi, 300)
    ax.plot(np.cos(arc_th), np.sin(arc_th), color=COLORS['e_gold'], lw=3.5,
            label=r'$e^{i\theta}$, $\theta: 0 \to \pi$', zorder=5)

    # Starting point e^(i·0) = 1
    ax.plot(1, 0, 'o', color=COLORS['e_green'], markersize=14, zorder=10,
            label=r'$e^{i \cdot 0} = 1$')
    ax.annotate(r'$e^{i\cdot 0} = 1$', xy=(1, 0),
                xytext=(1.05, 0.18), color=COLORS['e_green'], fontsize=12,
                arrowprops=dict(arrowstyle='->', color=COLORS['e_green'], lw=1.5))

    # Endpoint e^(iπ) = -1
    ax.plot(-1, 0, '*', color=COLORS['e_red'], markersize=22, zorder=10,
            label=r'$e^{i\pi} = -1$')
    ax.annotate(r'$e^{i\pi} = -1$', xy=(-1, 0),
                xytext=(-1.35, 0.22), color=COLORS['e_red'], fontsize=13,
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['e_red'], lw=2))

    # Midpoint at θ = π/2
    ax.plot(0, 1, 'D', color=COLORS['e_purple'], markersize=10, zorder=8,
            label=r'$e^{i\pi/2} = i$')
    ax.annotate(r'$e^{i\pi/2} = i$', xy=(0, 1),
                xytext=(0.15, 1.1), color=COLORS['e_purple'], fontsize=11,
                arrowprops=dict(arrowstyle='->', color=COLORS['e_purple'], lw=1.5))

    # Radius lines
    for angle, col in [(0, COLORS['e_green']), (np.pi / 2, COLORS['e_purple']),
                       (np.pi, COLORS['e_red'])]:
        ax.plot([0, np.cos(angle)], [0, np.sin(angle)],
                color=col, lw=1.5, alpha=0.6, linestyle=':')

    # Origin
    ax.plot(0, 0, '+', color=COLORS['text'], markersize=12, lw=2)

    # Axes
    ax.axhline(0, color=COLORS['grid'], lw=0.8)
    ax.axvline(0, color=COLORS['grid'], lw=0.8)

    # Identity box
    identity_text = (
        r"$e^{i\pi} + 1 = 0$" + "\n\n"
        r"$\mathbf{e}$  =  2.71828…" + "\n"
        r"$\mathbf{i}$   =  $\sqrt{-1}$" + "\n"
        r"$\mathbf{\pi}$  =  3.14159…" + "\n"
        r"$\mathbf{1}$  =  unity" + "\n"
        r"$\mathbf{0}$  =  zero"
    )
    bbox_props = dict(boxstyle='round,pad=0.6', facecolor=COLORS['bg_dark'],
                      edgecolor=COLORS['e_gold'], lw=2, alpha=0.92)
    ax.text(0.02, 0.02, identity_text, transform=ax.transAxes,
            fontsize=11, color=COLORS['e_gold'], verticalalignment='bottom',
            bbox=bbox_props)

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect('equal')
    ax.set_xlabel('Real axis', color=COLORS['text'])
    ax.set_ylabel('Imaginary axis', color=COLORS['text'])
    ax.set_title('The Complex Plane', color=COLORS['text'], fontsize=14)
    ax.legend(loc='upper right', fontsize=9.5, facecolor=COLORS['bg_dark'],
              edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax.grid(True, alpha=0.2)

    # ── Right panel: e^(iθ) rotation from 0 to π ─────────────────────────
    ax2 = ax_right
    ax2.set_facecolor(COLORS['bg_card'])

    n_frames = 8
    angles = np.linspace(0, np.pi, n_frames)
    cmap_vals = np.linspace(0, 1, n_frames)

    th2 = np.linspace(0, 2 * np.pi, 400)
    ax2.plot(np.cos(th2), np.sin(th2), color=COLORS['e_cyan'], lw=1.5, alpha=0.5)

    for i, (angle, cv) in enumerate(zip(angles, cmap_vals)):
        r = np.cos(angle)
        im = np.sin(angle)
        color = plt.cm.plasma(cv)  # type: ignore[attr-defined]

        ax2.plot([0, r], [0, im], color=color, lw=2.5, alpha=0.85, zorder=4)
        ax2.plot(r, im, 'o', color=color, markersize=10, zorder=5)

        label_r = r + 0.07 * np.cos(angle + 0.15)
        label_i = im + 0.07 * np.sin(angle + 0.15)
        frac = '' if i == 0 else (r'$\pi$' if i == n_frames - 1
                                  else rf'$\frac{{{i}}}{{{n_frames-1}}}\pi$')
        ax2.text(label_r, label_i, frac, color=color, fontsize=9,
                 ha='center', va='center')

    # Mark final point
    ax2.plot(-1, 0, '*', color=COLORS['e_red'], markersize=24, zorder=10)
    ax2.text(-1.4, -0.12, r'$e^{i\pi}=-1$', color=COLORS['e_red'],
             fontsize=13, fontweight='bold')

    ax2.axhline(0, color=COLORS['grid'], lw=0.8)
    ax2.axvline(0, color=COLORS['grid'], lw=0.8)
    ax2.set_xlim(-1.6, 1.6)
    ax2.set_ylim(-0.5, 1.5)
    ax2.set_aspect('equal')
    ax2.set_xlabel('Real axis', color=COLORS['text'])
    ax2.set_ylabel('Imaginary axis', color=COLORS['text'])
    ax2.set_title(r'$e^{i\theta}$ sweeping from $\theta=0$ to $\theta=\pi$',
                  color=COLORS['text'], fontsize=14)
    ax2.grid(True, alpha=0.2)

    # Add colorbar indication
    sm = plt.cm.ScalarMappable(cmap='plasma',  # type: ignore[attr-defined]
                               norm=plt.Normalize(0, np.pi))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax2, fraction=0.04, pad=0.02)
    cbar.set_label('θ (radians)', color=COLORS['text'])
    cbar.ax.yaxis.set_tick_params(color=COLORS['text'])
    cbar.set_ticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
    cbar.set_ticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=COLORS['text'])

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_plot(fig, 'euler_identity', OUTPUT_DIR)
    plt.close(fig)
    print("euler_identity.py done.")


if __name__ == '__main__':
    main()
