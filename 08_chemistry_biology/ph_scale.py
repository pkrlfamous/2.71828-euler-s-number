"""
ph_scale.py — The logarithmic pH scale

pH = −log₁₀[H⁺]  =  −ln[H⁺] / ln(10)

Shows the full pH 0–14 scale as a colour bar, marks common substances,
and illustrates the logarithmic (base-10 / natural log) connection.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

# Common substances with their approximate pH
SUBSTANCES = {
    'Battery acid':   0.5,
    'Lemon juice':    2.0,
    'Vinegar':        3.0,
    'Coffee':         5.0,
    'Rain water':     5.6,
    'Pure water':     7.0,
    'Blood':          7.4,
    'Baking soda':    8.3,
    'Milk of magnesia': 10.5,
    'Bleach':         13.0,
    'Drain cleaner':  14.0,
}

# pH colour gradient: red (acid) → green (neutral) → blue (base)
PH_CMAP = LinearSegmentedColormap.from_list(
    'ph', ['#E74C3C', '#F39C12', '#FFD700', '#2ECC71', '#4A90D9', '#9B59B6'], N=256
)


def h_concentration(pH):
    return 10 ** (-pH)


def pH_from_h(H):
    return -math.log10(H)


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.42)

    # ── Left: pH colour bar with substance markers ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    pH_range = np.linspace(0, 14, 300)
    ax1.imshow(pH_range.reshape(1, -1), aspect='auto',
               extent=[0, 14, -0.5, 0.5],
               cmap=PH_CMAP, alpha=0.6)

    # Horizontal band
    ax1.set_ylim(-3, len(SUBSTANCES) + 1)

    for i, (name, pH) in enumerate(sorted(SUBSTANCES.items(), key=lambda x: x[1])):
        color = PH_CMAP(pH / 14)
        y = i * 0.85 - 0.5
        ax1.plot(pH, y, 'o', color=color, ms=11, zorder=5,
                 markeredgecolor=COLORS['text'], markeredgewidth=0.5)
        ax1.plot([pH, pH], [-0.5, y], color=color, lw=1, ls=':', alpha=0.5)
        align = 'left' if pH < 7 else 'right'
        offset = 0.15 if pH < 7 else -0.15
        ax1.text(pH + offset, y, f'{name}\n(pH {pH})',
                 color=COLORS['text'], fontsize=8, va='center', ha=align)

    ax1.axvline(7, color=COLORS['e_green'], ls='--', lw=2, alpha=0.8, label='Neutral (pH 7)')
    ax1.set_xlabel('pH', color=COLORS['text'])
    ax1.set_title('The pH Scale — Common Substances', color=COLORS['text'], pad=10)
    ax1.set_xlim(0, 14)
    ax1.set_yticks([])
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10, loc='upper right')
    ax1.grid(True, axis='x', alpha=0.3, color=COLORS['grid'])

    # Acid / Base labels
    ax1.text(2, len(SUBSTANCES) * 0.85,  'ACIDIC', color=COLORS['e_red'],
             fontsize=13, fontweight='bold', ha='center', alpha=0.8)
    ax1.text(11, len(SUBSTANCES) * 0.85, 'BASIC',  color=COLORS['e_blue'],
             fontsize=13, fontweight='bold', ha='center', alpha=0.8)

    # ── Right: [H⁺] vs pH — logarithmic relationship ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    pH_vals = np.linspace(0, 14, 500)
    H_vals  = 10 ** (-pH_vals)

    ax2.semilogy(pH_vals, H_vals, color=COLORS['e_gold'], lw=3,
                 label=r'$[H^+] = 10^{-\mathrm{pH}}$')
    ax2.fill_between(pH_vals, H_vals, 1e-15, color=COLORS['e_gold'], alpha=0.12)

    # Mark 10× steps
    for pH_mark in range(0, 15):
        H_mark = 10**(-pH_mark)
        ax2.plot(pH_mark, H_mark, 'o', color=COLORS['e_cyan'], ms=6, zorder=5)

    ax2.axvline(7, color=COLORS['e_green'], ls='--', lw=1.5, alpha=0.7)
    ax2.axhline(1e-7, color=COLORS['e_green'], ls='--', lw=1.5, alpha=0.7,
                label=r'$[H^+] = 10^{-7}$ (neutral)')

    ax2.text(0.97, 0.97,
             r'$\mathrm{pH} = -\log_{10}[H^+]$' + '\n\n' +
             r'$= -\dfrac{\ln[H^+]}{\ln 10}$',
             transform=ax2.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    # Each pH unit = 10× change in [H⁺]
    ax2.annotate('Each pH unit\n= 10× change in [H⁺]',
                 xy=(5, 10**-5), xytext=(9, 10**-3),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.5),
                 color=COLORS['e_cyan'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('pH', color=COLORS['text'])
    ax2.set_ylabel('[H⁺] concentration  (mol/L)', color=COLORS['text'])
    ax2.set_title('Logarithmic Relationship: pH ↔ [H⁺]', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax2.set_xlim(0, 14)

    fig.suptitle('pH Scale  —  $\\mathrm{pH} = -\\log_{10}[H^+] = -\\ln[H^+]/\\ln 10$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'ph_scale', out_dir)
    plt.close(fig)
    print("Done: ph_scale")


if __name__ == '__main__':
    main()
