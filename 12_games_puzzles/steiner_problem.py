"""
Steiner's Problem — Find x that maximises x^(1/x).
The answer is x = e. Demonstrates e as the natural base of exponentiation.
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

# f(x) = x^(1/x) = e^(ln(x)/x)
x = np.linspace(0.15, 10, 2000)
with np.errstate(divide='ignore', invalid='ignore'):
    f = np.where(x > 0, np.exp(np.log(x) / x), np.nan)

# Derivative: d/dx [x^(1/x)] = x^(1/x) * (1 - ln(x)) / x²
with np.errstate(divide='ignore', invalid='ignore'):
    df = np.where(x > 0, f * (1 - np.log(x)) / x**2, np.nan)

e_val = math.e
f_at_e = e_val ** (1 / e_val)  # = e^(1/e) ≈ 1.4447

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Steiner's Problem — Which x maximises x^(1/x)?  Answer: x = e",
             fontsize=18, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: x^(1/x) with maximum marked ────────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
ax.plot(x, f, color=COLORS['e_cyan'], lw=3, label='f(x) = x^(1/x)')
ax.fill_between(x, f, alpha=0.10, color=COLORS['e_cyan'])

# Mark maximum at x=e
ax.plot(e_val, f_at_e, 'o', color=COLORS['e_gold'], ms=14, zorder=6,
        label=f'Maximum at x=e ≈ {e_val:.4f}')
ax.axvline(e_val, color=COLORS['e_gold'], lw=1.5, linestyle='--', alpha=0.7)
ax.axhline(f_at_e, color=COLORS['e_gold'], lw=1, linestyle=':', alpha=0.5)
ax.annotate(f'e^(1/e) ≈ {f_at_e:.5f}',
            xy=(e_val, f_at_e), xytext=(e_val + 1.5, f_at_e + 0.03),
            fontsize=11, color=COLORS['e_gold'],
            arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.5))

# Compare with some competitors
competitors = [2, 3, math.pi]
comp_labels = ['2', '3', 'π']
comp_colors = [COLORS['e_red'], COLORS['e_green'], COLORS['e_purple']]
for xc, lbl, col in zip(competitors, comp_labels, comp_colors):
    fc = xc ** (1/xc)
    ax.plot(xc, fc, 's', color=col, ms=9, zorder=5)
    ax.annotate(f'{lbl}^(1/{lbl}) = {fc:.4f}', (xc, fc),
                textcoords='offset points', xytext=(6, -18),
                fontsize=8.5, color=col)

ax.set_title('f(x) = x^(1/x)', color=COLORS['e_gold'])
ax.set_xlabel('x', color=COLORS['text'])
ax.set_ylabel('x^(1/x)', color=COLORS['text'])
ax.legend(fontsize=9.5)
ax.set_xlim(0, 10)
ax.set_ylim(0.8, 1.55)
ax.grid(True, alpha=0.2)

# ── Middle: Derivative (1 − ln x) / x² — zero crossing at x=e ───────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
# d/dx [x^(1/x)] = x^(1/x) * (1 - ln x) / x²
# Sign determined by (1 - ln x): positive for x<e, negative for x>e
sign_factor = (1 - np.log(x)) / x**2
ax.plot(x, df, color=COLORS['e_green'], lw=2.5, label="f'(x)")
ax.plot(x, sign_factor, color=COLORS['e_orange'], lw=2, linestyle='--',
        label='(1−ln x)/x²  [sign factor]', alpha=0.8)
ax.axhline(0, color='white', lw=1.5, linestyle='-', alpha=0.5)
ax.axvline(e_val, color=COLORS['e_gold'], lw=2, linestyle='--',
           label=f"f'(e) = 0  at x=e")
ax.fill_between(x[x < e_val], df[x < e_val], 0, alpha=0.15, color=COLORS['e_green'],
                label='Increasing (f′>0)')
ax.fill_between(x[x > e_val], df[x > e_val], 0, alpha=0.15, color=COLORS['e_red'],
                label='Decreasing (f′<0)')

ax.set_title("Derivative f'(x) — zero at x=e", color=COLORS['e_gold'])
ax.set_xlabel('x', color=COLORS['text'])
ax.set_ylabel("f'(x)", color=COLORS['text'])
ax.set_ylim(-0.15, 0.25)
ax.set_xlim(0.5, 8)
ax.legend(fontsize=8.5)
ax.grid(True, alpha=0.2)
ax.text(0.04, 0.95,
        "f'(x) = x^(1/x) · (1−ln x)/x²\n\n"
        "f'(x) = 0  ⟺  ln x = 1  ⟺  x = e",
        transform=ax.transAxes, fontsize=9, color=COLORS['text'], va='top',
        bbox=dict(boxstyle='round,pad=0.35', facecolor=COLORS['bg_dark'], alpha=0.85))

# ── Right: Comparison table and second form x^x^(1/x) approaches ─────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])

# Plot x^(1/x) for integer x vs e^(1/e)
int_xs = np.arange(1, 13)
int_fs = int_xs ** (1 / int_xs.astype(float))
bar_cols = [COLORS['e_red'] if abs(xi - e_val) > 0.5 else COLORS['e_gold']
            for xi in int_xs]

bars = ax.bar(int_xs, int_fs, color=bar_cols, edgecolor='white',
              linewidth=0.7, alpha=0.85)
ax.axhline(f_at_e, color=COLORS['e_gold'], lw=2.5, linestyle='--',
           label=f'e^(1/e) = {f_at_e:.5f} [maximum]')

for bar, xi, fi in zip(bars, int_xs, int_fs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{fi:.4f}', ha='center', va='bottom', fontsize=8, color=COLORS['text'],
            rotation=90)

# Highlight x=2 and x=3 which are closest integers
ax.bar([2, 3], [2**(1/2), 3**(1/3)], color=[COLORS['e_blue'], COLORS['e_purple']],
       edgecolor='white', linewidth=1.2, alpha=0.85)

ax.set_title('x^(1/x) for Integer x  (e is between 2 and 3!)', color=COLORS['e_gold'])
ax.set_xlabel('x', color=COLORS['text'])
ax.set_ylabel('x^(1/x)', color=COLORS['text'])
ax.set_xticks(int_xs)
ax.legend(fontsize=9.5)
ax.grid(True, alpha=0.2, axis='y')
ax.set_ylim(0.9, 1.6)
ax.text(0.38, 0.18,
        f'2^(1/2) = {2**0.5:.5f}\n3^(1/3) = {3**(1/3):.5f}\ne^(1/e) = {f_at_e:.5f}  ← MAX\n'
        f'\ne^(1/e) > 3^(1/3) > 2^(1/2)',
        transform=ax.transAxes, fontsize=9.5, color=COLORS['e_gold'],
        bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'steiner_problem', output_dir)
plt.close(fig)
print("steiner_problem.py complete.")
