# Module 12 — Games & Puzzles

Interactive and visual puzzles that let you *discover* **e ≈ 2.71828…** through play.

## Scripts

| Script | Description | Key e Connection |
|--------|-------------|-----------------|
| `guess_the_digit.py` | Guess the next digit of e | Digit distribution of e |
| `e_memory_challenge.py` | Memorise digits in blocks of 5 | Visual digit map of e |
| `compound_interest_game.py` | Bernoulli's bank problem | (1+1/n)ⁿ → e |
| `e_approximation_race.py` | Three methods race to e | Limit vs series vs CF |
| `steiner_problem.py` | Which x maximises x^(1/x)? | Answer: x = e |
| `optimal_stopping_sim.py` | Secretary problem simulation | Optimal stop at n/e |

## Running

```bash
cd 12_games_puzzles

# Interactive mode (when run from a terminal with a tty):
python guess_the_digit.py
python e_memory_challenge.py
python compound_interest_game.py

# Always non-interactive (just generate plots):
python e_approximation_race.py
python steiner_problem.py
python optimal_stopping_sim.py
```

All plots are saved to `outputs/` as both PNG and SVG.

## Interactivity

The game scripts (`guess_the_digit.py`, `e_memory_challenge.py`, `compound_interest_game.py`)
detect whether they are running in a terminal:

```python
import sys
if sys.stdin.isatty():
    # interactive mode
else:
    # non-interactive demo mode
```

In non-interactive mode (e.g. piped input, CI) they run a preset demo and still generate
the full plot output.

## Key Puzzles

- **Guess the Digit**: Digits of e appear uniformly distributed — hard to predict!
- **Memory Challenge**: Colour-coded digit map makes patterns visible.
- **Compound Interest**: Experience Bernoulli's 1683 discovery firsthand.
- **Approximation Race**: Taylor series wins — exponential convergence vs polynomial for the limit.
- **Steiner Problem**: e^(1/e) ≈ 1.4447 is the global maximum of x^(1/x).
- **Optimal Stopping**: 10,000 simulated hires confirm the 1/e ≈ 37% rule.
