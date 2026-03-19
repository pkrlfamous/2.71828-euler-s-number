"""
radioactive_decay.py — Radioactive decay: N(t) = N₀·e^(-λt)

Plots decay curves for C-14, U-238, and Ra-226 with half-life markers.
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

# Physical constants
HALF_LIVES = {
    'C-14':  5730,           # years
    'Ra-226': 1600,          # years
    'Cs-137': 30.17,         # years
}

LAMBDAS = {iso: math.log(2) / t12 for iso, t12 in HALF_LIVES.items()}

ISO_COLORS = {
    'C-14':   COLORS['e_gold'],
    'Ra-226': COLORS['e_cyan'],
    'Cs-137': COLORS['e_pink'],
}


def decay(t, lam):
    return np.exp(-lam * t)


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ── Left: C-14 and Ra-226 on a common normalized time axis ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    # Use "number of half-lives" as x-axis so all isotopes align
    half_life_units = np.linspace(0, 6, 600)

    for iso, color in ISO_COLORS.items():
        N = decay(half_life_units, math.log(2))   # N vs t/t½  →  e^{-ln2 · n}
        ax1.plot(half_life_units, N * 100, color=color, lw=2.5, label=iso)

    # Mark half-life positions
    for n in range(1, 7):
        frac = (0.5 ** n) * 100
        ax1.axvline(n, color=COLORS['grid'], ls=':', lw=1, alpha=0.6)
        ax1.text(n + 0.05, 95, f'$n={n}$', color=COLORS['text'], fontsize=8, alpha=0.7)

    ax1.axhline(50, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.8, label='50% remaining')
    ax1.set_xlabel('Number of Half-Lives', color=COLORS['text'])
    ax1.set_ylabel('Remaining Amount (%)', color=COLORS['text'])
    ax1.set_title('Decay in Half-Life Units\n(Universal Curve)', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 105)

    # ── Right: C-14 and Ra-226 on actual year timescale ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    # C-14 — 0 to 30 000 years
    t_c14 = np.linspace(0, 30000, 1000)
    N_c14 = decay(t_c14, LAMBDAS['C-14']) * 100
    ax2.plot(t_c14, N_c14, color=COLORS['e_gold'], lw=2.5, label='C-14  (t½ = 5 730 yr)')
    # half-life markers for C-14
    for n in range(1, 6):
        t_mark = n * HALF_LIVES['C-14']
        if t_mark <= 30000:
            ax2.axvline(t_mark, color=COLORS['e_gold'], ls=':', lw=1, alpha=0.5)

    # Ra-226 — 0 to 10 000 years
    t_ra = np.linspace(0, 10000, 1000)
    N_ra = decay(t_ra, LAMBDAS['Ra-226']) * 100
    ax2.plot(t_ra, N_ra, color=COLORS['e_cyan'], lw=2.5, label='Ra-226  (t½ = 1 600 yr)')
    for n in range(1, 7):
        t_mark = n * HALF_LIVES['Ra-226']
        if t_mark <= 10000:
            ax2.axvline(t_mark, color=COLORS['e_cyan'], ls=':', lw=1, alpha=0.5)

    ax2.axhline(50, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.8, label='50% (half-life)')

    # Annotate formula
    ax2.text(0.97, 0.95,
             r'$N(t) = N_0 \cdot e^{-\lambda t}$' + '\n' +
             r'$\lambda = \ln 2 / t_{1/2}$',
             transform=ax2.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Time (years)', color=COLORS['text'])
    ax2.set_ylabel('Remaining Amount (%)', color=COLORS['text'])
    ax2.set_title('Actual Time Scale', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_ylim(0, 105)

    fig.suptitle('Radioactive Decay  —  $N(t) = N_0 \\cdot e^{-\\lambda t}$',
                 fontsize=18, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'radioactive_decay', out_dir)
    plt.close(fig)
    print("Done: radioactive_decay")


if __name__ == '__main__':
    main()
