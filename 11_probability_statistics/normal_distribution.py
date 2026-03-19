"""
Normal Distribution — Bell curve with e at its heart.
Formula: f(x) = (1/σ√2π) · e^(-(x-μ)²/2σ²)
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Normal Distribution — The Bell Curve & Euler's Number",
             fontsize=20, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# ── Left: Standard normal PDF + CDF with σ regions ──────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
x = np.linspace(-4, 4, 1000)
pdf = stats.norm.pdf(x)
cdf = stats.norm.cdf(x)

sigma_colors = [COLORS['e_blue'], COLORS['e_purple'], COLORS['e_red']]
sigma_labels = ['1σ (68.27%)', '2σ (95.45%)', '3σ (99.73%)']
for k, (col, lbl) in enumerate(zip(sigma_colors, sigma_labels), start=1):
    mask = (x >= -k) & (x <= k)
    ax.fill_between(x[mask], pdf[mask], alpha=0.25 + 0.05 * k, color=col, label=lbl)

ax.plot(x, pdf, color=COLORS['e_gold'], lw=2.5, label='PDF')
ax.plot(x, cdf, color=COLORS['e_cyan'], lw=2, linestyle='--', label='CDF')

for k in [1, 2, 3]:
    ax.axvline(k, color='white', lw=0.6, alpha=0.4, linestyle=':')
    ax.axvline(-k, color='white', lw=0.6, alpha=0.4, linestyle=':')
    ax.text(k + 0.05, 0.01, f'+{k}σ', color='white', fontsize=8, alpha=0.7)
    ax.text(-k - 0.35, 0.01, f'-{k}σ', color='white', fontsize=8, alpha=0.7)

ax.set_title('Standard Normal  μ=0, σ=1', color=COLORS['e_gold'])
ax.set_xlabel('x', color=COLORS['text'])
ax.set_ylabel('Probability', color=COLORS['text'])
ax.legend(fontsize=9, loc='upper left')
ax.grid(True, alpha=0.2)
ax.text(0.02, 0.97,
        r'$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$',
        transform=ax.transAxes, fontsize=10, color=COLORS['e_gold'],
        va='top', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.7))

# ── Middle: Varying μ (shift) ────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
mus = [-2, -1, 0, 1, 2]
mu_colors = [COLORS['e_red'], COLORS['e_orange'], COLORS['e_gold'],
             COLORS['e_green'], COLORS['e_cyan']]
for mu, col in zip(mus, mu_colors):
    y = stats.norm.pdf(x, loc=mu, scale=1)
    ax.plot(x, y, color=col, lw=2, label=f'μ={mu}, σ=1')
    ax.axvline(mu, color=col, lw=0.8, linestyle=':', alpha=0.5)

ax.set_title('Varying Mean μ  (σ=1 fixed)', color=COLORS['e_gold'])
ax.set_xlabel('x', color=COLORS['text'])
ax.set_ylabel('PDF', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)
ax.text(0.5, 0.97, 'Shift changes location,\nnot shape',
        transform=ax.transAxes, fontsize=9, color=COLORS['text'],
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.7))

# ── Right: Varying σ (spread) ────────────────────────────────────────────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])
sigmas = [0.5, 1.0, 1.5, 2.0, 3.0]
sig_colors = [COLORS['e_pink'], COLORS['e_gold'], COLORS['e_green'],
              COLORS['e_blue'], COLORS['e_purple']]
for sigma, col in zip(sigmas, sig_colors):
    y = stats.norm.pdf(x, loc=0, scale=sigma)
    ax.plot(x, y, color=col, lw=2, label=f'μ=0, σ={sigma}')

ax.set_title('Varying Spread σ  (μ=0 fixed)', color=COLORS['e_gold'])
ax.set_xlabel('x', color=COLORS['text'])
ax.set_ylabel('PDF', color=COLORS['text'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2)
ax.text(0.5, 0.97, 'σ controls width & height\n(area always = 1)',
        transform=ax.transAxes, fontsize=9, color=COLORS['text'],
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.7))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'normal_distribution', output_dir)
plt.close(fig)
print("normal_distribution.py complete.")
