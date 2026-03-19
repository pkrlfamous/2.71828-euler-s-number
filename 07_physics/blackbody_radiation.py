"""
blackbody_radiation.py — Planck's blackbody radiation law

B(λ, T) = (2hc²/λ⁵) · 1 / (e^(hc/λk_BT) − 1)

Plots spectral radiance vs wavelength for T = 3000 K, 5778 K (Sun), 10000 K.
Marks Wien's displacement law peaks and visible-light band.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

# Physical constants (SI)
h   = 6.62607015e-34   # Planck constant (J·s)
c   = 2.99792458e8     # speed of light (m/s)
k_B = 1.380649e-23     # Boltzmann constant (J/K)

WIEN_B = 2.897771955e-3   # Wien's displacement constant (m·K)

TEMPERATURES = [3000, 5778, 10000]
T_LABELS     = ['3 000 K  (incandescent)', '5 778 K  (Sun surface)', '10 000 K  (hot star)']
T_COLORS     = [COLORS['e_orange'], COLORS['e_gold'], COLORS['e_cyan']]


def planck(lam, T):
    """Spectral radiance B(λ,T) in W sr⁻¹ m⁻³."""
    exponent = h * c / (lam * k_B * T)
    with np.errstate(over='ignore', invalid='ignore'):
        result = (2 * h * c**2 / lam**5) / (np.exp(exponent) - 1)
    result = np.where(np.isfinite(result), result, 0.0)
    return result


def wien_peak(T):
    """Peak wavelength from Wien's law."""
    return WIEN_B / T


def main():
    apply_euler_style()

    # Wavelength range: 100 nm – 3000 nm
    lam = np.linspace(1e-7, 3e-6, 5000)   # metres
    lam_nm = lam * 1e9                     # nanometres (for display)

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ── Left: linear scale ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    # Shade visible light band (380–700 nm)
    vis_colors = ['violet', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red']
    vis_edges  = [380, 430, 480, 530, 580, 620, 660, 700]
    for i, vc in enumerate(vis_colors):
        ax1.axvspan(vis_edges[i], vis_edges[i+1], color=vc, alpha=0.07, lw=0)
    ax1.axvspan(380, 700, color='white', alpha=0.04, lw=0, label='Visible light')

    max_B = 0.0
    for T, label, color in zip(TEMPERATURES, T_LABELS, T_COLORS):
        B = planck(lam, T)
        # Normalise to visible maximum for comparison
        ax1.plot(lam_nm, B, color=color, lw=2.5, label=label)
        # Peak marker
        lam_pk = wien_peak(T)
        B_pk   = planck(np.array([lam_pk]), T)[0]
        ax1.plot(lam_pk * 1e9, B_pk, 'o', color=color, ms=8, zorder=6)
        max_B = max(max_B, B_pk)

    ax1.text(0.97, 0.97,
             r'$B(\lambda,T) = \dfrac{2hc^2}{\lambda^5} \cdot \dfrac{1}{e^{hc/\lambda k_BT}-1}$',
             transform=ax1.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax1.set_xlabel('Wavelength (nm)', color=COLORS['text'])
    ax1.set_ylabel('Spectral Radiance  (W sr⁻¹ m⁻³)', color=COLORS['text'])
    ax1.set_title("Planck's Blackbody Law", color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(100, 3000)

    # ── Right: log scale showing all three clearly ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    ax2.axvspan(380, 700, color='white', alpha=0.05, lw=0, label='Visible')
    for T, label, color in zip(TEMPERATURES, T_LABELS, T_COLORS):
        B = planck(lam, T)
        mask = B > 0
        ax2.semilogy(lam_nm[mask], B[mask], color=color, lw=2.5, label=label)
        # Wien peak arrow
        lam_pk_nm = wien_peak(T) * 1e9
        B_pk = planck(np.array([wien_peak(T)]), T)[0]
        ax2.axvline(lam_pk_nm, color=color, ls=':', lw=1.2, alpha=0.7)
        ax2.text(lam_pk_nm + 20, B_pk * 0.5,
                 f'λ_peak\n= {lam_pk_nm:.0f} nm',
                 color=color, fontsize=7.5, va='center')

    ax2.set_xlabel('Wavelength (nm)', color=COLORS['text'])
    ax2.set_ylabel('Spectral Radiance  (log scale)', color=COLORS['text'])
    ax2.set_title("Wien's Displacement  ($\\lambda_{peak} = b/T$)", color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax2.set_xlim(100, 3000)

    fig.suptitle("Blackbody Radiation  —  Planck's Law",
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'blackbody_radiation', out_dir)
    plt.close(fig)
    print("Done: blackbody_radiation")


if __name__ == '__main__':
    main()
