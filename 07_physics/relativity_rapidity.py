"""
relativity_rapidity.py — Special Relativity Rapidity

Rapidity:  φ = atanh(v/c)   →   v/c = tanh(φ) = (e^φ − e^{−φ}) / (e^φ + e^{−φ})

Shows:
  1. v/c vs rapidity (hyperbolic saturation below c)
  2. Rapidity is additive vs relativistic velocity addition
  3. Lorentz factor γ = cosh(φ)
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


def rapidity_to_beta(phi):
    """v/c = tanh(φ)."""
    return np.tanh(phi)


def beta_to_rapidity(beta):
    """φ = atanh(v/c)."""
    return np.arctanh(np.clip(beta, -0.9999, 0.9999))


def lorentz_gamma(phi):
    """γ = cosh(φ)."""
    return np.cosh(phi)


def relativistic_add(beta1, beta2):
    """Relativistic velocity addition formula."""
    return (beta1 + beta2) / (1 + beta1 * beta2)


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.38, hspace=0.48)

    phi = np.linspace(0, 5, 1000)

    # ── Top-left: v/c vs rapidity ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['bg_card'])
    beta = rapidity_to_beta(phi)
    ax1.plot(phi, beta, color=COLORS['e_gold'], lw=3, label=r'$v/c = \tanh(\varphi)$')
    ax1.axhline(1.0, color=COLORS['e_red'], ls='--', lw=2, alpha=0.85, label='$v = c$  (light speed)')
    # Mark key points
    for ph_mark, label in [(1, 'φ=1'), (2, 'φ=2'), (3, 'φ=3')]:
        b = math.tanh(ph_mark)
        ax1.plot(ph_mark, b, 'o', color=COLORS['e_cyan'], ms=8, zorder=5)
        ax1.annotate(f'{label}\nv/c={b:.3f}',
                     xy=(ph_mark, b), xytext=(ph_mark + 0.25, b - 0.08),
                     color=COLORS['e_cyan'], fontsize=8,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7))

    ax1.text(0.97, 0.10,
             r'$\tanh\varphi = \dfrac{e^\varphi - e^{-\varphi}}{e^\varphi + e^{-\varphi}}$',
             transform=ax1.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Rapidity φ', color=COLORS['text'])
    ax1.set_ylabel('v / c', color=COLORS['text'])
    ax1.set_title('Velocity vs Rapidity', color=COLORS['text'], pad=8)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_ylim(0, 1.05)

    # ── Top-right: Lorentz factor γ = cosh(φ) ──
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['bg_card'])
    gamma = lorentz_gamma(phi)
    # Classical γ = 1/sqrt(1-β²) for comparison
    beta_vals = rapidity_to_beta(phi)
    gamma_classical = 1 / np.sqrt(1 - beta_vals**2 + 1e-30)

    ax2.plot(phi, gamma, color=COLORS['e_cyan'], lw=3, label=r'$\gamma = \cosh(\varphi)$')
    ax2.plot(phi, gamma_classical, color=COLORS['e_pink'], lw=1.5, ls='--', alpha=0.7,
             label=r'$\gamma = 1/\sqrt{1-v^2/c^2}$  (same!)')
    ax2.set_xlabel('Rapidity φ', color=COLORS['text'])
    ax2.set_ylabel('Lorentz Factor γ', color=COLORS['text'])
    ax2.set_title('Lorentz Factor  $\\gamma = \\cosh(\\varphi)$', color=COLORS['text'], pad=8)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_yscale('log')
    ax2.set_ylim(1, 200)

    # ── Bottom-left: Rapidity is additive ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])

    # Two objects each at β₁, combined velocity
    beta1_vals = np.linspace(0, 0.99, 200)
    beta2_fixed = 0.6

    # Classical (wrong): v_tot = v1 + v2
    beta_classical = beta1_vals + beta2_fixed
    beta_classical = np.clip(beta_classical, 0, 2.0)  # can exceed c (wrong)

    # Relativistic (correct)
    beta_rel = relativistic_add(beta1_vals, beta2_fixed)

    # Rapidity approach: φ_total = φ₁ + φ₂
    phi1 = beta_to_rapidity(beta1_vals)
    phi2 = beta_to_rapidity(np.full_like(beta1_vals, beta2_fixed))
    phi_total = phi1 + phi2
    beta_rapidity = rapidity_to_beta(phi_total)   # should equal beta_rel

    ax3.plot(beta1_vals, beta_classical, color=COLORS['e_red'], lw=2, ls='--',
             label=f'Classical: v₁ + v₂ (can exceed c!)')
    ax3.plot(beta1_vals, beta_rel,      color=COLORS['e_gold'], lw=2.5,
             label=f'Relativistic addition (β₂ = {beta2_fixed})')
    ax3.plot(beta1_vals, beta_rapidity, color=COLORS['e_cyan'], lw=1.8, ls=':',
             label='Via rapidity addition  φ₁+φ₂  (identical)')
    ax3.axhline(1.0, color=COLORS['text'], ls=':', lw=1, alpha=0.5, label='v = c')
    ax3.set_xlabel('v₁ / c', color=COLORS['text'])
    ax3.set_ylabel('Combined v / c', color=COLORS['text'])
    ax3.set_title('Velocity Addition  (β₂ = 0.6)', color=COLORS['text'], pad=8)
    ax3.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=8.5)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])
    ax3.set_ylim(0, 1.6)

    # ── Bottom-right: Exponential form of tanh ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])
    phi2 = np.linspace(-3, 3, 800)
    e_pos = np.exp(phi2)
    e_neg = np.exp(-phi2)
    tanh_vals = (e_pos - e_neg) / (e_pos + e_neg)
    ax4.plot(phi2, e_pos,    color=COLORS['e_green'],  lw=2, label=r'$e^{\varphi}$')
    ax4.plot(phi2, e_neg,    color=COLORS['e_orange'], lw=2, label=r'$e^{-\varphi}$')
    ax4.plot(phi2, tanh_vals, color=COLORS['e_gold'],  lw=3, label=r'$\tanh\varphi = \frac{e^\varphi - e^{-\varphi}}{e^\varphi + e^{-\varphi}}$')
    ax4.axhline( 1, color=COLORS['e_red'], ls=':', lw=1.2, alpha=0.7)
    ax4.axhline(-1, color=COLORS['e_red'], ls=':', lw=1.2, alpha=0.7)
    ax4.set_title('Exponential Components of tanh', color=COLORS['text'], pad=8)
    ax4.set_xlabel('Rapidity φ', color=COLORS['text'])
    ax4.set_ylabel('Value', color=COLORS['text'])
    ax4.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax4.grid(True, alpha=0.3, color=COLORS['grid'])
    ax4.set_ylim(-2, 8)

    fig.suptitle('Special Relativity Rapidity  —  $v/c = \\tanh(\\varphi)$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'relativity_rapidity', out_dir)
    plt.close(fig)
    print("Done: relativity_rapidity")


if __name__ == '__main__':
    main()
