"""
Neural network initialization: He/Xavier.
Simulates forward pass through 10 layers with too-large, too-small, and He init.
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

np.random.seed(0)

N_LAYERS = 10
N_NEURONS = 256
N_SAMPLES = 1024


def forward_pass(sigma_init, activation='relu'):
    """Run a forward pass and return activations at each layer."""
    x = np.random.randn(N_SAMPLES, N_NEURONS)
    layer_acts = [x.copy()]
    for _ in range(N_LAYERS):
        W = np.random.normal(0, sigma_init, (N_NEURONS, N_NEURONS))
        x = x @ W
        if activation == 'relu':
            x = np.maximum(0, x)
        elif activation == 'tanh':
            x = np.tanh(x)
        layer_acts.append(x.copy())
    return layer_acts


n_in = N_NEURONS
sigma_he      = np.sqrt(2.0 / n_in)    # He init for ReLU
sigma_xavier  = np.sqrt(1.0 / n_in)    # Xavier init for tanh
sigma_large   = 2.0                    # too large → exploding
sigma_small   = 0.01                   # too small  → vanishing

configs = [
    ('Too Large  σ=2.0\n(Exploding)', sigma_large,  'relu', COLORS['e_red']),
    ('Too Small  σ=0.01\n(Vanishing)', sigma_small, 'relu', COLORS['e_orange']),
    ('He Init  σ=√(2/n)\n(Healthy ReLU)', sigma_he,  'relu', COLORS['e_green']),
]

fig = plt.figure(figsize=(18, 10))
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.50, wspace=0.40)

for col, (label, sigma, act_fn, color) in enumerate(configs):
    acts = forward_pass(sigma, activation=act_fn)

    # ── Top row: std of activations across layers ─────────────────────────────
    ax_top = fig.add_subplot(gs[0, col])
    stds  = [np.std(a) for a in acts]
    means = [np.mean(a) for a in acts]

    ax_top.plot(range(N_LAYERS + 1), stds,  color=color,             lw=2.5,
                marker='o', ms=5, label='std')
    ax_top.plot(range(N_LAYERS + 1), means, color=COLORS['e_purple'], lw=1.8,
                marker='s', ms=4, ls='--', label='mean')
    ax_top.set_yscale('symlog', linthresh=1e-10)
    ax_top.set_xlabel('Layer', fontsize=11)
    ax_top.set_ylabel('Value', fontsize=11)
    ax_top.set_title(label, fontsize=12, color=color, pad=8)
    ax_top.legend(fontsize=9)
    ax_top.grid(True, alpha=0.25)

    # ── Bottom row: histogram at layers 0, 3, 6, 9 ───────────────────────────
    ax_bot = fig.add_subplot(gs[1, col])
    layer_indices = [0, 3, 6, N_LAYERS]
    hist_colors = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_orange'], color]
    ls_cycle = ['-', '--', ':', '-.']

    for li, hc, ls in zip(layer_indices, hist_colors, ls_cycle):
        flat = acts[li].flatten()
        clip_val = np.percentile(np.abs(flat), 99.5)
        flat_clipped = np.clip(flat, -clip_val, clip_val)
        if clip_val == 0 or np.std(flat_clipped) == 0:
            ax_bot.axvline(0, color=hc, lw=2, ls=ls, label=f'Layer {li} (collapsed)')
            continue
        counts, bins = np.histogram(flat_clipped, bins=60, density=True)
        centers = 0.5 * (bins[:-1] + bins[1:])
        ax_bot.plot(centers, counts, color=hc, lw=1.8, ls=ls, label=f'Layer {li}')

    ax_bot.set_xlabel('Activation value', fontsize=11)
    ax_bot.set_ylabel('Density', fontsize=11)
    ax_bot.set_title(f'Activation Distributions\n{label.split(chr(10))[0]}',
                     fontsize=12, color=color, pad=8)
    ax_bot.legend(fontsize=9)
    ax_bot.grid(True, alpha=0.25)

fig.suptitle('Neural Network Initialization  He σ=√(2/n)  —  Preventing Gradient Pathologies',
             fontsize=15, color=COLORS['e_gold'], y=1.01, fontweight='bold')

save_plot(fig, 'neural_network_init', OUTPUT_DIR)
plt.close(fig)
