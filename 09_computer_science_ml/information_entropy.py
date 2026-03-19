"""
Information entropy: H = -Σ p·ln(p)
Binary entropy, multi-distribution comparison, maximum at uniform distribution.
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


def entropy(p_vec):
    """Shannon entropy in nats (natural log)."""
    p_vec = np.asarray(p_vec, dtype=float)
    p_vec = p_vec[p_vec > 0]
    return -np.sum(p_vec * np.log(p_vec))


fig = plt.figure(figsize=(18, 6))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Binary entropy H(p) ─────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

eps = 1e-9
p_binary = np.linspace(eps, 1 - eps, 600)
H_binary  = -(p_binary * np.log(p_binary) + (1 - p_binary) * np.log(1 - p_binary))

ax1.plot(p_binary, H_binary, color=COLORS['e_gold'], lw=2.8)
ax1.fill_between(p_binary, H_binary, alpha=0.15, color=COLORS['e_gold'])

# Maximum at p=0.5
ax1.axvline(0.5, color=COLORS['e_cyan'], lw=1.5, ls='--', alpha=0.8)
ax1.scatter([0.5], [np.log(2)], color=COLORS['e_cyan'], s=100, zorder=5)
ax1.annotate(f'Maximum H = ln 2 ≈ {np.log(2):.3f} nat', xy=(0.5, np.log(2)),
             xytext=(0.58, 0.58),
             color=COLORS['e_cyan'], fontsize=10,
             arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.3))
ax1.annotate('Certain:\nH → 0', xy=(eps, 0), xytext=(0.04, 0.25),
             color=COLORS['text'], fontsize=9,
             arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=1))
ax1.annotate('Certain:\nH → 0', xy=(1 - eps, 0), xytext=(0.72, 0.25),
             color=COLORS['text'], fontsize=9,
             arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=1))

ax1.set_xlabel('Probability of outcome 1  (p)', fontsize=12)
ax1.set_ylabel('Entropy H(p)  [nats]', fontsize=12)
ax1.set_title('Binary Entropy\nH(p) = −p·ln p − (1−p)·ln(1−p)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.grid(True, alpha=0.25)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 0.8)

# ── Panel 2: Entropy of various distributions ─────────────────────────────────
ax2 = fig.add_subplot(gs[1])

n_classes = 6
x_pos = np.arange(n_classes)

distributions = {
    'Uniform':   np.ones(n_classes) / n_classes,
    'Peaked':    np.array([0.7, 0.1, 0.06, 0.06, 0.05, 0.03]),
    'Two peaks': np.array([0.4, 0.0, 0.4, 0.0, 0.1, 0.1]),
    'Certain':   np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
}
dist_colors = [COLORS['e_green'], COLORS['e_orange'], COLORS['e_cyan'], COLORS['e_red']]
bar_width = 0.18

for i, (label, dist) in enumerate(distributions.items()):
    H = entropy(dist)
    offset = (i - 1.5) * bar_width
    bars = ax2.bar(x_pos + offset, dist, bar_width, color=dist_colors[i],
                   alpha=0.85, label=f'{label}  H={H:.3f} nat',
                   edgecolor=COLORS['bg_dark'], linewidth=0.5)

ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'C{i+1}' for i in range(n_classes)])
ax2.set_ylabel('Probability', fontsize=12)
ax2.set_title('Entropy of Different Distributions\nHigher spread → Higher H',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.25, axis='y')

# ── Panel 3: Max entropy → uniform distribution ───────────────────────────────
ax3 = fig.add_subplot(gs[2])

n_classes_range = np.arange(2, 51)
H_max_uniform   = np.log(n_classes_range)          # H = ln(n) for uniform
H_max_theory    = np.log(n_classes_range)

# Show a non-uniform distribution's entropy vs n
# Peaked distribution: p1 = 0.6, rest share 0.4
H_peaked = []
for n in n_classes_range:
    p = np.array([0.6] + [0.4 / (n - 1)] * (n - 1))
    H_peaked.append(entropy(p))

ax3.plot(n_classes_range, H_max_uniform, color=COLORS['e_green'], lw=2.5,
         label='Uniform  H = ln n  (theoretical max)')
ax3.plot(n_classes_range, H_peaked,      color=COLORS['e_orange'], lw=2.2, ls='--',
         label='Peaked (p₁=0.6)')
ax3.fill_between(n_classes_range, H_peaked, H_max_uniform,
                 alpha=0.12, color=COLORS['e_green'], label='Entropy gap')

ax3.set_xlabel('Number of classes n', fontsize=12)
ax3.set_ylabel('Maximum Entropy  [nats]', fontsize=12)
ax3.set_title('Entropy Maximised by Uniform\nH_max = ln n',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)

fig.suptitle('Information Entropy  H = −Σ pᵢ·ln pᵢ  —  Uncertainty Measured in Nats',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'information_entropy', OUTPUT_DIR)
plt.close(fig)
