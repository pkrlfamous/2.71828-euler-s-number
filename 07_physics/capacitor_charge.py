"""
capacitor_charge.py — RC circuit charging & discharging

Charging:    V(t) = V₀ · (1 − e^(−t/RC))
Discharging: V(t) = V₀ · e^(−t/RC)

Shows both processes for multiple RC time constants and marks the
63.2% (one time constant) characteristic point.
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

V0 = 12.0          # supply voltage (V)
RC_VALUES = [0.5, 1.0, 1.5, 2.0]   # time constants (s)
RC_COLORS = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink']]


def charge(t, RC):
    return V0 * (1 - np.exp(-t / RC))


def discharge(t, RC):
    return V0 * np.exp(-t / RC)


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    t_max = 10.0
    t = np.linspace(0, t_max, 1000)

    # ── Left: Charging ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for RC, color in zip(RC_VALUES, RC_COLORS):
        V = charge(t, RC)
        ax1.plot(t, V, color=color, lw=2.5, label=f'RC = {RC} s')

    # Mark 63.2% point for RC=1.0 (canonical demo)
    RC_demo = 1.0
    V_tau = V0 * (1 - np.exp(-1))   # ≈ 7.585 V
    ax1.axhline(V_tau, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.85)
    ax1.axvline(RC_demo, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.85)
    ax1.annotate(f'τ = RC = 1 s\nV = {V_tau:.2f} V\n(63.2% of V₀)',
                 xy=(RC_demo, V_tau),
                 xytext=(RC_demo + 1.2, V_tau - 2.5),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_red'], lw=1.5),
                 color=COLORS['e_red'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.axhline(V0, color=COLORS['text'], ls=':', lw=1, alpha=0.5)
    ax1.text(t_max * 0.02, V0 + 0.2, f'V₀ = {V0} V', color=COLORS['text'], fontsize=9)

    ax1.text(0.97, 0.05,
             r'$V(t) = V_0\!\left(1 - e^{-t/RC}\right)$',
             transform=ax1.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Time (s)', color=COLORS['text'])
    ax1.set_ylabel('Voltage (V)', color=COLORS['text'])
    ax1.set_title('Capacitor Charging', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_ylim(-0.5, V0 + 1.5)
    ax1.set_xlim(0, t_max)

    # ── Right: Discharging ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    for RC, color in zip(RC_VALUES, RC_COLORS):
        V = discharge(t, RC)
        ax2.plot(t, V, color=color, lw=2.5, label=f'RC = {RC} s')

    # Mark 36.8% point for RC=1.0
    V_tau_d = V0 * np.exp(-1)    # ≈ 4.415 V
    ax2.axhline(V_tau_d, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.85)
    ax2.axvline(RC_demo, color=COLORS['e_red'], ls='--', lw=1.5, alpha=0.85)
    ax2.annotate(f'τ = 1 s\nV = {V_tau_d:.2f} V\n(36.8% of V₀)',
                 xy=(RC_demo, V_tau_d),
                 xytext=(RC_demo + 1.2, V_tau_d + 2.0),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_red'], lw=1.5),
                 color=COLORS['e_red'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.text(0.97, 0.95,
             r'$V(t) = V_0 \cdot e^{-t/RC}$',
             transform=ax2.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Time (s)', color=COLORS['text'])
    ax2.set_ylabel('Voltage (V)', color=COLORS['text'])
    ax2.set_title('Capacitor Discharging', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=10)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_ylim(-0.5, V0 + 1.5)
    ax2.set_xlim(0, t_max)

    fig.suptitle('RC Capacitor Charge & Discharge  (V₀ = 12 V)',
                 fontsize=18, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'capacitor_charge', out_dir)
    plt.close(fig)
    print("Done: capacitor_charge")


if __name__ == '__main__':
    main()
