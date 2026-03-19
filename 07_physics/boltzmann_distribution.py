"""
boltzmann_distribution.py — Boltzmann / Maxwell-Boltzmann energy distributions

P(E) ∝ sqrt(E) · e^(−E / k_B T)      (3D Maxwell-Boltzmann)

Shows energy distributions at T = 100, 300, 1000, 5000 K and how
temperature shifts the peak and broadens the distribution.
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

# Boltzmann constant in eV/K
k_B = 8.617333262e-5   # eV K⁻¹

TEMPERATURES = [100, 300, 1000, 5000]
T_COLORS = [COLORS['e_blue'], COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_red']]


def maxwell_boltzmann(E, T):
    """3-D Maxwell-Boltzmann speed → energy distribution (unnormalized)."""
    kT = k_B * T
    with np.errstate(over='ignore', invalid='ignore'):
        result = np.sqrt(E) * np.exp(-E / kT)
    result = np.where(np.isfinite(result), result, 0.0)
    return result


def peak_energy(T):
    """Peak of Maxwell-Boltzmann distribution: E_peak = k_B T / 2."""
    return 0.5 * k_B * T


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    E_max = 5 * k_B * max(TEMPERATURES)
    E = np.linspace(1e-8, E_max, 3000)

    # ── Left: normalized distributions ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for T, color in zip(TEMPERATURES, T_COLORS):
        dist = maxwell_boltzmann(E, T)
        norm = np.trapz(dist, E)
        ax1.plot(E, dist / norm, color=color, lw=2.5, label=f'T = {T} K')
        # mark peak
        E_pk = peak_energy(T)
        pk_val = maxwell_boltzmann(np.array([E_pk]), T)[0] / norm
        ax1.plot(E_pk, pk_val, 'o', color=color, ms=7, zorder=5)

    ax1.text(0.97, 0.97,
             r'$P(E) \propto \sqrt{E}\, e^{-E/k_B T}$',
             transform=ax1.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Energy (eV)', color=COLORS['text'])
    ax1.set_ylabel('Probability Density (eV⁻¹)', color=COLORS['text'])
    ax1.set_title('Maxwell-Boltzmann Energy Distribution', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, E_max)

    # ── Right: log scale + kT lines ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    E2 = np.linspace(1e-6, E_max, 3000)
    for T, color in zip(TEMPERATURES, T_COLORS):
        dist = maxwell_boltzmann(E2, T)
        norm = np.trapz(dist, E2)
        pdf  = dist / norm
        mask = pdf > 0
        ax2.semilogy(E2[mask], pdf[mask], color=color, lw=2.5, label=f'T = {T} K')
        # Mark kT energy
        kT = k_B * T
        ax2.axvline(kT, color=color, ls=':', lw=1, alpha=0.6)

    ax2.set_xlabel('Energy (eV)', color=COLORS['text'])
    ax2.set_ylabel('Probability Density  (log scale)', color=COLORS['text'])
    ax2.set_title('Log-Scale View  (dashed = k_B T per temperature)',
                  color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax2.set_xlim(0, E_max)

    # Note on e
    ax2.text(0.97, 0.05,
             'High-energy tail:\n' + r'$P(E) \sim e^{-E/k_BT}$',
             transform=ax2.transAxes, fontsize=10,
             color=COLORS['e_cyan'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    fig.suptitle('Boltzmann Distribution  —  $P(E) \\propto \\sqrt{E}\\,e^{-E/k_BT}$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'boltzmann_distribution', out_dir)
    plt.close(fig)
    print("Done: boltzmann_distribution")


if __name__ == '__main__':
    main()
