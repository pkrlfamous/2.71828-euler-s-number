"""
Euler / Cornu Spiral (Clothoid): Fresnel Integrals
C(t) = ∫₀ᵗ cos(πs²/2) ds
S(t) = ∫₀ᵗ sin(πs²/2) ds
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.special import fresnel

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def main():
    apply_euler_style()

    # Fresnel integrals: scipy returns (S, C) — note the order!
    t = np.linspace(-10, 10, 8000)
    S_pos, C_pos = fresnel(t)   # scipy convention: S(t), C(t)

    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        'Euler / Cornu Spiral (Clothoid) — Fresnel Integrals',
        fontsize=22, color=COLORS['e_gold'], fontweight='bold'
    )

    # ── Main spiral plot ──────────────────────────────────────────────────
    ax_main = fig.add_subplot(1, 2, 1)
    ax_main.set_facecolor(COLORS['bg_card'])

    # Color by parameter t for a rainbow effect
    norm = mcolors.Normalize(vmin=t.min(), vmax=t.max())
    cmap = plt.cm.plasma  # type: ignore[attr-defined]

    # Draw colored segments
    n_seg = len(t) - 1
    for i in range(0, n_seg, 4):
        color = cmap(norm(t[i]))
        ax_main.plot(C_pos[i:i + 5], S_pos[i:i + 5], color=color, lw=1.8)

    # Mark the limit points (Cornu targets)
    ax_main.plot(0.5, 0.5, '*', color=COLORS['e_gold'], markersize=18, zorder=10,
                 label=r'Limit: $(C(\infty), S(\infty)) = (0.5, 0.5)$')
    ax_main.plot(-0.5, -0.5, '*', color=COLORS['e_red'], markersize=18, zorder=10,
                 label=r'Limit: $(C(-\infty), S(-\infty)) = (-0.5, -0.5)$')
    ax_main.plot(0, 0, 'o', color=COLORS['e_cyan'], markersize=10, zorder=9,
                 label='Origin: t=0')

    ax_main.axhline(0, color=COLORS['grid'], lw=0.6, alpha=0.5)
    ax_main.axvline(0, color=COLORS['grid'], lw=0.6, alpha=0.5)
    ax_main.axhline(0.5, color=COLORS['e_gold'], lw=0.7, alpha=0.3, linestyle=':')
    ax_main.axvline(0.5, color=COLORS['e_gold'], lw=0.7, alpha=0.3, linestyle=':')
    ax_main.axhline(-0.5, color=COLORS['e_red'], lw=0.7, alpha=0.3, linestyle=':')
    ax_main.axvline(-0.5, color=COLORS['e_red'], lw=0.7, alpha=0.3, linestyle=':')

    ax_main.set_aspect('equal')
    ax_main.set_xlabel(r'$C(t) = \int_0^t \cos\!\left(\frac{\pi s^2}{2}\right)ds$',
                       color=COLORS['text'], fontsize=11)
    ax_main.set_ylabel(r'$S(t) = \int_0^t \sin\!\left(\frac{\pi s^2}{2}\right)ds$',
                       color=COLORS['text'], fontsize=11)
    ax_main.set_title('Cornu Spiral in the CS-plane', color=COLORS['text'])
    ax_main.legend(fontsize=9, facecolor=COLORS['bg_dark'],
                   edgecolor=COLORS['grid'], labelcolor=COLORS['text'],
                   loc='lower right')
    ax_main.grid(True, alpha=0.2)

    # Colorbar for t
    sm = plt.cm.ScalarMappable(cmap='plasma', norm=norm)  # type: ignore[attr-defined]
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_main, fraction=0.04, pad=0.02)
    cbar.set_label('Parameter t', color=COLORS['text'])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=COLORS['text'])

    # ── Right panel: C(t) and S(t) vs t ──────────────────────────────────
    ax_cs = fig.add_subplot(2, 2, 2)
    ax_cs.set_facecolor(COLORS['bg_card'])
    t_pos = np.linspace(0, 10, 2000)
    S_r, C_r = fresnel(t_pos)

    ax_cs.plot(t_pos, C_r, color=COLORS['e_blue'], lw=2.5,
               label=r'$C(t)$')
    ax_cs.plot(t_pos, S_r, color=COLORS['e_red'], lw=2.5,
               label=r'$S(t)$')
    ax_cs.axhline(0.5, color=COLORS['e_gold'], lw=1, linestyle='--', alpha=0.6,
                  label='Limit = 0.5')

    ax_cs.set_xlabel('t', color=COLORS['text'])
    ax_cs.set_ylabel('Value', color=COLORS['text'])
    ax_cs.set_title(r'Fresnel Integrals vs $t$', color=COLORS['text'])
    ax_cs.legend(fontsize=9, facecolor=COLORS['bg_dark'],
                 edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax_cs.grid(True, alpha=0.2)

    # ── Bottom-right: curvature κ = πt ───────────────────────────────────
    ax_curv = fig.add_subplot(2, 2, 4)
    ax_curv.set_facecolor(COLORS['bg_card'])
    ax_curv.plot(t_pos, np.pi * t_pos, color=COLORS['e_green'], lw=2.5,
                 label=r'Curvature $\kappa = \pi t$')
    ax_curv.fill_between(t_pos, np.pi * t_pos, alpha=0.15, color=COLORS['e_green'])

    ax_curv.set_xlabel('Arc length t', color=COLORS['text'])
    ax_curv.set_ylabel(r'Curvature $\kappa$', color=COLORS['text'])
    ax_curv.set_title('Linear Curvature — Clothoid Property', color=COLORS['text'])
    ax_curv.legend(fontsize=10, facecolor=COLORS['bg_dark'],
                   edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax_curv.grid(True, alpha=0.2)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_plot(fig, 'euler_spiral', OUTPUT_DIR)
    plt.close(fig)
    print("euler_spiral.py done.")


if __name__ == '__main__':
    main()
