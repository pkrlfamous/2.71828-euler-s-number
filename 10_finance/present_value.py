"""
Present Value: PV = FV · e^(-rt)
How $1 million in the future is worth less today.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

FV = 1_000_000  # future value: $1 million
t  = np.linspace(0, 50, 500)

rates = [0.02, 0.05, 0.08, 0.12]
rate_colors = [COLORS['e_cyan'], COLORS['e_green'], COLORS['e_gold'], COLORS['e_red']]
rate_labels = ['2% (low/risk-free)', '5% (moderate)', '8% (equity)', '12% (high yield)']

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: PV vs time horizon ───────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

for rate, color, label in zip(rates, rate_colors, rate_labels):
    pv = FV * np.exp(-rate * t)
    ax1.plot(t, pv / 1e3, color=color, lw=2.3, label=f'r = {label}')
    ax1.fill_between(t, pv / 1e3, alpha=0.05, color=color)

ax1.axhline(FV / 1e3, color=COLORS['text'], lw=1.2, ls=':', alpha=0.6,
            label='FV = $1,000,000')
ax1.set_xlabel('Years into the future (t)', fontsize=12)
ax1.set_ylabel('Present Value ($000s)', fontsize=12)
ax1.set_title('PV of $1,000,000\nPV = FV · e⁻ʳᵗ',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.25)
ax1.set_ylim(0, FV / 1e3 * 1.05)

# ── Panel 2: Discount factor surface (heatmap) ────────────────────────────────
ax2 = fig.add_subplot(gs[1])

t_grid  = np.linspace(0, 30, 200)
r_grid  = np.linspace(0.01, 0.20, 200)
T_mesh, R_mesh = np.meshgrid(t_grid, r_grid)
Discount = np.exp(-R_mesh * T_mesh)

im = ax2.imshow(Discount, extent=[0, 30, 0.01, 0.20], origin='lower',
                aspect='auto', cmap='viridis', vmin=0, vmax=1)
cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
cbar.set_label('Discount factor e⁻ʳᵗ', fontsize=9)

# Add contour lines at 50% and 25% discounts
contours = ax2.contour(T_mesh, R_mesh, Discount,
                       levels=sorted([0.75, 0.5, 0.25, 0.1]),
                       colors='white', linewidths=1.2, alpha=0.7)
ax2.clabel(contours, fmt='%.2f', inline=True, fontsize=8)

ax2.set_xlabel('Time t (years)', fontsize=12)
ax2.set_ylabel('Discount rate r', fontsize=12)
ax2.set_yticks(np.arange(0.02, 0.22, 0.04))
ax2.set_yticklabels([f'{r:.0%}' for r in np.arange(0.02, 0.22, 0.04)])
ax2.set_title('Discount Factor Heatmap\ne⁻ʳᵗ  across r and t',
              fontsize=13, color=COLORS['e_gold'], pad=10)

# ── Panel 3: "Rule of 69" — time to halve PV ─────────────────────────────────
ax3 = fig.add_subplot(gs[2])

rates_wide = np.linspace(0.01, 0.25, 300)
half_life_exact = np.log(2) / rates_wide     # t s.t. e^(-rt) = 0.5 → t = ln2/r
half_life_rule  = 0.693 / rates_wide         # same: ln2 ≈ 0.693

ax3.plot(rates_wide * 100, half_life_exact, color=COLORS['e_gold'], lw=2.8,
         label='t½ = ln2/r  (exact)')
ax3.plot(rates_wide * 100, half_life_rule, color=COLORS['e_cyan'], lw=1.5, ls='--',
         alpha=0.6, label='Rule of 69  ≈ 69/r%')

# Mark standard rates
for rate, color in zip(rates, rate_colors):
    hl = np.log(2) / rate
    ax3.scatter([rate * 100], [hl], color=color, s=90, zorder=5)
    ax3.annotate(f'{hl:.1f}y', (rate * 100, hl),
                 textcoords='offset points', xytext=(6, 4),
                 fontsize=9, color=color)

ax3.set_xlabel('Discount rate r (%)', fontsize=12)
ax3.set_ylabel('Half-life (years)', fontsize=12)
ax3.set_title('Rule of 69\nYears for PV to Halve = ln2/r',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)

fig.suptitle('Present Value  PV = FV·e⁻ʳᵗ  —  Money Has a Time Value, e Captures It',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'present_value', OUTPUT_DIR)
plt.close(fig)
