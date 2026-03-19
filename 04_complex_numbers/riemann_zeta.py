"""
Riemann Zeta Function along the critical line: s = 1/2 + it
Computed using mpmath.zeta. First few non-trivial zeros are marked.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpmath import mp, zeta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

# First 10 known non-trivial zeros (imaginary part on the critical line)
ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
         37.5862, 40.9187, 43.3271, 48.0052, 49.7738]


def compute_zeta_critical_line(t_values):
    """Evaluate ζ(1/2 + it) for each t in t_values using mpmath."""
    mp.dps = 20
    results = []
    for t in t_values:
        val = zeta(0.5 + 1j * float(t))
        results.append(complex(val))
    return np.array(results)


def main():
    apply_euler_style()

    print("  Computing ζ(1/2 + it) — this may take ~30 s …")
    t_vals = np.linspace(0.5, 50, 600)
    zeta_vals = compute_zeta_critical_line(t_vals)

    real_z = zeta_vals.real
    imag_z = zeta_vals.imag
    abs_z = np.abs(zeta_vals)

    fig = plt.figure(figsize=(18, 13))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Riemann Zeta Function: $\zeta(1/2+it)$ along the Critical Line',
        fontsize=20, color=COLORS['e_gold'], fontweight='bold'
    )

    gs = fig.add_gridspec(3, 2, hspace=0.48, wspace=0.32)

    # ── Re(ζ) ─────────────────────────────────────────────────────────────
    ax_re = fig.add_subplot(gs[0, :])
    ax_re.set_facecolor(COLORS['bg_card'])
    ax_re.plot(t_vals, real_z, color=COLORS['e_blue'], lw=1.8,
               label=r'$\mathrm{Re}\,\zeta(1/2+it)$')
    ax_re.axhline(0, color=COLORS['grid'], lw=0.8)

    for z0 in ZEROS:
        ax_re.axvline(z0, color=COLORS['e_gold'], lw=1, alpha=0.5, linestyle=':')

    ax_re.set_ylabel('Re(ζ)', color=COLORS['text'])
    ax_re.set_title(r'Real Part of $\zeta(1/2+it)$', color=COLORS['text'])
    ax_re.legend(fontsize=10, facecolor=COLORS['bg_dark'],
                 edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax_re.grid(True, alpha=0.2)
    ax_re.set_xlim(0.5, 50)

    # ── Im(ζ) ─────────────────────────────────────────────────────────────
    ax_im = fig.add_subplot(gs[1, :])
    ax_im.set_facecolor(COLORS['bg_card'])
    ax_im.plot(t_vals, imag_z, color=COLORS['e_red'], lw=1.8,
               label=r'$\mathrm{Im}\,\zeta(1/2+it)$')
    ax_im.axhline(0, color=COLORS['grid'], lw=0.8)

    for z0 in ZEROS:
        ax_im.axvline(z0, color=COLORS['e_gold'], lw=1, alpha=0.5, linestyle=':')

    ax_im.set_ylabel('Im(ζ)', color=COLORS['text'])
    ax_im.set_title(r'Imaginary Part of $\zeta(1/2+it)$', color=COLORS['text'])
    ax_im.legend(fontsize=10, facecolor=COLORS['bg_dark'],
                 edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax_im.grid(True, alpha=0.2)
    ax_im.set_xlim(0.5, 50)

    # ── |ζ| with zeros marked ─────────────────────────────────────────────
    ax_abs = fig.add_subplot(gs[2, 0])
    ax_abs.set_facecolor(COLORS['bg_card'])
    ax_abs.plot(t_vals, abs_z, color=COLORS['e_green'], lw=2,
                label=r'$|\zeta(1/2+it)|$')
    ax_abs.axhline(0, color=COLORS['grid'], lw=0.8)

    for i, z0 in enumerate(ZEROS):
        ax_abs.axvline(z0, color=COLORS['e_gold'], lw=1.2, alpha=0.7, linestyle=':')
        ax_abs.text(z0, ax_abs.get_ylim()[1] if i == 0 else 0,
                    f'  t={z0:.2f}', rotation=90, va='bottom',
                    color=COLORS['e_gold'], fontsize=6.5)

    # Mark near-zero values (|ζ| < threshold)
    threshold = 0.3
    near_zero = abs_z < threshold
    ax_abs.fill_between(t_vals, 0, abs_z, where=near_zero,
                        color=COLORS['e_gold'], alpha=0.35, label=f'|ζ| < {threshold}')

    ax_abs.set_xlabel('t', color=COLORS['text'])
    ax_abs.set_ylabel(r'$|\zeta|$', color=COLORS['text'])
    ax_abs.set_title(r'Modulus $|\zeta(1/2+it)|$ — zeros at dashed lines',
                     color=COLORS['text'])
    ax_abs.legend(fontsize=9, facecolor=COLORS['bg_dark'],
                  edgecolor=COLORS['grid'], labelcolor=COLORS['text'])
    ax_abs.grid(True, alpha=0.2)
    ax_abs.set_xlim(0.5, 50)

    # ── Parametric curve Re vs Im ─────────────────────────────────────────
    ax_par = fig.add_subplot(gs[2, 1])
    ax_par.set_facecolor(COLORS['bg_card'])

    norm_t = (t_vals - t_vals.min()) / (t_vals.max() - t_vals.min())
    for i in range(len(t_vals) - 1):
        color = plt.cm.plasma(norm_t[i])  # type: ignore[attr-defined]
        ax_par.plot(real_z[i:i + 2], imag_z[i:i + 2], color=color, lw=1.2)

    # Mark the zeros on the parametric plot
    for z0 in ZEROS:
        idx = np.argmin(np.abs(t_vals - z0))
        ax_par.plot(real_z[idx], imag_z[idx], '*',
                    color=COLORS['e_gold'], markersize=12, zorder=8)

    ax_par.plot(0, 0, '+', color='white', markersize=14, lw=2.5, zorder=10)
    ax_par.axhline(0, color=COLORS['grid'], lw=0.7, alpha=0.5)
    ax_par.axvline(0, color=COLORS['grid'], lw=0.7, alpha=0.5)
    ax_par.set_xlabel(r'Re$(\zeta)$', color=COLORS['text'])
    ax_par.set_ylabel(r'Im$(\zeta)$', color=COLORS['text'])
    ax_par.set_title(r'Parametric: Im vs Re of $\zeta(1/2+it)$'
                     '\n(stars = zeros, t: 0→50)',
                     color=COLORS['text'])
    ax_par.grid(True, alpha=0.2)

    sm = plt.cm.ScalarMappable(  # type: ignore[attr-defined]
        cmap='plasma', norm=plt.Normalize(0.5, 50))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_par, fraction=0.05, pad=0.02)
    cbar.set_label('t', color=COLORS['text'])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=COLORS['text'])

    # Zero table annotation on abs plot
    zero_text = "Non-trivial zeros:\n" + "\n".join(
        f"  t_{i+1} ≈ {z:.4f}" for i, z in enumerate(ZEROS[:6])
    )
    ax_abs.text(0.68, 0.95, zero_text, transform=ax_abs.transAxes,
                fontsize=7.5, color=COLORS['e_gold'], va='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'],
                          edgecolor=COLORS['e_gold'], alpha=0.9))

    save_plot(fig, 'riemann_zeta', OUTPUT_DIR)
    plt.close(fig)
    print("riemann_zeta.py done.")


if __name__ == '__main__':
    main()
