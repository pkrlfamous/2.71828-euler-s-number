"""
hyperbolic_functions.py — sinh, cosh, tanh and their relationship to e.

Four panels:
  1. All three functions plotted with e-based definitions annotated
  2. Identity verification: cosh²(x) − sinh²(x) = 1
  3. Unit hyperbola x² − y² = 1 with parametric tracing (cosh t, sinh t)
  4. Comparison: sinh vs sin, cosh vs cos
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"Hyperbolic Functions via $e$:  "
        r"$\sinh x = \frac{e^x-e^{-x}}{2}$,  "
        r"$\cosh x = \frac{e^x+e^{-x}}{2}$,  "
        r"$\tanh x = \frac{e^x-e^{-x}}{e^x+e^{-x}}$",
        fontsize=14, fontweight='bold', color=COLORS['e_gold'], y=0.99,
    )

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32)
    x = np.linspace(-4, 4, 800)

    sinh_x = np.sinh(x)
    cosh_x = np.cosh(x)
    tanh_x = np.tanh(x)

    # ── Panel 1: sinh, cosh, tanh ─────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['bg_card'])

    ax1.plot(x, sinh_x, color=COLORS['e_gold'], lw=2.5, label=r'$\sinh x$')
    ax1.plot(x, cosh_x, color=COLORS['e_cyan'], lw=2.5, label=r'$\cosh x$')
    ax1.plot(x, tanh_x, color=COLORS['e_green'], lw=2.5, label=r'$\tanh x$')
    ax1.axhline(0, color=COLORS['text'], lw=0.5, alpha=0.5)
    ax1.axvline(0, color=COLORS['text'], lw=0.5, alpha=0.5)
    ax1.axhline(1, color=COLORS['e_green'], lw=1, ls=':', alpha=0.6, label=r'Asymptote $\tanh→±1$')
    ax1.axhline(-1, color=COLORS['e_green'], lw=1, ls=':', alpha=0.6)

    # Annotate minimum of cosh
    ax1.annotate(r'$\cosh(0)=1$', xy=(0, 1), xytext=(1.2, 0.5),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.5),
                 color=COLORS['e_cyan'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_ylim(-6, 6)
    ax1.set_xlabel('x', color=COLORS['text'])
    ax1.set_ylabel('f(x)', color=COLORS['text'])
    ax1.set_title('Hyperbolic Functions', color=COLORS['text'], fontsize=14)
    ax1.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.25, color=COLORS['grid'])
    ax1.tick_params(colors=COLORS['text'])

    # ── Panel 2: Identity verification ───────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['bg_card'])

    identity = cosh_x**2 - sinh_x**2
    residual = identity - 1.0

    ax2.plot(x, cosh_x**2, color=COLORS['e_cyan'], lw=2, label=r'$\cosh^2 x$')
    ax2.plot(x, sinh_x**2, color=COLORS['e_gold'], lw=2, label=r'$\sinh^2 x$')
    ax2.plot(x, identity, color=COLORS['e_green'], lw=3, ls='-',
             label=r'$\cosh^2 x - \sinh^2 x = 1$')

    ax2_r = ax2.twinx()
    ax2_r.plot(x, residual, color=COLORS['e_pink'], lw=1.5, ls='--', alpha=0.7,
               label='Residual (numerical)')
    ax2_r.set_ylabel('Residual (should be 0)', color=COLORS['e_pink'], fontsize=9)
    ax2_r.tick_params(colors=COLORS['e_pink'])
    ax2_r.set_ylim(-1e-14, 1e-14)

    ax2.text(0.5, 0.12, r'$\cosh^2 x - \sinh^2 x \equiv 1$',
             transform=ax2.transAxes, ha='center',
             fontsize=13, color=COLORS['e_green'],
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_green'], alpha=0.9))

    ax2.set_xlabel('x', color=COLORS['text'])
    ax2.set_ylabel('Value', color=COLORS['text'])
    ax2.set_title(r'Identity: $\cosh^2 x - \sinh^2 x = 1$', color=COLORS['text'], fontsize=13)
    ax2.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=9, loc='upper center')
    ax2.grid(True, alpha=0.25, color=COLORS['grid'])
    ax2.tick_params(colors=COLORS['text'])

    # ── Panel 3: Unit hyperbola ───────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])

    # Hyperbola branches x² - y² = 1
    y_hyp = np.linspace(-4, 4, 800)
    x_hyp_pos = np.sqrt(1 + y_hyp**2)
    x_hyp_neg = -np.sqrt(1 + y_hyp**2)
    ax3.plot(x_hyp_pos, y_hyp, color=COLORS['e_purple'], lw=2, label=r'$x^2 - y^2 = 1$')
    ax3.plot(x_hyp_neg, y_hyp, color=COLORS['e_purple'], lw=2)

    # Asymptotes y = ±x
    x_asym = np.linspace(-4, 4, 100)
    ax3.plot(x_asym, x_asym, color=COLORS['grid'], lw=1, ls='--', label='Asymptotes y=±x')
    ax3.plot(x_asym, -x_asym, color=COLORS['grid'], lw=1, ls='--')

    # Parametric tracing
    t_trace = np.linspace(-2, 2, 200)
    xp = np.cosh(t_trace)
    yp = np.sinh(t_trace)
    ax3.plot(xp, yp, color=COLORS['e_gold'], lw=3, label=r'$(\cosh t, \sinh t)$')

    # Highlight specific points
    for t_val, label in [(-1.5, 't=−1.5'), (0, 't=0'), (1.5, 't=1.5')]:
        xv, yv = math.cosh(t_val), math.sinh(t_val)
        ax3.plot(xv, yv, 'o', color=COLORS['e_cyan'], markersize=8, zorder=5)
        ax3.annotate(f'{label}\n({xv:.2f}, {yv:.2f})',
                     xy=(xv, yv), xytext=(xv + 0.4, yv + 0.3),
                     color=COLORS['e_cyan'], fontsize=8,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7))

    # Shaded area (area property)
    t_shade = np.linspace(0, 1.0, 100)
    xs = np.cosh(t_shade)
    ys = np.sinh(t_shade)
    ax3.fill_between([1] + list(xs) + [xs[-1]],
                     [0] + list(ys) + [0],
                     color=COLORS['e_gold'], alpha=0.2, label='Area = t/2')

    ax3.set_xlim(-4.5, 4.5)
    ax3.set_ylim(-4, 4)
    ax3.set_aspect('equal')
    ax3.set_xlabel('x', color=COLORS['text'])
    ax3.set_ylabel('y', color=COLORS['text'])
    ax3.set_title(r'Unit Hyperbola: $x^2 - y^2 = 1$', color=COLORS['text'], fontsize=13)
    ax3.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=9, loc='lower right')
    ax3.grid(True, alpha=0.25, color=COLORS['grid'])
    ax3.tick_params(colors=COLORS['text'])

    # ── Panel 4: Circular vs hyperbolic comparison ─────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])

    ax4.plot(x, np.sinh(x), color=COLORS['e_gold'], lw=2.5, label=r'$\sinh x$ (hyperbolic)')
    ax4.plot(x, np.sin(x), color=COLORS['e_gold'], lw=2, ls='--', alpha=0.6, label=r'$\sin x$ (circular)')
    ax4.plot(x, np.cosh(x), color=COLORS['e_cyan'], lw=2.5, label=r'$\cosh x$ (hyperbolic)')
    ax4.plot(x, np.cos(x), color=COLORS['e_cyan'], lw=2, ls='--', alpha=0.6, label=r'$\cos x$ (circular)')
    ax4.plot(x, np.tanh(x), color=COLORS['e_green'], lw=2.5, label=r'$\tanh x$ (hyperbolic)')
    ax4.plot(x, np.tan(x), color=COLORS['e_green'], lw=1.5, ls='--', alpha=0.6, label=r'$\tan x$ (circular)')

    ax4.set_ylim(-5, 5)
    ax4.axhline(0, color=COLORS['text'], lw=0.5, alpha=0.4)
    ax4.axvline(0, color=COLORS['text'], lw=0.5, alpha=0.4)
    ax4.set_xlabel('x', color=COLORS['text'])
    ax4.set_ylabel('f(x)', color=COLORS['text'])
    ax4.set_title('Hyperbolic vs Circular Functions', color=COLORS['text'], fontsize=13)
    ax4.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=8,
               ncol=2, loc='upper left')
    ax4.grid(True, alpha=0.25, color=COLORS['grid'])
    ax4.tick_params(colors=COLORS['text'])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'hyperbolic_functions', out_dir)
    plt.close(fig)
    print("Done: hyperbolic_functions")


if __name__ == '__main__':
    main()
