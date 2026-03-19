"""
schrodinger.py — Quantum wave functions featuring e^(ikx) and Gaussians

Panels:
  1. Free particle: Re[e^(ikx)], Im[e^(ikx)], |e^(ikx)|²  (= 1)
  2. Gaussian wave packet: ψ = e^(ikx)·e^(−αx²)  — real, imaginary, |ψ|²
  3. Harmonic-oscillator ground state: ψ₀ ∝ e^(−x²/2)  and excited ψ₁ ∝ x·e^(−x²/2)
  4. Bound-state probability densities |ψₙ|² for n = 0, 1, 2, 3
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

# Hermite polynomials (physicist's, H_n)
def hermite(n, x):
    if n == 0:
        return np.ones_like(x)
    elif n == 1:
        return 2 * x
    elif n == 2:
        return 4 * x**2 - 2
    elif n == 3:
        return 8 * x**3 - 12 * x
    else:
        raise ValueError(f"n={n} not supported")


def qho_wavefunction(n, x):
    """Harmonic-oscillator eigenstate (dimensionless units)."""
    norm = (2**n * math.factorial(n) * np.sqrt(np.pi))**(-0.5)
    return norm * hermite(n, x) * np.exp(-x**2 / 2)


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.38, hspace=0.48)

    # ── Top-left: Free particle e^(ikx) ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['bg_card'])
    x = np.linspace(-3, 3, 1000)
    k = 3.0
    psi = np.exp(1j * k * x)
    ax1.plot(x, psi.real, color=COLORS['e_cyan'], lw=2.5, label=r'Re[$e^{ikx}$]')
    ax1.plot(x, psi.imag, color=COLORS['e_pink'], lw=2.5, label=r'Im[$e^{ikx}$]')
    ax1.plot(x, np.abs(psi)**2, color=COLORS['e_gold'], lw=2, ls='--',
             label=r'$|\psi|^2 = 1$  (uniform)')
    ax1.set_title(r'Free Particle: $\psi = e^{ikx}$', color=COLORS['text'], pad=8)
    ax1.set_xlabel('x', color=COLORS['text'])
    ax1.set_ylabel('Amplitude', color=COLORS['text'])
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)

    # ── Top-right: Gaussian wave packet ──
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['bg_card'])
    alpha = 1.5
    psi_g = np.exp(1j * k * x) * np.exp(-alpha * x**2)
    ax2.plot(x, psi_g.real,       color=COLORS['e_cyan'], lw=2.5, label=r'Re[$\psi$]')
    ax2.plot(x, psi_g.imag,       color=COLORS['e_pink'], lw=2.5, label=r'Im[$\psi$]')
    ax2.plot(x, np.abs(psi_g)**2, color=COLORS['e_gold'], lw=2.5, label=r'$|\psi|^2$')
    ax2.plot(x,  np.exp(-alpha * x**2), color=COLORS['e_orange'], lw=1.5, ls=':',
             alpha=0.8, label='Gaussian envelope')
    ax2.plot(x, -np.exp(-alpha * x**2), color=COLORS['e_orange'], lw=1.5, ls=':', alpha=0.8)
    ax2.set_title(r'Gaussian Wave Packet: $\psi = e^{ikx}\,e^{-\alpha x^2}$',
                  color=COLORS['text'], pad=8)
    ax2.set_xlabel('x', color=COLORS['text'])
    ax2.set_ylabel('Amplitude', color=COLORS['text'])
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)

    # ── Bottom-left: QHO wave functions n=0,1,2,3 ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])
    x_qho = np.linspace(-4, 4, 1000)
    qho_colors = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink']]
    for n, color in enumerate(qho_colors):
        psi_n = qho_wavefunction(n, x_qho)
        ax3.plot(x_qho, psi_n + n, color=color, lw=2.5, label=f'ψ_{n}  (n={n})')
        ax3.axhline(n, color=color, ls=':', lw=0.8, alpha=0.5)

    ax3.text(0.97, 0.97,
             r'$\psi_n \propto H_n(x)\,e^{-x^2/2}$',
             transform=ax3.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax3.set_title('QHO Wave Functions  (offset by n)', color=COLORS['text'], pad=8)
    ax3.set_xlabel('x', color=COLORS['text'])
    ax3.set_ylabel(r'$\psi_n + n$', color=COLORS['text'])
    ax3.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Bottom-right: Probability densities |ψ_n|² ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])
    for n, color in enumerate(qho_colors):
        psi_n = qho_wavefunction(n, x_qho)
        prob  = psi_n**2
        ax4.plot(x_qho, prob + n * 0.35, color=color, lw=2.5, label=f'|ψ_{n}|²')
        ax4.fill_between(x_qho, n * 0.35, prob + n * 0.35,
                         color=color, alpha=0.15)

    ax4.set_title('Probability Densities  $|\\psi_n|^2$', color=COLORS['text'], pad=8)
    ax4.set_xlabel('x', color=COLORS['text'])
    ax4.set_ylabel(r'$|\psi_n|^2$  (offset)', color=COLORS['text'])
    ax4.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax4.grid(True, alpha=0.3, color=COLORS['grid'])

    fig.suptitle(r"Schrödinger Wave Functions  —  $\psi = A\,e^{ikx}$  and  $e^{-\alpha x^2}$",
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'schrodinger', out_dir)
    plt.close(fig)
    print("Done: schrodinger")


if __name__ == '__main__':
    main()
