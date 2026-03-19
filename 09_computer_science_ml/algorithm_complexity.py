"""
Algorithm complexity: O(eⁿ) and exponential growth.
Compares O(n), O(n²), O(n!), O(2ⁿ), O(eⁿ).
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

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

E = math.e

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Wide range — exponential explosion ────────────────────────────────
ax1 = fig.add_subplot(gs[0])

n_wide = np.linspace(1, 20, 400)

complexities = {
    'O(n)':    n_wide,
    'O(n²)':   n_wide ** 2,
    'O(2ⁿ)':   2 ** n_wide,
    'O(eⁿ)':   np.e ** n_wide,
}
palette = [COLORS['e_green'], COLORS['e_cyan'], COLORS['e_orange'], COLORS['e_gold']]

for (label, vals), color in zip(complexities.items(), palette):
    ax1.plot(n_wide, vals, color=color, lw=2.3, label=label)

ax1.set_yscale('log')
ax1.set_xlabel('Input size n', fontsize=12)
ax1.set_ylabel('Operations (log scale)', fontsize=12)
ax1.set_title('Algorithm Complexity\nExponential vs Polynomial',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.25)
ax1.set_xlim(1, 20)

# ── Panel 2: Small n — including O(n!) ────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])

n_small = np.arange(1, 16)
ops_n     = n_small.astype(float)
ops_n2    = n_small.astype(float) ** 2
ops_2n    = 2.0 ** n_small
ops_en    = np.e  ** n_small
ops_nfact = np.array([float(math.factorial(int(k))) for k in n_small])

ax2.plot(n_small, ops_n,     color=COLORS['e_green'],  lw=2.2, marker='o', ms=5, label='O(n)')
ax2.plot(n_small, ops_n2,    color=COLORS['e_cyan'],   lw=2.2, marker='s', ms=5, label='O(n²)')
ax2.plot(n_small, ops_2n,    color=COLORS['e_orange'], lw=2.2, marker='^', ms=5, label='O(2ⁿ)')
ax2.plot(n_small, ops_en,    color=COLORS['e_gold'],   lw=2.5, marker='D', ms=5, label='O(eⁿ)')
ax2.plot(n_small, ops_nfact, color=COLORS['e_red'],    lw=2.2, marker='*', ms=7, label='O(n!)')

ax2.set_yscale('log')
ax2.set_xlabel('Input size n', fontsize=12)
ax2.set_ylabel('Operations (log scale)', fontsize=12)
ax2.set_title('All Classes at Small n\n(log scale)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)
ax2.set_xlim(1, 15)

# ── Panel 3: Real-world time estimates ────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])

n_vals = np.array([5, 10, 15, 20, 25, 30])
ops_per_second = 1e9   # 1 GHz computer

time_n    = n_vals / ops_per_second
time_n2   = n_vals**2 / ops_per_second
time_2n   = 2.0**n_vals / ops_per_second
time_en   = np.e**n_vals / ops_per_second
time_nfact= np.array([math.factorial(int(k)) for k in n_vals]) / ops_per_second

bar_width = 0.15
x_pos = np.arange(len(n_vals))

for i, (label, times, color) in enumerate([
    ('O(n)',  time_n,    COLORS['e_green']),
    ('O(n²)', time_n2,   COLORS['e_cyan']),
    ('O(2ⁿ)', time_2n,   COLORS['e_orange']),
    ('O(eⁿ)', time_en,   COLORS['e_gold']),
    ('O(n!)', time_nfact,COLORS['e_red']),
]):
    offset = (i - 2) * bar_width
    valid = times < 1e20
    ax3.bar(x_pos[valid] + offset, times[valid], bar_width, color=color,
            alpha=0.85, label=label, edgecolor=COLORS['bg_dark'], linewidth=0.4)

ax3.set_yscale('log')
ax3.set_xticks(x_pos)
ax3.set_xticklabels([f'n={k}' for k in n_vals])
ax3.set_ylabel('Estimated Time (seconds, log scale)', fontsize=11)
ax3.set_title('Real-World Time @ 1 GHz\n(bars clipped at 10²⁰ s)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.25, axis='y')

# Add age-of-universe reference line (≈ 4.3×10¹⁷ s)
ax3.axhline(4.3e17, color=COLORS['e_pink'], lw=1.5, ls='--', alpha=0.8)
ax3.text(0.01, 4.3e17 * 1.5, 'Age of Universe', transform=ax3.get_yaxis_transform(),
         color=COLORS['e_pink'], fontsize=8, va='bottom')

fig.suptitle('Algorithm Complexity  O(eⁿ)  —  Why Exponential Algorithms Are Intractable',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'algorithm_complexity', OUTPUT_DIR)
plt.close(fig)
