"""
factorial_series.py — e = Σ_{k=0}^{∞} 1/k!

Left:  bar chart of partial sums approaching e (terms 0 to 15).
Right: semilog error plot showing rapid convergence.
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
MAX_TERM = 15


def partial_sums():
    total = 0.0
    sums = []
    for k in range(MAX_TERM + 1):
        total += 1.0 / math.factorial(k)
        sums.append(total)
    return sums


def main():
    apply_euler_style()

    sums = partial_sums()
    indices = np.arange(len(sums))
    errors = [abs(s - E) for s in sums]

    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # --- Left: bar chart of partial sums ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    # Colour bars by how close they are to e
    cmap_vals = np.linspace(0.3, 1.0, len(sums))
    bar_colors = plt.cm.plasma(cmap_vals)
    bars = ax1.bar(indices, sums, color=bar_colors, edgecolor=COLORS['grid'], linewidth=0.6, zorder=3)
    ax1.axhline(E, color=COLORS['e_red'], lw=2, ls='--', zorder=4,
                label=f'$e = {E:.8f}...$')

    # Annotate final bar
    ax1.annotate(f'Sum({MAX_TERM}) ≈ {sums[-1]:.10f}',
                 xy=(MAX_TERM, sums[-1]),
                 xytext=(MAX_TERM - 6, 2.0),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.2),
                 color=COLORS['e_cyan'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Number of Terms  $n$', color=COLORS['text'])
    ax1.set_ylabel('Partial Sum', color=COLORS['text'])
    ax1.set_title(r'$e = \sum_{k=0}^{n} \frac{1}{k!}$ — Partial Sums', color=COLORS['text'], pad=12)
    ax1.set_xticks(indices)
    ax1.set_ylim(0, 3.1)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax1.grid(True, axis='y', alpha=0.3, color=COLORS['grid'])

    # Term labels on bars
    for i, s in enumerate(sums):
        term_val = 1.0 / math.factorial(i)
        if term_val > 0.02:
            ax1.text(i, s / 2, f'1/{i}!' if i <= 4 else '', ha='center', va='center',
                     fontsize=7, color='white', alpha=0.7)

    # --- Right: semilog error ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    # Filter zeros for log scale
    valid = [(i, e_val) for i, e_val in enumerate(errors) if e_val > 1e-17]
    if valid:
        vi, ve = zip(*valid)
        ax2.semilogy(vi, ve, color=COLORS['e_green'], lw=2, marker='o',
                     markersize=6, markerfacecolor=COLORS['e_gold'],
                     markeredgecolor=COLORS['bg_dark'], label=r'$|S_n - e|$')

    ax2.set_xlabel('Number of Terms  $n$', color=COLORS['text'])
    ax2.set_ylabel('Absolute Error  (log scale)', color=COLORS['text'])
    ax2.set_title(r'Error $|\sum_{k=0}^{n} 1/k! - e|$', color=COLORS['text'], pad=12)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax2.set_xticks(range(0, len(valid) + 1, 2))

    # Annotate rate of convergence
    if len(valid) >= 3:
        ax2.text(0.55, 0.75,
                 'Super-exponential\nconvergence\n(faster than geometric)',
                 transform=ax2.transAxes, color=COLORS['e_orange'], fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    fig.suptitle("Euler's Number via the Factorial Series", fontsize=18,
                 color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'factorial_series', out_dir)
    plt.close(fig)
    print("Done: factorial_series")


if __name__ == '__main__':
    main()
