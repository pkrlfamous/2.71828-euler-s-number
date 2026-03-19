"""
Weight initialization distributions for neural networks.
He init σ=√(2/n), Xavier σ=√(1/n), and why they prevent vanishing/exploding gradients.
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
n_in = 512   # fan-in

sigma_he      = np.sqrt(2.0 / n_in)
sigma_xavier  = np.sqrt(1.0 / n_in)
sigma_too_large = 1.0
sigma_too_small = 0.001

x = np.linspace(-0.25, 0.25, 800)


def normal_pdf(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Initialization distributions ─────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

ax1.plot(x, normal_pdf(x, 0, sigma_he),       color=COLORS['e_green'],  lw=2.5,
         label=f'He init  σ=√(2/n) ≈ {sigma_he:.4f}')
ax1.plot(x, normal_pdf(x, 0, sigma_xavier),   color=COLORS['e_cyan'],   lw=2.5,
         label=f'Xavier  σ=√(1/n) ≈ {sigma_xavier:.4f}')
ax1.plot(x, normal_pdf(x, 0, sigma_too_large),color=COLORS['e_red'],    lw=2.2, ls='--',
         label=f'Too large  σ={sigma_too_large}')

x_small = np.linspace(-0.01, 0.01, 800)
ax1_twin = ax1.twinx()
ax1_twin.plot(x_small, normal_pdf(x_small, 0, sigma_too_small),
              color=COLORS['e_orange'], lw=2.2, ls=':',
              label=f'Too small  σ={sigma_too_small}')
ax1_twin.set_ylabel('pdf (too-small scale)', color=COLORS['e_orange'], fontsize=10)
ax1_twin.tick_params(colors=COLORS['e_orange'])

ax1.set_xlim(-0.25, 0.25)
ax1.set_xlabel('Weight value', fontsize=12)
ax1.set_ylabel('Probability Density', fontsize=12)
ax1.set_title('Weight Initialization Distributions\n(fan-in n = 512)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.25)

# ── Panel 2: Activation variance across layers ────────────────────────────────
ax2 = fig.add_subplot(gs[1])
n_layers = 20
n_neurons = 256
init_configs = {
    'Too large  σ=1':     sigma_too_large,
    'Too small σ=0.001':  sigma_too_small,
    'Xavier  σ=√(1/n)':   sigma_xavier,
    'He init σ=√(2/n)':   sigma_he,
}
init_colors = [COLORS['e_red'], COLORS['e_orange'], COLORS['e_cyan'], COLORS['e_green']]

for (label, sigma), color in zip(init_configs.items(), init_colors):
    layer_vars = []
    x_act = np.random.randn(n_neurons)
    for _ in range(n_layers):
        W = np.random.normal(0, sigma, (n_neurons, n_neurons))
        x_act = np.tanh(W @ x_act)
        layer_vars.append(np.var(x_act))
    ax2.plot(range(1, n_layers + 1), layer_vars, color=color, lw=2.2, label=label)

ax2.set_xlabel('Layer', fontsize=12)
ax2.set_ylabel('Activation Variance (log scale)', fontsize=12)
ax2.set_yscale('log')
ax2.set_title('Activation Variance Across Layers\n(tanh activations)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.25)

# ── Panel 3: Distribution shift per layer ─────────────────────────────────────
ax3 = fig.add_subplot(gs[2])

configs_to_show = [
    ('Too large', sigma_too_large, COLORS['e_red']),
    ('He init',   sigma_he,        COLORS['e_green']),
]
layer_indices = [0, 4, 9, 19]
style_cycle = ['-', '--', ':', '-.']

for label, sigma, color in configs_to_show:
    x_act = np.random.randn(512)
    history = [x_act.copy()]
    for _ in range(19):
        W = np.random.normal(0, sigma, (512, 512))
        x_act = np.tanh(W @ x_act)
        history.append(x_act.copy())

    bin_range = (-1.2, 1.2) if label == 'He init' else (-1.2, 1.2)
    for idx, ls in zip(layer_indices, style_cycle):
        counts, bins = np.histogram(history[idx], bins=60, range=bin_range, density=True)
        centers = 0.5 * (bins[:-1] + bins[1:])
        ax3.plot(centers, counts, color=color, lw=1.5, ls=ls,
                 label=f'{label} Layer {idx + 1}', alpha=0.85)

ax3.set_xlabel('Activation value', fontsize=12)
ax3.set_ylabel('Density', fontsize=12)
ax3.set_title('Activation Distributions\nToo-Large vs He Init',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=8, ncol=2)
ax3.grid(True, alpha=0.25)

fig.suptitle('Weight Initialization  He: σ=√(2/n)  Xavier: σ=√(1/n)  —  Preventing Gradient Pathologies',
             fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'normal_distribution_ml', OUTPUT_DIR)
plt.close(fig)
