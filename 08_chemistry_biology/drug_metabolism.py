"""
drug_metabolism.py — Pharmacokinetics: drug concentration over time

Single dose:   C(t) = C_max · (e^(−k_e·t) − e^(−k_a·t))   (one-compartment)
Multiple doses: accumulation via superposition.

k_a = absorption rate constant
k_e = elimination rate constant
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

# Pharmacokinetic parameters (dimensionless / generic units)
K_A  = 1.5     # absorption rate constant (h⁻¹)
K_E  = 0.3     # elimination rate constant (h⁻¹)
DOSE = 100.0   # dose (mg)
V_D  = 10.0    # volume of distribution (L) — to give mg/L

DOSING_INTERVAL = 8.0   # hours between doses


def single_dose_conc(t, dose, ka, ke, Vd):
    """One-compartment first-order absorption and elimination."""
    C_max_factor = (dose / Vd) * (ka / (ka - ke))
    conc = C_max_factor * (np.exp(-ke * t) - np.exp(-ka * t))
    return np.where(t >= 0, conc, 0.0)


def multi_dose_conc(t, n_doses, interval, dose, ka, ke, Vd):
    """Superposition of n_doses doses given at intervals."""
    C = np.zeros_like(t, dtype=float)
    for n in range(n_doses):
        t_shifted = t - n * interval
        C += single_dose_conc(t_shifted, dose, ka, ke, Vd)
    return C


def main():
    apply_euler_style()

    t_single = np.linspace(0, 24, 1000)
    t_multi  = np.linspace(0, 72, 3000)

    fig = plt.figure(figsize=(15, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.4)

    # ── Left: Single dose ──
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    C_single = single_dose_conc(t_single, DOSE, K_A, K_E, V_D)
    ax1.plot(t_single, C_single, color=COLORS['e_gold'], lw=3, label='Drug concentration')

    # Separate absorption & elimination components
    C_abs  = (DOSE / V_D) * (K_A / (K_A - K_E)) * np.exp(-K_A * t_single)
    C_elim = (DOSE / V_D) * (K_A / (K_A - K_E)) * np.exp(-K_E * t_single)
    ax1.plot(t_single, C_elim, color=COLORS['e_cyan'],  lw=1.8, ls='--', alpha=0.8,
             label=r'Elimination term  $\propto e^{-k_e t}$')
    ax1.plot(t_single, C_abs,  color=COLORS['e_pink'],  lw=1.8, ls='--', alpha=0.8,
             label=r'Absorption term  $\propto e^{-k_a t}$')

    # Mark Cmax
    idx_max = np.argmax(C_single)
    t_max_pk = t_single[idx_max]
    C_max_pk = C_single[idx_max]
    ax1.plot(t_max_pk, C_max_pk, 'o', color=COLORS['e_red'], ms=10, zorder=6)
    ax1.annotate(f'C_max = {C_max_pk:.1f} mg/L\nt_max = {t_max_pk:.1f} h',
                 xy=(t_max_pk, C_max_pk),
                 xytext=(t_max_pk + 3, C_max_pk - 1),
                 arrowprops=dict(arrowstyle='->', color=COLORS['e_red'], lw=1.5),
                 color=COLORS['e_red'], fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    ax1.text(0.97, 0.97,
             r'$C(t) = \frac{D\,k_a}{V_d(k_a-k_e)}\!\left(e^{-k_e t} - e^{-k_a t}\right)$',
             transform=ax1.transAxes, fontsize=9.5,
             color=COLORS['e_gold'], ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.85))

    ax1.set_xlabel('Time (h)', color=COLORS['text'])
    ax1.set_ylabel('Concentration (mg/L)', color=COLORS['text'])
    ax1.set_title(f'Single Dose Pharmacokinetics  (k_a={K_A}, k_e={K_E})',
                  color=COLORS['text'], pad=10)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])
    ax1.set_xlim(0, 24)
    ax1.set_ylim(0)

    # ── Right: Multiple doses ──
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])

    n_doses = int(72 / DOSING_INTERVAL)
    C_multi = multi_dose_conc(t_multi, n_doses, DOSING_INTERVAL, DOSE, K_A, K_E, V_D)

    ax2.plot(t_multi, C_multi, color=COLORS['e_gold'], lw=2.5, label='Total concentration')

    # Mark each dose administration
    for n in range(n_doses):
        t_dose = n * DOSING_INTERVAL
        ax2.axvline(t_dose, color=COLORS['e_cyan'], ls=':', lw=1, alpha=0.5)

    ax2.text(0.5, 0.98,
             f'Dosing every {DOSING_INTERVAL:.0f} h  (× {n_doses} doses)',
             transform=ax2.transAxes, fontsize=10,
             color=COLORS['e_cyan'], ha='center', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    # Trough and peak at steady state (approx last 2 doses)
    C_ss_peak  = np.max(C_multi[-500:])
    C_ss_trough = np.min(C_multi[-500:])
    ax2.axhline(C_ss_peak,   color=COLORS['e_green'], ls='--', lw=1.5, alpha=0.7,
                label=f'SS peak ≈ {C_ss_peak:.1f} mg/L')
    ax2.axhline(C_ss_trough, color=COLORS['e_orange'], ls='--', lw=1.5, alpha=0.7,
                label=f'SS trough ≈ {C_ss_trough:.1f} mg/L')

    ax2.set_xlabel('Time (h)', color=COLORS['text'])
    ax2.set_ylabel('Concentration (mg/L)', color=COLORS['text'])
    ax2.set_title('Multiple-Dose Accumulation', color=COLORS['text'], pad=10)
    ax2.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'], fontsize=9)
    ax2.grid(True, alpha=0.3, color=COLORS['grid'])
    ax2.set_xlim(0, 72)
    ax2.set_ylim(0)

    fig.suptitle('Drug Metabolism  —  $C(t) = C_0\\,e^{-k_e t}$  (Pharmacokinetics)',
                 fontsize=17, color=COLORS['e_gold'], fontweight='bold', y=1.01)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'drug_metabolism', out_dir)
    plt.close(fig)
    print("Done: drug_metabolism")


if __name__ == '__main__':
    main()
