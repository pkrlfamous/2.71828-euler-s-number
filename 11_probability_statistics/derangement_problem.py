"""
Derangement Problem (Hat-Check Problem)
P(derangement of n items) = D(n)/n! → 1/e as n → ∞

D(n) = n! · Σ_{k=0}^{n} (-1)^k / k!
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

# Compute exact derangement probabilities for n=1..20
def derangement_prob(n):
    """Exact probability that a random permutation is a derangement."""
    total = sum((-1) ** k / math.factorial(k) for k in range(n + 1))
    return total  # = D(n)/n!

ns = list(range(1, 21))
probs = [derangement_prob(n) for n in ns]
exact_inv_e = 1 / math.e

# Partial sums of the series Σ(-1)^k/k!
partial_sums = []
running = 0
for k in range(16):
    running += (-1) ** k / math.factorial(k)
    partial_sums.append(running)

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Derangement Problem — Hat-Check: P(derangement) → 1/e",
             fontsize=19, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: Convergence of P(derangement, n) to 1/e ────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.plot(ns, probs, 'o-', color=COLORS['e_cyan'], lw=2.5, ms=8, label='P(derangement, n)')
ax.axhline(exact_inv_e, color=COLORS['e_gold'], lw=2, linestyle='--',
           label=f'1/e ≈ {exact_inv_e:.6f}')
ax.fill_between(ns, probs, exact_inv_e, alpha=0.12, color=COLORS['e_cyan'])
for i, (n, p) in enumerate(zip(ns, probs)):
    if n <= 6:
        ax.annotate(f'{p:.4f}', (n, p), textcoords='offset points',
                    xytext=(6, 5), fontsize=7.5, color=COLORS['text'])

ax.set_title('Convergence to 1/e', color=COLORS['e_gold'])
ax.set_xlabel('n (number of items)', color=COLORS['text'])
ax.set_ylabel('P(derangement)', color=COLORS['text'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.2)
ax.set_xlim(0.5, 20.5)
ax.text(0.6, 0.15,
        f'1/e = {exact_inv_e:.8f}\n\n'
        'For n≥3 error < 0.01%\nConverges incredibly fast!',
        transform=ax.transAxes, fontsize=9, color=COLORS['e_gold'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Middle: Error from 1/e ────────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
errors = [abs(p - exact_inv_e) for p in probs]
ax.semilogy(ns, errors, 's-', color=COLORS['e_pink'], lw=2.5, ms=7)
ax.set_title('|P(derangement, n) − 1/e|  (log scale)', color=COLORS['e_gold'])
ax.set_xlabel('n', color=COLORS['text'])
ax.set_ylabel('Absolute error', color=COLORS['text'])
ax.grid(True, alpha=0.2, which='both')
ax.text(0.38, 0.85,
        'Error ≈ 1/(n+1)!\n(alternating series)',
        transform=ax.transAxes, fontsize=10, color=COLORS['e_pink'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: Partial sums of alternating series ─────────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])
k_range = list(range(len(partial_sums)))
ax.step(k_range, partial_sums, where='post', color=COLORS['e_green'], lw=2.5,
        label='Σ(-1)^k/k! (partial sums)')
ax.axhline(exact_inv_e, color=COLORS['e_gold'], lw=2, linestyle='--',
           label=f'1/e = {exact_inv_e:.6f}')

# Colour even/odd terms
for k in k_range:
    col = COLORS['e_blue'] if k % 2 == 0 else COLORS['e_red']
    ax.plot(k, partial_sums[k], 'o', color=col, ms=9, zorder=5)
    if k <= 8:
        sign = '+' if k % 2 == 0 else '-'
        ax.annotate(f'{sign}1/{k}!', (k, partial_sums[k]),
                    textcoords='offset points', xytext=(4, 5), fontsize=7, color=COLORS['text'])

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['e_blue'],
           ms=9, label='Positive term (+1/k!)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['e_red'],
           ms=9, label='Negative term (−1/k!)'),
    Line2D([0], [0], color=COLORS['e_green'], lw=2, label='Running sum'),
    Line2D([0], [0], color=COLORS['e_gold'], lw=2, linestyle='--', label='1/e'),
]
ax.legend(handles=legend_elements, fontsize=8)
ax.set_title('Alternating Series  1 − 1 + 1/2! − 1/3! + …', color=COLORS['e_gold'])
ax.set_xlabel('Number of terms k', color=COLORS['text'])
ax.set_ylabel('Partial sum value', color=COLORS['text'])
ax.grid(True, alpha=0.2)

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'derangement_problem', output_dir)
plt.close(fig)
print("derangement_problem.py complete.")
