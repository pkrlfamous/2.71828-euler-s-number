# Module 11 — Probability & Statistics

Euler's number **e ≈ 2.71828…** is woven into the foundations of probability and statistics.
This module visualises eight distinct appearances.

## Scripts

| Script | Topic | Key Formula |
|--------|-------|-------------|
| `normal_distribution.py` | Bell curve | f(x) = (1/σ√2π)·e^(−(x−μ)²/2σ²) |
| `poisson_distribution.py` | Rare events | P(k) = λᵏ·e^(−λ)/k! |
| `exponential_distribution.py` | Waiting times | f(x) = λ·e^(−λx) |
| `derangement_problem.py` | Hat-check | P(derangement) → 1/e |
| `secretary_problem.py` | Optimal stopping | Stop after n/e candidates |
| `birthday_problem.py` | Birthday paradox | P(no match) ≈ e^(−n(n−1)/730) |
| `bernoulli_trials.py` | Independent failures | (1−1/n)ⁿ → 1/e |
| `stirling_approximation.py` | Factorial growth | n! ≈ √(2πn)·(n/e)ⁿ |

## Running

```bash
cd 11_probability_statistics
python normal_distribution.py
python poisson_distribution.py
python exponential_distribution.py
python derangement_problem.py
python secretary_problem.py
python birthday_problem.py
python bernoulli_trials.py
python stirling_approximation.py
```

All plots are saved to `outputs/` as both PNG and SVG.

## Key Insights

- **Normal distribution**: e controls the shape of the universal bell curve via e^(−x²/2).
- **Poisson distribution**: e^(−λ) is the probability of zero events; e normalises the entire PMF.
- **Exponential distribution**: The only continuous memoryless distribution; its PDF is λ·e^(−λx).
- **Derangements**: P(random permutation is a derangement) converges to exactly 1/e for large n.
- **Secretary problem**: The optimal strategy uses the threshold 1/e ≈ 37% of candidates.
- **Birthday paradox**: The approximation P(no match) ≈ e^(−n²/730) uses the identity Π(1−k/d) ≈ e^(−Σk/d).
- **Bernoulli trials**: (1−1/n)ⁿ → 1/e — failing n independent trials each with probability 1/n.
- **Stirling**: n! ≈ √(2πn)·(n/e)ⁿ — e appears in the denominator of the dominant term.
