# 🔢 Euler's Number (e = 2.71828...) — Python Exploration

## A Comprehensive Guide to Computing, Visualizing & Demonstrating Every Property of `e`

**Repository:** `github.com/pkrlfamous/2.71828-euler-s-number`

---

## Table of Contents

1. [Project Vision](#project-vision)
2. [Repository Structure](#repository-structure)
3. [Setup & Dependencies](#setup--dependencies)
4. [Shared Utilities](#shared-utilities)
5. [Module 1: Computing e](#module-1-computing-e)
6. [Module 2: Calculus of e](#module-2-calculus-of-e)
7. [Module 3: e and Trigonometry](#module-3-e-and-trigonometry)
8. [Module 4: e in Complex Numbers](#module-4-e-in-complex-numbers)
9. [Module 5: e in Coordinate Systems](#module-5-e-in-coordinate-systems)
10. [Module 6: e in Nature & Art](#module-6-e-in-nature-and-art)
11. [Module 7: e in Physics](#module-7-e-in-physics)
12. [Module 8: e in Chemistry & Biology](#module-8-e-in-chemistry-and-biology)
13. [Module 9: e in Computer Science & ML/AI](#module-9-e-in-computer-science-and-mlai)
14. [Module 10: e in Finance & Economics](#module-10-e-in-finance-and-economics)
15. [Module 11: e in Probability & Statistics](#module-11-e-in-probability-and-statistics)
16. [Module 12: Games & Puzzles about e](#module-12-games-and-puzzles-about-e)
17. [Development Roadmap](#development-roadmap)
18. [Reference: All Formulas to Implement](#reference-all-formulas-to-implement)
19. [Claude Code Commands](#claude-code-commands)
20. [Resources](#resources)

---

## Project Vision

Build the most comprehensive pure-Python open-source project dedicated to Euler's number `e ≈ 2.71828`. This repository is a collection of 80+ scripts that compute, visualize, and demonstrate every known property and application of `e` across mathematics, science, art, and technology. Every script generates publication-quality plots saved as PNG/SVG.

**What makes this different:**
- Not just formulas — every concept has a runnable script with a beautiful plot
- Consistent dark-theme styling across all visualizations
- Reproduces key Wikipedia graphs (like the a^x comparison chart)
- Covers e's role in 10+ fields: calculus, physics, chemistry, biology, ML/AI, finance, probability, nature, art, and more
- Includes interactive terminal games and puzzles
- All outputs saved to `outputs/` folders for easy sharing

**Sister project:** The interactive Next.js website lives in a separate repo: `github.com/pkrlfamous/euler-website`

---

## Repository Structure

```
2.71828-euler-s-number/
│
├── README.md                          # Project overview with badges and sample outputs
├── LICENSE                            # MIT
├── .github/
│   └── workflows/
│       └── ci.yml                     # Auto-run linting + tests
│
├── requirements.txt                   # All Python dependencies
│
├── utils/
│   ├── __init__.py
│   ├── plot_style.py                  # Consistent plot styling (dark theme, fonts, colors)
│   └── math_helpers.py                # Common math utilities
│
├── 01_computing_e/
│   ├── README.md
│   ├── limit_definition.py            # lim (1 + 1/n)^n as n → ∞
│   ├── factorial_series.py            # e = Σ 1/n!
│   ├── continued_fraction.py          # e as continued fraction [2; 1, 2, 1, 1, 4, 1, ...]
│   ├── digit_extraction.py            # Compute e to N digits (arbitrary precision)
│   ├── convergence_race.py            # Compare convergence speed of different methods
│   └── outputs/                       # Generated plots saved here
│
├── 02_calculus/
│   ├── README.md
│   ├── derivative_equals_self.py      # d/dx(e^x) = e^x  ← THE key property
│   ├── integral_ex.py                 # ∫e^x dx = e^x + C
│   ├── taylor_series.py              # e^x = Σ x^n/n! (animated convergence)
│   ├── limit_definition_plot.py       # Visual: (1+1/n)^n approaching e
│   ├── ax_vs_ex.py                    # Compare d/dx(2^x), d/dx(e^x), d/dx(4^x) — Wikipedia graph
│   ├── tangent_line_slope1.py         # Show that at x=0, slope of e^x = 1 (red line from Wikipedia)
│   ├── natural_log_derivative.py      # d/dx(ln x) = 1/x
│   ├── ln_integral.py                # ∫(1/t)dt from 1 to e = 1
│   └── outputs/
│
├── 03_trigonometry/
│   ├── README.md
│   ├── euler_formula.py               # e^(iθ) = cos(θ) + i·sin(θ)
│   ├── euler_identity.py              # e^(iπ) + 1 = 0 — "most beautiful equation"
│   ├── sin_cos_from_exp.py            # sin(x) = (e^ix - e^-ix)/2i
│   ├── de_moivre.py                  # (e^iθ)^n = e^(inθ) — de Moivre's formula
│   ├── unit_circle_animation.py       # Animate e^(iθ) tracing the unit circle
│   └── outputs/
│
├── 04_complex_numbers/
│   ├── README.md
│   ├── complex_exp_map.py             # Map of e^z in the complex plane
│   ├── euler_spiral.py                # Cornu spiral / Euler spiral
│   ├── mandelbrot_connection.py       # e in fractal mathematics
│   ├── riemann_zeta.py                # Connection to ζ(s) and prime numbers
│   └── outputs/
│
├── 05_coordinate_systems/
│   ├── README.md
│   ├── polar_exponential.py           # r = e^(aθ) — logarithmic spiral
│   ├── parametric_curves.py           # Parametric curves involving e
│   ├── spherical_coordinates.py       # e in 3D coordinate systems
│   ├── catenary_curve.py              # y = a·cosh(x/a) = a(e^(x/a) + e^(-x/a))/2
│   ├── hyperbolic_functions.py        # sinh, cosh, tanh — all defined via e
│   └── outputs/
│
├── 06_nature_and_art/
│   ├── README.md
│   ├── logarithmic_spiral.py          # r = e^(aθ) — shells, galaxies, hurricanes
│   ├── golden_spiral_vs_log.py        # Compare golden spiral (φ) with e-based spiral
│   ├── phyllotaxis.py                 # Sunflower seed arrangement using e/φ
│   ├── nautilus_shell.py              # Plot nautilus shell cross-section
│   ├── galaxy_spiral.py              # Spiral galaxy arms (logarithmic spiral)
│   ├── fractal_trees.py              # L-system trees with exponential branching
│   ├── flower_petals.py              # Fibonacci petal counts and e connection
│   ├── spider_web.py                 # Logarithmic spiral in spider webs
│   ├── horn_growth.py                # Ram horns / animal horns growth curve
│   ├── population_nature.py          # Population growth in ecosystems
│   └── outputs/
│
├── 07_physics/
│   ├── README.md
│   ├── radioactive_decay.py           # N(t) = N₀·e^(-λt)
│   ├── capacitor_charge.py            # V(t) = V₀(1 - e^(-t/RC))
│   ├── damped_oscillation.py          # x(t) = A·e^(-γt)·cos(ωt + φ)
│   ├── heat_equation.py               # Newton's law of cooling: T(t) = Tₑ + (T₀-Tₑ)e^(-kt)
│   ├── wave_attenuation.py            # Wave amplitude decay
│   ├── boltzmann_distribution.py      # P(E) ∝ e^(-E/kT) — statistical mechanics
│   ├── schrodinger.py                 # e in quantum wave functions ψ = Ae^(ikx)
│   ├── blackbody_radiation.py         # Planck's law involves e^(hν/kT)
│   ├── relativity_rapidity.py         # Rapidity and hyperbolic functions (via e)
│   └── outputs/
│
├── 08_chemistry_biology/
│   ├── README.md
│   ├── chemical_kinetics.py           # First-order reaction: [A] = [A]₀·e^(-kt)
│   ├── arrhenius_equation.py          # k = A·e^(-Ea/RT) — reaction rate vs temperature
│   ├── ph_scale.py                   # pH = -log₁₀[H+] — logarithmic scale
│   ├── bacterial_growth.py            # P(t) = P₀·e^(rt) — exponential phase
│   ├── logistic_growth.py             # P(t) = K / (1 + ((K-P₀)/P₀)·e^(-rt))
│   ├── drug_metabolism.py             # C(t) = C₀·e^(-kt) — pharmacokinetics
│   ├── carbon_dating.py               # N(t) = N₀·e^(-t/τ) — archaeology
│   ├── dna_melting_curve.py           # Sigmoid curve in DNA denaturation
│   ├── enzyme_kinetics.py             # Michaelis-Menten with exponential components
│   └── outputs/
│
├── 09_computer_science_ml/
│   ├── README.md
│   ├── sigmoid_function.py            # σ(x) = 1/(1 + e^(-x)) — THE activation function
│   ├── softmax_function.py            # softmax(x_i) = e^(x_i) / Σe^(x_j)
│   ├── cross_entropy_loss.py          # L = -Σ y·log(ŷ) — uses natural log (base e)
│   ├── learning_rate_decay.py         # lr(t) = lr₀·e^(-λt) — exponential schedule
│   ├── normal_distribution_ml.py      # Gaussian: (1/σ√2π)·e^(-(x-μ)²/2σ²)
│   ├── batch_norm.py                 # Normalization using exponential moving average
│   ├── attention_mechanism.py         # softmax in transformer attention: e^(QK^T/√d)
│   ├── gradient_descent_viz.py        # Visualize loss landscape with exp surfaces
│   ├── information_entropy.py         # H = -Σ p·ln(p) — Shannon entropy (base e = nats)
│   ├── algorithm_complexity.py        # O(e^n) — exponential complexity visualization
│   ├── neural_network_init.py         # He/Xavier initialization uses e-based distributions
│   └── outputs/
│
├── 10_finance/
│   ├── README.md
│   ├── compound_interest.py           # A = P(1 + r/n)^(nt) → Pe^(rt) as n → ∞
│   ├── continuous_compounding.py      # Compare discrete vs continuous compounding
│   ├── black_scholes.py               # Options pricing: uses e^(-rT) and N(d)
│   ├── present_value.py               # PV = FV·e^(-rt) — continuous discounting
│   ├── mortgage_amortization.py       # Exponential decay of principal
│   └── outputs/
│
├── 11_probability_statistics/
│   ├── README.md
│   ├── normal_distribution.py         # Bell curve: (1/σ√2π)·e^(-(x-μ)²/2σ²)
│   ├── poisson_distribution.py        # P(k) = (λ^k · e^(-λ)) / k!
│   ├── exponential_distribution.py    # f(x) = λ·e^(-λx) — waiting times
│   ├── derangement_problem.py         # Hat check problem: P → 1/e as n → ∞
│   ├── secretary_problem.py           # Optimal stopping at n/e candidates
│   ├── birthday_problem.py            # Approximation using e
│   ├── bernoulli_trials.py            # (1-1/n)^n → 1/e — slot machine problem
│   ├── stirling_approximation.py      # n! ≈ √(2πn)·(n/e)^n
│   └── outputs/
│
├── 12_games_puzzles/
│   ├── README.md
│   ├── guess_the_digit.py             # Interactive: guess next digit of e
│   ├── e_memory_challenge.py          # Memorize digits of e
│   ├── compound_interest_game.py      # Discover e through compounding
│   ├── e_approximation_race.py        # Race: which method converges fastest?
│   ├── steiner_problem.py             # Find x that maximizes x^(1/x) → answer: e
│   ├── optimal_stopping_sim.py        # Secretary problem simulation
│   └── outputs/
│
└── docs/
    ├── CONTRIBUTING.md
    ├── FORMULAS.md                    # Complete formula reference
    └── RESOURCES.md                   # Books, papers, links
```

---

## Setup & Dependencies

### Requirements

```txt
# requirements.txt
numpy>=1.24.0
matplotlib>=3.7.0
scipy>=1.10.0
sympy>=1.12
mpmath>=1.3.0          # Arbitrary precision arithmetic
pillow>=10.0.0
seaborn>=0.12.0
plotly>=5.15.0         # Interactive HTML plots
manim>=0.17.0          # Mathematical animations (optional)
```

### Installation

```bash
git clone https://github.com/pkrlfamous/2.71828-euler-s-number.git
cd 2.71828-euler-s-number
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Running Scripts

```bash
# Run any script from the repo root
python 01_computing_e/limit_definition.py

# Outputs saved to the module's outputs/ folder
# e.g. 01_computing_e/outputs/limit_definition.png
```

### CI/CD

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install flake8 pytest
      - run: flake8 . --max-line-length=120
      - run: pytest tests/ -v
```

---

## Shared Utilities

### `utils/plot_style.py` — Every plot should look stunning and consistent

```python
"""
Shared plot styling for all e-related visualizations.
Dark theme with accent colors. All plots saved as PNG + SVG.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# Color palette
COLORS = {
    'e_gold': '#FFD700',
    'e_blue': '#4A90D9',
    'e_red': '#E74C3C',
    'e_green': '#2ECC71',
    'e_purple': '#9B59B6',
    'e_orange': '#F39C12',
    'e_cyan': '#00D2FF',
    'e_pink': '#FF6B9D',
    'bg_dark': '#1A1A2E',
    'bg_card': '#16213E',
    'text': '#EAEAEA',
    'grid': '#2A2A4A',
}

def apply_euler_style():
    """Apply consistent dark theme to all matplotlib plots."""
    plt.style.use('dark_background')
    mpl.rcParams.update({
        'figure.facecolor': COLORS['bg_dark'],
        'axes.facecolor': COLORS['bg_card'],
        'axes.edgecolor': COLORS['grid'],
        'axes.labelcolor': COLORS['text'],
        'text.color': COLORS['text'],
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'grid.color': COLORS['grid'],
        'grid.alpha': 0.3,
        'font.size': 12,
        'axes.titlesize': 16,
        'figure.figsize': (12, 8),
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
    })

def save_plot(fig, name, output_dir='outputs'):
    """Save figure as both PNG and SVG."""
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(f'{output_dir}/{name}.png')
    fig.savefig(f'{output_dir}/{name}.svg')
    print(f'Saved: {output_dir}/{name}.png and .svg')
```

### `utils/math_helpers.py` — Shared math utilities

```python
"""
Common math utilities used across modules.
"""
import numpy as np
from mpmath import mp, mpf, e as mp_e, factorial as mp_factorial

def compute_e_limit(n):
    """Compute e using limit definition: (1 + 1/n)^n"""
    return (1 + 1/n) ** n

def compute_e_series(terms):
    """Compute e using factorial series: Σ 1/k! for k=0..terms"""
    return sum(1 / np.math.factorial(k) for k in range(terms + 1))

def compute_e_digits(num_digits):
    """Compute e to arbitrary precision using mpmath."""
    mp.dps = num_digits + 5
    return str(mp_e)[:num_digits + 2]  # +2 for "2."

def numerical_derivative(f, x, h=1e-8):
    """Central difference numerical derivative."""
    return (f(x + h) - f(x - h)) / (2 * h)

def numerical_integral(f, a, b, n=10000):
    """Simpson's rule numerical integration."""
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return h/3 * (y[0] + y[-1] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]))
```

---

## Module 1: Computing e

**Purpose:** Show every known method to compute e, compare convergence speeds, and compute e to arbitrary precision.

### Scripts

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `limit_definition.py` | Compute `(1 + 1/n)^n` for n = 1 to 10^8 | Line plot showing convergence to e |
| `factorial_series.py` | Compute `Σ 1/n!` for increasing terms | Bar chart of partial sums approaching e |
| `continued_fraction.py` | e = [2; 1, 2, 1, 1, 4, 1, 1, 6, ...] | Convergent fractions plotted |
| `digit_extraction.py` | Use `mpmath` to compute e to N digits | Display e to 1000+ digits formatted beautifully |
| `convergence_race.py` | Race all methods against each other | Multi-line plot: error vs iterations |

### Key Code: `limit_definition.py`

```python
"""
Visualize the limit definition of e: lim(n→∞) (1 + 1/n)^n
Shows how the expression converges to e as n increases.
"""
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

n_values = np.logspace(0, 8, 1000)
approximations = (1 + 1/n_values) ** n_values

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Left: convergence curve
ax1.semilogx(n_values, approximations, color=COLORS['e_gold'], linewidth=2)
ax1.axhline(y=np.e, color=COLORS['e_red'], linestyle='--', linewidth=1.5,
            label=f'e ≈ {np.e:.10f}')
ax1.set_xlabel('n')
ax1.set_ylabel('(1 + 1/n)ⁿ')
ax1.set_title('Limit Definition: (1 + 1/n)ⁿ → e')
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)

# Right: error plot
errors = np.abs(approximations - np.e)
ax2.loglog(n_values, errors, color=COLORS['e_cyan'], linewidth=2)
ax2.set_xlabel('n')
ax2.set_ylabel('|approximation - e|')
ax2.set_title('Error Decreases as n → ∞')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
save_plot(fig, 'limit_definition', output_dir='01_computing_e/outputs')
plt.show()
```

### Key Code: `convergence_race.py`

```python
"""
Race: which method converges to e fastest?
Compare limit definition, factorial series, and continued fraction.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpmath import e as true_e
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

iterations = range(1, 25)

# Method 1: Limit (1 + 1/n)^n
limit_errors = [abs(float((1 + 1/n)**n - true_e)) for n in iterations]

# Method 2: Factorial series Σ 1/k!
series_vals = []
s = 0
for k in iterations:
    s += 1 / np.math.factorial(k - 1)
    series_vals.append(abs(s - float(true_e)))

# Method 3: Continued fraction convergents
def e_continued_fraction_convergents(n_terms):
    """Generate continued fraction convergents for e."""
    # e = [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]
    cf = [2]
    for k in range(1, n_terms + 1):
        if k % 3 == 2:
            cf.append(2 * (k // 3 + 1))
        else:
            cf.append(1)
    convergents = []
    for i in range(len(cf)):
        h_prev, h_curr = 1, cf[0]
        k_prev, k_curr = 0, 1
        for j in range(1, i + 1):
            h_prev, h_curr = h_curr, cf[j] * h_curr + h_prev
            k_prev, k_curr = k_curr, cf[j] * k_curr + k_prev
        convergents.append(abs(h_curr/k_curr - float(true_e)))
    return convergents

cf_errors = e_continued_fraction_convergents(24)

fig, ax = plt.subplots(figsize=(14, 8))
ax.semilogy(list(iterations), limit_errors, 'o-', color=COLORS['e_blue'],
            linewidth=2, label='Limit: (1+1/n)ⁿ', markersize=6)
ax.semilogy(list(iterations), series_vals, 's-', color=COLORS['e_gold'],
            linewidth=2, label='Series: Σ 1/k!', markersize=6)
ax.semilogy(range(len(cf_errors)), cf_errors, '^-', color=COLORS['e_green'],
            linewidth=2, label='Continued Fraction', markersize=6)
ax.set_xlabel('Iterations / Terms')
ax.set_ylabel('Absolute Error')
ax.set_title('🏎️ Convergence Race: Which Method Reaches e Fastest?')
ax.legend(fontsize=13)
ax.grid(True, alpha=0.3)

save_plot(fig, 'convergence_race', output_dir='01_computing_e/outputs')
plt.show()
```

---

## Module 2: Calculus of e

**Purpose:** Demonstrate the fundamental calculus property: d/dx(e^x) = e^x. This is THE core reason e matters.

### Scripts

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `derivative_equals_self.py` | Plot e^x and its derivative overlaid — they're identical | Two identical curves (mind-blowing visual) |
| `integral_ex.py` | Plot ∫e^x dx | Area under curve visualization |
| `taylor_series.py` | Animate adding Taylor terms: 1, +x, +x²/2!, +x³/3!... | Animated GIF of polynomial approaching e^x |
| `ax_vs_ex.py` | **Wikipedia graph reproduction**: Plot 2^x, e^x, 4^x with derivatives | Multi-curve with tangent lines |
| `tangent_line_slope1.py` | At x=0, e^x has slope = 1 (the red line from Wikipedia) | Zoomed plot at origin |
| `natural_log_derivative.py` | d/dx(ln x) = 1/x | Side-by-side: ln(x) and 1/x |
| `ln_integral.py` | ∫₁ᵉ (1/t) dt = 1 | Shaded area under 1/t curve |

### Key Code: `ax_vs_ex.py` — Wikipedia Graph Reproduction

```python
"""
Reproduce the Wikipedia graph from the e article:
Functions x ↦ aˣ for a = 2 (dotted), a = e (solid), a = 4 (dashed).
All pass through (0,1), but only eˣ has tangent line with slope 1 at origin.
The red line y = x + 1 is tangent to eˣ at x = 0.
"""
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

x = np.linspace(-2.5, 1.5, 500)
fig, ax = plt.subplots(figsize=(10, 8))

# Three exponential functions
ax.plot(x, 2**x, color=COLORS['e_blue'], linestyle=':', linewidth=2.5, label='a = 2 (dotted)')
ax.plot(x, np.exp(x), color=COLORS['e_blue'], linestyle='-', linewidth=3, label='a = e (solid)')
ax.plot(x, 4**x, color=COLORS['e_blue'], linestyle='--', linewidth=2.5, label='a = 4 (dashed)')

# Tangent line at origin: y = x + 1 (slope 1)
ax.plot(x, x + 1, color=COLORS['e_red'], linewidth=2.5, label='y = x + 1 (tangent to eˣ)')

# Mark the common point (0, 1)
ax.plot(0, 1, 'ko', markersize=10, zorder=5)
ax.annotate('(0, 1)', xy=(0, 1), xytext=(0.15, 1.2), fontsize=12,
            color=COLORS['text'], fontweight='bold')

# Axis settings
ax.set_xlim(-2.5, 1.5)
ax.set_ylim(-0.5, 4)
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
ax.set_title('The graphs of x ↦ aˣ — only eˣ has slope 1 at the origin', fontsize=15)
ax.legend(fontsize=12, loc='upper left')
ax.grid(True, alpha=0.2)

save_plot(fig, 'ax_vs_ex_wikipedia', output_dir='02_calculus/outputs')
plt.show()
```

### Key Code: `derivative_equals_self.py`

```python
"""
THE most important property of e: d/dx(eˣ) = eˣ
Plot eˣ and its numerical derivative — they overlap perfectly.
"""
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS
from utils.math_helpers import numerical_derivative

apply_euler_style()

x = np.linspace(-2, 3, 500)
y = np.exp(x)
dy = np.array([numerical_derivative(np.exp, xi) for xi in x])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Left: overlapping curves
ax1.plot(x, y, color=COLORS['e_gold'], linewidth=3, label='eˣ')
ax1.plot(x, dy, color=COLORS['e_red'], linewidth=2, linestyle='--', label="d/dx(eˣ)")
ax1.set_title('eˣ and its derivative are IDENTICAL', fontsize=15)
ax1.legend(fontsize=13)
ax1.grid(True, alpha=0.3)

# Right: the error (should be ~0 everywhere)
error = np.abs(y - dy)
ax2.semilogy(x, error, color=COLORS['e_cyan'], linewidth=2)
ax2.set_title('Difference |eˣ - d/dx(eˣ)| ≈ 0 (numerical precision)', fontsize=13)
ax2.set_ylabel('Absolute Error')
ax2.grid(True, alpha=0.3)

plt.suptitle('d/dx(eˣ) = eˣ — The defining property of Euler\'s number', fontsize=16, y=1.02)
plt.tight_layout()
save_plot(fig, 'derivative_equals_self', output_dir='02_calculus/outputs')
plt.show()
```

### Key Code: `taylor_series.py`

```python
"""
Animate the Taylor series for eˣ: adding terms one at a time.
eˣ = 1 + x + x²/2! + x³/3! + x⁴/4! + ...
Watch the polynomial approximate eˣ more closely with each term.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

x = np.linspace(-4, 4, 500)
max_terms = 12

fig, ax = plt.subplots(figsize=(12, 8))

def taylor_e(x, n_terms):
    """Compute Taylor polynomial of eˣ with n_terms."""
    result = np.zeros_like(x)
    for k in range(n_terms):
        result += x**k / np.math.factorial(k)
    return result

def animate(frame):
    ax.clear()
    ax.plot(x, np.exp(x), color=COLORS['e_gold'], linewidth=3, label='eˣ (exact)', alpha=0.7)
    n = frame + 1
    y_approx = taylor_e(x, n)
    ax.plot(x, y_approx, color=COLORS['e_cyan'], linewidth=2.5,
            label=f'Taylor polynomial (n={n-1})')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-2, 20)
    ax.set_title(f'Taylor Series: eˣ ≈ Σ xⁿ/n! — using {n} terms', fontsize=15)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

anim = FuncAnimation(fig, animate, frames=max_terms, interval=800, repeat=True)
os.makedirs('02_calculus/outputs', exist_ok=True)
anim.save('02_calculus/outputs/taylor_series.gif', writer=PillowWriter(fps=1.5))
print('Saved: 02_calculus/outputs/taylor_series.gif')
plt.show()
```

---

## Module 3: e and Trigonometry

**Purpose:** Show how e connects to sine and cosine through Euler's formula — arguably the most beautiful equation in mathematics.

### Scripts

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `euler_formula.py` | e^(iθ) = cos(θ) + i·sin(θ) | 3D helix: x=cos(θ), y=sin(θ), z=θ |
| `euler_identity.py` | e^(iπ) + 1 = 0 | Artistic visualization of the 5 constants |
| `sin_cos_from_exp.py` | Derive sin/cos from exponentials | Split-view: exponential → trig |
| `de_moivre.py` | Powers of complex exponentials | Animated points on unit circle |
| `unit_circle_animation.py` | e^(iθ) traces the unit circle | Animated GIF of point moving on circle |

### Key Code: `euler_formula.py`

```python
"""
Euler's Formula: e^(iθ) = cos(θ) + i·sin(θ)
Visualize as a 3D helix — the real part is cos, imaginary is sin,
and the vertical axis is θ.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

theta = np.linspace(0, 4 * np.pi, 1000)
x = np.cos(theta)  # Real part
y = np.sin(theta)  # Imaginary part

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 3D helix
ax.plot(x, y, theta, color=COLORS['e_gold'], linewidth=2.5)

# Projections
ax.plot(x, y, zs=0, zdir='z', color=COLORS['e_blue'], alpha=0.4, linewidth=1)  # Unit circle
ax.plot(x, theta, zs=1.2, zdir='y', color=COLORS['e_red'], alpha=0.4, linewidth=1)  # cos(θ)
ax.plot(y, theta, zs=-1.2, zdir='x', color=COLORS['e_green'], alpha=0.4, linewidth=1)  # sin(θ)

ax.set_xlabel('cos(θ) — Real', fontsize=12)
ax.set_ylabel('sin(θ) — Imaginary', fontsize=12)
ax.set_zlabel('θ', fontsize=12)
ax.set_title('Euler\'s Formula: e^(iθ) = cos(θ) + i·sin(θ)\nA helix in 3D', fontsize=15)

save_plot(fig, 'euler_formula_3d', output_dir='03_trigonometry/outputs')
plt.show()
```

---

## Module 4: e in Complex Numbers

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `complex_exp_map.py` | Color map of e^z in complex plane | Domain coloring visualization |
| `euler_spiral.py` | Cornu spiral (Fresnel integrals) | Elegant double spiral |
| `mandelbrot_connection.py` | e in fractal escape-time algorithms | Fractal with e-based coloring |
| `riemann_zeta.py` | ζ(s) = Σ 1/n^s and its connection to e | Critical line visualization |

---

## Module 5: e in Coordinate Systems

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `polar_exponential.py` | r = e^(aθ) — logarithmic spiral | Spiral with varying 'a' parameter |
| `parametric_curves.py` | Lissajous-like curves with e^t components | Parametric art |
| `catenary_curve.py` | Hanging chain: y = a·cosh(x/a) | Plot + real-world comparison |
| `hyperbolic_functions.py` | sinh, cosh, tanh — all from e | Family of curves |

---

## Module 6: e in Nature and Art

**Purpose:** This is the "wow factor" module. Show how e appears in shells, galaxies, flowers, and living organisms.

### Scripts

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `logarithmic_spiral.py` | r = e^(aθ) overlaid on shell photos | Mathematical spiral on nature images |
| `golden_spiral_vs_log.py` | Compare φ-based golden spiral with e-spiral | Side-by-side spirals |
| `phyllotaxis.py` | Sunflower seed arrangement using golden angle | Dot pattern (Vogel's model) |
| `nautilus_shell.py` | Cross-section of chambered nautilus | Mathematical curve + shell overlay |
| `galaxy_spiral.py` | Logarithmic spiral arms of galaxies | Simulated galaxy with spiral fit |
| `fractal_trees.py` | L-system trees with exponential branching | Recursive tree drawings |
| `flower_petals.py` | Why flowers have Fibonacci petal counts | Petal arrangement simulation |
| `spider_web.py` | Logarithmic spiral web | Web pattern plot |
| `horn_growth.py` | Ram horn growth as logarithmic spiral | Growth curve animation |
| `population_nature.py` | Population growth in ecosystems | Time-series growth curves |

### Key Code: `phyllotaxis.py`

```python
"""
Sunflower seed pattern using Vogel's model.
The golden angle (≈137.5°) produces the most efficient packing.
e connects to this through the logarithmic spiral — seed positions
follow r = c·√n, θ = n·golden_angle, and the underlying spiral is logarithmic.
"""
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

n = 2000
golden_angle = np.pi * (3 - np.sqrt(5))  # ≈ 137.508° in radians

theta = np.arange(n) * golden_angle
r = np.sqrt(np.arange(n))

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Left: sunflower pattern with golden angle
colors = np.arange(n)
axes[0].scatter(r * np.cos(theta), r * np.sin(theta),
                c=colors, cmap='YlOrBr', s=4, alpha=0.8)
axes[0].set_aspect('equal')
axes[0].set_title(f'Golden Angle ≈ 137.508°\n{n} seeds — optimal packing', fontsize=13)
axes[0].axis('off')

# Middle: slightly off angle — shows gaps
bad_angle = 2.4  # close to golden but not quite
theta_bad = np.arange(n) * bad_angle
axes[1].scatter(r * np.cos(theta_bad), r * np.sin(theta_bad),
                c=colors, cmap='Blues', s=4, alpha=0.8)
axes[1].set_aspect('equal')
axes[1].set_title(f'Angle = 137.6° (slightly off)\nGaps appear!', fontsize=13)
axes[1].axis('off')

# Right: rational angle — obvious spokes
rational_angle = 2 * np.pi / 7
theta_rational = np.arange(n) * rational_angle
axes[2].scatter(r * np.cos(theta_rational), r * np.sin(theta_rational),
                c=colors, cmap='Reds', s=4, alpha=0.8)
axes[2].set_aspect('equal')
axes[2].set_title(f'Rational Angle (2π/7)\nWasted space in spokes', fontsize=13)
axes[2].axis('off')

plt.suptitle('Phyllotaxis: Nature Optimizes Seed Packing with the Golden Angle', fontsize=16, y=1.02)
plt.tight_layout()
save_plot(fig, 'phyllotaxis', output_dir='06_nature_and_art/outputs')
plt.show()
```

---

## Module 7: e in Physics

| Script | What It Does | Key Formula |
|--------|-------------|-------------|
| `radioactive_decay.py` | Half-life visualization | N(t) = N₀·e^(-λt) |
| `capacitor_charge.py` | RC circuit charging/discharging | V(t) = V₀(1 - e^(-t/RC)) |
| `damped_oscillation.py` | Spring-mass with damping | x(t) = A·e^(-γt)·cos(ωt) |
| `heat_equation.py` | Newton's cooling law | T(t) = Tₑ + (T₀-Tₑ)·e^(-kt) |
| `boltzmann_distribution.py` | Energy distribution at temperature T | P(E) ∝ e^(-E/kT) |
| `schrodinger.py` | Quantum wave function | ψ = A·e^(ikx - iωt) |
| `blackbody_radiation.py` | Planck's radiation law | B(ν,T) involves e^(hν/kT) |
| `wave_attenuation.py` | Wave amplitude decay | Exponential envelope |
| `relativity_rapidity.py` | Rapidity and hyperbolic functions | via e |

---

## Module 8: e in Chemistry & Biology

| Script | What It Does | Key Formula |
|--------|-------------|-------------|
| `chemical_kinetics.py` | First-order reaction | [A] = [A]₀·e^(-kt) |
| `arrhenius_equation.py` | Reaction rate vs temperature | k = A·e^(-Ea/RT) |
| `ph_scale.py` | Logarithmic pH scale | pH = -log₁₀[H+] |
| `bacterial_growth.py` | Exponential growth phase | P(t) = P₀·e^(rt) |
| `logistic_growth.py` | Carrying capacity model | P(t) = K/(1 + Ce^(-rt)) |
| `drug_metabolism.py` | Pharmacokinetics | C(t) = C₀·e^(-kt) |
| `carbon_dating.py` | Archaeological dating | N(t) = N₀·e^(-t/τ) |
| `dna_melting_curve.py` | DNA denaturation sigmoid | Fraction vs temperature |
| `enzyme_kinetics.py` | Michaelis-Menten | Exponential components |

---

## Module 9: e in Computer Science & ML/AI

**Purpose:** Show how e powers modern AI. Every neural network uses e through sigmoid, softmax, and loss functions.

### Scripts

| Script | What It Does | Why It Matters for AI |
|--------|-------------|----------------------|
| `sigmoid_function.py` | σ(x) = 1/(1+e^(-x)) with adjustable steepness | Logistic regression, old neural nets |
| `softmax_function.py` | Convert logits to probabilities | Every classifier's output layer |
| `cross_entropy_loss.py` | L = -Σ y·ln(ŷ) | The loss function that trains neural nets |
| `learning_rate_decay.py` | lr(t) = lr₀·e^(-λt) | Training stability |
| `normal_distribution_ml.py` | Gaussian distribution | Weight initialization, VAEs |
| `attention_mechanism.py` | softmax(QK^T/√d) | Transformers — ChatGPT, Claude |
| `information_entropy.py` | H = -Σ p·ln(p) | Information theory foundation |
| `gradient_descent_viz.py` | Loss landscape with exp surfaces | Optimization visualization |
| `algorithm_complexity.py` | O(e^n) exponential complexity | Complexity classes |
| `batch_norm.py` | Exponential moving average | Training normalization |
| `neural_network_init.py` | He/Xavier initialization | e-based distributions |

### Key Code: `sigmoid_function.py`

```python
"""
The sigmoid function: σ(x) = 1 / (1 + e^(-kx))
Interactive exploration with different steepness values.
Also shows the derivative: σ'(x) = σ(x)(1 - σ(x))
"""
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

x = np.linspace(-10, 10, 1000)

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Panel 1: Different steepness
steepness_colors = [COLORS['e_blue'], COLORS['e_gold'], COLORS['e_red'], COLORS['e_green']]
for k, color in zip([0.5, 1, 2, 5], steepness_colors):
    y = 1 / (1 + np.exp(-k * x))
    axes[0].plot(x, y, color=color, linewidth=2.5, label=f'k = {k}')
axes[0].axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
axes[0].set_title('Sigmoid: varying steepness (k)', fontsize=14)
axes[0].set_xlabel('x')
axes[0].set_ylabel('σ(x)')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

# Panel 2: Softmax temperature scaling
logits = np.array([2.0, 1.0, 0.1])
temps = [0.5, 1.0, 2.0, 5.0]
temp_colors = [COLORS['e_red'], COLORS['e_gold'], COLORS['e_blue'], COLORS['e_green']]
x_pos = np.arange(3)
width = 0.18
for i, (T, color) in enumerate(zip(temps, temp_colors)):
    probs = np.exp(logits / T) / np.sum(np.exp(logits / T))
    axes[1].bar(x_pos + i * width, probs, width=width, color=color,
                label=f'T = {T}', alpha=0.9)
axes[1].set_xticks(x_pos + width * 1.5)
axes[1].set_xticklabels(['Class A', 'Class B', 'Class C'])
axes[1].set_title('Softmax Temperature Scaling', fontsize=14)
axes[1].set_ylabel('Probability')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3, axis='y')

# Panel 3: Cross-entropy loss
y_hat = np.linspace(0.01, 0.99, 200)
axes[2].plot(y_hat, -np.log(y_hat), color=COLORS['e_red'], linewidth=2.5, label='Loss when y=1')
axes[2].plot(y_hat, -np.log(1 - y_hat), color=COLORS['e_blue'], linewidth=2.5, label='Loss when y=0')
axes[2].set_xlabel('Predicted probability ŷ')
axes[2].set_ylabel('Loss')
axes[2].set_title('Cross-Entropy Loss', fontsize=14)
axes[2].legend(fontsize=11)
axes[2].grid(True, alpha=0.3)

plt.suptitle('e Powers Every Neural Network: Sigmoid, Softmax & Cross-Entropy', fontsize=16, y=1.02)
plt.tight_layout()
save_plot(fig, 'sigmoid_softmax_ce', output_dir='09_computer_science_ml/outputs')
plt.show()
```

---

## Module 10: e in Finance & Economics

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `compound_interest.py` | Bernoulli's original problem | Table + plot: discrete → continuous |
| `continuous_compounding.py` | Compare annual, monthly, daily, continuous | Convergence to Pe^(rt) |
| `black_scholes.py` | Options pricing model | Call option price surface |
| `present_value.py` | Discounting future cash flows | PV curve |
| `mortgage_amortization.py` | Exponential decay of principal | Amortization chart |

---

## Module 11: e in Probability & Statistics

| Script | What It Does | Key Visual |
|--------|-------------|------------|
| `normal_distribution.py` | The bell curve | Animated: changing μ and σ |
| `poisson_distribution.py` | Event counting | Bar chart with e-based formula |
| `derangement_problem.py` | Hat check problem (→ 1/e) | Probability convergence plot |
| `secretary_problem.py` | Optimal stopping at n/e | Simulation with success rate |
| `bernoulli_trials.py` | Slot machine: (1-1/n)^n → 1/e | Probability of losing all bets |
| `stirling_approximation.py` | n! ≈ √(2πn)·(n/e)^n | Actual vs approximated factorial |
| `exponential_distribution.py` | Waiting time distribution | f(x) = λ·e^(-λx) |
| `birthday_problem.py` | Birthday approximation using e | Probability curve |

---

## Module 12: Games & Puzzles about e

| Script | What It Does | Interaction |
|--------|-------------|-------------|
| `guess_the_digit.py` | Given first N digits, guess the (N+1)th | Terminal input game |
| `e_memory_challenge.py` | Memorize as many digits as possible | Timer + scoring |
| `compound_interest_game.py` | Discover e by choosing compounding frequency | Guided discovery |
| `e_approximation_race.py` | Race: limit vs series vs continued fraction | Visual race animation |
| `steiner_problem.py` | Find x that maximizes x^(1/x) → answer: e | Interactive slider |
| `optimal_stopping_sim.py` | Play the secretary problem 100 times | Win rate → 1/e ≈ 37% |

---

## Development Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Set up repository structure with all folders
- [ ] Create `utils/plot_style.py` and `utils/math_helpers.py`
- [ ] Build Module 1: Computing e (all 5 scripts)
- [ ] Build Module 2: Calculus (all 8 scripts) — reproduce Wikipedia graphs
- [ ] Write module-level README.md files

### Phase 2: Core Math (Week 3-4)
- [ ] Build Module 3: Trigonometry (all 5 scripts)
- [ ] Build Module 4: Complex Numbers (all 4 scripts)
- [ ] Build Module 5: Coordinate Systems (all 5 scripts)
- [ ] Add tests for math_helpers.py

### Phase 3: Applications (Week 5-7)
- [ ] Build Module 7: Physics (all 9 scripts)
- [ ] Build Module 8: Chemistry & Biology (all 9 scripts)
- [ ] Build Module 9: ML/AI (all 11 scripts)
- [ ] Build Module 10: Finance (all 5 scripts)

### Phase 4: Art, Probability & Games (Week 8-10)
- [ ] Build Module 6: Nature & Art (all 10 scripts)
- [ ] Build Module 11: Probability & Statistics (all 8 scripts)
- [ ] Build Module 12: Games & Puzzles (all 6 scripts)

### Phase 5: Polish & Share (Week 11-12)
- [ ] Write comprehensive root README.md with sample output images
- [ ] Create `docs/FORMULAS.md` with all 38 formulas
- [ ] Create `docs/CONTRIBUTING.md`
- [ ] Create `docs/RESOURCES.md`
- [ ] Add GitHub badges (CI, license, Python version)
- [ ] Share on Reddit r/math, r/Python, r/datascience, Hacker News

---

## Reference: All Formulas to Implement

### Definitions of e
| # | Formula | Script Location |
|---|---------|-----------------|
| 1 | `e = lim(n→∞) (1 + 1/n)^n` | `01_computing_e/limit_definition.py` |
| 2 | `e = Σ(n=0→∞) 1/n!` | `01_computing_e/factorial_series.py` |
| 3 | `e = [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]` | `01_computing_e/continued_fraction.py` |
| 4 | `∫₁ᵉ (1/t) dt = 1` | `02_calculus/ln_integral.py` |

### Calculus Properties
| # | Formula | Script Location |
|---|---------|-----------------|
| 5 | `d/dx(eˣ) = eˣ` | `02_calculus/derivative_equals_self.py` |
| 6 | `∫eˣ dx = eˣ + C` | `02_calculus/integral_ex.py` |
| 7 | `d/dx(aˣ) = aˣ · ln(a)` | `02_calculus/ax_vs_ex.py` |
| 8 | `d/dx(ln x) = 1/x` | `02_calculus/natural_log_derivative.py` |
| 9 | `eˣ = Σ xⁿ/n!` | `02_calculus/taylor_series.py` |

### Complex Analysis
| # | Formula | Script Location |
|---|---------|-----------------|
| 10 | `e^(iθ) = cos(θ) + i·sin(θ)` | `03_trigonometry/euler_formula.py` |
| 11 | `e^(iπ) + 1 = 0` | `03_trigonometry/euler_identity.py` |
| 12 | `sin(x) = (e^(ix) - e^(-ix)) / 2i` | `03_trigonometry/sin_cos_from_exp.py` |
| 13 | `cos(x) = (e^(ix) + e^(-ix)) / 2` | `03_trigonometry/sin_cos_from_exp.py` |

### Physics
| # | Formula | Script Location |
|---|---------|-----------------|
| 14 | `N(t) = N₀·e^(-λt)` | `07_physics/radioactive_decay.py` |
| 15 | `V(t) = V₀(1 - e^(-t/RC))` | `07_physics/capacitor_charge.py` |
| 16 | `x(t) = A·e^(-γt)·cos(ωt)` | `07_physics/damped_oscillation.py` |
| 17 | `P(E) ∝ e^(-E/kT)` | `07_physics/boltzmann_distribution.py` |
| 18 | `ψ = A·e^(ikx - iωt)` | `07_physics/schrodinger.py` |
| 19 | `T(t) = Tₑ + (T₀-Tₑ)·e^(-kt)` | `07_physics/heat_equation.py` |

### Chemistry & Biology
| # | Formula | Script Location |
|---|---------|-----------------|
| 20 | `k = A·e^(-Ea/RT)` | `08_chemistry_biology/arrhenius_equation.py` |
| 21 | `P(t) = P₀·e^(rt)` | `08_chemistry_biology/bacterial_growth.py` |
| 22 | `P(t) = K/(1 + Ce^(-rt))` | `08_chemistry_biology/logistic_growth.py` |
| 23 | `C(t) = C₀·e^(-kt)` | `08_chemistry_biology/drug_metabolism.py` |

### ML/AI
| # | Formula | Script Location |
|---|---------|-----------------|
| 24 | `σ(x) = 1/(1 + e^(-x))` | `09_computer_science_ml/sigmoid_function.py` |
| 25 | `softmax(xᵢ) = e^(xᵢ)/Σe^(xⱼ)` | `09_computer_science_ml/softmax_function.py` |
| 26 | `L = -Σ y·ln(ŷ)` | `09_computer_science_ml/cross_entropy_loss.py` |
| 27 | `lr(t) = lr₀·e^(-λt)` | `09_computer_science_ml/learning_rate_decay.py` |
| 28 | `H = -Σ p·ln(p)` | `09_computer_science_ml/information_entropy.py` |

### Finance
| # | Formula | Script Location |
|---|---------|-----------------|
| 29 | `A = P·e^(rt)` | `10_finance/compound_interest.py` |
| 30 | `PV = FV·e^(-rt)` | `10_finance/present_value.py` |

### Probability
| # | Formula | Script Location |
|---|---------|-----------------|
| 31 | `f(x) = (1/σ√2π)·e^(-(x-μ)²/2σ²)` | `11_probability_statistics/normal_distribution.py` |
| 32 | `P(k) = (λᵏ·e^(-λ))/k!` | `11_probability_statistics/poisson_distribution.py` |
| 33 | `n! ≈ √(2πn)·(n/e)ⁿ` | `11_probability_statistics/stirling_approximation.py` |
| 34 | `P(derangement) → 1/e` | `11_probability_statistics/derangement_problem.py` |
| 35 | `Optimal stop at n/e` | `11_probability_statistics/secretary_problem.py` |

### Geometry
| # | Formula | Script Location |
|---|---------|-----------------|
| 36 | `r = e^(aθ)` | `05_coordinate_systems/polar_exponential.py` |
| 37 | `y = a·cosh(x/a)` | `05_coordinate_systems/catenary_curve.py` |
| 38 | `max of x^(1/x) at x = e` | `12_games_puzzles/steiner_problem.py` |

---

## Claude Code Commands

Feed these prompts to Claude Code in sequence:

```
1. "Set up the repo structure as defined in PYTHON_PROJECT_PLAN.md — create all folders, empty README.md files, and the requirements.txt"
2. "Build utils/plot_style.py and utils/math_helpers.py exactly as specified in the plan"
3. "Build 01_computing_e/ — all 5 scripts. Each script should import from utils/, generate plots, and save to outputs/"
4. "Build 02_calculus/ — all 8 scripts. Reproduce the Wikipedia e^x comparison graph in ax_vs_ex.py"
5. "Build 03_trigonometry/ — all 5 scripts including the 3D Euler formula helix"
6. "Build 04_complex_numbers/ — all 4 scripts with domain coloring"
7. "Build 05_coordinate_systems/ — all 5 scripts including catenary and hyperbolic functions"
8. "Build 06_nature_and_art/ — all 10 scripts. Make the phyllotaxis comparison (3 panels)"
9. "Build 07_physics/ — all 9 scripts with real physical parameter values"
10. "Build 08_chemistry_biology/ — all 9 scripts"
11. "Build 09_computer_science_ml/ — all 11 scripts. Make the sigmoid/softmax/CE triple panel"
12. "Build 10_finance/ — all 5 scripts"
13. "Build 11_probability_statistics/ — all 8 scripts"
14. "Build 12_games_puzzles/ — all 6 terminal games"
15. "Write the root README.md with badges, project description, sample outputs, and getting started guide"
16. "Write docs/FORMULAS.md, docs/CONTRIBUTING.md, and docs/RESOURCES.md"
```

---

## Resources

- **Wikipedia**: https://en.wikipedia.org/wiki/E_(mathematical_constant)
- **Euler's Number in ML**: https://www.ml-science.com/eulers-number
- **DataCamp Tutorial**: https://www.datacamp.com/tutorial/eulers-number
- **3Blue1Brown**: "What's so special about Euler's number e?" (YouTube)
- **Mathologer**: "e to the pi i for dummies" (YouTube)
- **Better Explained**: https://betterexplained.com/articles/an-intuitive-guide-to-exponential-functions-e/
- **mpmath Documentation**: https://mpmath.org/doc/current/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/

---

*Built with curiosity and the constant that powers the universe: e = 2.71828182845904523536028747135266249775724709369995...*
