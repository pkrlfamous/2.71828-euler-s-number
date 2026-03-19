"""
convergence_race.py — Compare convergence speed of three methods for computing e:
  1. Limit definition: (1 + 1/n)^n
  2. Factorial series: Σ 1/k!
  3. Continued fraction convergents

Plots absolute error vs iteration count on semilogy axes.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS
from utils.math_helpers import (
    compute_e_limit,
    compute_e_series,
    e_continued_fraction_coeffs,
    e_continued_fraction_convergent,
)

E = math.e
MAX_ITER = 40


def get_limit_errors(max_iter):
    """Error for limit method at n = 10^k steps."""
    iters = np.arange(1, max_iter + 1)
    n_vals = 10 ** (iters / 4.0)   # grow n geometrically
    errors = [abs(compute_e_limit(n) - E) for n in n_vals]
    return iters, errors


def get_series_errors(max_iter):
    iters = np.arange(0, max_iter)
    errors = []
    total = 0.0
    for k in range(max_iter):
        total += 1.0 / math.factorial(k)
        errors.append(abs(total - E))
    return iters, errors


def get_cf_errors(max_iter):
    coeffs = e_continued_fraction_coeffs(max_iter)
    iters = np.arange(max_iter)
    errors = []
    for i in range(max_iter):
        p, q = e_continued_fraction_convergent(coeffs, i)
        errors.append(abs(p / q - E))
    return iters, errors


def main():
    apply_euler_style()

    limit_iters, limit_errs = get_limit_errors(MAX_ITER)
    series_iters, series_errs = get_series_errors(MAX_ITER)
    cf_iters, cf_errs = get_cf_errors(MAX_ITER)

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    ax.set_facecolor(COLORS['bg_card'])

    # Filter zeros for log scale
    def safe_plot(iters, errs, color, label, marker, ls='-'):
        valid = [(i, e_v) for i, e_v in zip(iters, errs) if e_v > 1e-17]
        if valid:
            vi, ve = zip(*valid)
            ax.semilogy(vi, ve, color=color, lw=2.5, marker=marker,
                        markersize=7, markerfacecolor='white',
                        markeredgecolor=color, markeredgewidth=1.5,
                        ls=ls, label=label, zorder=3)

    safe_plot(limit_iters, limit_errs, COLORS['e_gold'],
              r'Method 1: $(1+1/n)^n$  [slow, $O(1/n)$]', 's', ls='-')
    safe_plot(series_iters, series_errs, COLORS['e_green'],
              r'Method 2: $\sum 1/k!$  [super-exponential]', 'o', ls='-')
    safe_plot(cf_iters, cf_errs, COLORS['e_purple'],
              r'Method 3: Continued fraction  [exponential]', 'D', ls='-')

    # Reference lines
    ref = np.arange(1, MAX_ITER + 1, dtype=float)
    ax.semilogy(ref, E / (2 * (10 ** (ref / 4))), color=COLORS['e_orange'],
                lw=1.2, ls=':', alpha=0.7, label=r'$\sim e/(2n)$ reference (limit)')

    ax.set_xlabel('Iteration Index', color=COLORS['text'], fontsize=13)
    ax.set_ylabel('Absolute Error  $|\\hat{e} - e|$  (log scale)',
                  color=COLORS['text'], fontsize=13)
    ax.set_title('Convergence Race: Three Methods for Computing $e$',
                 color=COLORS['text'], fontsize=16, pad=14)

    legend = ax.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'],
                       fontsize=11, loc='upper right')

    ax.grid(True, alpha=0.3, which='both', color=COLORS['grid'])
    ax.set_xlim(0, MAX_ITER)

    # Winner annotation
    ax.text(0.02, 0.08,
            'Factorial series wins!\nReaches machine epsilon in ~17 terms.\n'
            'Continued fraction beats limit definition.',
            transform=ax.transAxes, fontsize=11,
            color=COLORS['e_green'],
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.85))

    fig.suptitle("Convergence Race — Computing Euler's $e$", fontsize=18,
                 color=COLORS['e_gold'], y=1.01, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'convergence_race', out_dir)
    plt.close(fig)
    print("Done: convergence_race")


if __name__ == '__main__':
    main()
