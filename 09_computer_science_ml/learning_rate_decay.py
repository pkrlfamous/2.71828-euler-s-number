"""
Learning rate decay: lr(t) = lr₀ · e^(-λt)
Compares exponential decay, step decay, cosine annealing, and constant lr.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

epochs = np.arange(0, 100)
lr0 = 0.1
lam = 0.04  # exponential decay rate

# Schedule definitions
lr_constant    = np.full_like(epochs, lr0, dtype=float)
lr_exponential = lr0 * np.exp(-lam * epochs)
lr_step        = np.array([lr0 * (0.5 ** (e // 20)) for e in epochs])
lr_cosine      = 0.5 * lr0 * (1 + np.cos(np.pi * epochs / epochs[-1]))

np.random.seed(42)


def simulate_loss(lr_schedule, base_loss=2.5, noise_scale=0.06):
    """Simulate a training loss curve driven by the given lr schedule."""
    loss = [base_loss]
    vel  = 0.0
    momentum = 0.85
    for i, lr in enumerate(lr_schedule[:-1]):
        grad = (loss[-1] - 0.05) * (0.8 + 0.2 * np.random.rand())
        vel  = momentum * vel + lr * grad
        new_loss = loss[-1] - vel + noise_scale * np.random.randn()
        loss.append(max(new_loss, 0.04))
    return np.array(loss)


loss_constant    = simulate_loss(lr_constant,    noise_scale=0.10)
loss_exponential = simulate_loss(lr_exponential, noise_scale=0.04)
loss_step        = simulate_loss(lr_step,        noise_scale=0.05)
loss_cosine      = simulate_loss(lr_cosine,      noise_scale=0.04)

fig = plt.figure(figsize=(16, 7))
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

# ── Panel 1: Learning rate schedules ─────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

ax1.plot(epochs, lr_constant,    color=COLORS['e_red'],    lw=2.2, ls='--',
         label='Constant  lr₀=0.1')
ax1.plot(epochs, lr_exponential, color=COLORS['e_gold'],   lw=2.5,
         label=f'Exponential  lr₀·e⁻λᵗ (λ={lam})')
ax1.plot(epochs, lr_step,        color=COLORS['e_cyan'],   lw=2.2, ls='-.',
         label='Step decay  ×0.5 / 20 epochs')
ax1.plot(epochs, lr_cosine,      color=COLORS['e_purple'], lw=2.2, ls=':',
         label='Cosine annealing')

# shade under exponential curve
ax1.fill_between(epochs, lr_exponential, alpha=0.12, color=COLORS['e_gold'])

ax1.set_xlabel('Epoch', fontsize=13)
ax1.set_ylabel('Learning Rate', fontsize=13)
ax1.set_title('Learning Rate Schedules\nlr(t) = lr₀·e⁻λᵗ  and alternatives',
              fontsize=14, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.25)

# ── Panel 2: Simulated loss curves ────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])

ax2.plot(epochs, loss_constant,    color=COLORS['e_red'],    lw=2.0, ls='--',
         label='Constant', alpha=0.9)
ax2.plot(epochs, loss_exponential, color=COLORS['e_gold'],   lw=2.5,
         label='Exponential decay', alpha=0.9)
ax2.plot(epochs, loss_step,        color=COLORS['e_cyan'],   lw=2.0, ls='-.',
         label='Step decay', alpha=0.9)
ax2.plot(epochs, loss_cosine,      color=COLORS['e_purple'], lw=2.0, ls=':',
         label='Cosine annealing', alpha=0.9)

ax2.set_xlabel('Epoch', fontsize=13)
ax2.set_ylabel('Training Loss (simulated)', fontsize=13)
ax2.set_title('Effect on Training Convergence\n(Simulated Loss Curves)',
              fontsize=14, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)
ax2.set_ylim(bottom=0)

fig.suptitle('Learning Rate Decay  lr(t) = lr₀·e⁻λᵗ  —  Taming the Optimiser',
             fontsize=15, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'learning_rate_decay', OUTPUT_DIR)
plt.close(fig)
