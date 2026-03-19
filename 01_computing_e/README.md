# Module 01 — Computing Euler's Number e

This module explores five distinct ways to compute or represent Euler's number
**e ≈ 2.71828 18284 59045…**, from elementary definitions to arbitrary-precision
digit extraction.

---

## Scripts

### 1. `limit_definition.py`
**Formula:** $e = \lim_{n \to \infty} \left(1 + \dfrac{1}{n}\right)^n$

- Left panel: semilog-x convergence curve (gold line) with the true value of *e*
  shown as a red dashed reference.
- Right panel: log-log error plot confirming $O(1/n)$ convergence rate.

**Output:** `outputs/limit_definition.png / .svg`

---

### 2. `factorial_series.py`
**Formula:** $e = \sum_{k=0}^{\infty} \dfrac{1}{k!}$

- Left panel: coloured bar chart of partial sums $S_0, S_1, \ldots, S_{15}$
  climbing toward *e*.
- Right panel: semilog error plot demonstrating super-exponential convergence —
  the error shrinks faster than any geometric sequence.

**Output:** `outputs/factorial_series.png / .svg`

---

### 3. `continued_fraction.py`
**Formula:** $e = [2;\, 1,\,2,\,1,\,1,\,4,\,1,\,1,\,6,\,1,\,1,\,8,\,\ldots]$

- Top-left: convergents $p_n/q_n$ alternating above and below *e*, converging
  exponentially.
- Top-right: semilog error for the convergents.
- Bottom: stem plot revealing the coefficient pattern (every third coefficient
  is an even number 2, 4, 6, 8, …).

**Output:** `outputs/continued_fraction.png / .svg`

---

### 4. `digit_extraction.py`
Uses **mpmath** arbitrary-precision arithmetic to compute *e* to **1000
significant digits**.

- Prints the digits to the console in rows of 50.
- Left panel: bar chart of digit-frequency distribution in the first 999 decimal
  places (tests whether *e* behaves as a "normal" number).
- Right panel: formatted first 200 decimal digits.

**Output:** `outputs/digit_extraction.png / .svg`

---

### 5. `convergence_race.py`
Side-by-side comparison of all three methods on a common semilogy axis:

| Method | Rate | Terms to 1e-15 |
|--------|------|----------------|
| Limit $(1+1/n)^n$ | $O(1/n)$ — slow | ~10¹⁵ evaluations |
| Factorial series $\sum 1/k!$ | Super-exponential | **~17 terms** |
| Continued fraction | Exponential | ~25 convergents |

**Output:** `outputs/convergence_race.png / .svg`

---

## Running the Scripts

```bash
# From the repo root
python 01_computing_e/limit_definition.py
python 01_computing_e/factorial_series.py
python 01_computing_e/continued_fraction.py
python 01_computing_e/digit_extraction.py
python 01_computing_e/convergence_race.py
```

All outputs are written to `01_computing_e/outputs/`.

## Dependencies

- `numpy`, `matplotlib`, `mpmath`
- `utils/plot_style.py`, `utils/math_helpers.py` (shared utilities)
