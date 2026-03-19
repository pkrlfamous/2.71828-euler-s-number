"""
Cross-entropy loss: L = -Σ y·ln(ŷ)
Shows loss surface, encouraging correct predictions, and CE vs MSE comparison.
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

eps = 1e-7
p = np.linspace(eps, 1 - eps, 500)

fig = plt.figure(figsize=(18, 6))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.40)

# ── Panel 1: CE loss surface ──────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

ce_y1 = -np.log(p)
ce_y0 = -np.log(1 - p)

ax1.plot(p, ce_y1, color=COLORS['e_cyan'], lw=2.5, label='y=1: −log(p̂)')
ax1.plot(p, ce_y0, color=COLORS['e_orange'], lw=2.5, label='y=0: −log(1−p̂)')
ax1.fill_between(p, ce_y1, alpha=0.10, color=COLORS['e_cyan'])
ax1.fill_between(p, ce_y0, alpha=0.10, color=COLORS['e_orange'])

# annotate perfect-prediction points
ax1.scatter([1.0], [0.0], color=COLORS['e_cyan'], s=80, zorder=5)
ax1.scatter([0.0], [0.0], color=COLORS['e_orange'], s=80, zorder=5)
ax1.annotate('Perfect (y=1)\nLoss → 0', xy=(1.0, 0), xytext=(0.7, 1.2),
             color=COLORS['e_cyan'], fontsize=9,
             arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.2))
ax1.annotate('Perfect (y=0)\nLoss → 0', xy=(0.0, 0), xytext=(0.12, 1.2),
             color=COLORS['e_orange'], fontsize=9,
             arrowprops=dict(arrowstyle='->', color=COLORS['e_orange'], lw=1.2))

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 4.5)
ax1.set_xlabel('Predicted probability  p̂', fontsize=12)
ax1.set_ylabel('Loss', fontsize=12)
ax1.set_title('Binary Cross-Entropy\nL = −[y·log(p̂) + (1−y)·log(1−p̂)]',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.25)

# ── Panel 2: How loss encourages correct predictions ──────────────────────────
ax2 = fig.add_subplot(gs[1])

pred_probs = np.linspace(eps, 1 - eps, 300)

# gradient magnitude: how strongly does loss push the prediction?
grad_y1 = -1 / pred_probs          # dL/dp for y=1
grad_y0 =  1 / (1 - pred_probs)    # dL/dp for y=0

ax2.plot(pred_probs, np.abs(grad_y1), color=COLORS['e_cyan'], lw=2.2,
         label='|∂L/∂p̂| when y=1')
ax2.plot(pred_probs, np.abs(grad_y0), color=COLORS['e_orange'], lw=2.2,
         label='|∂L/∂p̂| when y=0')
ax2.fill_between(pred_probs, np.abs(grad_y1), alpha=0.08, color=COLORS['e_cyan'])
ax2.fill_between(pred_probs, np.abs(grad_y0), alpha=0.08, color=COLORS['e_orange'])
ax2.axvline(0.5, color=COLORS['grid'], ls='--', alpha=0.7)

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 15)
ax2.set_xlabel('Predicted probability  p̂', fontsize=12)
ax2.set_ylabel('|Gradient|', fontsize=12)
ax2.set_title('Gradient Magnitude\nStrong Signal for Wrong Predictions',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.25)

# ── Panel 3: CE vs MSE comparison ────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])

# True label y = 1; p̂ is our prediction
ce_loss  = -np.log(p)                # CE loss
mse_loss = (1 - p) ** 2             # MSE loss (scaled)

# Normalise so they start at same point for fair visual comparison
ax3.plot(p, ce_loss / ce_loss[0], color=COLORS['e_gold'], lw=2.5,
         label='CE: −log(p̂)  [normalised]')
ax3.plot(p, mse_loss / mse_loss[0], color=COLORS['e_purple'], lw=2.5, ls='--',
         label='MSE: (1−p̂)²  [normalised]')

ax3.fill_between(p, ce_loss / ce_loss[0], mse_loss / mse_loss[0],
                 where=(ce_loss / ce_loss[0] > mse_loss / mse_loss[0]),
                 alpha=0.12, color=COLORS['e_gold'],
                 label='CE penalises wrong predictions more')

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1.05)
ax3.set_xlabel('Predicted probability  p̂  (true label y=1)', fontsize=12)
ax3.set_ylabel('Normalised Loss', fontsize=12)
ax3.set_title('CE vs MSE Loss\n(y=1, normalised to [0,1])',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)

fig.suptitle('Cross-Entropy Loss  L = −Σ yᵢ·ln(ŷᵢ)  —  Why Logarithms Drive Learning',
             fontsize=15, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'cross_entropy_loss', OUTPUT_DIR)
plt.close(fig)
