"""
Exponential Distribution — f(x) = λ·e^(-λx)
Models waiting times between events. Shows the memoryless property.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Exponential Distribution — f(x) = λ·e^(−λx)  |  Waiting Times & Memoryless Property",
             fontsize=18, color=COLORS['e_gold'], fontweight='bold', y=1.01)

lambdas = [0.5, 1.0, 2.0, 3.0]
lam_colors = [COLORS['e_purple'], COLORS['e_gold'], COLORS['e_green'], COLORS['e_red']]

x = np.linspace(0, 6, 1000)

# ── Left: PDF for different λ ────────────────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
for lam, col in zip(lambdas, lam_colors):
    pdf = lam * np.exp(-lam * x)
    ax.plot(x, pdf, color=col, lw=2.5, label=f'λ={lam}')
    ax.fill_between(x, pdf, alpha=0.08, color=col)

ax.set_title('PDF: f(x) = λ·e^(−λx)', color=COLORS['e_gold'])
ax.set_xlabel('x (time)', color=COLORS['text'])
ax.set_ylabel('f(x)', color=COLORS['text'])
ax.legend(fontsize=10)
ax.set_xlim(0, 6)
ax.set_ylim(0, 3.2)
ax.grid(True, alpha=0.2)
ax.text(0.62, 0.92,
        'Mean = 1/λ\nVariance = 1/λ²',
        transform=ax.transAxes, fontsize=10, color=COLORS['text'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Middle: CDF + survival function ─────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
lam = 1.0
cdf = 1 - np.exp(-lam * x)
survival = np.exp(-lam * x)
ax.plot(x, cdf, color=COLORS['e_cyan'], lw=2.5, label='CDF: P(X ≤ x) = 1−e^(−x)')
ax.plot(x, survival, color=COLORS['e_orange'], lw=2.5,
        linestyle='--', label='Survival: P(X > x) = e^(−x)')
ax.axhline(1 - np.exp(-1), color='white', lw=1, linestyle=':', alpha=0.6)
ax.axvline(1, color='white', lw=1, linestyle=':', alpha=0.6)
ax.text(1.05, 0.55, f'P(X≤1) = 1−1/e\n≈ {1-np.exp(-1):.4f}',
        color=COLORS['text'], fontsize=9)
ax.set_title('CDF & Survival Function  (λ=1)', color=COLORS['e_gold'])
ax.set_xlabel('x (time)', color=COLORS['text'])
ax.set_ylabel('Probability', color=COLORS['text'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.2)

# ── Right: Memoryless property ───────────────────────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])

lam = 1.0
s = 1.0   # already waited s units
t_vals = np.linspace(0, 4, 200)

# P(X > s+t | X > s) = P(X > t)  — both are e^(-λt), identical
p_conditional = np.exp(-lam * t_vals)   # P(X>s+t | X>s)
p_unconditional = np.exp(-lam * t_vals)  # P(X>t) — exactly the same

# Illustrate visually: plot the original distribution and the "shifted" version
x_all = np.linspace(0, 5, 600)
full_survival = np.exp(-lam * x_all)
ax.plot(x_all, full_survival, color=COLORS['e_gold'], lw=2.5, label='P(X > x)  [full]')

# Shade the "already waited" region
mask_waited = x_all <= s
ax.fill_between(x_all[mask_waited], full_survival[mask_waited],
                alpha=0.3, color=COLORS['e_red'], label=f'Already waited s={s}')

# The conditional distribution shifted to start at s
x_cond = np.linspace(s, 5, 400)
cond_survival = np.exp(-lam * (x_cond - s))  # = e^(-λt), t = x-s
ax.plot(x_cond, cond_survival, color=COLORS['e_cyan'], lw=2.5, linestyle='--',
        label=f'P(X > s+t | X > s)  [rescaled]')

ax.axvline(s, color=COLORS['e_red'], lw=1.5, linestyle=':', alpha=0.8)
ax.text(s + 0.05, 0.95, f's={s}', color=COLORS['e_red'], fontsize=10, va='top')

ax.set_title('Memoryless Property  (λ=1)', color=COLORS['e_gold'])
ax.set_xlabel('x (time)', color=COLORS['text'])
ax.set_ylabel('Survival probability', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)
ax.text(0.38, 0.55,
        'P(X>s+t | X>s) = P(X>t)\n= e^(−λt)\n\n"The future doesn\'t\ndepend on the past"',
        transform=ax.transAxes, fontsize=9, color=COLORS['e_cyan'],
        bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'exponential_distribution', output_dir)
plt.close(fig)
print("exponential_distribution.py complete.")
