"""
Batch normalization and exponential moving averages.
μ_EMA = β·μ_EMA + (1-β)·μ_batch
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

np.random.seed(42)
n_steps = 200
batch_size = 32

# Simulate activations with drifting mean and variance
true_means = 3.0 * np.sin(np.linspace(0, 2 * np.pi, n_steps)) + 5.0
true_stds  = 2.0 + 0.5 * np.cos(np.linspace(0, 4 * np.pi, n_steps))

batch_means = true_means + 0.4 * np.random.randn(n_steps)
batch_stds  = true_stds  + 0.15 * np.abs(np.random.randn(n_steps))


def compute_ema(values, beta):
    ema = np.zeros_like(values)
    ema[0] = values[0]
    for t in range(1, len(values)):
        ema[t] = beta * ema[t - 1] + (1 - beta) * values[t]
    return ema


betas = [0.5, 0.9, 0.99]
ema_colors = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_pink']]

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.40)

# ── Panel 1: Raw vs normalised activations ────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

# Generate a batch of raw and BN-normalised activations
raw  = np.random.randn(512) * 4 + 6          # large mean, large variance
bn_scale, bn_shift = 2.0, 0.5
bn   = ((raw - raw.mean()) / (raw.std() + 1e-8)) * bn_scale + bn_shift

bins = np.linspace(-12, 18, 80)
ax1.hist(raw, bins=bins, color=COLORS['e_red'],   alpha=0.65, density=True,
         label=f'Raw  μ={raw.mean():.1f}, σ={raw.std():.1f}', edgecolor='none')
ax1.hist(bn,  bins=np.linspace(-8, 8, 80), color=COLORS['e_green'], alpha=0.65, density=True,
         label=f'After BN  μ={bn.mean():.2f}, σ={bn.std():.2f}', edgecolor='none')

ax1.axvline(raw.mean(), color=COLORS['e_red'],   lw=1.8, ls='--')
ax1.axvline(bn.mean(),  color=COLORS['e_green'], lw=1.8, ls='--')
ax1.set_xlabel('Activation value', fontsize=12)
ax1.set_ylabel('Density', fontsize=12)
ax1.set_title('Raw vs Batch-Normalised Activations\nBN re-centres and rescales',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.25)

# ── Panel 2: EMA tracking of batch mean ───────────────────────────────────────
ax2 = fig.add_subplot(gs[1])

t = np.arange(n_steps)
ax2.scatter(t, batch_means, color=COLORS['text'], s=4, alpha=0.4, label='Batch means')
ax2.plot(t, true_means, color=COLORS['e_orange'], lw=1.8, ls='--', alpha=0.7,
         label='True mean')

for beta, color in zip(betas, ema_colors):
    ema = compute_ema(batch_means, beta)
    ax2.plot(t, ema, color=color, lw=2.2, label=f'EMA β={beta}')

ax2.set_xlabel('Training step', fontsize=12)
ax2.set_ylabel('Mean', fontsize=12)
ax2.set_title('EMA of Batch Mean\nμ_EMA = β·μ_EMA + (1−β)·μ_batch',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)

# ── Panel 3: EMA lag and β effect ─────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])

# Show how quickly EMA responds to a step change
n_pts = 120
signal = np.zeros(n_pts)
signal[40:] = 1.0  # step change at t=40

ax3.plot(range(n_pts), signal, color=COLORS['e_orange'], lw=2.0, ls='--',
         label='True signal (step change)', alpha=0.8)

for beta, color in zip(betas, ema_colors):
    ema = compute_ema(signal, beta)
    half_life = np.log(0.5) / np.log(beta) if beta > 0 else 0
    ax3.plot(range(n_pts), ema, color=color, lw=2.2,
             label=f'β={beta}  half-life≈{half_life:.1f} steps')

ax3.axvline(40, color=COLORS['grid'], lw=1.2, ls=':', alpha=0.8)
ax3.set_xlabel('Step', fontsize=12)
ax3.set_ylabel('EMA value', fontsize=12)
ax3.set_title('EMA Response to Step Change\nHigher β = slower adaptation',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)

fig.suptitle('Batch Normalization & Exponential Moving Averages  —  Stable Training Dynamics',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'batch_norm', OUTPUT_DIR)
plt.close(fig)
