# 🔢 Euler's Number — e = 2.71828...

> It's fascinating to think that humans like us **discovered** this number through curiosity and constant questioning. The number is already in the universe and could be found wherever continuous growth, decay, or change occurs — foundational to biology, physics, finance, and AI.

[![CI](https://github.com/pkrlfamous/2.71828-euler-s-number/actions/workflows/ci.yml/badge.svg)](https://github.com/pkrlfamous/2.71828-euler-s-number/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Scripts](https://img.shields.io/badge/scripts-80%2B-green.svg)](#modules-at-a-glance)

**80+ scripts** that compute, visualize, and demonstrate every known property and application of `e ≈ 2.71828` — across mathematics, physics, chemistry, biology, machine learning, finance, probability, nature, and art. Every script generates publication-quality dark-theme plots.

**You are encouraged to edit, update, create issues, and create pull requests.** I want everyone to know about this phenomenal number.

---

## What is e?

```
e = 2.71828182845904523536028747135266249...
  = lim(n→∞) (1 + 1/n)^n        ← Bernoulli's limit (1683)
  = 1 + 1 + 1/2! + 1/3! + 1/4!  ← Factorial series
  = [2; 1, 2, 1, 1, 4, 1, 1, 6] ← Continued fraction
  ∫₁ᵉ (1/t) dt = 1               ← Integral definition
```

**Why does e matter?**
- It's the **only** base whose exponential equals its own derivative: `d/dx(eˣ) = eˣ`
- Every neural network uses e (sigmoid, softmax, cross-entropy loss)
- It governs radioactive decay, compound interest, population growth, heat transfer
- It appears in Euler's identity: `e^(iπ) + 1 = 0` — "the most beautiful equation in mathematics"
- It appears in shells, galaxies, sunflowers, and spider webs (logarithmic spirals)

---

## Repository Structure

```
2.71828-euler-s-number/
│
├── utils/                          # Shared: plot styling + math helpers
├── tests/                          # 84+ unit tests
│
├── 01_computing_e/                 # How to compute e (5 scripts)
├── 02_calculus/                    # d/dx(eˣ)=eˣ, Taylor series, Wikipedia graph (8 scripts)
├── 03_trigonometry/                # Euler's formula e^(iθ)=cos+i·sin (5 scripts)
├── 04_complex_numbers/             # Cornu spiral, Mandelbrot, Riemann ζ (4 scripts)
├── 05_coordinate_systems/          # Logarithmic spiral, catenary, hyperbolic (5 scripts)
├── 06_nature_and_art/              # Shells, galaxies, sunflowers, spider webs (10 scripts)
├── 07_physics/                     # Decay, RC circuits, quantum, blackbody (9 scripts)
├── 08_chemistry_biology/           # Kinetics, Arrhenius, DNA, pharmacokinetics (9 scripts)
├── 09_computer_science_ml/         # Sigmoid, softmax, attention, entropy (11 scripts)
├── 10_finance/                     # Compound interest, Black-Scholes, PV (5 scripts)
├── 11_probability_statistics/      # Normal, Poisson, secretary problem (8 scripts)
├── 12_games_puzzles/               # Interactive terminal games (6 scripts)
│
└── docs/
    ├── FORMULAS.md                 # All 54+ formulas implemented
    ├── CONTRIBUTING.md
    └── RESOURCES.md
```

---

## Quick Start

```bash
git clone https://github.com/pkrlfamous/2.71828-euler-s-number.git
cd 2.71828-euler-s-number
pip install -r requirements.txt

# Run any script — outputs saved to the module's outputs/ folder
python 01_computing_e/limit_definition.py
python 02_calculus/derivative_equals_self.py
python 06_nature_and_art/phyllotaxis.py
python 09_computer_science_ml/sigmoid_function.py
python 11_probability_statistics/secretary_problem.py
```

---

## Modules at a Glance

### 📐 Module 1: Computing e
Five methods to compute e, compared side-by-side.

| Script | Description |
|--------|-------------|
| `limit_definition.py` | `(1+1/n)^n` converging to e — log-scale convergence + error |
| `factorial_series.py` | `Σ 1/n!` partial sums approaching e |
| `continued_fraction.py` | `e = [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]` convergents |
| `digit_extraction.py` | e to 1000 digits with digit frequency analysis |
| `convergence_race.py` | Race: which method reaches e fastest? |

### ∂ Module 2: Calculus
The fundamental reason e is special: it's its own derivative.

| Script | Description |
|--------|-------------|
| `derivative_equals_self.py` | `d/dx(eˣ) = eˣ` — two identical overlapping curves |
| `ax_vs_ex.py` | **Wikipedia graph**: 2^x, e^x, 4^x with tangent lines |
| `taylor_series.py` | 6-panel: polynomial adding terms → e^x |
| `ln_integral.py` | `∫₁ᵉ (1/t)dt = 1` — shaded area = exactly 1 |

### 🌀 Module 3: Trigonometry
Euler's formula connects e to circles, sin, and cos.

| Script | Description |
|--------|-------------|
| `euler_formula.py` | 3D helix: `e^(iθ) = cos(θ) + i·sin(θ)` with projections |
| `euler_identity.py` | `e^(iπ) + 1 = 0` — unit circle, all 5 constants |
| `sin_cos_from_exp.py` | Derive sin/cos from exponentials |
| `de_moivre.py` | Regular polygons inscribed in unit circle |
| `unit_circle_animation.py` | 8-frame unit circle tour |

### 🧲 Module 7: Physics

| Script | Formula |
|--------|---------|
| `radioactive_decay.py` | `N(t) = N₀·e^(-λt)` — C-14, U-238, Ra-226 |
| `capacitor_charge.py` | `V(t) = V₀(1 - e^(-t/RC))` — charge + discharge |
| `damped_oscillation.py` | `x(t) = A·e^(-γt)·cos(ωt)` — over/under/critical damping |
| `blackbody_radiation.py` | Planck: `1/(e^(hν/kT) - 1)` — Sun spectrum |
| `boltzmann_distribution.py` | `P(E) ∝ e^(-E/kT)` — statistical mechanics |

### 🧬 Module 8: Chemistry & Biology

| Script | Formula |
|--------|---------|
| `arrhenius_equation.py` | `k = A·e^(-Ea/RT)` — Arrhenius plot |
| `bacterial_growth.py` | `P(t) = P₀·e^(rt)` — E. coli growth |
| `logistic_growth.py` | `K/(1 + Ce^(-rt))` — carrying capacity |
| `carbon_dating.py` | `N(t) = N₀·e^(-t·ln2/5730)` — archaeology |
| `drug_metabolism.py` | Pharmacokinetics: single + multi-dose |

### 🤖 Module 9: Machine Learning
Every modern AI uses e.

| Script | Formula |
|--------|---------|
| `sigmoid_function.py` | `σ(x) = 1/(1+e^(-x))` with steepness comparison |
| `softmax_function.py` | `e^(xᵢ)/Σe^(xⱼ)` — temperature scaling |
| `attention_mechanism.py` | `softmax(QKᵀ/√d)·V` — transformer attention heatmap |
| `information_entropy.py` | `H = -Σ p·ln(p)` — Shannon entropy in nats |
| `cross_entropy_loss.py` | `L = -Σ y·ln(ŷ)` — why it trains neural nets |

### 💰 Module 10: Finance

| Script | Formula |
|--------|---------|
| `compound_interest.py` | `(1+r/n)^(nt) → e^(rt)` — Bernoulli's problem |
| `black_scholes.py` | `C = S·N(d₁) - K·e^(-rT)·N(d₂)` — options pricing |
| `present_value.py` | `PV = FV·e^(-rt)` — continuous discounting |

### 🎲 Module 11: Probability & Statistics

| Script | Description |
|--------|-------------|
| `derangement_problem.py` | Hat-check problem: `P → 1/e` as n → ∞ |
| `secretary_problem.py` | Optimal stopping: look at first `n/e` candidates |
| `poisson_distribution.py` | `P(k; λ) = λᵏe^(-λ)/k!` for λ = 1,3,5,10 |
| `stirling_approximation.py` | `n! ≈ √(2πn)·(n/e)^n` — accuracy vs n |
| `bernoulli_trials.py` | `(1-1/n)^n → 1/e` — slot machine problem |

### 🌿 Module 6: Nature & Art
e appears in shells, galaxies, sunflowers, and spider webs.

| Script | Description |
|--------|-------------|
| `phyllotaxis.py` | Sunflower seeds: golden angle vs off-angle vs rational |
| `logarithmic_spiral.py` | `r = e^(aθ)` — self-similar growth |
| `nautilus_shell.py` | Chambered nautilus cross-section |
| `galaxy_spiral.py` | Logarithmic spiral galaxy arms |
| `fractal_trees.py` | Recursive trees with `e^(-0.3)` branch scaling |

---

## Running Tests

```bash
pip install pytest

# Core mathematical correctness (84 tests)
pytest tests/test_math_helpers.py tests/test_formulas.py -v

# Smoke tests — verify all 80+ scripts run without errors
MPLBACKEND=Agg pytest tests/test_modules_importable.py -v
```

---

## Key Facts About e

| Property | Value |
|----------|-------|
| e (50 digits) | `2.71828182845904523536028747135266249775724709369995` |
| 1/e | `0.367879441171442...` (probability of derangement) |
| e² | `7.389056098930650...` |
| √e | `1.648721270700128...` |
| ln(2) | `0.693147180559945...` (half-life formula constant) |
| e^π | `23.140692632779269...` |
| e^(iπ) | `-1` (Euler's identity) |
| Discovered | Jacob Bernoulli, 1683 (compound interest) |
| Named 'e' | Leonhard Euler, 1731 |
| Irrationality | Proved by Euler, 1737 |
| Transcendence | Proved by Hermite, 1873 |

---

## Resources

See [docs/RESOURCES.md](docs/RESOURCES.md) for books, videos, papers, and tools.
See [docs/FORMULAS.md](docs/FORMULAS.md) for all 54 formulas implemented.

---

*"The most remarkable formula in mathematics." — Richard Feynman (on Euler's identity)*

*e = 2.71828182845904523536028747135266249775724709369995...*
