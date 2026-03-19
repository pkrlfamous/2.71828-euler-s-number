"""
Gradient descent on an exponential loss surface.
Shows 2-D loss landscape with exponential terms and paths for different learning rates.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

# Loss surface: L(w1,w2) = e^(w1²/4) + e^(w2²/2) - 1.5·e^(-w1²/8 - w2²/8)
def loss(w1, w2):
    return np.exp(w1**2 / 4) + np.exp(w2**2 / 2) - 1.5 * np.exp(-w1**2 / 8 - w2**2 / 8)


def grad_loss(w1, w2):
    dw1 = (w1 / 2) * np.exp(w1**2 / 4) + (w1 / 4) * 1.5 * np.exp(-w1**2 / 8 - w2**2 / 8)
    dw2 = w2 * np.exp(w2**2 / 2)        + (w2 / 4) * 1.5 * np.exp(-w1**2 / 8 - w2**2 / 8)
    return dw1, dw2


def run_gd(w1_init, w2_init, lr, steps=60):
    path = [(w1_init, w2_init)]
    w1, w2 = w1_init, w2_init
    for _ in range(steps):
        g1, g2 = grad_loss(w1, w2)
        w1 -= lr * g1
        w2 -= lr * g2
        # clip to plot region
        w1 = np.clip(w1, -3.5, 3.5)
        w2 = np.clip(w2, -3.5, 3.5)
        path.append((w1, w2))
    return np.array(path)


grid_w = np.linspace(-3.5, 3.5, 400)
W1, W2 = np.meshgrid(grid_w, grid_w)
Z = loss(W1, W2)

lrs         = [0.02, 0.08, 0.25, 0.55]
lr_colors   = [COLORS['e_green'], COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_red']]
w1_start, w2_start = -3.0, 3.0

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.38)

# ── Panel 1: Contour plot with GD paths ──────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
levels = np.geomspace(Z.min() + 0.01, Z.max(), 25)
cf = ax1.contourf(W1, W2, Z, levels=levels, cmap='inferno', alpha=0.75, norm=LogNorm())
ax1.contour(W1, W2, Z, levels=levels, colors='white', alpha=0.12, linewidths=0.5)
plt.colorbar(cf, ax=ax1, label='Loss', fraction=0.046, pad=0.04)

for lr, color in zip(lrs, lr_colors):
    path = run_gd(w1_start, w2_start, lr)
    ax1.plot(path[:, 0], path[:, 1], color=color, lw=2.0, label=f'lr={lr}')
    ax1.scatter(path[-1, 0], path[-1, 1], color=color, s=80, zorder=6, marker='*')

ax1.scatter(w1_start, w2_start, color=COLORS['text'], s=120, zorder=7,
            marker='o', edgecolors=COLORS['bg_dark'], lw=1.5, label='Start')

ax1.set_xlabel('w₁', fontsize=12)
ax1.set_ylabel('w₂', fontsize=12)
ax1.set_title('Loss Landscape & GD Paths\nL = eʷ¹²/⁴ + eʷ²²/² − 1.5·e⁻(ʷ¹²+ʷ²²)/⁸',
              fontsize=12, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=9, loc='lower right')
ax1.set_xlim(-3.5, 3.5)
ax1.set_ylim(-3.5, 3.5)

# ── Panel 2: Loss vs iteration ────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
for lr, color in zip(lrs, lr_colors):
    path = run_gd(w1_start, w2_start, lr)
    losses = [loss(p[0], p[1]) for p in path]
    ax2.plot(losses, color=color, lw=2.2, label=f'lr={lr}')

ax2.set_xlabel('Iteration', fontsize=12)
ax2.set_ylabel('Loss (log scale)', fontsize=12)
ax2.set_yscale('log')
ax2.set_title('Convergence Speed\nDifferent Learning Rates',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)

# ── Panel 3: 1-D slice of the loss surface ────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
w_1d = np.linspace(-3.5, 3.5, 400)
loss_1d = loss(w_1d, 0.0)
grad_1d = np.array([grad_loss(w, 0.0)[0] for w in w_1d])

ax3.plot(w_1d, loss_1d,  color=COLORS['e_gold'], lw=2.5, label='L(w₁, w₂=0)')
ax3_twin = ax3.twinx()
ax3_twin.plot(w_1d, grad_1d, color=COLORS['e_cyan'], lw=2.0, ls='--',
              label='∂L/∂w₁')
ax3_twin.axhline(0, color=COLORS['grid'], lw=1, ls=':')
ax3_twin.set_ylabel('Gradient ∂L/∂w₁', color=COLORS['e_cyan'], fontsize=11)
ax3_twin.tick_params(colors=COLORS['e_cyan'])

# Mark minimum
min_idx = np.argmin(loss_1d)
ax3.scatter(w_1d[min_idx], loss_1d[min_idx], color=COLORS['e_green'], s=120,
            zorder=5, label=f'Minimum @ w₁={w_1d[min_idx]:.2f}')

ax3.set_xlabel('w₁  (w₂ fixed at 0)', fontsize=12)
ax3.set_ylabel('Loss L', fontsize=12)
ax3.set_title('1-D Slice of Loss Surface\nLoss and Gradient',
              fontsize=13, color=COLORS['e_gold'], pad=10)
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, fontsize=9)
ax3.grid(True, alpha=0.25)

fig.suptitle('Gradient Descent on an Exponential Loss Surface  —  Learning via eˣ',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'gradient_descent_viz', OUTPUT_DIR)
plt.close(fig)
