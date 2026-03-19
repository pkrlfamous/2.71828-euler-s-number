"""
Compound interest: A = P(1 + r/n)^(nt) → Pe^(rt) as n → ∞
Bernoulli's original problem: $1 at 100% interest, value approaches e.
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

# Compounding frequencies (n per year)
freq_labels = ['Annual\n(n=1)', 'Semi-annual\n(n=2)', 'Quarterly\n(n=4)',
               'Monthly\n(n=12)', 'Weekly\n(n=52)', 'Daily\n(n=365)', 'Continuous\n(n→∞)']
freq_n = [1, 2, 4, 12, 52, 365, np.inf]

# Bernoulli: P=1, r=100%, t=1 year
P, r, t = 1.0, 1.0, 1.0
values = []
for n in freq_n:
    if np.isinf(n):
        values.append(P * math.e ** (r * t))
    else:
        values.append(P * (1 + r / n) ** (n * t))

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Value approaches e as n increases ────────────────────────────────
ax1 = fig.add_subplot(gs[0])

bar_colors = [COLORS['e_blue'], COLORS['e_cyan'], COLORS['e_green'],
              COLORS['e_gold'], COLORS['e_orange'], COLORS['e_red'], COLORS['e_pink']]

bars = ax1.bar(range(len(freq_labels)), values, color=bar_colors, alpha=0.85,
               edgecolor=COLORS['bg_dark'], linewidth=0.8)
ax1.axhline(E, color=COLORS['e_gold'], lw=2.0, ls='--', label=f'e = {E:.6f}', zorder=3)

for bar, val in zip(bars, values):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
             f'{val:.5f}', ha='center', va='bottom', fontsize=7.5,
             color=COLORS['text'])

ax1.set_xticks(range(len(freq_labels)))
ax1.set_xticklabels(freq_labels, fontsize=8.5)
ax1.set_ylabel('Final value ($)', fontsize=12)
ax1.set_title("Bernoulli's Problem\n$1 at 100% interest for 1 year",
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.set_ylim(1, E + 0.12)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.25, axis='y')

# ── Panel 2: Convergence to e as n → ∞ ───────────────────────────────────────
ax2 = fig.add_subplot(gs[1])

n_range = np.logspace(0, 6, 500)
converge = (1 + 1 / n_range) ** n_range

ax2.plot(n_range, converge, color=COLORS['e_cyan'], lw=2.5)
ax2.axhline(E, color=COLORS['e_gold'], lw=1.8, ls='--', label=f'e = {E:.8f}')
ax2.fill_between(n_range, converge, E,
                 where=(converge < E), alpha=0.15, color=COLORS['e_cyan'],
                 label='Convergence gap')

# Mark specific n values
mark_n = [1, 2, 12, 365, 1e6]
mark_v = [(1 + 1/n)**n for n in mark_n]
ax2.scatter(mark_n, mark_v, color=COLORS['e_orange'], s=80, zorder=5)
for n, v in zip(mark_n, mark_v):
    ax2.annotate(f'n={int(n) if n < 1e5 else "10⁶"}\n{v:.4f}',
                 xy=(n, v), xytext=(n * 2, v - 0.03),
                 fontsize=7.5, color=COLORS['e_orange'],
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_orange'], lw=0.8))

ax2.set_xscale('log')
ax2.set_xlabel('Compounding frequency n (log scale)', fontsize=12)
ax2.set_ylabel('(1 + 1/n)ⁿ', fontsize=12)
ax2.set_title('Convergence to e\n(1 + 1/n)ⁿ → e as n → ∞',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)

# ── Panel 3: Growth over time with continuous compounding ─────────────────────
ax3 = fig.add_subplot(gs[2])

t_range = np.linspace(0, 5, 300)
r_cont  = 1.0  # 100%

freq_subset = [(1, 'Annual n=1', COLORS['e_blue']),
               (4, 'Quarterly n=4', COLORS['e_cyan']),
               (12, 'Monthly n=12', COLORS['e_green']),
               (365, 'Daily n=365', COLORS['e_orange'])]

for n, label, color in freq_subset:
    vals = (1 + r_cont / n) ** (n * t_range)
    ax3.plot(t_range, vals, color=color, lw=2.0, ls='--', label=label)

# Continuous compounding
ax3.plot(t_range, np.e ** (r_cont * t_range), color=COLORS['e_gold'], lw=2.8,
         label='Continuous eʳᵗ')
ax3.fill_between(t_range, np.e ** (r_cont * t_range), alpha=0.10,
                 color=COLORS['e_gold'])

ax3.set_xlabel('Time (years)', fontsize=12)
ax3.set_ylabel('Value of $1 invested', fontsize=12)
ax3.set_title('Growth at 100% Interest\nDiscrete vs Continuous Compounding',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.25)

fig.suptitle('Compound Interest  A = P(1 + r/n)ⁿᵗ → Peʳᵗ  —  The Birth of e',
             fontsize=15, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'compound_interest', OUTPUT_DIR)
plt.close(fig)
