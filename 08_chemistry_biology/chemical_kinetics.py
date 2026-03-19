"""
chemical_kinetics.py — First-order reaction kinetics

[A](t) = [A]₀ · e^(−k·t)

Plots concentration decay for different rate constants and marks
half-lives t₁/₂ = ln(2)/k.
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

A0 = 1.0   # initial concentration (normalised to 1)
K_VALUES = [0.1, 0.5, 1.0, 2.0]   # rate constants (s⁻¹)
K_COLORS = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink']]


def concentration(t, k):
    return A0 * np.exp(-k * t)


def half_life(k):
    return math.log(2) / k


def main():
    apply_euler_style()

    t_max = 30.0
    t = np.linspace(0, t_max, 1000)

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ── Left: linear concentration vs time ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for k, color in zip(K_VALUES, K_COLORS):
        C = concentration(t, k)
        t12 = half_life(k)
        ax1.plot(t, C, color=color, lw=2.5, label=f'k = {k} s⁻¹  (t½ = {t12:.2f} s)')
        # Mark the half-life point
        if t12 <= t_max:
            ax1.plot(t12, 0.5, 'o', color=color, ms=7, zorder=5)
            ax1.plot([t12, t12], [0, 0.5], color=color, ls=':', lw=1, alpha=0.6)

    ax1.axhline(0.5, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.7,
                label='50% concentration\n(half-life level)')

    ax1.text(0.97, 0.97,
             r'$[A](t) = [A]_0\, e^{-kt}$' + '\n' + r'$t_{1/2} = \ln 2 / k$',
             transform=ax1.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Time (s)', color=COLORS['text'])
    ax1.set_ylabel('[A] / [A]₀', color=COLORS['text'])
    ax1.set_title('First-Order Reaction Kinetics  (linear scale)', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, t_max)
    ax1.set_ylim(0, 1.05)

    # ── Right: log scale (should be straight lines) ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    for k, color in zip(K_VALUES, K_COLORS):
        C = concentration(t, k)
        ax2.semilogy(t, C, color=color, lw=2.5, label=f'k = {k} s⁻¹')

    ax2.axhline(0.5, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.7,
                label='50% level')

    ax2.text(0.97, 0.97,
             'Log-scale: straight lines\n' + r'confirm $e^{-kt}$ dependence',
             transform=ax2.transAxes, fontsize=10,
             color=COLORS['e_cyan'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Time (s)', color=COLORS['text'])
    ax2.set_ylabel('[A] / [A]₀  (log scale)', color=COLORS['text'])
    ax2.set_title('First-Order Kinetics  (log scale)', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax2.set_xlim(0, t_max)

    fig.suptitle('Chemical Kinetics  —  First-Order Decay  $[A](t) = [A]_0\\,e^{-kt}$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'chemical_kinetics', out_dir)
    plt.close(fig)
    print("Done: chemical_kinetics")


if __name__ == '__main__':
    main()
