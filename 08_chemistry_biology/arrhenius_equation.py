"""
arrhenius_equation.py — Arrhenius equation for reaction rate constants

k(T) = A · e^(−Ea / RT)

Left panel: Arrhenius plot — ln(k) vs 1/T  (should be linear)
Right panel: k vs T for several activation energies Ea
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

R = 8.314          # J mol⁻¹ K⁻¹ (gas constant)
A_PRE = 1e13       # pre-exponential factor (s⁻¹) — typical value

# Activation energies in J/mol
EA_VALUES = [20e3, 40e3, 60e3, 80e3, 100e3]   # 20–100 kJ/mol
EA_LABELS = ['20 kJ/mol', '40 kJ/mol', '60 kJ/mol', '80 kJ/mol', '100 kJ/mol']
EA_COLORS = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'],
             COLORS['e_pink'], COLORS['e_orange']]


def arrhenius(T, Ea, A=A_PRE):
    return A * np.exp(-Ea / (R * T))


def main():
    apply_euler_style()

    T_vals = np.linspace(200, 1200, 2000)      # K
    inv_T  = 1 / T_vals                        # 1/T

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.4)

    # ── Left: Arrhenius plot ln(k) vs 1/T ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for Ea, label, color in zip(EA_VALUES, EA_LABELS, EA_COLORS):
        k_vals = arrhenius(T_vals, Ea)
        ln_k   = np.log(k_vals)
        ax1.plot(inv_T * 1000, ln_k, color=color, lw=2.5, label=label)

    # Annotate slope = −Ea/R
    Ea_demo = 60e3
    slope = -Ea_demo / R
    ax1.text(0.97, 0.97,
             r'$\ln k = \ln A - \dfrac{E_a}{R} \cdot \dfrac{1}{T}$' + '\n\nSlope = −Eₐ/R',
             transform=ax1.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('1/T  (×10⁻³ K⁻¹)', color=COLORS['text'])
    ax1.set_ylabel('ln(k)', color=COLORS['text'])
    ax1.set_title('Arrhenius Plot  —  ln(k) vs 1/T', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9,
               title='Activation Energy', title_fontsize=8)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Right: k vs T ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    for Ea, label, color in zip(EA_VALUES, EA_LABELS, EA_COLORS):
        k_vals = arrhenius(T_vals, Ea)
        # Normalise by value at T=1200 K so curves are comparable
        k_norm = k_vals / arrhenius(1200, Ea)
        ax2.plot(T_vals, k_norm, color=color, lw=2.5, label=label)

    ax2.text(0.03, 0.97,
             r'$k(T) = A \cdot e^{-E_a/RT}$',
             transform=ax2.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='left', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.text(0.97, 0.15,
             'Higher Ea → reaction rate\nmore sensitive to temperature',
             transform=ax2.transAxes, fontsize=9,
             color=COLORS['e_cyan'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Temperature (K)', color=COLORS['text'])
    ax2.set_ylabel('Normalised k  (k / k_max)', color=COLORS['text'])
    ax2.set_title('Rate Constant vs Temperature', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9,
               title='Activation Energy', title_fontsize=8)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_xlim(200, 1200)

    fig.suptitle('Arrhenius Equation  —  $k = A\\,e^{-E_a/RT}$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'arrhenius_equation', out_dir)
    plt.close(fig)
    print("Done: arrhenius_equation")


if __name__ == '__main__':
    main()
