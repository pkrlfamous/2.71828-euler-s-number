"""
population_nature.py — Exponential and logistic population growth.

Three panels:
  1. Exponential growth P(t) = P0·e^(rt) for multiple growth rates
  2. Exponential vs logistic (carrying capacity K) comparison
  3. Phase plane: dP/dt vs P for both models
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


def logistic(t, P0, r, K):
    """P(t) = K / (1 + ((K-P0)/P0)·e^(-r·t))"""
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))


def main():
    apply_euler_style()

    fig = plt.figure(figsize=(18, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r"Population Dynamics:  $P(t) = P_0\,e^{rt}$  vs Logistic Growth",
        fontsize=18, fontweight='bold', color=COLORS['e_gold'], y=1.01,
    )

    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.32)

    P0 = 100.0
    K = 10000.0
    t = np.linspace(0, 50, 1000)

    growth_rates = [0.05, 0.1, 0.15, 0.20, 0.30]
    palette = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_green'],
               COLORS['e_orange'], COLORS['e_pink']]

    # ── Panel 1: Pure exponential growth ─────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    for r, color in zip(growth_rates, palette):
        P_exp = P0 * np.exp(r * t)
        mask = P_exp < K * 3
        ax1.plot(t[mask], P_exp[mask], color=color, lw=2.5, label=f'r = {r}')

    ax1.axhline(K, color='white', lw=1.2, ls='--', alpha=0.4,
                label=f'Carrying capacity K={int(K)}')
    ax1.set_xlabel('Time t', color=COLORS['text'], fontsize=12)
    ax1.set_ylabel('Population P(t)', color=COLORS['text'], fontsize=12)
    ax1.set_title(r'Exponential Growth: $P=P_0\,e^{rt}$', color=COLORS['text'], fontsize=13)
    ax1.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.25, color=COLORS['grid'])
    ax1.tick_params(colors=COLORS['text'])

    # Doubling time annotation
    r_demo = 0.1
    t_double = math.log(2) / r_demo
    ax1.annotate(
        f'Doubling time\n(r=0.1): {t_double:.1f} yrs',
        xy=(t_double, P0 * 2),
        xytext=(t_double + 3, P0 * 2 * 0.5),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.3),
        color=COLORS['e_gold'], fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85),
    )

    # ── Panel 2: Exponential vs Logistic ─────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    r_comp = 0.15
    P_exp_comp = P0 * np.exp(r_comp * t)
    P_log_comp = logistic(t, P0, r_comp, K)

    ax2.plot(t, P_exp_comp, color=COLORS['e_red'], lw=2.5,
             label=r'Exponential $P_0 e^{rt}$')
    ax2.plot(t, P_log_comp, color=COLORS['e_cyan'], lw=2.5,
             label=f'Logistic (K={int(K)})')
    ax2.axhline(K, color=COLORS['e_gold'], lw=1.5, ls='--',
                label=f'Carrying capacity K={int(K)}')
    ax2.axhline(K / 2, color=COLORS['grid'], lw=1, ls=':', alpha=0.5,
                label='K/2 (inflection point)')

    # Shade the "overshoot" area
    mask_above = P_exp_comp > K
    if mask_above.any():
        ax2.fill_between(t[mask_above], K, P_exp_comp[mask_above],
                         color=COLORS['e_red'], alpha=0.15,
                         label='Unsustainable zone')

    # Inflection point of logistic
    t_infl = math.log((K - P0) / P0) / r_comp
    P_infl = K / 2
    ax2.plot(t_infl, P_infl, 'o', color=COLORS['e_gold'], markersize=9, zorder=5)
    ax2.annotate(
        f'Inflection\nt={t_infl:.1f}\nP=K/2',
        xy=(t_infl, P_infl), xytext=(t_infl + 3, P_infl - 1500),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.3),
        color=COLORS['e_gold'], fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85),
    )

    ax2.set_ylim(0, K * 2.5)
    ax2.set_xlabel('Time t', color=COLORS['text'], fontsize=12)
    ax2.set_ylabel('Population P(t)', color=COLORS['text'], fontsize=12)
    ax2.set_title('Exponential vs Logistic\n(r=0.15)', color=COLORS['text'], fontsize=13)
    ax2.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=8)
    ax2.grid(True, alpha=0.25, color=COLORS['grid'])
    ax2.tick_params(colors=COLORS['text'])

    # ── Panel 3: Phase plane dP/dt vs P ───────────────────────────────────
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(COLORS['bg_card'])

    P_phase = np.linspace(0, K * 1.3, 500)
    r_phase = 0.15

    # Exponential: dP/dt = r·P
    dP_exp = r_phase * P_phase

    # Logistic: dP/dt = r·P·(1 - P/K)
    dP_log = r_phase * P_phase * (1 - P_phase / K)

    ax3.plot(P_phase, dP_exp, color=COLORS['e_red'], lw=2.5,
             label=r'Exponential: $\frac{dP}{dt}=rP$')
    ax3.plot(P_phase, dP_log, color=COLORS['e_cyan'], lw=2.5,
             label=r'Logistic: $\frac{dP}{dt}=rP(1-P/K)$')
    ax3.axhline(0, color='white', lw=1, alpha=0.5)
    ax3.axvline(K, color=COLORS['e_gold'], lw=1.5, ls='--', alpha=0.7, label='K')

    # Max growth rate
    P_max = K / 2
    dP_max = r_phase * K / 4
    ax3.plot(P_max, dP_max, 'o', color=COLORS['e_gold'], markersize=9, zorder=5)
    ax3.annotate(
        f'Max growth\nP=K/2={int(P_max)}\ndP/dt={dP_max:.0f}',
        xy=(P_max, dP_max), xytext=(P_max + 500, dP_max - 100),
        arrowprops=dict(arrowstyle='->', color=COLORS['e_gold'], lw=1.2),
        color=COLORS['e_gold'], fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.85),
    )

    # Fill stable equilibrium region
    mask_stable = dP_log > 0
    ax3.fill_between(P_phase[mask_stable], 0, dP_log[mask_stable],
                     color=COLORS['e_cyan'], alpha=0.12, label='Growth zone')

    ax3.set_xlabel('Population P', color=COLORS['text'], fontsize=12)
    ax3.set_ylabel('Growth rate dP/dt', color=COLORS['text'], fontsize=12)
    ax3.set_title('Phase Plane: Growth Rate vs Population',
                  color=COLORS['text'], fontsize=13)
    ax3.legend(facecolor=COLORS['bg_dark'], edgecolor=COLORS['grid'], fontsize=8)
    ax3.grid(True, alpha=0.25, color=COLORS['grid'])
    ax3.tick_params(colors=COLORS['text'])

    # ── Real-world examples footnote ──────────────────────────────────────
    examples = [
        ("Bacteria (optimal)", "r ≈ 1.0–3.0 /hr"),
        ("E. coli", "r ≈ 1.4 /hr"),
        ("Human population", "r ≈ 0.011 /yr"),
        ("COVID-19 (unmitigated)", "r ≈ 0.3 /day"),
    ]
    example_str = "   |   ".join([f"{nm}: {rv}" for nm, rv in examples])
    fig.text(0.5, -0.04, f"Real growth rates — {example_str}",
             ha='center', color=COLORS['text'], fontsize=8, style='italic')

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'population_nature', out_dir)
    plt.close(fig)
    print("Done: population_nature")


if __name__ == '__main__':
    main()
