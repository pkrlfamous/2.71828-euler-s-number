"""
e Approximation Race — Visual "race" showing three methods converging to e.
Methods: limit (1+1/n)^n, Taylor series Σ(1/k!), continued fraction.
Shows error decreasing across iterations in a race-style multi-panel figure.
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
from utils.math_helpers import (compute_e_limit, compute_e_series,
                                 e_continued_fraction_coeffs,
                                 e_continued_fraction_convergent)

apply_euler_style()

E_TRUE = math.e
MAX_STEPS = 20

# ── Method 1: Limit (1+1/n)^n — n grows exponentially ───────────────────────
ns_limit = [int(10 ** (k / 4)) for k in range(1, MAX_STEPS + 1)]
limit_approx = [compute_e_limit(n) for n in ns_limit]
limit_errors = [abs(v - E_TRUE) for v in limit_approx]

# ── Method 2: Taylor series Σ_{k=0}^{n} 1/k! ─────────────────────────────────
series_approx = [compute_e_series(n) for n in range(MAX_STEPS)]
series_errors = [abs(v - E_TRUE) for v in series_approx]

# ── Method 3: Continued fraction convergents ──────────────────────────────────
cf_coeffs = e_continued_fraction_coeffs(MAX_STEPS + 2)
cf_approx = []
cf_errors = []
for idx in range(MAX_STEPS):
    p, q = e_continued_fraction_convergent(cf_coeffs, idx)
    approx = p / q
    cf_approx.append(approx)
    cf_errors.append(abs(approx - E_TRUE))

# ── Figure layout: 3 "race frames" showing snapshots + race bar chart ─────────
steps_to_show = [1, 3, 5, 8, 12, 16, 19]
n_frames = len(steps_to_show)

fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("e Approximation Race — Three Methods Converging to e",
             fontsize=22, color=COLORS['e_gold'], fontweight='bold', y=0.98)

gs = gridspec.GridSpec(3, n_frames + 1,
                       figure=fig, wspace=0.35, hspace=0.45,
                       left=0.04, right=0.98, top=0.92, bottom=0.06)

method_colors = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_pink']]
method_names = ['Limit (1+1/n)ⁿ', 'Series Σ1/k!', 'Continued Fraction']
method_errors = [limit_errors, series_errors, cf_errors]
method_approx = [limit_approx, series_approx, cf_approx]
method_steps = [list(range(MAX_STEPS)), list(range(MAX_STEPS)), list(range(MAX_STEPS))]

# ── Top row: error curves for each method ─────────────────────────────────────
for mi, (col, name, errs) in enumerate(zip(method_colors, method_names, method_errors)):
    ax = fig.add_subplot(gs[mi, :n_frames])
    ax.set_facecolor(COLORS['bg_card'])
    ax.semilogy(range(len(errs)), errs, 'o-', color=col, lw=2.5, ms=6, label=name)
    ax.axhline(1e-15, color='white', lw=0.5, linestyle=':', alpha=0.4)
    ax.set_ylabel('|approx − e|', color=COLORS['text'], fontsize=10)
    ax.set_title(f'Method {mi+1}: {name}', color=col, fontsize=12)
    ax.grid(True, alpha=0.2, which='both')
    ax.legend(fontsize=9, loc='upper right')
    if mi == 2:
        ax.set_xlabel('Iteration (step)', color=COLORS['text'])

    # Mark snapshot frames
    for step in steps_to_show:
        if step < len(errs):
            ax.axvline(step, color='white', lw=0.7, linestyle=':', alpha=0.4)

# ── Right column: Race bar chart at final step ────────────────────────────────
ax_race = fig.add_subplot(gs[:, n_frames])
ax_race.set_facecolor(COLORS['bg_card'])

final_errs = [max(limit_errors[-1], 1e-16),
              max(series_errors[-1], 1e-16),
              max(cf_errors[-1], 1e-16)]
max_err = max(limit_errors[0], series_errors[0], cf_errors[0])

bar_heights = [max_err - e for e in final_errs]  # progress made
bars = ax_race.barh(method_names, bar_heights,
                    color=method_colors, alpha=0.85,
                    edgecolor='white', linewidth=0.7)
for bar, err in zip(bars, final_errs):
    ax_race.text(bar.get_width() + max_err * 0.01,
                 bar.get_y() + bar.get_height() / 2,
                 f'err={err:.2e}', va='center', fontsize=9, color=COLORS['text'])

ax_race.set_title('Race Progress\n(after 20 steps)', color=COLORS['e_gold'], fontsize=11)
ax_race.set_xlabel('Convergence progress\n(larger = better)', color=COLORS['text'])
ax_race.grid(True, alpha=0.2, axis='x')
ax_race.text(0.05, 0.05,
             f'Winner:\nSeries!\n\nAfter 20 terms:\n{series_errors[-1]:.2e}',
             transform=ax_race.transAxes, fontsize=9,
             color=COLORS['e_cyan'],
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'e_approximation_race', output_dir)
plt.close(fig)
print("e_approximation_race.py complete.")
