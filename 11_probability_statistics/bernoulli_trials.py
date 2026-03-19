"""
Bernoulli Trials & the Limit (1 - 1/n)^n → 1/e

Slot machine analogy: n symbols, probability 1/n per spin, spin n times.
The probability of NEVER winning converges to 1/e.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

inv_e = 1.0 / math.e

# Compute (1 - 1/n)^n for many n
ns_dense = np.logspace(0, 5, 500)
vals_dense = (1 - 1 / ns_dense) ** ns_dense

ns_int = np.array([1, 2, 3, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 100000])
vals_int = (1 - 1 / ns_int) ** ns_int

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Bernoulli Trials — (1 − 1/n)ⁿ → 1/e as n → ∞",
             fontsize=19, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: Main convergence curve ──────────────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.semilogx(ns_dense, vals_dense, color=COLORS['e_cyan'], lw=2.5,
            label='(1 − 1/n)ⁿ')
ax.axhline(inv_e, color=COLORS['e_gold'], lw=2.5, linestyle='--',
           label=f'1/e = {inv_e:.6f}')
ax.scatter(ns_int, vals_int, color=COLORS['e_orange'], s=60, zorder=5,
           label='Integer n values')

# Annotate a few key points
for n, v in zip([2, 10, 100, 10000], [(1-1/2)**2, (1-1/10)**10,
                                       (1-1/100)**100, (1-1/10000)**10000]):
    ax.annotate(f'n={n}\n{v:.5f}', (n, v), textcoords='offset points',
                xytext=(5, 8), fontsize=7.5, color=COLORS['text'],
                arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=0.8))

ax.set_title('Convergence (log scale)', color=COLORS['e_gold'])
ax.set_xlabel('n  (log scale)', color=COLORS['text'])
ax.set_ylabel('(1 − 1/n)ⁿ', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, which='both')
ax.set_ylim(0.25, 0.75)

# ── Middle: Error from 1/e ─────────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
errors = np.abs(vals_dense - inv_e)
ax.loglog(ns_dense, errors, color=COLORS['e_pink'], lw=2.5, label='|(1−1/n)ⁿ − 1/e|')

# Theoretical error ≈ 1/(2n)
theoretical = 1 / (2 * ns_dense)
ax.loglog(ns_dense, theoretical, color=COLORS['e_green'], lw=1.8, linestyle='--',
          label='1/(2n) [theoretical]', alpha=0.8)

ax.set_title('Error Decay  (log-log scale)', color=COLORS['e_gold'])
ax.set_xlabel('n  (log scale)', color=COLORS['text'])
ax.set_ylabel('|Error|  (log scale)', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, which='both')
ax.text(0.32, 0.22,
        'Error ∝ 1/n\n(slow decay!)',
        transform=ax.transAxes, fontsize=10, color=COLORS['e_pink'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: Slot machine analogy visualization ──────────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])

slot_ns = [5, 10, 20, 50, 100]
slot_probs_no_win = [(1 - 1/n)**n for n in slot_ns]
slot_probs_win = [1 - p for p in slot_probs_no_win]

x_pos = np.arange(len(slot_ns))
width = 0.35
bars1 = ax.bar(x_pos - width/2, slot_probs_no_win, width,
               color=COLORS['e_red'], alpha=0.8, label='P(never win) = (1−1/n)ⁿ',
               edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x_pos + width/2, slot_probs_win, width,
               color=COLORS['e_green'], alpha=0.8, label='P(at least one win)',
               edgecolor='white', linewidth=0.5)
ax.axhline(inv_e, color=COLORS['e_gold'], lw=2, linestyle='--',
           label=f'1/e ≈ {inv_e:.4f}')
ax.axhline(1 - inv_e, color=COLORS['e_cyan'], lw=2, linestyle=':',
           label=f'1−1/e ≈ {1-inv_e:.4f}')

# Annotate bars
for bar, pv in zip(bars1, slot_probs_no_win):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{pv:.4f}', ha='center', va='bottom', fontsize=8, color=COLORS['e_red'])
for bar, pv in zip(bars2, slot_probs_win):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{pv:.4f}', ha='center', va='bottom', fontsize=8, color=COLORS['e_green'])

ax.set_xticks(x_pos)
ax.set_xticklabels([f'n={n}' for n in slot_ns])
ax.set_title('Slot Machine  (n symbols, 1/n chance, n spins)', color=COLORS['e_gold'])
ax.set_xlabel('n  (number of symbols / spins)', color=COLORS['text'])
ax.set_ylabel('Probability', color=COLORS['text'])
ax.legend(fontsize=8.5, loc='center right')
ax.grid(True, alpha=0.2, axis='y')
ax.set_ylim(0, 0.80)
ax.text(0.02, 0.97,
        'As n → ∞:\n• P(never win) → 1/e ≈ 36.8%\n• P(at least one win) → 1−1/e ≈ 63.2%',
        transform=ax.transAxes, fontsize=9, color=COLORS['text'], va='top',
        bbox=dict(boxstyle='round,pad=0.35', facecolor=COLORS['bg_dark'], alpha=0.85))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'bernoulli_trials', output_dir)
plt.close(fig)
print("bernoulli_trials.py complete.")
