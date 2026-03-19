"""
Continuous compounding vs discrete compounding.
$1000 over 10 years at 8% with various compounding frequencies.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

P   = 1000.0
r   = 0.08
T   = 10       # years
t   = np.linspace(0, T, 500)

schedules = [
    (1,       'Annual  (n=1)',    COLORS['e_blue']),
    (4,       'Quarterly (n=4)',  COLORS['e_cyan']),
    (12,      'Monthly (n=12)',   COLORS['e_green']),
    (52,      'Weekly (n=52)',    COLORS['e_orange']),
    (365,     'Daily (n=365)',    COLORS['e_red']),
    (np.inf,  'Continuous eʳᵗ',  COLORS['e_gold']),
]

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Growth curves ─────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

for n, label, color in schedules:
    if np.isinf(n):
        vals = P * np.exp(r * t)
        lw, ls = 3.0, '-'
    else:
        vals = P * (1 + r / n) ** (n * t)
        lw, ls = 1.8, '--'
    ax1.plot(t, vals, color=color, lw=lw, ls=ls, label=label)

ax1.fill_between(t, P * np.exp(r * t), P, alpha=0.08, color=COLORS['e_gold'])
ax1.set_xlabel('Time (years)', fontsize=12)
ax1.set_ylabel('Account Value ($)', fontsize=12)
ax1.set_title('$1,000 at 8% — Growth Over 10 Years\nDiscrete vs Continuous Compounding',
              fontsize=12, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.25)

# ── Panel 2: Final value at t=10 vs compounding frequency ────────────────────
ax2 = fig.add_subplot(gs[1])

n_vals = [1, 2, 4, 12, 52, 365, 8760, 525600, np.inf]
n_labels = ['1\nAnnual', '2\nSemi', '4\nQtly', '12\nMthly', '52\nWkly',
            '365\nDaily', '8760\nHourly', '525k\nMinutely', '∞\nContinuous']
final_vals = []
for n in n_vals:
    if np.isinf(n):
        final_vals.append(P * np.exp(r * T))
    else:
        final_vals.append(P * (1 + r / n) ** (n * T))

continuous_val = P * np.exp(r * T)
bar_colors = [COLORS['e_blue'], COLORS['e_cyan'], COLORS['e_green'],
              COLORS['e_gold'], COLORS['e_orange'], COLORS['e_red'],
              COLORS['e_pink'], COLORS['e_purple'], COLORS['e_gold']]

bars = ax2.bar(range(len(n_vals)), final_vals, color=bar_colors, alpha=0.85,
               edgecolor=COLORS['bg_dark'], linewidth=0.6)
ax2.axhline(continuous_val, color=COLORS['e_gold'], lw=1.8, ls='--',
            label=f'Continuous = ${continuous_val:.2f}')

for bar, val in zip(bars, final_vals):
    diff = val - final_vals[0]  # difference vs annual
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
             f'${val:.0f}', ha='center', va='bottom', fontsize=7, color=COLORS['text'])

ax2.set_xticks(range(len(n_vals)))
ax2.set_xticklabels(n_labels, fontsize=7.5)
ax2.set_ylabel('Final Value ($)', fontsize=12)
ax2.set_title('Final Value at 10 Years\nvs Compounding Frequency',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.set_ylim(final_vals[0] * 0.995, continuous_val * 1.008)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25, axis='y')

# ── Panel 3: Effective annual rate ────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])

n_range = np.logspace(0, 6, 400)
ear_discrete   = (1 + r / n_range) ** n_range - 1
ear_continuous = np.exp(r) - 1

ax3.plot(n_range, ear_discrete * 100, color=COLORS['e_cyan'], lw=2.5,
         label='EAR discrete: (1 + r/n)ⁿ − 1')
ax3.axhline(ear_continuous * 100, color=COLORS['e_gold'], lw=2.0, ls='--',
            label=f'EAR continuous: eʳ−1 = {ear_continuous*100:.4f}%')
ax3.fill_between(n_range, ear_discrete * 100, ear_continuous * 100,
                 alpha=0.12, color=COLORS['e_cyan'])

# Nominal rate annotation
ax3.axhline(r * 100, color=COLORS['e_red'], lw=1.5, ls=':', alpha=0.7,
            label=f'Nominal rate r = {r*100:.0f}%')

ax3.set_xscale('log')
ax3.set_xlabel('Compounding frequency n (log scale)', fontsize=12)
ax3.set_ylabel('Effective Annual Rate (%)', fontsize=12)
ax3.set_title('Effective Annual Rate\nConverges to eʳ − 1',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.25)

fig.suptitle('Continuous Compounding  A = P·eʳᵗ  —  The Limit of Infinite Compounding',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'continuous_compounding', OUTPUT_DIR)
plt.close(fig)
