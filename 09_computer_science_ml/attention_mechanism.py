"""
Attention mechanism: Attention = softmax(QKᵀ/√d) · V
Visualises attention weights, scaling effect, and saturation comparison.
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

np.random.seed(7)

tokens = ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy']
seq_len = len(tokens)
d_model = 64

Q = np.random.randn(seq_len, d_model)
K = np.random.randn(seq_len, d_model)
V = np.random.randn(seq_len, d_model)


def softmax_2d(x):
    """Row-wise softmax."""
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)


scores_unscaled = Q @ K.T
scores_scaled   = scores_unscaled / np.sqrt(d_model)

attn_unscaled = softmax_2d(scores_unscaled)
attn_scaled   = softmax_2d(scores_scaled)

fig = plt.figure(figsize=(18, 6))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.45)

# ── Panel 1: Scaled attention heatmap ─────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
im1 = ax1.imshow(attn_scaled, cmap='magma', aspect='auto', vmin=0, vmax=attn_scaled.max())
ax1.set_xticks(range(seq_len))
ax1.set_yticks(range(seq_len))
ax1.set_xticklabels(tokens, rotation=40, ha='right', fontsize=9)
ax1.set_yticklabels(tokens, fontsize=9)
ax1.set_title('Scaled Attention Weights\nsoftmax(QKᵀ/√d)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
cbar1.set_label('Attention weight', fontsize=9)

# Annotate cells with values
for i in range(seq_len):
    for j in range(seq_len):
        val = attn_scaled[i, j]
        ax1.text(j, i, f'{val:.2f}', ha='center', va='center',
                 fontsize=6.5, color='white' if val < 0.15 else 'black')

# ── Panel 2: Unscaled vs scaled — softmax saturation ─────────────────────────
ax2 = fig.add_subplot(gs[1])

dims = [1, 4, 16, 64, 256]
entropy_unscaled, entropy_scaled = [], []

for d in dims:
    q = np.random.randn(1, d)
    k = np.random.randn(seq_len, d)
    raw = (q @ k.T).flatten()
    scaled = raw / np.sqrt(d)
    p_raw    = softmax_2d(raw.reshape(1, -1)).flatten()
    p_scaled = softmax_2d(scaled.reshape(1, -1)).flatten()
    # entropy as measure of spread (higher = less saturated)
    entropy_unscaled.append(-np.sum(p_raw    * np.log(p_raw    + 1e-9)))
    entropy_scaled.append(  -np.sum(p_scaled * np.log(p_scaled + 1e-9)))

ax2.plot(dims, entropy_unscaled, color=COLORS['e_red'], lw=2.5, marker='o', ms=7,
         label='Unscaled QKᵀ')
ax2.plot(dims, entropy_scaled,   color=COLORS['e_green'], lw=2.5, marker='s', ms=7,
         label='Scaled QKᵀ/√d')
ax2.set_xscale('log')
ax2.set_xlabel('Embedding dimension d', fontsize=12)
ax2.set_ylabel('Attention Entropy  H(attn)', fontsize=12)
ax2.set_title('Softmax Saturation vs Dimension\nHigher entropy = less peaked',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.25)

# ── Panel 3: Attended output per query token ──────────────────────────────────
ax3 = fig.add_subplot(gs[2])

output = attn_scaled @ V   # (seq_len, d_model)
# Project to 2D for visualisation using first two principal components
U, S, Vt = np.linalg.svd(output, full_matrices=False)
proj = output @ Vt[:2].T   # (seq_len, 2)

scatter = ax3.scatter(proj[:, 0], proj[:, 1],
                      c=range(seq_len),
                      cmap='plasma', s=180, zorder=5, edgecolors=COLORS['bg_dark'], lw=1.5)

for i, token in enumerate(tokens):
    ax3.annotate(token, (proj[i, 0], proj[i, 1]),
                 textcoords='offset points', xytext=(8, 4),
                 fontsize=9, color=COLORS['text'])

# Draw arrows showing attention-weighted flow from 'fox' (index 3)
query_idx = 3
for j in range(seq_len):
    if j == query_idx:
        continue
    weight = attn_scaled[query_idx, j]
    ax3.annotate('', xy=(proj[j, 0], proj[j, 1]),
                 xytext=(proj[query_idx, 0], proj[query_idx, 1]),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'],
                                 lw=weight * 5, alpha=weight * 3))

ax3.set_xlabel('PC 1', fontsize=12)
ax3.set_ylabel('PC 2', fontsize=12)
ax3.set_title('Attended Output (PCA)\nArrows from "fox" weighted by attention',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.grid(True, alpha=0.25)
cbar3 = plt.colorbar(scatter, ax=ax3, fraction=0.046, pad=0.04)
cbar3.set_label('Token position', fontsize=9)

fig.suptitle('Attention = softmax(QKᵀ/√d)·V  —  Where e Powers Transformers',
             fontsize=15, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'attention_mechanism', OUTPUT_DIR)
plt.close(fig)
