"""
Optimal Stopping Simulation — Secretary Problem.
Simulate 10,000 rounds of the secretary problem.
Compare strategy "stop at k" for k=1..n, show optimal k ≈ n/e gives ~37% success.
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

rng = np.random.default_rng(2718281828)

N_CANDIDATES = 50    # secretary pool size
N_SIMULATIONS = 10_000

inv_e = 1.0 / math.e
opt_k_theory = max(1, round(N_CANDIDATES * inv_e))  # ≈ 18

print(f"Secretary Problem Simulation")
print(f"  n = {N_CANDIDATES} candidates, {N_SIMULATIONS:,} simulations per strategy")
print(f"  Theoretical optimal k = n/e ≈ {N_CANDIDATES * inv_e:.1f} → {opt_k_theory}")
print(f"  Expected success rate  ≈ 1/e ≈ {inv_e:.4f} = {inv_e*100:.2f}%")
print()

def simulate_secretary(n, k, n_sims, rng):
    """
    Simulate n_sims rounds of the secretary problem with threshold k.
    Returns success rate.
    """
    wins = 0
    for _ in range(n_sims):
        # Generate a random permutation of n candidates (ranked 1=best..n=worst)
        ranks = rng.permutation(n)  # 0-indexed, 0 = best
        # Observe first k, find best among them
        if k == 0:
            # Pick first one immediately
            wins += 1 if ranks[0] == 0 else 0
            continue
        best_in_sample = min(ranks[:k])
        # From position k onwards, pick the first better than sample best
        hired = False
        for i in range(k, n):
            if ranks[i] < best_in_sample:
                if ranks[i] == 0:
                    wins += 1
                hired = True
                break
        if not hired:
            # Forced to pick last; wins if it's the best
            if ranks[-1] == 0:
                wins += 1
    return wins / n_sims

# Simulate for k = 1..n-1
print("Running simulations...", end=' ', flush=True)
k_values = np.arange(1, N_CANDIDATES)
success_rates = np.array([simulate_secretary(N_CANDIDATES, k, N_SIMULATIONS, rng)
                           for k in k_values])
print("done.\n")

opt_k_sim = k_values[np.argmax(success_rates)]
opt_rate_sim = success_rates[np.argmax(success_rates)]
print(f"  Simulation optimal k = {opt_k_sim}  (success rate = {opt_rate_sim:.4f})")
print(f"  Theoretical k = {opt_k_theory} = n/e = {N_CANDIDATES}/{math.e:.4f}")

# Theoretical success probability
def secretary_prob_exact(n, k):
    if k == 0:
        return 1 / n
    return (k / n) * sum(1.0 / j for j in range(k, n))

theo_probs = np.array([secretary_prob_exact(N_CANDIDATES, k) for k in k_values])

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle(f"Secretary Problem — Optimal Stopping Simulation  (n={N_CANDIDATES}, {N_SIMULATIONS:,} rounds)",
             fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: Simulated vs theoretical success rate ───────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
k_fracs = k_values / N_CANDIDATES

ax.plot(k_fracs, success_rates, color=COLORS['e_cyan'], lw=2.5, alpha=0.9,
        label='Simulated success rate')
ax.plot(k_fracs, theo_probs, color=COLORS['e_gold'], lw=2.5, linestyle='--',
        label='Theoretical P(success)')
ax.axvline(inv_e, color=COLORS['e_orange'], lw=2, linestyle=':',
           label=f'k/n = 1/e ≈ {inv_e:.3f}')
ax.axhline(inv_e, color=COLORS['e_pink'], lw=1.5, linestyle=':',
           label=f'P = 1/e ≈ {inv_e:.3f}')
ax.plot(opt_k_sim / N_CANDIDATES, opt_rate_sim, 'o', color=COLORS['e_gold'],
        ms=12, zorder=6, label=f'Sim optimal: k={opt_k_sim}, P={opt_rate_sim:.4f}')

ax.set_title('Success Rate vs Stopping Threshold', color=COLORS['e_gold'])
ax.set_xlabel('k/n  (fraction observed)', color=COLORS['text'])
ax.set_ylabel('P(hiring the best candidate)', color=COLORS['text'])
ax.legend(fontsize=8.5)
ax.grid(True, alpha=0.2)
ax.set_xlim(0, 1)

# ── Middle: Distribution of success rates near optimal k ─────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])

# Run many simulations at fixed optimal k to show distribution
n_dist = 2000
results_at_opt = []
for _ in range(n_dist):
    ranks = rng.permutation(N_CANDIDATES)
    k = opt_k_theory
    best_in_sample = min(ranks[:k])
    won = False
    for i in range(k, N_CANDIDATES):
        if ranks[i] < best_in_sample:
            won = (ranks[i] == 0)
            break
    results_at_opt.append(int(won))

win_rate = np.mean(results_at_opt)
# Rolling 100-sim window
window = 100
rolling = np.convolve(results_at_opt, np.ones(window)/window, mode='valid')

ax.plot(rolling, color=COLORS['e_green'], lw=2, label=f'Rolling win rate (window={window})')
ax.axhline(inv_e, color=COLORS['e_gold'], lw=2, linestyle='--', label=f'1/e = {inv_e:.4f}')
ax.axhline(win_rate, color=COLORS['e_cyan'], lw=1.5, linestyle=':',
           label=f'Overall: {win_rate:.4f}')
ax.set_title(f'Win Rate Over {n_dist} Games  (k={opt_k_theory})', color=COLORS['e_gold'])
ax.set_xlabel('Game number', color=COLORS['text'])
ax.set_ylabel('Rolling P(win)', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)
ax.set_ylim(0.1, 0.65)
ax.text(0.04, 0.96,
        f'Converges to 1/e ≈ {inv_e:.4f}\nwith enough games',
        transform=ax.transAxes, fontsize=9, color=COLORS['e_cyan'],
        va='top', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: Heat map — success rate for all (n, k) pairs ──────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])

ns_heat = np.arange(5, 61)
Z = np.zeros((len(ns_heat), len(ns_heat)))
Z[:] = np.nan
for i, nv in enumerate(ns_heat):
    for kv in range(1, nv):
        j = kv - 1
        if j < len(ns_heat):
            Z[i, j] = secretary_prob_exact(nv, kv)

im = ax.imshow(Z, aspect='auto', origin='lower', cmap='plasma',
               extent=[1, len(ns_heat), ns_heat[0], ns_heat[-1]],
               vmin=0, vmax=0.42)
# Draw the n/e line
ks_line = ns_heat * inv_e
ax.plot(ks_line, ns_heat, color=COLORS['e_gold'], lw=2.5, linestyle='--',
        label='k = n/e (optimal)')
ax.set_title('P(success) Heatmap over (n, k)', color=COLORS['e_gold'])
ax.set_xlabel('k (stop-and-pick threshold)', color=COLORS['text'])
ax.set_ylabel('n (candidates)', color=COLORS['text'])
ax.legend(fontsize=9.5)
plt.colorbar(im, ax=ax, label='P(success)')

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'optimal_stopping_sim', output_dir)
plt.close(fig)
print("\noptimal_stopping_sim.py complete — plot saved.")
