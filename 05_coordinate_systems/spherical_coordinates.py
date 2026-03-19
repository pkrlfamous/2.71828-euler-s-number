"""
spherical_coordinates.py — e in 3D spherical / radial coordinates.

Three panels:
  1. 3D surface: z = e^(-r) where r = sqrt(x²+y²)  — radial decay bell
  2. Spherical shell coloring: intensity ∝ e^(-ρ/2) on a unit sphere
  3. Contour map of the radial decay e^(-r)
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib import cm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(18, 6))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"$e$ in 3D: Radial Decay  $f(\rho) = e^{-\rho/2}$",
        fontsize=20, fontweight='bold', color=COLORS['e_gold'], y=1.01,
    )

    # ── Panel 1: 3D surface z = e^(-r) ──────────────────────────────────────
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.set_facecolor(COLORS['bg_card'])

    lim = 4.0
    x_g = np.linspace(-lim, lim, 200)
    y_g = np.linspace(-lim, lim, 200)
    X, Y = np.meshgrid(x_g, y_g)
    R = np.sqrt(X**2 + Y**2)
    Z = np.exp(-R)

    surf = ax1.plot_surface(X, Y, Z, cmap='plasma', alpha=0.92,
                            linewidth=0, antialiased=True)
    ax1.set_xlabel('x', color=COLORS['text'], labelpad=6)
    ax1.set_ylabel('y', color=COLORS['text'], labelpad=6)
    ax1.set_zlabel(r'$e^{-r}$', color=COLORS['text'], labelpad=6)
    ax1.set_title(r'$z = e^{-\sqrt{x^2+y^2}}$', color=COLORS['text'], fontsize=13, pad=10)
    ax1.tick_params(colors=COLORS['text'], labelsize=7)
    ax1.xaxis.pane.fill = False
    ax1.yaxis.pane.fill = False
    ax1.zaxis.pane.fill = False
    ax1.xaxis.pane.set_edgecolor(COLORS['grid'])
    ax1.yaxis.pane.set_edgecolor(COLORS['grid'])
    ax1.zaxis.pane.set_edgecolor(COLORS['grid'])
    fig.colorbar(surf, ax=ax1, shrink=0.5, pad=0.1,
                 label=r'$e^{-r}$').ax.yaxis.label.set_color(COLORS['text'])

    # ── Panel 2: Unit sphere colored by e^(-ρ/2) ───────────────────────────
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.set_facecolor(COLORS['bg_card'])

    phi = np.linspace(0, math.pi, 120)
    theta_s = np.linspace(0, 2 * math.pi, 240)
    Phi, Theta = np.meshgrid(phi, theta_s)
    rho = 1.0
    Xs = rho * np.sin(Phi) * np.cos(Theta)
    Ys = rho * np.sin(Phi) * np.sin(Theta)
    Zs = rho * np.cos(Phi)

    # Color intensity: e^(-|z|/2) — poles are brightest
    intensity = np.exp(-np.abs(Zs) / 2.0)
    surf2 = ax2.plot_surface(Xs, Ys, Zs, facecolors=cm.cool(intensity),
                              alpha=0.9, linewidth=0, antialiased=True)
    ax2.set_xlabel('x', color=COLORS['text'], labelpad=6)
    ax2.set_ylabel('y', color=COLORS['text'], labelpad=6)
    ax2.set_zlabel('z', color=COLORS['text'], labelpad=6)
    ax2.set_title(r'Unit sphere: intensity $\propto e^{-|z|/2}$',
                  color=COLORS['text'], fontsize=12, pad=10)
    ax2.tick_params(colors=COLORS['text'], labelsize=7)
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False
    ax2.xaxis.pane.set_edgecolor(COLORS['grid'])
    ax2.yaxis.pane.set_edgecolor(COLORS['grid'])
    ax2.zaxis.pane.set_edgecolor(COLORS['grid'])

    # ── Panel 3: 2D contour of e^(-r) ───────────────────────────────────────
    ax3 = fig.add_subplot(133)
    ax3.set_facecolor(COLORS['bg_card'])

    lim3 = 5.0
    x3 = np.linspace(-lim3, lim3, 400)
    y3 = np.linspace(-lim3, lim3, 400)
    X3, Y3 = np.meshgrid(x3, y3)
    R3 = np.sqrt(X3**2 + Y3**2)
    Z3 = np.exp(-R3 / 2.0)

    levels = np.linspace(0, 1, 30)
    cf = ax3.contourf(X3, Y3, Z3, levels=levels, cmap='inferno')
    cs = ax3.contour(X3, Y3, Z3,
                     levels=[0.1, 0.2, 0.4, 0.6, 0.8],
                     colors='white', linewidths=0.8, alpha=0.6)
    ax3.clabel(cs, fmt=r'$%.1f$', colors='white', fontsize=8)
    fig.colorbar(cf, ax=ax3, label=r'$e^{-\rho/2}$').ax.yaxis.label.set_color(COLORS['text'])

    # Radial annotation
    for r_ann in [1, 2, 3]:
        val = math.exp(-r_ann / 2.0)
        ax3.annotate(
            f'r={r_ann}\n{val:.3f}',
            xy=(r_ann / math.sqrt(2), r_ann / math.sqrt(2)),
            color=COLORS['e_cyan'], fontsize=8,
            bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7),
        )

    ax3.set_title(r'Contour: $e^{-\rho/2}$ in 2D cross-section',
                  color=COLORS['text'], fontsize=13)
    ax3.set_xlabel('x', color=COLORS['text'])
    ax3.set_ylabel('y', color=COLORS['text'])
    ax3.tick_params(colors=COLORS['text'])
    ax3.set_aspect('equal')

    plt.tight_layout()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'spherical_coordinates', out_dir)
    plt.close(fig)
    print("Done: spherical_coordinates")


if __name__ == '__main__':
    main()
