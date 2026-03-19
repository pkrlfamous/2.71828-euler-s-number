"""
Softmax function: softmax(xᵢ) = e^(xᵢ) / Σe^(xⱼ)
Shows logit-to-probability conversion and numerically stable implementation.
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


def softmax_naive(z):
    exp_z = np.exp(z)
    return exp_z / exp_z.sum()


def softmax_stable(z):
    z = np.array(z, dtype=float)
    shifted = z - z.max()
    exp_z = np.exp(shifted)
    return exp_z / exp_z.sum()


fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.40)

# ── Panel 1: Raw logits vs softmax probabilities ─────────────────────────────
ax1 = fig.add_subplot(gs[0])
logit_sets = {
    'Spread': [3.0, 1.0, -1.0, -3.0],
    'Peaked': [5.0, 0.5,  0.0, -1.0],
    'Flat':   [1.0, 1.0,  1.0,  1.0],
}
bar_width = 0.22
x_pos = np.arange(4)
palette = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_pink']]
class_names = ['C1', 'C2', 'C3', 'C4']

for i, (label, logits) in enumerate(logit_sets.items()):
    probs = softmax_stable(logits)
    offset = (i - 1) * bar_width
    ax1.bar(x_pos + offset, probs, bar_width, color=palette[i], alpha=0.85,
            label=label, edgecolor=COLORS['bg_dark'], linewidth=0.5)

ax1.set_xticks(x_pos)
ax1.set_xticklabels(class_names)
ax1.set_ylabel('Softmax Probability', fontsize=12)
ax1.set_title('3-Class Softmax\nDifferent Logit Vectors', fontsize=14,
              color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.25, axis='y')
ax1.set_ylim(0, 1.0)

# ── Panel 2: Numerical stability ─────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
offsets = np.linspace(0, 800, 60)
logits_base = np.array([3.0, 1.0, 0.2])

naive_results, stable_results = [], []
for shift in offsets:
    z_shifted = logits_base + shift
    try:
        with np.errstate(over='raise'):
            r = softmax_naive(z_shifted)
        naive_results.append(r[0])
    except FloatingPointError:
        naive_results.append(np.nan)
    stable_results.append(softmax_stable(z_shifted)[0])

ax2.plot(offsets, naive_results, color=COLORS['e_red'], lw=2.2,
         label='Naive (overflows)', ls='--')
ax2.plot(offsets, stable_results, color=COLORS['e_green'], lw=2.2,
         label='Stable (subtract max)')
ax2.axvline(709, color=COLORS['e_orange'], lw=1.2, ls=':', alpha=0.8,
            label='float64 overflow ≈ e⁷⁰⁹')
ax2.set_xlabel('Logit offset (added to all logits)', fontsize=12)
ax2.set_ylabel('Softmax(C1)', fontsize=12)
ax2.set_title('Numerical Stability\nNaive vs Subtract-Max', fontsize=14,
              color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)

# ── Panel 3: Softmax as "probability dial" ────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
# Vary the leading logit, keep others fixed, show class probabilities
lead_logit = np.linspace(-4, 8, 300)
rest = [0.0, 0.0]
colors_3class = [COLORS['e_cyan'], COLORS['e_orange'], COLORS['e_purple']]
class_labels_3 = ['Class 1 (variable)', 'Class 2 (fixed=0)', 'Class 3 (fixed=0)']
probs_3 = np.array([softmax_stable([l] + rest) for l in lead_logit])

for j, (col, lbl) in enumerate(zip(colors_3class, class_labels_3)):
    ax3.plot(lead_logit, probs_3[:, j], color=col, lw=2.2, label=lbl)

ax3.fill_between(lead_logit, probs_3[:, 0], alpha=0.12, color=COLORS['e_cyan'])
ax3.set_xlabel('Logit₁  (logits₂=logits₃=0)', fontsize=12)
ax3.set_ylabel('Softmax Probability', fontsize=12)
ax3.set_title('Softmax as Probability Dial\nVarying One Logit', fontsize=14,
              color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)
ax3.set_ylim(-0.02, 1.02)

fig.suptitle('Softmax  softmax(xᵢ) = eˣⁱ / Σeˣʲ  —  Converting Logits to Probabilities',
             fontsize=15, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'softmax_function', OUTPUT_DIR)
plt.close(fig)
