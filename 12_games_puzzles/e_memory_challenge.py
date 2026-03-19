"""
e Memory Challenge — Memorize digits of e in blocks of 5.
Interactive: show blocks and ask user to retype them.
Non-interactive: display beautifully and generate digit-map visualization.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

# ── Get digits of e ───────────────────────────────────────────────────────────
try:
    from mpmath import mp, e as mp_e
    mp.dps = 205
    e_str = mp.nstr(mp_e, 202, strip_zeros=False)
    e_digits_str = e_str.replace('.', '').replace('-', '')
    e_digits_all = [int(d) for d in e_digits_str if d.isdigit()][:201]
except Exception:
    known = "2718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427427466391932003"
    e_digits_all = [int(d) for d in known if d.isdigit()]

# Decimal digits start from index 1 (skip the leading "2")
e_digits = e_digits_all[1:201]  # 200 decimal digits: [7,1,8,2,8,1,8,2,8,4,...]

BLOCK_SIZE = 5
blocks = []
for i in range(0, len(e_digits), BLOCK_SIZE):
    blocks.append(e_digits[i:i + BLOCK_SIZE])

INTERACTIVE = sys.stdin.isatty()

print("=" * 65)
print("   e MEMORY CHALLENGE — Memorize the digits of e!")
print("=" * 65)
print(f"\n  e = 2.{''.join(str(d) for d in e_digits[:50])}")
print(f"         {''.join(str(d) for d in e_digits[50:100])}")
print()
print("  Digits shown in blocks of 5:\n")
for i, blk in enumerate(blocks[:10]):
    blk_str = ''.join(str(d) for d in blk)
    print(f"  Block {i+1:2d}: {blk_str}", end='')
    if (i + 1) % 4 == 0:
        print()
    else:
        print('   ', end='')
print("\n")

if INTERACTIVE:
    print("  Study the digits above, then type each block from memory.\n")
    score = 0
    total = 0
    for i, blk in enumerate(blocks[:6]):
        blk_str = ''.join(str(d) for d in blk)
        print(f"  Block {i+1}: (5 digits) > ", end='', flush=True)
        user = input().strip()
        total += 1
        if user == blk_str:
            score += 1
            print(f"  CORRECT! That was: {blk_str}")
        else:
            print(f"  Incorrect. Correct: {blk_str}  You entered: {user}")
    print(f"\n  Score: {score}/{total}")
else:
    print("  Non-interactive mode — displaying digit layout and generating plot.")
    for i, blk in enumerate(blocks[:20]):
        blk_str = ''.join(str(d) for d in blk)
        print(f"  Block {i+1:2d}: {blk_str}")

# ── Visualization ─────────────────────────────────────────────────────────────
apply_euler_style()

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("e Memory Challenge — Digit Map of e = 2.71828…",
             fontsize=20, color=COLORS['e_gold'], fontweight='bold')

# Create custom colormap: each digit 0-9 gets a distinct vibrant colour
digit_palette = [
    '#1A1A2E',  # 0 — near black
    '#E74C3C',  # 1 — red
    '#F39C12',  # 2 — orange
    '#FFD700',  # 3 — gold
    '#2ECC71',  # 4 — green
    '#00D2FF',  # 5 — cyan
    '#4A90D9',  # 6 — blue
    '#9B59B6',  # 7 — purple
    '#FF6B9D',  # 8 — pink
    '#FFFFFF',  # 9 — white
]
cmap_digit = mcolors.ListedColormap(digit_palette)

# ── Main digit map: 200 digits in 20×10 grid ──────────────────────────────────
ax_map = fig.add_axes([0.03, 0.22, 0.62, 0.68])
ax_map.set_facecolor(COLORS['bg_card'])
n_rows, n_cols = 20, 10
grid = np.array(e_digits[:n_rows * n_cols]).reshape(n_rows, n_cols)
im = ax_map.imshow(grid, cmap=cmap_digit, vmin=0, vmax=9, aspect='auto',
                   interpolation='nearest')
# Overlay digit text
for r in range(n_rows):
    for c in range(n_cols):
        dv = grid[r, c]
        # Choose contrasting text colour
        txt_col = 'white' if dv in [0, 1, 2, 6, 7, 8] else 'black'
        ax_map.text(c, r, str(dv), ha='center', va='center',
                    fontsize=11, fontweight='bold', color=txt_col)

# Label rows with positional info
row_labels = [f'{r*n_cols+1}–{(r+1)*n_cols}' for r in range(n_rows)]
ax_map.set_yticks(range(n_rows))
ax_map.set_yticklabels(row_labels, fontsize=8)
ax_map.set_xticks(range(n_cols))
ax_map.set_xticklabels([f'Col {c+1}' for c in range(n_cols)], fontsize=8)
ax_map.set_title(f'First {n_rows*n_cols} Digits of e — Colour-coded by Digit Value',
                 color=COLORS['e_gold'], fontsize=13, pad=10)

# ── Colour legend ─────────────────────────────────────────────────────────────
ax_leg = fig.add_axes([0.03, 0.06, 0.62, 0.10])
ax_leg.set_facecolor(COLORS['bg_dark'])
for d in range(10):
    rect = plt.Rectangle([d, 0], 1, 1, color=digit_palette[d])
    ax_leg.add_patch(rect)
    txt_col = 'white' if d in [0, 1, 2, 6, 7, 8] else 'black'
    ax_leg.text(d + 0.5, 0.5, str(d), ha='center', va='center',
                fontsize=16, fontweight='bold', color=txt_col)
ax_leg.set_xlim(0, 10)
ax_leg.set_ylim(0, 1)
ax_leg.set_xticks([])
ax_leg.set_yticks([])
ax_leg.set_title('Digit → Colour Key', color=COLORS['e_gold'], fontsize=11, pad=4)

# ── Right side: block-format memory display ───────────────────────────────────
ax_txt = fig.add_axes([0.68, 0.06, 0.30, 0.84])
ax_txt.set_facecolor(COLORS['bg_card'])
ax_txt.axis('off')

lines = ['Blocks of 5 digits\n']
for i, blk in enumerate(blocks[:20]):
    blk_str = ''.join(str(d) for d in blk)
    lines.append(f'Block {i+1:2d}: {blk_str}')
full_text = '\n'.join(lines)
ax_txt.text(0.08, 0.97, full_text, transform=ax_txt.transAxes,
            fontsize=11, color=COLORS['e_gold'], va='top', fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'], alpha=0.9))
ax_txt.set_title('Memory Cards', color=COLORS['e_gold'], fontsize=13)

plt.tight_layout(rect=[0, 0, 1, 0.95])
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'e_memory_challenge', output_dir)
plt.close(fig)
print("\ne_memory_challenge.py complete — plot saved.")
