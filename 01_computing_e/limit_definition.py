"""
limit_definition.py — Visualize lim(1 + 1/n)^n as n → ∞

Shows convergence to e on a semilog x-axis and the log-log error decay.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

E = math.e

def main():
    apply_euler_style()

    # Generate n values on a log scale
    n_values = np.logspace(0, 8, 500)
    approx = (1 + 1 / n_values) ** n_values
    error = np.abs(approx - E)

    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # --- Left: convergence curve (semilog x) ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])
    ax1.semilogx(n_values, approx, color=COLORS['e_gold'], lw=2, label=r'$(1 + 1/n)^n$')
    ax1.axhline(E, color=COLORS['e_red'], lw=1.5, ls='--', label=f'$e = {E:.6f}...$')
    ax1.set_xlabel('$n$  (log scale)', color=COLORS['text'])
    ax1.set_ylabel('Approximation', color=COLORS['text'])
    ax1.set_title(r'Convergence of $(1+1/n)^n \to e$', color=COLORS['text'], pad=12)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_ylim(2.0, 2.82)

    # Annotate a few milestones
    for n_mark, label in [(1, 'n=1'), (10, 'n=10'), (1000, 'n=1000'), (1e7, 'n=10⁷')]:
        y_mark = (1 + 1 / n_mark) ** n_mark
        ax1.annotate(f'{label}\n≈{y_mark:.4f}',
                     xy=(n_mark, y_mark),
                     xytext=(n_mark * 3, y_mark - 0.05),
                     arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1),
                     color=COLORS['e_cyan'], fontsize=8,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7))

    # --- Right: log-log error ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])
    # Avoid log(0) — filter valid errors
    mask = error > 0
    ax2.loglog(n_values[mask], error[mask], color=COLORS['e_purple'], lw=2,
               label=r'$|(1+1/n)^n - e|$')
    # Reference slope ~ 1/n
    ref_n = n_values[mask]
    ax2.loglog(ref_n, E / (2 * ref_n), color=COLORS['e_orange'], lw=1.5, ls=':',
               label=r'$\sim e/(2n)$ (slope $-1$)')
    ax2.set_xlabel('$n$  (log scale)', color=COLORS['text'])
    ax2.set_ylabel('Absolute Error  (log scale)', color=COLORS['text'])
    ax2.set_title(r'Error $|(1+1/n)^n - e|$', color=COLORS['text'], pad=12)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])

    fig.suptitle("Euler's Number via the Limit Definition", fontsize=18,
                 color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'limit_definition', out_dir)
    plt.close(fig)
    print("Done: limit_definition")

if __name__ == '__main__':
    main()
