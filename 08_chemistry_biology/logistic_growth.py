"""
logistic_growth.py — Logistic population growth

P(t) = K / (1 + ((K − P₀) / P₀) · e^(−r·t))

Compares exponential vs logistic growth and shows multiple initial
conditions all converging to the carrying capacity K.
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

K = 1000.0    # carrying capacity
r = 0.3       # intrinsic growth rate
P0_DEFAULT = 10.0

INITIAL_CONDITIONS = [5, 20, 100, 500, 950]
IC_COLORS = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'],
             COLORS['e_pink'], COLORS['e_orange']]


def logistic(t, P0, r, K):
    b = (K - P0) / P0
    return K / (1 + b * np.exp(-r * t))


def exponential(t, P0, r):
    return P0 * np.exp(r * t)


def main():
    apply_euler_style()

    t = np.linspace(0, 30, 1000)

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ── Left: Exponential vs Logistic for default P0 ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    P_logistic = logistic(t, P0_DEFAULT, r, K)
    P_exp      = exponential(t, P0_DEFAULT, r)

    ax1.plot(t, P_logistic, color=COLORS['e_gold'],  lw=3, label='Logistic growth')
    ax1.plot(t, P_exp,      color=COLORS['e_red'],   lw=2, ls='--', alpha=0.8,
             label='Exponential growth (unbounded)')
    ax1.axhline(K,     color=COLORS['e_cyan'], ls='--', lw=1.8, alpha=0.8,
                label=f'Carrying capacity K = {K}')
    ax1.axhline(K / 2, color=COLORS['text'], ls=':', lw=1, alpha=0.5,
                label='K/2 (inflection point)')

    # Inflection point at P = K/2
    t_infl = math.log((K - P0_DEFAULT) / P0_DEFAULT) / r
    ax1.plot(t_infl, K / 2, 'o', color=COLORS['e_pink'], ms=10, zorder=6)
    ax1.annotate(f'Inflection\nt = {t_infl:.1f}',
                 xy=(t_infl, K / 2),
                 xytext=(t_infl + 2.5, K / 2 - 120),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_pink'], lw=1.5),
                 color=COLORS['e_pink'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.text(0.97, 0.45,
             r'$P(t) = \dfrac{K}{1 + \frac{K-P_0}{P_0}\,e^{-rt}}$',
             transform=ax1.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Time', color=COLORS['text'])
    ax1.set_ylabel('Population', color=COLORS['text'])
    ax1.set_title(f'Exponential vs Logistic  (P₀ = {P0_DEFAULT}, r = {r})',
                  color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, 30)
    ax1.set_ylim(-50, K * 2.2)

    # ── Right: Multiple initial conditions ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    for P0_ic, color in zip(INITIAL_CONDITIONS, IC_COLORS):
        P = logistic(t, P0_ic, r, K)
        ax2.plot(t, P, color=color, lw=2.5, label=f'P₀ = {P0_ic}')

    ax2.axhline(K, color=COLORS['text'], ls='--', lw=2, alpha=0.7,
                label=f'K = {K}  (equilibrium)')

    ax2.text(0.03, 0.97,
             f'All initial conditions\nconverge to K = {K}',
             transform=ax2.transAxes, fontsize=10,
             color=COLORS['e_cyan'], ha='left', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Time', color=COLORS['text'])
    ax2.set_ylabel('Population', color=COLORS['text'])
    ax2.set_title('Multiple Initial Conditions  (r = {})'.format(r), color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_xlim(0, 30)
    ax2.set_ylim(-30, K * 1.1)

    fig.suptitle('Logistic Growth  —  $P(t) = K / (1 + \\frac{K-P_0}{P_0}\\,e^{-rt})$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'logistic_growth', out_dir)
    plt.close(fig)
    print("Done: logistic_growth")


if __name__ == '__main__':
    main()
