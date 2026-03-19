"""
carbon_dating.py — Radiocarbon dating

N(t) = N₀ · e^(−t · ln2 / 5730)

Panels:
  1. C-14 decay curve
  2. "Carbon dating ruler": age from measured fraction
  3. Inverse problem: given fraction, find age
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

T_HALF = 5730.0                     # C-14 half-life (years)
LAMBDA = math.log(2) / T_HALF      # decay constant (yr⁻¹)


def fraction_remaining(t):
    """N(t)/N₀ = e^{−λt}."""
    return np.exp(-LAMBDA * t)


def age_from_fraction(f):
    """t = −ln(f) / λ."""
    f = np.clip(f, 1e-10, 1.0)
    return -np.log(f) / LAMBDA


def main():
    apply_euler_style()

    t = np.linspace(0, 50000, 2000)
    f = fraction_remaining(t)

    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.40, hspace=0.50)

    # ── Top-left: decay curve ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['bg_card'])
    ax1.plot(t / 1000, f * 100, color=COLORS['e_gold'], lw=3, label='C-14 remaining')

    # Mark half-lives
    for n in range(1, 9):
        t_hl = n * T_HALF
        if t_hl <= 50000:
            f_hl = fraction_remaining(t_hl) * 100
            ax1.plot(t_hl / 1000, f_hl, 'o', color=COLORS['e_cyan'], ms=7, zorder=5)
            ax1.axvline(t_hl / 1000, color=COLORS['e_cyan'], ls=':', lw=0.8, alpha=0.5)
            ax1.text(t_hl / 1000 + 0.4, f_hl + 1.5,
                     f'{n}×t½', color=COLORS['e_cyan'], fontsize=7.5)

    ax1.axhline(50, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.7,
                label='50% (t½ = 5 730 yr)')

    ax1.text(0.97, 0.97,
             r'$N(t) = N_0 \cdot e^{-\lambda t}$' + '\n' + r'$\lambda = \ln 2 / 5730$',
             transform=ax1.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Time (thousands of years)', color=COLORS['text'])
    ax1.set_ylabel('C-14 Remaining (%)', color=COLORS['text'])
    ax1.set_title('C-14 Radioactive Decay Curve', color=COLORS['text'], pad=8)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Top-right: Carbon dating ruler (fraction → age) ──
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['bg_card'])
    fractions = np.linspace(0.001, 1.0, 1000)
    ages = age_from_fraction(fractions)
    ax2.plot(fractions * 100, ages / 1000, color=COLORS['e_cyan'], lw=3,
             label=r'Age = $-\ln(f)/\lambda$')

    # Mark example measurements
    examples = [(0.75, 'f=75%'), (0.50, 'f=50%'), (0.25, 'f=25%'),
                (0.10, 'f=10%'), (0.01, 'f=1%')]
    for frac, label in examples:
        age_ex = age_from_fraction(frac) / 1000
        ax2.plot(frac * 100, age_ex, 'o', color=COLORS['e_pink'], ms=8, zorder=5)
        ax2.text(frac * 100 + 1.5, age_ex, f'{label}\n→ {age_ex:.1f} kyr',
                 color=COLORS['e_pink'], fontsize=7.5, va='center')

    ax2.set_xlabel('C-14 Fraction Remaining (%)', color=COLORS['text'])
    ax2.set_ylabel('Age (thousands of years)', color=COLORS['text'])
    ax2.set_title('Carbon Dating Ruler', color=COLORS['text'], pad=8)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 55)

    # ── Bottom-left: inverse problem visualisation ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])

    # Measured fraction = 23%
    f_measured = 0.23
    age_measured = age_from_fraction(f_measured)
    ax3.plot(t / 1000, f * 100, color=COLORS['e_gold'], lw=3, label='Decay curve')
    ax3.axhline(f_measured * 100, color=COLORS['e_red'], ls='--', lw=2,
                label=f'Measured: {f_measured*100:.0f}%')
    ax3.axvline(age_measured / 1000, color=COLORS['e_green'], ls='--', lw=2,
                label=f'Age: {age_measured:,.0f} yr')
    ax3.plot(age_measured / 1000, f_measured * 100, 'o', color=COLORS['e_pink'],
             ms=12, zorder=6)
    ax3.annotate(f'Age = {age_measured/1000:.1f} kyr',
                 xy=(age_measured / 1000, f_measured * 100),
                 xytext=(age_measured / 1000 + 4, f_measured * 100 + 15),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_pink'], lw=1.5),
                 color=COLORS['e_pink'], fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax3.set_xlabel('Time (thousands of years)', color=COLORS['text'])
    ax3.set_ylabel('C-14 Remaining (%)', color=COLORS['text'])
    ax3.set_title('Inverse Problem: Fraction → Age', color=COLORS['text'], pad=8)
    ax3.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])
    ax3.set_xlim(0, 50)
    ax3.set_ylim(0, 105)

    # ── Bottom-right: calibration notes (uncertainty) ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])

    # Show sensitivity: small fraction error → large age uncertainty
    f_central = 0.10
    age_central = age_from_fraction(f_central)
    f_range = np.linspace(0.07, 0.13, 100)
    age_range = age_from_fraction(f_range)
    ax4.fill_between(f_range * 100, age_range / 1000,
                     color=COLORS['e_orange'], alpha=0.3, label='Age uncertainty band')
    ax4.plot(f_range * 100, age_range / 1000, color=COLORS['e_orange'], lw=2)
    ax4.plot(f_central * 100, age_central / 1000, 'o',
             color=COLORS['e_gold'], ms=10, zorder=5, label=f'f={f_central*100:.0f}% → {age_central/1000:.1f} kyr')

    # Also plot derivative (sensitivity)
    ax4_twin = ax4.twinx()
    df = np.gradient(f_range)
    dage = np.gradient(age_range / 1000)
    sensitivity = np.abs(dage / df) if len(df) > 0 else np.zeros_like(f_range)
    ax4_twin.plot(f_range * 100, np.abs(dage / df),
                  color=COLORS['e_pink'], lw=2, ls='--', alpha=0.8)
    ax4_twin.set_ylabel('|dAge/df|  (sensitivity)', color=COLORS['e_pink'])
    ax4_twin.tick_params(colors=COLORS['e_pink'])

    ax4.set_xlabel('C-14 Fraction (%)', color=COLORS['text'])
    ax4.set_ylabel('Age (thousands of years)', color=COLORS['text'])
    ax4.set_title('Dating Sensitivity  (old samples harder to date)', color=COLORS['text'], pad=8)
    ax4.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax4.grid(True, alpha=0.3, color=COLORS['grid'])

    fig.suptitle('Carbon-14 Dating  —  $N(t) = N_0\\,e^{-\\lambda t}$  (t½ = 5 730 yr)',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'carbon_dating', out_dir)
    plt.close(fig)
    print("Done: carbon_dating")


if __name__ == '__main__':
    main()
