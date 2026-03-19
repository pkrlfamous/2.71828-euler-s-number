"""
Guess the Digit of e — Interactive game.
Load first 1000 digits of e, show digits one by one, ask user to guess the next.
Non-interactive: run 10 demo rounds automatically and show digit distribution.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

# ── Compute 1000 digits of e ──────────────────────────────────────────────────
try:
    from mpmath import mp, e as mp_e
    mp.dps = 1005
    e_str = mp.nstr(mp_e, 1002, strip_zeros=False)
    # Remove "2." to get just the digit string, then rejoin
    e_digits_str = e_str.replace('.', '').replace('-', '')
    e_digits = [int(d) for d in e_digits_str if d.isdigit()][:1000]
except Exception:
    # Fallback: first 50 known digits
    known = "27182818284590452353602874713526624977572470936999"
    e_digits = [int(d) for d in known]

# e_digits[0] = 2 (the integer part), e_digits[1:] = decimal digits
decimal_digits = e_digits[1:]  # [7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, ...]

INTERACTIVE = sys.stdin.isatty()

print("=" * 60)
print("  GUESS THE NEXT DIGIT OF  e = 2.71828182845904...")
print("=" * 60)
print(f"  e starts with: 2.{''.join(str(d) for d in decimal_digits[:24])}")
print()

# ── Game logic ────────────────────────────────────────────────────────────────
num_rounds = 10
score = 0
guesses = []
correct_digits = []

if INTERACTIVE:
    print(f"You will be shown decimal digits of e one by one.")
    print(f"Guess the NEXT digit (0-9). Type 'q' to quit.\n")
    print(f"e = 2.  (first decimal digit = {decimal_digits[0]})")
    for rnd in range(num_rounds):
        idx = rnd + 1  # next decimal digit index
        if idx >= len(decimal_digits):
            break
        print(f"\nSo far: 2.{''.join(str(d) for d in decimal_digits[:idx])}")
        print(f"Round {rnd+1}/{num_rounds} — What is decimal digit #{idx+1}?", end=' ')
        user_input = input().strip()
        if user_input.lower() == 'q':
            print("Quitting early.")
            break
        try:
            guess = int(user_input)
        except ValueError:
            print("  Invalid input — skipping round.")
            continue
        actual = decimal_digits[idx]
        guesses.append(guess)
        correct_digits.append(actual)
        if guess == actual:
            score += 1
            print(f"  CORRECT! The digit is {actual}. Score: {score}/{rnd+1}")
        else:
            print(f"  Wrong. The digit was {actual}. Score: {score}/{rnd+1}")

    print(f"\nFinal score: {score}/{len(guesses)} rounds")
else:
    # Non-interactive demo
    print("Non-interactive mode: running 10 demo rounds with random guesses.\n")
    rng = np.random.default_rng(42)
    for rnd in range(num_rounds):
        idx = rnd + 1  # next decimal digit index
        if idx >= len(decimal_digits):
            break
        actual = decimal_digits[idx]
        guess = int(rng.integers(0, 10))
        guesses.append(guess)
        correct_digits.append(actual)
        result = "CORRECT" if guess == actual else "Wrong "
        print(f"  Round {rnd+1}: e = 2.{''.join(str(d) for d in decimal_digits[:idx])}? "
              f"| Guess: {guess} | Actual: {actual} | {result}")
        if guess == actual:
            score += 1

    print(f"\nDemo score: {score}/{num_rounds} (expected ~1/10 by random chance)")

# ── Digit frequency distribution plot ────────────────────────────────────────
apply_euler_style()

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(COLORS['bg_dark'])
fig.suptitle("Guess the Digit of e — Digit Distribution Analysis",
             fontsize=19, color=COLORS['e_gold'], fontweight='bold', y=1.01)

# Frequency of each digit in first 1000 decimal digits
digits_range = list(range(10))
freq = Counter(decimal_digits[:1000])
counts = [freq.get(d, 0) for d in digits_range]

# ── Left: Bar chart of digit frequencies ─────────────────────────────────────
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
bar_colors = [COLORS['e_gold'], COLORS['e_cyan'], COLORS['e_green'], COLORS['e_red'],
              COLORS['e_purple'], COLORS['e_orange'], COLORS['e_pink'], COLORS['e_blue'],
              '#88FFAA', '#FF8844']
bars = ax.bar(digits_range, counts, color=bar_colors, edgecolor='white',
              linewidth=0.7, alpha=0.85)
ax.axhline(100, color='white', lw=1.5, linestyle='--', alpha=0.6, label='Expected (100)')
for bar, cnt in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(cnt), ha='center', va='bottom', fontsize=10, color=COLORS['text'])
ax.set_title('Digit Frequency in First 1000 Digits of e', color=COLORS['e_gold'])
ax.set_xlabel('Digit', color=COLORS['text'])
ax.set_ylabel('Count', color=COLORS['text'])
ax.set_xticks(digits_range)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.2, axis='y')
ax.text(0.05, 0.9, 'Digits appear\n~uniformly!\n(Normal number)',
        transform=ax.transAxes, fontsize=9, color=COLORS['text'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg_dark'], alpha=0.8))

# ── Middle: Running frequency of each digit over first 500 digits ─────────────
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
sample = decimal_digits[:500]
for digit in range(10):
    running = np.cumsum([1 if d == digit else 0 for d in sample]) / np.arange(1, 501)
    ax.plot(running, color=bar_colors[digit], lw=1.5, alpha=0.85, label=str(digit))
ax.axhline(0.1, color='white', lw=2, linestyle='--', alpha=0.5, label='Expected 0.1')
ax.set_title('Running Frequency of Each Digit', color=COLORS['e_gold'])
ax.set_xlabel('Number of digits seen', color=COLORS['text'])
ax.set_ylabel('Running frequency', color=COLORS['text'])
ax.legend(ncol=2, fontsize=8, title='Digit', title_fontsize=8)
ax.grid(True, alpha=0.2)

# ── Right: Heatmap of digit sequence (first 300 digits in 10×30 grid) ─────────
ax = axes[2]
ax.set_facecolor(COLORS['bg_card'])
grid_data = np.array(decimal_digits[:300]).reshape(30, 10)
im = ax.imshow(grid_data, cmap='plasma', aspect='auto', vmin=0, vmax=9)
ax.set_title('First 300 Digits of e  (Heatmap)', color=COLORS['e_gold'])
ax.set_xlabel('Column', color=COLORS['text'])
ax.set_ylabel('Row (10 digits per row)', color=COLORS['text'])
plt.colorbar(im, ax=ax, label='Digit value')
ax.text(0.02, 0.98, 'Each row = 10 consecutive digits',
        transform=ax.transAxes, fontsize=8, color=COLORS['text'], va='top',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['bg_dark'], alpha=0.7))

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
save_plot(fig, 'guess_the_digit', output_dir)
plt.close(fig)
print("\nguess_the_digit.py complete — plot saved.")
