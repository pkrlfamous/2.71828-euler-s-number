"""
parametric_curves.py — Parametric curves involving e^t.

Four panels:
  1. Expanding helix: (e^(at)·cos t, e^(at)·sin t)
  2. Unit-circle modulated: (cos(e^t), sin(e^t))
  3. Lissajous-exponential: (e^(-t)·cos(2t), e^(-t)·sin(3t))
  4. Rose-exponential: r = e^(sin t) − 2cos(4t)  (Maclaurin's rose variant)

Color gradients are applied along each curve using t as the parameter.
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


def make_gradient_lc(x, y, cmap_name, lw=2.5, alpha=0.9):
    """Build a LineCollection with a color gradient along the parameter."""
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    n = len(segments)
    colors = matplotlib.colormaps[cmap_name](np.linspace(0, 1, n))
    lc = LineCollection(segments, colors=colors, linewidth=lw, alpha=alpha)
    return lc


def main():
    apply_euler_style()

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        "Parametric Curves Involving  $e^t$",
        fontsize=22, fontweight='bold', color=COLORS['e_gold'], y=0.98,
    )

    # ── Panel 1: Expanding helix (e^(at)·cos t, e^(at)·sin t) ──────────────
    ax = axes[0, 0]
    ax.set_facecolor(COLORS['bg_card'])
    t1 = np.linspace(0, 4 * math.pi, 4000)
    for a, cmap in [(0.05, 'plasma'), (0.1, 'cool'), (0.15, 'spring')]:
        x = np.exp(a * t1) * np.cos(t1)
        y = np.exp(a * t1) * np.sin(t1)
        lc = make_gradient_lc(x, y, cmap, lw=1.8)
        ax.add_collection(lc)
        ax.plot(x[-1], y[-1], 'o', color='white', markersize=4, zorder=5)
    ax.autoscale()
    ax.set_title(r'Expanding Helix: $(e^{at}\cos t,\; e^{at}\sin t)$',
                 color=COLORS['text'], fontsize=13)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.25, color=COLORS['grid'])
    ax.tick_params(colors=COLORS['text'])
    ax.text(0.03, 0.95, 'a = 0.05, 0.10, 0.15', transform=ax.transAxes,
            color=COLORS['e_cyan'], fontsize=9, va='top')

    # ── Panel 2: cos(e^t), sin(e^t) — high-frequency oscillation ───────────
    ax = axes[0, 1]
    ax.set_facecolor(COLORS['bg_card'])
    t2 = np.linspace(0, math.log(20 * math.pi), 6000)
    x2 = np.cos(np.exp(t2))
    y2 = np.sin(np.exp(t2))
    lc2 = make_gradient_lc(x2, y2, 'rainbow', lw=1.5)
    ax.add_collection(lc2)
    ax.autoscale()
    ax.set_title(r'Unit-Circle Modulated: $(\cos(e^t),\; \sin(e^t))$',
                 color=COLORS['text'], fontsize=13)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.25, color=COLORS['grid'])
    ax.tick_params(colors=COLORS['text'])
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')

    # ── Panel 3: Damped Lissajous: (e^(-t)cos 2t, e^(-t)sin 3t) ────────────
    ax = axes[1, 0]
    ax.set_facecolor(COLORS['bg_card'])
    t3 = np.linspace(0, 8 * math.pi, 8000)
    x3 = np.exp(-0.15 * t3) * np.cos(2 * t3)
    y3 = np.exp(-0.15 * t3) * np.sin(3 * t3)
    lc3 = make_gradient_lc(x3, y3, 'viridis', lw=1.8)
    ax.add_collection(lc3)
    ax.plot(x3[0], y3[0], 'o', color=COLORS['e_gold'], markersize=8,
            label='Start', zorder=5)
    ax.plot(0, 0, 'x', color=COLORS['e_red'], markersize=10,
            markeredgewidth=2, label='Attractor (0,0)', zorder=5)
    ax.autoscale()
    ax.set_title(r'Damped Lissajous: $(e^{-0.15t}\cos 2t,\; e^{-0.15t}\sin 3t)$',
                 color=COLORS['text'], fontsize=13)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.25, color=COLORS['grid'])
    ax.tick_params(colors=COLORS['text'])
    ax.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=9)

    # ── Panel 4: Maclaurin-rose variant: r = e^(sin t) − 2cos(4t) ──────────
    ax = axes[1, 1]
    ax.set_facecolor(COLORS['bg_card'])
    t4 = np.linspace(0, 2 * math.pi, 8000)
    r4 = np.exp(np.sin(t4)) - 2 * np.cos(4 * t4)
    x4 = r4 * np.cos(t4)
    y4 = r4 * np.sin(t4)
    lc4 = make_gradient_lc(x4, y4, 'inferno', lw=2.0)
    ax.add_collection(lc4)
    ax.autoscale()
    ax.set_title(r"Butterfly Curve: $r = e^{\sin t} - 2\cos(4t)$",
                 color=COLORS['text'], fontsize=13)
    ax.set_xlabel('x', color=COLORS['text'])
    ax.set_ylabel('y', color=COLORS['text'])
    ax.grid(True, alpha=0.25, color=COLORS['grid'])
    ax.tick_params(colors=COLORS['text'])
    ax.set_aspect('equal')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'parametric_curves', out_dir)
    plt.close(fig)
    print("Done: parametric_curves")


if __name__ == '__main__':
    main()
