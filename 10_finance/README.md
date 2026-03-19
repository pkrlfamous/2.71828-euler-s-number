# Module 10 — Finance

Euler's number **e** is the cornerstone of modern quantitative finance.  It
appears whenever money grows continuously, whenever options are priced, and
whenever future cash flows are discounted to the present.  This module traces
those appearances from Bernoulli's original problem (1683) to the
Black-Scholes equation (1973).

---

## Scripts

| File | Formula | Output |
|------|---------|--------|
| `compound_interest.py` | A = P(1+r/n)ⁿᵗ → Peʳᵗ | `compound_interest.png/svg` |
| `continuous_compounding.py` | A = P·eʳᵗ | `continuous_compounding.png/svg` |
| `black_scholes.py` | C = S·N(d₁) − K·e⁻ʳᵀ·N(d₂) | `black_scholes.png/svg` |
| `present_value.py` | PV = FV·e⁻ʳᵗ | `present_value.png/svg` |
| `mortgage_amortization.py` | M = P·(r/12)/(1−(1+r/12)⁻ⁿ) | `mortgage_amortization.png/svg` |

---

## Key Concepts

### Compound Interest — The Birth of e
Jacob Bernoulli (1683) asked: if a bank pays 100% interest, what is the
maximum value of $1 after one year?  With annual compounding the answer is $2.
With n compoundings per year it is (1 + 1/n)ⁿ.  As n → ∞ this converges to
**e ≈ 2.71828**.  This is why e is sometimes called "Napier's constant" or the
"natural base" — it is the mathematical limit of the compounding process.

### Continuous Compounding
When interest is compounded continuously, the balance grows as A = P·eʳᵗ.  The
effective annual rate becomes eʳ − 1, which is always slightly above the
nominal rate r.  The difference is small at low rates (5% nominal → 5.127%
effective) but non-negligible at higher rates (12% nominal → 12.75% effective).

### Present Value & Discounting
A dollar received t years from now is worth PV = FV·e⁻ʳᵗ today under
continuous discounting.  The discount factor e⁻ʳᵗ captures the time value of
money: at a 5% rate, a dollar 20 years out is worth only e⁻⁰·⁰⁵×²⁰ ≈ 37 cents
today.  The "Rule of 69" says the half-life of present value equals ln 2/r ≈
69/r%.

### Black-Scholes Options Pricing
The Black-Scholes formula for a European call option is:

    C = S·N(d₁) − K·e⁻ʳᵀ·N(d₂)

where d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T) and d₂ = d₁ − σ√T.  The term
K·e⁻ʳᵀ is the present value of the strike — the discounted cost of exercising
the option.  N(d₁) is the option's delta (sensitivity to stock price); N(d₂)
is the risk-neutral probability that the option expires in-the-money.

### Mortgage Amortization
The standard fixed-rate mortgage payment M = P·(r/12)/(1−(1+r/12)⁻ⁿ) can be
derived via a geometric series that is the discrete analogue of the continuous
formula for an exponentially decaying principal.  Early payments are mostly
interest; late payments are mostly principal — the crossover point (where
principal payment > interest payment) typically occurs past the halfway mark
in the loan term, demonstrating the asymmetric nature of exponential growth.

---

## Running the Scripts

```bash
cd 10_finance
python compound_interest.py
python continuous_compounding.py
python black_scholes.py
python present_value.py
python mortgage_amortization.py
```

Outputs are saved to `outputs/` as both `.png` and `.svg`.
