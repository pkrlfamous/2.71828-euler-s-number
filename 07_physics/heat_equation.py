"""
heat_equation.py — Newton's Law of Cooling

T(t) = T_env + (T₀ − T_env) · e^(−k·t)

Shows hot object cooling and cold object (ice) warming to room temperature,
with multiple cooling rate constants k.
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


T_ROOM = 22.0   # °C  ambient / environment temperature
T_HOT  = 95.0   # °C  freshly brewed coffee
T_ICE  = 0.0    # °C  ice cube

K_VALUES   = [0.05, 0.1, 0.2, 0.35]      # s⁻¹ cooling constants
K_LABELS   = ['Slow (k=0.05)', 'Medium (k=0.1)', 'Fast (k=0.2)', 'Very fast (k=0.35)']
K_COLORS   = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_pink']]


def newton_cooling(t, T0, T_env, k):
    return T_env + (T0 - T_env) * np.exp(-k * t)


def main():
    apply_euler_style()

    t = np.linspace(0, 60, 800)   # 0 – 60 minutes

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ── Left: Hot object cooling ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for k, label, color in zip(K_VALUES, K_LABELS, K_COLORS):
        T = newton_cooling(t, T_HOT, T_ROOM, k)
        ax1.plot(t, T, color=color, lw=2.5, label=label)

    ax1.axhline(T_ROOM, color=COLORS['text'], ls='--', lw=1.5, alpha=0.7,
                label=f'Room temp ({T_ROOM}°C)')
    ax1.axhline(T_HOT, color=COLORS['e_red'], ls=':', lw=1.2, alpha=0.6,
                label=f'Initial temp ({T_HOT}°C)')

    # Annotate 63.2% drop point for k=0.1
    k_demo = 0.1
    tau = 1 / k_demo
    T_tau = newton_cooling(tau, T_HOT, T_ROOM, k_demo)
    ax1.plot(tau, T_tau, 'o', color=COLORS['e_cyan'], ms=8, zorder=5)
    ax1.annotate(f'τ = 1/k = {tau:.0f} min\nT = {T_tau:.1f}°C',
                 xy=(tau, T_tau),
                 xytext=(tau + 4, T_tau + 8),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_cyan'], lw=1.4),
                 color=COLORS['e_cyan'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.text(0.97, 0.97,
             r'$T(t) = T_e + (T_0 - T_e)\,e^{-kt}$',
             transform=ax1.transAxes, fontsize=11,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Time (minutes)', color=COLORS['text'])
    ax1.set_ylabel('Temperature (°C)', color=COLORS['text'])
    ax1.set_title(f'Hot Object Cooling  (T₀ = {T_HOT}°C → T_env = {T_ROOM}°C)',
                  color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])

    # ── Right: Ice warming & combined phase plot ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    for k, label, color in zip(K_VALUES, K_LABELS, K_COLORS):
        T = newton_cooling(t, T_ICE, T_ROOM, k)
        ax2.plot(t, T, color=color, lw=2.5, label=label)

    ax2.axhline(T_ROOM, color=COLORS['text'], ls='--', lw=1.5, alpha=0.7,
                label=f'Room temp ({T_ROOM}°C)')
    ax2.axhline(T_ICE, color=COLORS['e_blue'], ls=':', lw=1.2, alpha=0.6,
                label=f'Ice temp ({T_ICE}°C)')

    # Annotate asymptote approach
    ax2.text(0.97, 0.05,
             'Ice warms asymptotically\nto room temperature',
             transform=ax2.transAxes, fontsize=10,
             color=COLORS['e_cyan'], ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Time (minutes)', color=COLORS['text'])
    ax2.set_ylabel('Temperature (°C)', color=COLORS['text'])
    ax2.set_title(f'Ice Warming  (T₀ = {T_ICE}°C → T_env = {T_ROOM}°C)',
                  color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])

    fig.suptitle("Newton's Law of Cooling  —  $T(t) = T_e + (T_0 - T_e)\\,e^{-kt}$",
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'heat_equation', out_dir)
    plt.close(fig)
    print("Done: heat_equation")


if __name__ == '__main__':
    main()
