"""
enzyme_kinetics.py — Michaelis-Menten enzyme kinetics

v = Vmax · [S] / (Km + [S])

Panels:
  1. v vs [S] hyperbolic curve
  2. Lineweaver-Burk double-reciprocal plot (1/v vs 1/[S])
  3. Inhibitor effects (competitive, uncompetitive, non-competitive)
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

# Kinetic parameters
VMAX = 10.0   # µmol/min
KM   = 2.0    # mM (Michaelis constant)

# Inhibitor parameters
KI   = 1.0    # mM inhibitor dissociation constant
I    = 2.0    # mM inhibitor concentration


def mm_velocity(S, Vmax, Km):
    return Vmax * S / (Km + S)


def competitive_inhibition(S, Vmax, Km, I, Ki):
    """Apparent Km increases: Km_app = Km(1 + I/Ki)."""
    Km_app = Km * (1 + I / Ki)
    return Vmax * S / (Km_app + S)


def uncompetitive_inhibition(S, Vmax, Km, I, Ki):
    """Both Vmax and Km decrease by factor α = 1 + I/Ki."""
    alpha = 1 + I / Ki
    Vmax_app = Vmax / alpha
    Km_app   = Km   / alpha
    return Vmax_app * S / (Km_app + S)


def noncompetitive_inhibition(S, Vmax, Km, I, Ki):
    """Vmax decreases; Km unchanged."""
    alpha = 1 + I / Ki
    Vmax_app = Vmax / alpha
    return Vmax_app * S / (Km + S)


def main():
    apply_euler_style()

    S = np.linspace(0.01, 20, 500)   # substrate concentration (mM)

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.42, hspace=0.50)

    # ── Top-left: v vs [S] ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['bg_card'])

    v = mm_velocity(S, VMAX, KM)
    ax1.plot(S, v, color=COLORS['e_gold'], lw=3, label='Michaelis-Menten')

    # Key parameters
    ax1.axhline(VMAX,      color=COLORS['e_red'],   ls='--', lw=1.8, alpha=0.8,
                label=f'Vmax = {VMAX}')
    ax1.axhline(VMAX / 2,  color=COLORS['e_cyan'],  ls='--', lw=1.5, alpha=0.8,
                label=f'Vmax/2 = {VMAX/2}')
    ax1.axvline(KM,        color=COLORS['e_cyan'],  ls='--', lw=1.5, alpha=0.8,
                label=f'Km = {KM} mM')
    ax1.plot(KM, VMAX / 2, 'o', color=COLORS['e_pink'], ms=10, zorder=6)

    ax1.text(0.97, 0.10,
             r'$v = \dfrac{V_{max}[S]}{K_m + [S]}$',
             transform=ax1.transAxes, fontsize=12,
             color=COLORS['e_gold'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax1.set_xlabel('[S]  (mM)', color=COLORS['text'])
    ax1.set_ylabel('Reaction velocity v  (µmol/min)', color=COLORS['text'])
    ax1.set_title('Michaelis-Menten Kinetics', color=COLORS['text'], pad=8)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Top-right: Lineweaver-Burk ──
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['bg_card'])

    S_lb = np.linspace(0.5, 20, 300)   # avoid very small S for reciprocal
    inv_S = 1 / S_lb
    inv_v = 1 / mm_velocity(S_lb, VMAX, KM)

    ax2.plot(inv_S, inv_v, color=COLORS['e_gold'], lw=3, label='No inhibitor')

    # Extend line to y-axis intercept
    S_ext = np.linspace(-1.5, 20, 500)
    inv_S_ext = 1 / S_ext[S_ext > 0.01]
    inv_v_ext = 1 / mm_velocity(S_ext[S_ext > 0.01], VMAX, KM)
    # Linear fit
    slope = KM / VMAX
    intercept = 1 / VMAX
    x_line = np.linspace(-0.8, 2.5, 300)
    ax2.plot(x_line, slope * x_line + intercept, color=COLORS['e_gold'],
             lw=1.5, ls=':', alpha=0.6)

    # Intercepts
    ax2.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax2.axvline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax2.plot(0,           1 / VMAX, 'o', color=COLORS['e_red'],   ms=9, zorder=5,
             label=f'y-int = 1/Vmax = {1/VMAX:.2f}')
    ax2.plot(-1 / KM,    0,         'o', color=COLORS['e_cyan'],  ms=9, zorder=5,
             label=f'x-int = −1/Km = {-1/KM:.2f}')
    ax2.annotate(f'slope = Km/Vmax\n= {slope:.2f}',
                 xy=(1.0, slope * 1.0 + intercept),
                 xytext=(1.2, slope * 0.5 + intercept + 0.02),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_pink'], lw=1.2),
                 color=COLORS['e_pink'], fontsize=8,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('1/[S]  (mM⁻¹)', color=COLORS['text'])
    ax2.set_ylabel('1/v  (min/µmol)', color=COLORS['text'])
    ax2.set_title('Lineweaver-Burk  (Double-Reciprocal Plot)', color=COLORS['text'], pad=8)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_xlim(-0.8, 2.5)

    # ── Bottom-left: Inhibitor effects on v vs [S] ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])

    v_none    = mm_velocity(S, VMAX, KM)
    v_comp    = competitive_inhibition(S, VMAX, KM, I, KI)
    v_uncomp  = uncompetitive_inhibition(S, VMAX, KM, I, KI)
    v_noncomp = noncompetitive_inhibition(S, VMAX, KM, I, KI)

    ax3.plot(S, v_none,    color=COLORS['e_gold'],   lw=2.5, label='No inhibitor')
    ax3.plot(S, v_comp,    color=COLORS['e_red'],    lw=2.5, label='Competitive')
    ax3.plot(S, v_uncomp,  color=COLORS['e_cyan'],   lw=2.5, label='Uncompetitive')
    ax3.plot(S, v_noncomp, color=COLORS['e_orange'], lw=2.5, label='Non-competitive')

    ax3.axhline(VMAX, color=COLORS['text'], ls=':', lw=1, alpha=0.4)
    ax3.text(0.97, 0.97,
             f'[I] = {I} mM,  Ki = {KI} mM',
             transform=ax3.transAxes, fontsize=9,
             color=COLORS['text'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.7))

    ax3.set_xlabel('[S]  (mM)', color=COLORS['text'])
    ax3.set_ylabel('Velocity v  (µmol/min)', color=COLORS['text'])
    ax3.set_title('Inhibitor Effects on Reaction Rate', color=COLORS['text'], pad=8)
    ax3.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Bottom-right: Lineweaver-Burk with inhibitors ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])

    inv_v_none   = 1 / mm_velocity(S_lb, VMAX, KM)
    inv_v_comp   = 1 / competitive_inhibition(S_lb, VMAX, KM, I, KI)
    inv_v_uncomp = 1 / uncompetitive_inhibition(S_lb, VMAX, KM, I, KI)
    inv_v_nonc   = 1 / noncompetitive_inhibition(S_lb, VMAX, KM, I, KI)

    ax4.plot(inv_S, inv_v_none,   color=COLORS['e_gold'],   lw=2.5, label='No inhibitor')
    ax4.plot(inv_S, inv_v_comp,   color=COLORS['e_red'],    lw=2.5, label='Competitive\n(same y-int)')
    ax4.plot(inv_S, inv_v_uncomp, color=COLORS['e_cyan'],   lw=2.5, label='Uncompetitive\n(same slope)')
    ax4.plot(inv_S, inv_v_nonc,   color=COLORS['e_orange'], lw=2.5, label='Non-competitive\n(same x-int)')

    ax4.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax4.axvline(0, color=COLORS['text'], lw=0.8, alpha=0.4)

    ax4.set_xlabel('1/[S]  (mM⁻¹)', color=COLORS['text'])
    ax4.set_ylabel('1/v  (min/µmol)', color=COLORS['text'])
    ax4.set_title('Lineweaver-Burk with Inhibitors', color=COLORS['text'], pad=8)
    ax4.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=8.5,
               loc='upper left')
    ax4.grid(True, alpha=0.3, color=COLORS['grid'])
    ax4.set_xlim(-0.2, 2.2)
    ax4.set_ylim(-0.05, 0.6)

    fig.suptitle('Enzyme Kinetics  —  $v = V_{max}[S]/(K_m + [S])$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'enzyme_kinetics', out_dir)
    plt.close(fig)
    print("Done: enzyme_kinetics")


if __name__ == '__main__':
    main()
