"""
Secretary Problem (Optimal Stopping)
Optimal stopping threshold r/n ≈ 1/e ≈ 37%
Strategy: observe first r candidates, then hire the next one better than all seen.
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

def secretary_success_prob(n, r):
    """
    Exact probability of success with threshold r (observe first r, then pick).
    P(success | n, r) = (r/n) * Σ_{k=r}^{n-1} 1/(k)
    """
    if r == 0:
        return 1.0 / n
    if r >= n:
        return 0.0
    return (r / n) * sum(1.0 / k for k in range(r, n))

n = 100
rs = np.arange(1, n)
probs = [secretary_success_prob(n, r) for r in rs]
r_fracs = rs / n

inv_e = 1.0 / math.e
opt_r = rs[np.argmax(probs)]
opt_prob = max(probs)

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Secretary Problem — Optimal Stopping at n/e ≈ 37%",
             fontsize=19, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: Success probability vs r/n ─────────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.plot(r_fracs, probs, color=COLORS['e_cyan'], lw=2.5, label='P(success | r, n=100)')
ax.axvline(inv_e, color=COLORS['e_gold'], lw=2, linestyle='--', label=f'r/n = 1/e ≈ {inv_e:.3f}')
ax.axhline(opt_prob, color=COLORS['e_pink'], lw=1.5, linestyle=':', alpha=0.7)
ax.plot(opt_r / n, opt_prob, 'o', color=COLORS['e_gold'], ms=12, zorder=5,
        label=f'Optimum: r={opt_r}, P≈{opt_prob:.4f}')
ax.fill_between(r_fracs, probs, alpha=0.15, color=COLORS['e_cyan'])

ax.set_title('P(success) vs Stopping Threshold r/n', color=COLORS['e_gold'])
ax.set_xlabel('r/n (fraction observed before deciding)', color=COLORS['text'])
ax.set_ylabel('Probability of choosing best', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)
ax.text(0.55, 0.25,
        f'n = {n} candidates\nOptimal r = {opt_r} = n/e\nMax P ≈ 1/e ≈ {inv_e:.4f}',
        transform=ax.transAxes, fontsize=9, color=COLORS['e_gold'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Middle: vary n, show optimal r/n always ≈ 1/e ────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
ns_range = list(range(5, 201))
opt_fracs = []
for nv in ns_range:
    ps = [secretary_success_prob(nv, rv) for rv in range(1, nv)]
    best_r = np.argmax(ps) + 1
    opt_fracs.append(best_r / nv)

ax.plot(ns_range, opt_fracs, color=COLORS['e_green'], lw=2.5, label='Optimal r/n')
ax.axhline(inv_e, color=COLORS['e_gold'], lw=2, linestyle='--', label=f'1/e = {inv_e:.4f}')
ax.fill_between(ns_range, opt_fracs, inv_e, alpha=0.15, color=COLORS['e_green'])
ax.set_title('Optimal r/n Converges to 1/e', color=COLORS['e_gold'])
ax.set_xlabel('n (number of candidates)', color=COLORS['text'])
ax.set_ylabel('Optimal stopping fraction r/n', color=COLORS['text'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.2)
ax.set_ylim(0.25, 0.55)
ax.text(0.4, 0.85, 'For any n, stop after\nobserving ≈ 37% of candidates',
        transform=ax.transAxes, fontsize=10, color=COLORS['text'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: Heat map of success probability P(success | r, n) ─────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])
ns_heat = np.arange(5, 51)
rs_heat = np.arange(0, 51)
Z = np.zeros((len(rs_heat), len(ns_heat)))
for j, nv in enumerate(ns_heat):
    for i, rv in enumerate(rs_heat):
        if rv < nv:
            Z[i, j] = secretary_success_prob(nv, rv)
        else:
            Z[i, j] = np.nan

im = ax.imshow(Z, aspect='auto', origin='lower',
               extent=[ns_heat[0], ns_heat[-1], rs_heat[0], rs_heat[-1]],
               cmap='plasma', vmin=0, vmax=0.42)
# Draw the 1/e line
ax.plot(ns_heat, ns_heat * inv_e, color=COLORS['e_gold'], lw=2.5,
        linestyle='--', label='r = n/e')
ax.set_title('P(success) Heatmap  [darker = higher]', color=COLORS['e_gold'])
ax.set_xlabel('n (candidates)', color=COLORS['text'])
ax.set_ylabel('r (observe first r)', color=COLORS['text'])
ax.legend(fontsize=10)
plt.colorbar(im, ax=ax, label='P(success)')

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'secretary_problem', output_dir)
plt.close(fig)
print("secretary_problem.py complete.")
