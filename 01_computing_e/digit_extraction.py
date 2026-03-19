"""
digit_extraction.py — Compute e to 1000 digits using mpmath.

Displays a formatted digit listing and a bar chart of digit frequency.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS
from utils.math_helpers import compute_e_digits

NUM_DIGITS = 1000
DIGITS_PER_ROW = 50


def format_digits(e_str):
    """Format the digit string into rows of DIGITS_PER_ROW."""
    # e_str looks like "2.71828..."
    # Split into integer part and decimal part
    if '.' in e_str:
        int_part, dec_part = e_str.split('.')
    else:
        int_part, dec_part = e_str, ''

    # Strip trailing noise / extra chars — keep exactly NUM_DIGITS significant digits
    all_digits = int_part + dec_part
    # Keep only digit characters
    all_digits = ''.join(ch for ch in all_digits if ch.isdigit())

    lines = []
    lines.append(f"e = {int_part}.")
    lines.append("")
    for row_start in range(0, len(dec_part), DIGITS_PER_ROW):
        chunk = dec_part[row_start: row_start + DIGITS_PER_ROW]
        row_num = row_start + 1
        lines.append(f"  [{row_num:>4}]  {chunk}")
    return '\n'.join(lines), all_digits


def main():
    apply_euler_style()

    print(f"Computing e to {NUM_DIGITS} digits...")
    e_str = compute_e_digits(NUM_DIGITS)

    formatted, all_digits = format_digits(e_str)
    print("\n" + "=" * 60)
    print(formatted)
    print("=" * 60 + "\n")

    # Digit frequency analysis (exclude the leading '2')
    # Use the decimal digits only for frequency
    if '.' in e_str:
        dec_digits = e_str.split('.')[1]
    else:
        dec_digits = ''
    dec_digits = ''.join(ch for ch in dec_digits if ch.isdigit())[:NUM_DIGITS - 1]

    freq = Counter(dec_digits)
    digit_labels = [str(d) for d in range(10)]
    counts = [freq.get(str(d), 0) for d in range(10)]
    expected = len(dec_digits) / 10

    # --- Figure ---
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # --- Left: bar chart of digit frequencies ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(COLORS['bg_card'])

    palette = [COLORS['e_gold'], COLORS['e_blue'], COLORS['e_red'], COLORS['e_green'],
               COLORS['e_purple'], COLORS['e_orange'], COLORS['e_cyan'], COLORS['e_pink'],
               '#AAAAAA', '#FF8C00']
    x = np.arange(10)
    bars = ax1.bar(x, counts, color=palette, edgecolor=COLORS['grid'], linewidth=0.8, zorder=3)
    ax1.axhline(expected, color=COLORS['e_red'], lw=2, ls='--',
                label=f'Expected ≈ {expected:.1f}')

    for bar, count in zip(bars, counts):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 str(count), ha='center', va='bottom', fontsize=11,
                 color=COLORS['text'], fontweight='bold')

    ax1.set_xticks(x)
    ax1.set_xticklabels(digit_labels, fontsize=13)
    ax1.set_xlabel('Digit', color=COLORS['text'])
    ax1.set_ylabel('Frequency in first 999 decimal digits', color=COLORS['text'])
    ax1.set_title(f'Digit Frequency Distribution in e\n(first {len(dec_digits)} decimal digits)',
                  color=COLORS['text'], pad=12)
    ax1.legend(facecolor=COLORS['bg_card'], edgecolor=COLORS['grid'])
    ax1.grid(True, axis='y', alpha=0.3, color=COLORS['grid'])
    ax1.set_ylim(0, max(counts) * 1.18)

    # --- Right: text figure of first digits ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(COLORS['bg_card'])
    ax2.axis('off')

    # Show first 200 decimal digits formatted nicely
    if '.' in e_str:
        dp = e_str.split('.')[1]
    else:
        dp = ''
    dp = ''.join(ch for ch in dp if ch.isdigit())

    display_lines = [r'$e\ =\ 2.$']
    for row_i in range(0, min(200, len(dp)), 10):
        chunk = dp[row_i: row_i + 10]
        display_lines.append(f'  {chunk}')

    display_text = '\n'.join(display_lines[:22])

    ax2.text(0.05, 0.98, display_text,
             transform=ax2.transAxes,
             fontsize=10, verticalalignment='top',
             color=COLORS['e_cyan'], fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.9))

    ax2.text(0.5, 0.08,
             f'e computed to {NUM_DIGITS} significant digits\nusing mpmath arbitrary-precision arithmetic',
             transform=ax2.transAxes, ha='center', fontsize=11,
             color=COLORS['e_gold'],
             bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['bg_dark'], alpha=0.8))

    # Chi-squared test note
    import math
    chi2 = sum((c - expected) ** 2 / expected for c in counts)
    ax1.text(0.02, 0.97,
             f'$\\chi^2 = {chi2:.2f}$ (9 dof)\n(uniform expected if normal number)',
             transform=ax1.transAxes, fontsize=9, verticalalignment='top',
             color=COLORS['e_orange'],
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

    fig.suptitle(f"Euler's Number e — {NUM_DIGITS} Digits", fontsize=18,
                 color=COLORS['e_gold'], y=1.02, fontweight='bold')

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    save_plot(fig, 'digit_extraction', out_dir)
    plt.close(fig)
    print("Done: digit_extraction")


if __name__ == '__main__':
    main()
