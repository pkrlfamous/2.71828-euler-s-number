"""
Compound Interest Game — Discover e through Bernoulli's bank problem.
$1 invested at 100% annual rate, compounded n times → (1 + 1/n)^n → e.
Interactive: user tries different n to maximise the final amount.
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

INTERACTIVE = sys.stdin.isatty()

print("=" * 65)
print("   COMPOUND INTEREST GAME — Discover Euler's Number!")
print("=" * 65)
print()
print("  The Bank offers: $1 at 100% annual interest.")
print("  You choose how many times per year to compound.")
print()
print("  Formula: A = (1 + 1/n)^n   where n = compounding frequency")
print()
print(f"  As n → ∞,  A → e ≈ {math.e:.10f}")
print()

examples = [1, 2, 4, 12, 52, 365, 1000, 10000, 1_000_000]
print("  Known compounding results:")
print(f"  {'n':>12s}  {'Name':20s}  {'Amount':>14s}  {'Distance to e':>14s}")
print("  " + "-" * 66)
for n in examples:
    amount = (1 + 1/n) ** n
    name_map = {1: 'Annual', 2: 'Semi-annual', 4: 'Quarterly',
                12: 'Monthly', 52: 'Weekly', 365: 'Daily',
                1000: '1000×/year', 10000: '10,000×/year', 1_000_000: 'Continuous'}
    print(f"  {n:>12,}  {name_map.get(n,''):20s}  ${amount:>12.8f}  {abs(amount - math.e):>14.10f}")
print()

user_results = []

if INTERACTIVE:
    print("  Try your own compounding frequencies!")
    print("  Enter n values (or 'q' to quit):\n")
    while True:
        try:
            raw = input("  n = ").strip()
            if raw.lower() == 'q':
                break
            n = int(raw)
            if n <= 0:
                print("  n must be positive.")
                continue
            amount = (1 + 1/n) ** n
            print(f"  (1 + 1/{n})^{n} = ${amount:.10f}  [distance to e: {abs(amount - math.e):.2e}]")
            user_results.append((n, amount))
        except ValueError:
            print("  Please enter an integer.")
        except EOFError:
            break
else:
    print("  Non-interactive mode — using preset n values for demonstration.")
    demo_ns = [1, 3, 10, 100, 1000]
    for n in demo_ns:
        amount = (1 + 1/n) ** n
        user_results.append((n, amount))
        print(f"  n={n:6d}: (1+1/{n})^{n} = ${amount:.10f}")

# ── Visualisation ─────────────────────────────────────────────────────────────
apply_euler_style()

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Compound Interest Game — (1 + 1/n)ⁿ → e  (Bernoulli's Discovery)",
             fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

ns_log = np.logspace(0, 7, 600)
vals_log = (1 + 1 / ns_log) ** ns_log

# ── Left: (1+1/n)^n on log scale ─────────────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.semilogx(ns_log, vals_log, color=COLORS['e_cyan'], lw=3,
            label='(1 + 1/n)ⁿ')
ax.axhline(math.e, color=COLORS['e_gold'], lw=2.5, linestyle='--',
           label=f'e = {math.e:.6f}')
# Mark preset examples
ex_ns = np.array(examples, dtype=float)
ex_vals = (1 + 1 / ex_ns) ** ex_ns
ax.scatter(ex_ns, ex_vals, color=COLORS['e_orange'], s=80, zorder=6)
for n, v in zip(examples, ex_vals):
    ax.annotate(f'n={n:,}', (n, v), textcoords='offset points',
                xytext=(3, 6), fontsize=7.5, color=COLORS['text'])

ax.set_title('Convergence to e  (log scale)', color=COLORS['e_gold'])
ax.set_xlabel('n (compounding frequency)', color=COLORS['text'])
ax.set_ylabel('Final amount ($)', color=COLORS['text'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.2, which='both')
ax.set_ylim(2.0, 2.80)

# ── Middle: Error from e ──────────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
errors = math.e - vals_log   # always positive (approaches from below)
ax.loglog(ns_log, errors, color=COLORS['e_pink'], lw=2.5,
          label='e − (1+1/n)ⁿ')
# Theoretical ~ e/(2n)
theory = math.e / (2 * ns_log)
ax.loglog(ns_log, theory, color=COLORS['e_green'], lw=2, linestyle='--',
          alpha=0.8, label='e/(2n)  [theoretical]')
ax.set_title('Gap to e  (log-log scale)', color=COLORS['e_gold'])
ax.set_xlabel('n', color=COLORS['text'])
ax.set_ylabel('e − (1+1/n)ⁿ', color=COLORS['text'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.2, which='both')
ax.text(0.3, 0.82, 'Error ∝ 1/n\n(halves when n doubles)',
        transform=ax.transAxes, fontsize=10, color=COLORS['e_pink'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Right: Bar chart for named compounding periods ────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])
bar_labels = ['Annual\n(n=1)', 'Semi\n(n=2)', 'Quarterly\n(n=4)', 'Monthly\n(n=12)',
              'Weekly\n(n=52)', 'Daily\n(n=365)', '1000×\n(n=1k)', 'e\n(n→∞)']
bar_vals = [(1 + 1/n)**n for n in [1, 2, 4, 12, 52, 365, 1000]] + [math.e]
bar_colors = [COLORS['e_red'], COLORS['e_orange'], COLORS['e_gold'],
              COLORS['e_green'], COLORS['e_cyan'], COLORS['e_blue'],
              COLORS['e_purple'], COLORS['e_pink']]

x_pos = np.arange(len(bar_labels))
bars = ax.bar(x_pos, bar_vals, color=bar_colors, edgecolor='white',
              linewidth=0.7, alpha=0.85)
ax.axhline(math.e, color='white', lw=2, linestyle='--', alpha=0.6,
           label=f'e = {math.e:.5f}')
ax.set_ylim(2.0, 2.85)
for bar, val in zip(bars, bar_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{val:.4f}', ha='center', va='bottom', fontsize=8.5, color=COLORS['text'])

ax.set_xticks(x_pos)
ax.set_xticklabels(bar_labels, fontsize=8.5)
ax.set_title('Final Amount by Compounding Period', color=COLORS['e_gold'])
ax.set_ylabel('$1 invested at 100% annual rate', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, axis='y')

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'compound_interest_game', output_dir)
plt.close(fig)
print("\ncompound_interest_game.py complete — plot saved.")
