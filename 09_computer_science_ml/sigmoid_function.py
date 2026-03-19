"""
Sigmoid function, softmax temperature scaling, and cross-entropy loss.
σ(x) = 1 / (1 + e^(-kx))
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

fig = plt.figure(figsize=(18, 6))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.38)

# ── Panel 1: Sigmoid with different steepness ───────────────────────────────
ax1 = fig.add_subplot(gs[0])
x = np.linspace(-6, 6, 400)
steepness = [0.5, 1, 2, 5]
palette = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_orange'], COLORS['e_red']]

for k, color in zip(steepness, palette):
    y = 1 / (1 + np.exp(-k * x))
    ax1.plot(x, y, color=color, lw=2.2, label=f'k = {k}')

ax1.axhline(0.5, color=COLORS['grid'], lw=1, ls='--', alpha=0.7)
ax1.axvline(0.0, color=COLORS['grid'], lw=1, ls='--', alpha=0.7)
ax1.set_xlabel('x', fontsize=13)
ax1.set_ylabel('σ(x)', fontsize=13)
ax1.set_title('Sigmoid  σ(x) = 1/(1+e⁻ᵏˣ)', fontsize=14, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=11, loc='upper left')
ax1.grid(True, alpha=0.25)
ax1.set_ylim(-0.05, 1.05)

# ── Panel 2: Softmax temperature scaling ─────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
logits = np.array([2.0, 1.0, 0.1])
temps = [0.5, 1, 2, 5]
class_labels = ['Class A', 'Class B', 'Class C']
x_pos = np.arange(len(logits))
bar_width = 0.18
t_colors = [COLORS['e_purple'], COLORS['e_blue'], COLORS['e_green'], COLORS['e_pink']]

for i, (T, color) in enumerate(zip(temps, t_colors)):
    shifted = logits - np.max(logits)
    exp_vals = np.exp(shifted / T)
    probs = exp_vals / exp_vals.sum()
    offset = (i - 1.5) * bar_width
    bars = ax2.bar(x_pos + offset, probs, bar_width, color=color, alpha=0.85,
                   label=f'T = {T}', edgecolor=COLORS['bg_dark'], linewidth=0.5)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(class_labels, fontsize=11)
ax2.set_ylabel('Softmax Probability', fontsize=13)
ax2.set_title('Softmax Temperature Scaling\nlogits = [2, 1, 0.1]', fontsize=14,
              color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25, axis='y')
ax2.set_ylim(0, 1.0)

# ── Panel 3: Cross-entropy loss ───────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
eps = 1e-7
p = np.linspace(eps, 1 - eps, 500)

loss_y1 = -np.log(p)         # y=1: penalises low predicted probability
loss_y0 = -np.log(1 - p)    # y=0: penalises high predicted probability

ax3.plot(p, loss_y1, color=COLORS['e_cyan'], lw=2.2, label='-log(p)  [y=1]')
ax3.plot(p, loss_y0, color=COLORS['e_orange'], lw=2.2, label='-log(1-p)  [y=0]')
ax3.axvline(0.5, color=COLORS['grid'], lw=1, ls='--', alpha=0.7)
ax3.fill_between(p, loss_y1, alpha=0.08, color=COLORS['e_cyan'])
ax3.fill_between(p, loss_y0, alpha=0.08, color=COLORS['e_orange'])
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 5)
ax3.set_xlabel('Predicted probability  p̂', fontsize=13)
ax3.set_ylabel('Loss', fontsize=13)
ax3.set_title('Cross-Entropy Loss\nL = -[y·log(p̂) + (1-y)·log(1-p̂)]',
              fontsize=14, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=11)
ax3.grid(True, alpha=0.25)

fig.suptitle('Sigmoid · Softmax · Cross-Entropy  —  Building Blocks of Deep Learning',
             fontsize=16, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'sigmoid_softmax_ce', OUTPUT_DIR)
plt.close(fig)
