"""
Poisson Distribution — P(k) = (λᵏ · e^(-λ)) / k!
Shows how e appears in counting rare events.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

lambdas = [1, 3, 5, 10]
lam_colors = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink']]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Poisson Distribution — P(k) = λᵏ · e⁻λ / k!",
             fontsize=20, color=COLORS['e_gold'], fontweight='bold')

for ax, lam, col in zip(axes.flat, lambdas, lam_colors):
    ax.set_facecolor(COLORS['bg_card'])
    k_max = max(20, int(lam + 4 * lam ** 0.5) + 1)
    k_vals = np.arange(0, k_max + 1)

    # PMF bars
    pmf = np.array([np.exp(-lam) * (lam ** k) / math.factorial(k) for k in k_vals])
    bars = ax.bar(k_vals, pmf, color=col, alpha=0.75, edgecolor='white',
                  linewidth=0.5, label=f'Poisson PMF λ={lam}')

    # Highlight the mode
    mode = int(lam) if lam == int(lam) else int(np.floor(lam))
    ax.bar(mode, pmf[mode], color='white', alpha=0.9, edgecolor=col, linewidth=1.5)

    # Normal approximation overlay for large λ
    if lam >= 5:
        x_cont = np.linspace(0, k_max, 300)
        normal_approx = stats.norm.pdf(x_cont, loc=lam, scale=np.sqrt(lam))
        ax.plot(x_cont, normal_approx, color=COLORS['e_red'], lw=2.5,
                linestyle='--', label=f'Normal(μ={lam}, σ={lam**0.5:.2f})')
        ax.legend(fontsize=9)

    ax.set_title(f'λ = {lam}  (mean = variance = λ)', color=COLORS['e_gold'], fontsize=13)
    ax.set_xlabel('k (number of events)', color=COLORS['text'])
    ax.set_ylabel('P(k)', color=COLORS['text'])
    ax.grid(True, alpha=0.2, axis='y')

    # Annotate formula
    ax.text(0.98, 0.95,
            f'P(k) = {lam}ᵏ·e⁻{lam}/k!\nP(0) = e⁻{lam} = {np.exp(-lam):.4f}',
            transform=ax.transAxes, fontsize=9, color=col,
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    # Mark mean
    ax.axvline(lam, color=col, lw=1.5, linestyle=':', alpha=0.8)
    ax.text(lam + 0.1, ax.get_ylim()[1] * 0.85, f'μ={lam}', color=col, fontsize=9)

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'poisson_distribution', output_dir)
plt.close(fig)
print("poisson_distribution.py complete.")
