"""
Stirling's Approximation — n! ≈ √(2πn) · (n/e)ⁿ
e appears in the approximation of the factorial function.
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

ns = np.arange(1, 26)
exact_factorials = np.array([math.factorial(n) for n in ns], dtype=float)

def stirling(n):
    return np.sqrt(2 * np.pi * n) * (n / np.e) ** n

stirling_vals = np.array([stirling(n) for n in ns])
relative_errors = np.abs(exact_factorials - stirling_vals) / exact_factorials * 100

# Refined Stirling with correction term
def stirling_refined(n):
    return stirling(n) * (1 + 1/(12*n))

stirling_ref_vals = np.array([stirling_refined(n) for n in ns])
ref_errors = np.abs(exact_factorials - stirling_ref_vals) / exact_factorials * 100

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Stirling's Approximation — n! ≈ √(2πn)·(n/e)ⁿ",
             fontsize=19, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: n! vs Stirling on log scale ────────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.semilogy(ns, exact_factorials, 'o-', color=COLORS['e_gold'], lw=2.5,
            ms=6, label='n! (exact)', zorder=5)
ax.semilogy(ns, stirling_vals, 's--', color=COLORS['e_cyan'], lw=2.5,
            ms=6, label='√(2πn)·(n/e)ⁿ', zorder=4)
ax.semilogy(ns, stirling_ref_vals, '^:', color=COLORS['e_pink'], lw=2, ms=5,
            label='Stirling + 1/(12n) correction', zorder=3, alpha=0.85)

ax.set_title('n! vs Stirling Approximation  (log scale)', color=COLORS['e_gold'])
ax.set_xlabel('n', color=COLORS['text'])
ax.set_ylabel('Value  (log scale)', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, which='both')
ax.text(0.05, 0.95,
        'n! ≈ √(2πn)·(n/e)ⁿ\n\nLines overlap — very accurate!',
        transform=ax.transAxes, fontsize=9, color=COLORS['e_gold'],
        va='top', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Middle: Relative error ────────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
ax.semilogy(ns, relative_errors, 'o-', color=COLORS['e_red'], lw=2.5,
            ms=7, label='Basic Stirling error')
ax.semilogy(ns, ref_errors + 1e-12, 's-', color=COLORS['e_green'], lw=2.5,
            ms=7, label='Refined error (+1/12n term)')

# Annotate first few values
for n, err in zip(ns[:8], relative_errors[:8]):
    ax.annotate(f'{err:.2f}%', (n, err), textcoords='offset points',
                xytext=(3, 5), fontsize=7, color=COLORS['e_red'])

ax.set_title('Relative Error |n! − Stirling| / n!', color=COLORS['e_gold'])
ax.set_xlabel('n', color=COLORS['text'])
ax.set_ylabel('Relative error (%) — log scale', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, which='both')
ax.text(0.4, 0.85,
        'Error ∝ 1/(12n)\nDecays as n grows',
        transform=ax.transAxes, fontsize=10, color=COLORS['e_red'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: log(n!) vs n log n ─────────────────────────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])

log_exact = np.log(exact_factorials)
log_stirling = np.log(stirling_vals)
log_stirling_approx_simple = ns * np.log(ns) - ns  # simplest: log(n!) ≈ n·ln(n) − n

ax.plot(ns, log_exact, 'o-', color=COLORS['e_gold'], lw=2.5, ms=6, label='ln(n!) exact')
ax.plot(ns, log_stirling, '--', color=COLORS['e_cyan'], lw=2.5, label='ln(Stirling)')
ax.plot(ns, log_stirling_approx_simple, ':', color=COLORS['e_orange'], lw=2.5,
        label='n·ln(n) − n  [simple]')

ax.set_title('ln(n!) — Comparing Approximations', color=COLORS['e_gold'])
ax.set_xlabel('n', color=COLORS['text'])
ax.set_ylabel('ln(n!)', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)

# Ratio label: add formula box
ax.text(0.03, 0.95,
        r'Stirling: $\ln(n!) \approx \frac{1}{2}\ln(2\pi n) + n\ln(n) - n$'
        '\n\nSimple: ln(n!) ≈ n·ln(n) − n',
        transform=ax.transAxes, fontsize=9, color=COLORS['text'], va='top',
        bbox=dict(boxstyle='round,pad=0.35', facecolor=COLORS['bg_dark'], alpha=0.85))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'stirling_approximation', output_dir)
plt.close(fig)
print("stirling_approximation.py complete.")
