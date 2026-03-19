"""
Birthday Problem — exact probability vs e-based approximation.
Exact:   P(no match) = 365!/((365-n)! · 365^n)
Approx:  P(no match) ≈ e^(-n(n-1)/(2·365))
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

days = 365
ns = np.arange(1, 80)

def p_no_match_exact(n, d=365):
    """P(all n people have different birthdays) — exact."""
    if n > d:
        return 0.0
    log_p = sum(math.log((d - k) / d) for k in range(n))
    return math.exp(log_p)

def p_no_match_approx(n, d=365):
    """e-approximation: e^(-n(n-1)/(2d))."""
    return math.exp(-n * (n - 1) / (2 * d))

exact = np.array([1 - p_no_match_exact(n) for n in ns])
approx = np.array([1 - p_no_match_approx(n) for n in ns])
error = np.abs(exact - approx)

# 50% crossover
n50_exact = ns[np.argmax(exact >= 0.5)]
n50_approx = ns[np.argmax(approx >= 0.5)]

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Birthday Problem — Exact Formula vs e-Approximation",
             fontsize=19, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: P(at least one shared birthday) ────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.plot(ns, exact, color=COLORS['e_gold'], lw=2.5, label='Exact probability')
ax.plot(ns, approx, color=COLORS['e_cyan'], lw=2.5, linestyle='--',
        label='e-approximation: 1−e^(−n(n−1)/730)')
ax.axhline(0.5, color='white', lw=1, linestyle=':', alpha=0.5)
ax.axvline(n50_exact, color=COLORS['e_gold'], lw=1.5, linestyle=':', alpha=0.7)
ax.axvline(n50_approx, color=COLORS['e_cyan'], lw=1.5, linestyle=':', alpha=0.7)
ax.fill_between(ns, exact, approx, alpha=0.2, color=COLORS['e_pink'],
                label='Difference')
ax.text(n50_exact + 0.5, 0.53, f'n={n50_exact}\n(exact)',
        color=COLORS['e_gold'], fontsize=8.5)

ax.set_title('P(at least one shared birthday)', color=COLORS['e_gold'])
ax.set_xlabel('Number of people (n)', color=COLORS['text'])
ax.set_ylabel('Probability', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)

# ── Middle: Log-scale on P(no match) ─────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
no_match_exact = np.array([p_no_match_exact(n) for n in ns])
no_match_approx = np.array([p_no_match_approx(n) for n in ns])

ax.semilogy(ns, no_match_exact, color=COLORS['e_green'], lw=2.5, label='Exact P(no match)')
ax.semilogy(ns, no_match_approx, color=COLORS['e_orange'], lw=2.5, linestyle='--',
            label='e-approx: e^(−n(n−1)/730)')
ax.axhline(0.5, color='white', lw=1, linestyle=':', alpha=0.5)
ax.text(2, 0.45, '50%', color='white', fontsize=9)
ax.set_title('P(no match) — Log Scale', color=COLORS['e_gold'])
ax.set_xlabel('Number of people (n)', color=COLORS['text'])
ax.set_ylabel('P(no shared birthday)', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, which='both')
ax.text(0.45, 0.85,
        'P(no match) ≈ e^(−n²/730)\nas n grows',
        transform=ax.transAxes, fontsize=10, color=COLORS['e_orange'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: Absolute error + annotation ───────────────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])
ax.plot(ns, error, color=COLORS['e_red'], lw=2.5, label='|Exact − Approx|')
ax.fill_between(ns, error, alpha=0.25, color=COLORS['e_red'])
peak_err_n = ns[np.argmax(error)]
peak_err = error[np.argmax(error)]
ax.plot(peak_err_n, peak_err, 'o', color=COLORS['e_gold'], ms=10,
        label=f'Peak error ≈ {peak_err:.4f} at n={peak_err_n}')

ax.set_title('Approximation Error  |Exact − e-Approx|', color=COLORS['e_gold'])
ax.set_xlabel('Number of people (n)', color=COLORS['text'])
ax.set_ylabel('Absolute error', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)

# Annotate the approximation formula clearly
ax.text(0.25, 0.78,
        'Approx uses the identity:\n'
        'Π(1 − k/365) ≈ e^(−Σk/365)\n'
        '= e^(−n(n−1)/730)\n\n'
        'Error is small for n ≤ 50',
        transform=ax.transAxes, fontsize=9, color=COLORS['text'],
        bbox=dict(boxstyle='round,pad=0.35', facecolor=COLORS['bg_dark'], alpha=0.85))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'birthday_problem', output_dir)
plt.close(fig)
print("birthday_problem.py complete.")
