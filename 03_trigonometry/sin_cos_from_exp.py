"""
sin and cos derived from complex exponentials:
  cos(x) = (e^(ix) + e^(-ix)) / 2
  sin(x) = (e^(ix) - e^(-ix)) / (2i)
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def main():
    apply_euler_style()

    x = np.linspace(-2 * np.pi, 2 * np.pi, 800)

    # Complex exponentials
    exp_pos = np.exp(1j * x)   # e^(ix)
    exp_neg = np.exp(-1j * x)  # e^(-ix)

    # Derived sin / cos
    cos_derived = (exp_pos + exp_neg) / 2
    sin_derived = (exp_pos - exp_neg) / (2j)

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'$\sin$ and $\cos$ from Complex Exponentials',
        fontsize=22, color=COLORS['e_gold'], fontweight='bold'
    )

    # ── Left panel: e^(ix) components ────────────────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor(COLORS['bg_card'])

    ax1.plot(x, exp_pos.real, color=COLORS['e_blue'], lw=2.5,
             label=r'$\mathrm{Re}(e^{ix}) = \cos x$')
    ax1.plot(x, exp_pos.imag, color=COLORS['e_red'], lw=2.5,
             label=r'$\mathrm{Im}(e^{ix}) = \sin x$')
    ax1.plot(x, exp_neg.real, color=COLORS['e_cyan'], lw=2, linestyle='--',
             label=r'$\mathrm{Re}(e^{-ix}) = \cos x$', alpha=0.8)
    ax1.plot(x, exp_neg.imag, color=COLORS['e_pink'], lw=2, linestyle='--',
             label=r'$\mathrm{Im}(e^{-ix}) = -\sin x$', alpha=0.8)

    ax1.axhline(0, color=COLORS['grid'], lw=0.8)
    ax1.axvline(0, color=COLORS['grid'], lw=0.8)

    # Fill between to show symmetry
    ax1.fill_between(x, exp_pos.imag, exp_neg.imag, alpha=0.12,
                     color=COLORS['e_red'], label='2i·sin(x) region')

    ax1.set_xticks(np.linspace(-2 * np.pi, 2 * np.pi, 9))
    ax1.set_xticklabels(['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
    ax1.set_xlim(-2 * np.pi, 2 * np.pi)
    ax1.set_ylim(-1.4, 1.4)
    ax1.set_xlabel('x', color=COLORS['text'])
    ax1.set_ylabel('Value', color=COLORS['text'])
    ax1.set_title(r'Components of $e^{ix}$ and $e^{-ix}$', color=COLORS['text'])
    ax1.legend(fontsize=9, facecolor=COLORS['bg_dark'],
               edgecolor=COLORS['grid'], labelcolor=COLORS['text'],
               loc='upper right')
    ax1.grid(True, alpha=0.25)

    formula_text = (
        r"$e^{ix}  = \cos x + i\sin x$" + "\n"
        r"$e^{-ix} = \cos x - i\sin x$"
    )
    ax1.text(0.02, 0.02, formula_text, transform=ax1.transAxes,
             fontsize=11, color=COLORS['e_gold'],
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_gold'], alpha=0.9))

    # ── Right panel: derived vs numpy ────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor(COLORS['bg_card'])

    # Plot derived cos
    ax2.plot(x, cos_derived.real, color=COLORS['e_blue'], lw=3.5,
             label=r'$\cos x = \frac{e^{ix}+e^{-ix}}{2}$ (derived)', zorder=4)
    # Verify against numpy
    ax2.plot(x, np.cos(x), color=COLORS['e_gold'], lw=1.5, linestyle=':',
             label=r'$\cos x$ (numpy — exact match)', zorder=5)

    # Plot derived sin
    ax2.plot(x, sin_derived.real, color=COLORS['e_red'], lw=3.5,
             label=r'$\sin x = \frac{e^{ix}-e^{-ix}}{2i}$ (derived)', zorder=4)
    ax2.plot(x, np.sin(x), color=COLORS['e_pink'], lw=1.5, linestyle=':',
             label=r'$\sin x$ (numpy — exact match)', zorder=5)

    # Error display
    cos_err = np.max(np.abs(cos_derived.real - np.cos(x)))
    sin_err = np.max(np.abs(sin_derived.real - np.sin(x)))

    ax2.axhline(0, color=COLORS['grid'], lw=0.8)
    ax2.axvline(0, color=COLORS['grid'], lw=0.8)

    ax2.set_xticks(np.linspace(-2 * np.pi, 2 * np.pi, 9))
    ax2.set_xticklabels(['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
    ax2.set_xlim(-2 * np.pi, 2 * np.pi)
    ax2.set_ylim(-1.4, 1.4)
    ax2.set_xlabel('x', color=COLORS['text'])
    ax2.set_ylabel('Value', color=COLORS['text'])
    ax2.set_title('Derived vs NumPy — Perfect Agreement', color=COLORS['text'])
    ax2.legend(fontsize=9, facecolor=COLORS['bg_dark'],
               edgecolor=COLORS['grid'], labelcolor=COLORS['text'],
               loc='upper right')
    ax2.grid(True, alpha=0.25)

    error_text = (
        f"Max |cos error|: {cos_err:.2e}\n"
        f"Max |sin error|: {sin_err:.2e}\n"
        "(floating-point precision only)"
    )
    ax2.text(0.02, 0.02, error_text, transform=ax2.transAxes,
             fontsize=10, color=COLORS['e_green'],
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_green'], alpha=0.9))

    formula_box = (
        r"$\cos x = \dfrac{e^{ix}+e^{-ix}}{2}$" + "\n\n"
        r"$\sin x = \dfrac{e^{ix}-e^{-ix}}{2i}$"
    )
    ax2.text(0.68, 0.02, formula_box, transform=ax2.transAxes,
             fontsize=11, color=COLORS['e_gold'],
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'],
                       edgecolor=COLORS['e_gold'], alpha=0.9))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_plot(fig, 'sin_cos_from_exp', OUTPUT_DIR)
    plt.close(fig)
    print("sin_cos_from_exp.py done.")


if __name__ == '__main__':
    main()
