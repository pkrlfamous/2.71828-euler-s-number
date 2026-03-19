"""
dna_melting_curve.py — DNA thermal denaturation (melting) curve

Fraction denatured: F(T) = 1 / (1 + e^(−k·(T − Tm)))

Tm depends on GC content; higher GC → higher Tm.
Shows sigmoid melting curves for different GC percentages.
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

# Empirical formula: Tm ≈ 69.3 + 0.41·(%GC) for short oligos in 1M NaCl
def melting_temp(gc_pct):
    return 69.3 + 0.41 * gc_pct   # °C

K_STEEP = 0.5   # steepness of the sigmoid (°C⁻¹)

GC_VALUES  = [30, 45, 55, 65, 80]   # %GC content
GC_COLORS  = [COLORS['e_blue'], COLORS['e_cyan'], COLORS['e_green'],
              COLORS['e_gold'], COLORS['e_red']]


def melting_fraction(T, Tm, k=K_STEEP):
    """Logistic sigmoid centred at Tm."""
    return 1 / (1 + np.exp(-k * (T - Tm)))


def main():
    apply_euler_style()

    T = np.linspace(40, 110, 1000)   # °C

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.40)

    # ── Left: Melting curves ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for gc, color in zip(GC_VALUES, GC_COLORS):
        Tm = melting_temp(gc)
        F  = melting_fraction(T, Tm)
        ax1.plot(T, F * 100, color=color, lw=2.8, label=f'{gc}% GC  (Tm = {Tm:.1f}°C)')
        # Mark Tm (F = 50%)
        ax1.plot(Tm, 50, 'o', color=color, ms=8, zorder=5,
                 markeredgecolor=COLORS['text'], markeredgewidth=0.5)
        ax1.axvline(Tm, color=color, ls=':', lw=0.8, alpha=0.4)

    ax1.axhline(50, color=COLORS['text'], ls='--', lw=1.5, alpha=0.6,
                label='50% denatured (Tm)')

    ax1.text(0.97, 0.05,
             r'$F(T) = \dfrac{1}{1 + e^{-k(T - T_m)}}$',
             transform=ax1.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax1.set_xlabel('Temperature (°C)', color=COLORS['text'])
    ax1.set_ylabel('Fraction Denatured (%)', color=COLORS['text'])
    ax1.set_title('DNA Melting Curves by GC Content', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(40, 110)
    ax1.set_ylim(-3, 105)

    # ── Right: Tm vs GC content + effect of steepness k ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    # Panel A (top part): Tm vs %GC
    gc_range = np.linspace(20, 90, 200)
    Tm_range = melting_temp(gc_range)
    ax2.plot(gc_range, Tm_range, color=COLORS['e_gold'], lw=3,
             label='Tm = 69.3 + 0.41·%GC')
    for gc, color in zip(GC_VALUES, GC_COLORS):
        Tm = melting_temp(gc)
        ax2.plot(gc, Tm, 'o', color=color, ms=10, zorder=5,
                 markeredgecolor=COLORS['text'], markeredgewidth=0.5)
        ax2.text(gc + 1, Tm + 0.3, f'{gc}%', color=color, fontsize=8)

    ax2.set_xlabel('%GC Content', color=COLORS['text'])
    ax2.set_ylabel('Melting Temperature Tm (°C)', color=COLORS['text'])
    ax2.set_title('Tm vs GC Content\n(empirical: Tm = 69.3 + 0.41·%GC)', color=COLORS['text'], pad=8)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])

    # Inset: effect of k (sharpness) for Tm=80°C
    ax2_inset = ax2.inset_axes([0.55, 0.05, 0.42, 0.38])
    ax2_inset.set_facecolor(COLORS['bg_dark'])
    T_inset = np.linspace(65, 95, 500)
    Tm_fixed = 80
    k_values = [0.2, 0.5, 1.0, 2.0]
    k_colors = [COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink'], COLORS['e_orange']]
    for k_val, k_col in zip(k_values, k_colors):
        F_i = melting_fraction(T_inset, Tm_fixed, k_val)
        ax2_inset.plot(T_inset, F_i * 100, color=k_col, lw=2, label=f'k={k_val}')
    ax2_inset.axvline(Tm_fixed, color=COLORS['text'], ls=':', lw=1, alpha=0.5)
    ax2_inset.set_title('Steepness k  (Tm=80°C)', color=COLORS['text'], fontsize=8)
    ax2_inset.set_xlabel('T (°C)', color=COLORS['text'], fontsize=7)
    ax2_inset.set_ylabel('F (%)', color=COLORS['text'], fontsize=7)
    ax2_inset.tick_params(labelsize=6)
    ax2_inset.legend(fontsize=6, facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax2_inset.grid(True, alpha=0.3, color=COLORS['grid'])

    fig.suptitle('DNA Melting Curve  —  $F(T) = 1/(1 + e^{-k(T-T_m)})$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'dna_melting_curve', out_dir)
    plt.close(fig)
    print("Done: dna_melting_curve")


if __name__ == '__main__':
    main()
