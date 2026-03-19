"""
bacterial_growth.py — Bacterial population growth

Exponential phase: P(t) = P₀ · e^(r·t)
Full logistic + lag + stationary curve for realism.

E. coli doubling time ≈ 20 minutes  →  r = ln(2)/20 per minute.
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

P0        = 100          # initial cell count
DOUBLING  = 20           # E. coli doubling time (min)
R         = math.log(2) / DOUBLING   # exponential growth rate (min⁻¹)
K_CAP     = 1e9          # carrying capacity (cells)

T_LAG     = 30           # lag phase end (min)
T_EXP_END = 180          # end of exponential phase (min)
T_STAT    = 300          # stationary phase start (min)
T_MAX     = 400          # total time (min)


def exponential_growth(t, P0, r):
    return P0 * np.exp(r * t)


def realistic_growth(t):
    """Piecewise: lag → exponential → stationary (logistic-like)."""
    result = np.zeros_like(t, dtype=float)
    for i, ti in enumerate(t):
        if ti < T_LAG:
            # Lag phase: slow start
            result[i] = P0 * (1 + 0.1 * (ti / T_LAG))
        elif ti < T_EXP_END:
            # Exponential phase from end of lag
            t_exp = ti - T_LAG
            result[i] = P0 * np.exp(R * t_exp)
        elif ti < T_STAT:
            # Transition into stationary (logistic approach to K)
            t_log = ti - T_LAG
            P_exp = P0 * np.exp(R * (T_EXP_END - T_LAG))
            K_eff = K_CAP
            b = (K_eff - P_exp) / P_exp
            result[i] = K_eff / (1 + b * np.exp(-R * (ti - T_EXP_END) * 0.3))
        else:
            # Stationary phase
            result[i] = K_CAP * (0.95 + 0.05 * np.sin(0.05 * (ti - T_STAT)))
    return np.clip(result, P0, K_CAP * 1.05)


def main():
    apply_euler_style()

    t = np.linspace(0, T_MAX, 1000)
    t_exp = np.linspace(0, T_EXP_END - T_LAG, 500)

    P_real   = realistic_growth(t)
    P_pure_exp = exponential_growth(t, P0, R)   # no saturation

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ── Left: Linear scale ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    ax1.plot(t, P_real,     color=COLORS['e_gold'], lw=3,   label='Realistic (lag + exp + stat)')
    ax1.plot(t, P_pure_exp, color=COLORS['e_red'],  lw=2, ls='--', alpha=0.7,
             label=r'Pure exponential $P_0 e^{rt}$')
    ax1.axhline(K_CAP, color=COLORS['e_cyan'], ls=':', lw=1.5, alpha=0.7,
                label=f'Carrying capacity K = {K_CAP:.0e}')

    # Phase annotations
    for (x_lo, x_hi, label, col) in [
        (0, T_LAG, 'Lag', COLORS['e_orange']),
        (T_LAG, T_EXP_END, 'Exponential', COLORS['e_green']),
        (T_EXP_END, T_STAT, 'Transition', COLORS['e_pink']),
        (T_STAT, T_MAX, 'Stationary', COLORS['e_blue']),
    ]:
        ax1.axvspan(x_lo, x_hi, color=col, alpha=0.07, lw=0)
        ax1.text((x_lo + x_hi) / 2, K_CAP * 1.03, label,
                 color=col, fontsize=9, ha='center', fontweight='bold')

    ax1.text(0.97, 0.45,
             r'$P(t) = P_0 \cdot e^{rt}$' + f'\nr = ln(2)/{DOUBLING} = {R:.4f} min⁻¹',
             transform=ax1.transAxes, fontsize=10,
             color=COLORS['e_gold'], ha='right', va='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.set_xlabel('Time (minutes)', color=COLORS['text'])
    ax1.set_ylabel('Cell Count', color=COLORS['text'])
    ax1.set_title('E. coli Growth  (linear scale)', color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, T_MAX)

    # ── Right: Log scale — exponential phase is linear ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    ax2.semilogy(t, P_real,     color=COLORS['e_gold'], lw=3, label='Realistic growth')
    ax2.semilogy(t, P_pure_exp, color=COLORS['e_red'],  lw=2, ls='--', alpha=0.7,
                 label=r'Pure exponential $P_0 e^{rt}$')
    ax2.axhline(K_CAP, color=COLORS['e_cyan'], ls=':', lw=1.5, alpha=0.7, label='K (carrying capacity)')

    # Mark doubling events
    for n in range(1, 8):
        t_double = n * DOUBLING + T_LAG
        if t_double < T_EXP_END and t_double < T_MAX:
            P_d = realistic_growth(np.array([t_double]))[0]
            ax2.plot(t_double, P_d, 'o', color=COLORS['e_pink'], ms=6, zorder=5)

    ax2.text(0.03, 0.97,
             f'Doubling time = {DOUBLING} min\n(E. coli, 37 °C)',
             transform=ax2.transAxes, fontsize=10,
             color=COLORS['e_cyan'], ha='left', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax2.set_xlabel('Time (minutes)', color=COLORS['text'])
    ax2.set_ylabel('Cell Count  (log scale)', color=COLORS['text'])
    ax2.set_title('E. coli Growth  (log scale)', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax2.set_xlim(0, T_MAX)

    fig.suptitle('Bacterial Growth  —  $P(t) = P_0\\,e^{rt}$  (E. coli, doubling time 20 min)',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'bacterial_growth', out_dir)
    plt.close(fig)
    print("Done: bacterial_growth")


if __name__ == '__main__':
    main()
