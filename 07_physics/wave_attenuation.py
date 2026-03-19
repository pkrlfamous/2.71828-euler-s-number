"""
wave_attenuation.py — Wave propagation with exponential amplitude decay

A(x) = A₀ · e^(−α·x) · cos(k·x)

Shows the attenuated wave alongside its exponential envelope,
and compares several attenuation coefficients α.
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

A0  = 1.0           # initial amplitude
k_wave = 2 * np.pi  # wavenumber (1 cycle per unit length)

ALPHA_VALUES = [0.2, 0.5, 1.0, 2.0]
ALPHA_COLORS = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink']]


def attenuated_wave(x, alpha):
    return A0 * np.exp(-alpha * x) * np.cos(k_wave * x)


def envelope(x, alpha):
    return A0 * np.exp(-alpha * x)


def main():
    apply_euler_style()

    x = np.linspace(0, 6, 3000)

    fig = plt.figure(figsize=(15, 9))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.35, hspace=0.48)

    # ── Top row: individual α panels ──
    for idx, (alpha, color) in enumerate(zip(ALPHA_VALUES[:2], ALPHA_COLORS[:2])):
        ax = fig.add_subplot(gs[0, idx])
        ax.set_facecolor(COLORS['bg_card'])
        wave = attenuated_wave(x, alpha)
        env  = envelope(x, alpha)
        ax.plot(x, wave, color=color, lw=2, label=f'α = {alpha}')
        ax.plot(x,  env, color=COLORS['e_gold'], lw=1.5, ls='--', alpha=0.85, label='Envelope')
        ax.plot(x, -env, color=COLORS['e_gold'], lw=1.5, ls='--', alpha=0.85)
        ax.fill_between(x, -env, env, color=COLORS['e_gold'], alpha=0.06)
        ax.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
        ax.set_title(f'Attenuation  α = {alpha}', color=COLORS['text'], pad=8)
        ax.set_xlabel('Distance x', color=COLORS['text'])
        ax.set_ylabel('Amplitude', color=COLORS['text'])
        ax.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
        ax.grid(True, alpha=0.3, color=COLORS['grid'])
        ax.set_ylim(-1.15, 1.15)

    # ── Bottom-left: all α overlaid ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])
    for alpha, color in zip(ALPHA_VALUES, ALPHA_COLORS):
        wave = attenuated_wave(x, alpha)
        ax3.plot(x, wave, color=color, lw=2, alpha=0.9, label=f'α = {alpha}')
    ax3.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax3.set_title('All Attenuation Coefficients', color=COLORS['text'], pad=8)
    ax3.set_xlabel('Distance x', color=COLORS['text'])
    ax3.set_ylabel('Amplitude', color=COLORS['text'])
    ax3.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Bottom-right: envelopes only on semi-log ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])
    for alpha, color in zip(ALPHA_VALUES, ALPHA_COLORS):
        env = envelope(x, alpha)
        ax4.semilogy(x, env, color=color, lw=2.5, label=f'α = {alpha}')

    ax4.text(0.97, 0.97,
             r'$A(x) = A_0 \cdot e^{-\alpha x} \cdot \cos(kx)$',
             transform=ax4.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax4.set_title('Decay Envelope  (semi-log)', color=COLORS['text'], pad=8)
    ax4.set_xlabel('Distance x', color=COLORS['text'])
    ax4.set_ylabel('Envelope amplitude (log scale)', color=COLORS['text'])
    ax4.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax4.grid(True, alpha=0.3, which='both', color=COLORS['grid'])

    fig.suptitle('Wave Attenuation  —  $A(x) = A_0\\, e^{-\\alpha x} \\cos(kx)$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'wave_attenuation', out_dir)
    plt.close(fig)
    print("Done: wave_attenuation")


if __name__ == '__main__':
    main()
