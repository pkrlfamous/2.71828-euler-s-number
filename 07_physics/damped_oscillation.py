"""
damped_oscillation.py — Damped harmonic oscillator

x(t) = A · e^(−γt) · cos(ωt + φ)

Shows underdamped, critically damped, and overdamped cases plus the
exponential envelope ±A·e^(−γt) for the underdamped case.
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

A  = 1.0    # initial amplitude
phi = 0.0   # initial phase
omega0 = 2 * np.pi   # natural angular frequency (1 Hz)


def underdamped(t, gamma):
    """x(t) = A·e^(−γt)·cos(ω_d·t)  where  ω_d = sqrt(ω₀² − γ²)"""
    omega_d = np.sqrt(max(omega0**2 - gamma**2, 0))
    return A * np.exp(-gamma * t) * np.cos(omega_d * t + phi)


def envelope(t, gamma):
    return A * np.exp(-gamma * t)


def critically_damped(t, gamma):
    """x(t) = A·(1 + γt)·e^(−γt)"""
    return A * (1 + gamma * t) * np.exp(-gamma * t)


def overdamped(t, gamma, omega0):
    """x(t) = A·cosh-style solution with two real roots."""
    disc = np.sqrt(gamma**2 - omega0**2)
    r1, r2 = -gamma + disc, -gamma - disc
    # Initial conditions: x(0)=A, x'(0)=0
    c1 = A * r2 / (r2 - r1)
    c2 = -A * r1 / (r2 - r1)
    return c1 * np.exp(r1 * t) + c2 * np.exp(r2 * t)


def main():
    apply_euler_style()

    t = np.linspace(0, 4, 2000)

    fig = plt.figure(figsize=(15, 9))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.35, hspace=0.45)

    gamma_crit = omega0    # critical damping

    # ── Top-left: Underdamped (low γ) ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['bg_card'])
    gamma_u = 0.5
    x_u = underdamped(t, gamma_u)
    env = envelope(t, gamma_u)
    ax1.plot(t, x_u, color=COLORS['e_cyan'], lw=2, label=f'γ = {gamma_u}  (underdamped)')
    ax1.plot(t, env, color=COLORS['e_gold'], lw=1.5, ls='--', label=r'Envelope $\pm A e^{-\gamma t}$')
    ax1.plot(t, -env, color=COLORS['e_gold'], lw=1.5, ls='--')
    ax1.fill_between(t, -env, env, color=COLORS['e_gold'], alpha=0.08)
    ax1.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax1.set_title('Underdamped  ($\\gamma < \\omega_0$)', color=COLORS['text'], pad=8)
    ax1.set_xlabel('Time (s)', color=COLORS['text'])
    ax1.set_ylabel('Displacement', color=COLORS['text'])
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Top-right: Critically damped ──
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['bg_card'])
    x_c = critically_damped(t, gamma_crit)
    ax2.plot(t, x_c, color=COLORS['e_pink'], lw=2.5, label=f'γ = ω₀ = {gamma_crit:.2f}  (critically damped)')
    ax2.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax2.set_title('Critically Damped  ($\\gamma = \\omega_0$)', color=COLORS['text'], pad=8)
    ax2.set_xlabel('Time (s)', color=COLORS['text'])
    ax2.set_ylabel('Displacement', color=COLORS['text'])
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Bottom-left: Overdamped ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['bg_card'])
    gamma_o = omega0 * 1.5
    x_o = overdamped(t, gamma_o, omega0)
    ax3.plot(t, x_o, color=COLORS['e_orange'], lw=2.5, label=f'γ = {gamma_o:.2f}  (overdamped)')
    ax3.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)
    ax3.set_title('Overdamped  ($\\gamma > \\omega_0$)', color=COLORS['text'], pad=8)
    ax3.set_xlabel('Time (s)', color=COLORS['text'])
    ax3.set_ylabel('Displacement', color=COLORS['text'])
    ax3.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Bottom-right: All three overlaid ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['bg_card'])
    ax4.plot(t, x_u,   color=COLORS['e_cyan'],   lw=2,   label='Underdamped')
    ax4.plot(t, x_c,   color=COLORS['e_pink'],   lw=2,   label='Critically damped')
    ax4.plot(t, x_o,   color=COLORS['e_orange'], lw=2,   label='Overdamped')
    ax4.plot(t, env,   color=COLORS['e_gold'],   lw=1.5, ls='--', alpha=0.7, label='Envelope')
    ax4.plot(t, -env,  color=COLORS['e_gold'],   lw=1.5, ls='--', alpha=0.7)
    ax4.axhline(0, color=COLORS['text'], lw=0.8, alpha=0.4)

    ax4.text(0.97, 0.97,
             r'$x(t) = A \cdot e^{-\gamma t} \cdot \cos(\omega_d t)$',
             transform=ax4.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax4.set_title('All Cases Compared', color=COLORS['text'], pad=8)
    ax4.set_xlabel('Time (s)', color=COLORS['text'])
    ax4.set_ylabel('Displacement', color=COLORS['text'])
    ax4.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax4.grid(True, alpha=0.3, color=COLORS['grid'])

    fig.suptitle('Damped Harmonic Oscillator  —  $x(t) = A e^{-\\gamma t} \\cos(\\omega_d t)$',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'damped_oscillation', out_dir)
    plt.close(fig)
    print("Done: damped_oscillation")


if __name__ == '__main__':
    main()
