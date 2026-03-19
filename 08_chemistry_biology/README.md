# Module 08 — Chemistry & Biology

Euler's number **e** is central to chemistry and biology: reaction rates,
population dynamics, pH logarithms, enzyme kinetics, and DNA biophysics all
express themselves through exponential and logistic functions.

## Scripts

| Script | Domain | Key Formula |
|---|---|---|
| `chemical_kinetics.py` | Reaction kinetics | [A](t) = [A]₀ e^{−kt} |
| `arrhenius_equation.py` | Thermochemistry | k = A e^{−Ea/RT} |
| `ph_scale.py` | Acid-base chemistry | pH = −ln[H⁺] / ln 10 |
| `bacterial_growth.py` | Microbiology | P(t) = P₀ e^{rt} |
| `logistic_growth.py` | Population ecology | P(t) = K / (1 + ((K−P₀)/P₀) e^{−rt}) |
| `drug_metabolism.py` | Pharmacokinetics | C(t) = C₀ e^{−k_e t} |
| `carbon_dating.py` | Geochronology | N(t) = N₀ e^{−λt}, t½ = 5 730 yr |
| `dna_melting_curve.py` | Molecular biology | F(T) = 1 / (1 + e^{−k(T−Tm)}) |
| `enzyme_kinetics.py` | Biochemistry | v = Vmax·[S] / (Km + [S]) |

## Running All Scripts

```bash
cd 08_chemistry_biology
for script in *.py; do python "$script"; done
```

Outputs (PNG + SVG) are written to `08_chemistry_biology/outputs/`.

## Key Concepts

### First-Order Kinetics
Rate law d[A]/dt = −k[A] gives [A](t) = [A]₀ e^{−kt}.  Half-life t₁/₂ = ln 2 / k
depends only on k, not on initial concentration — a defining feature of
first-order processes.

### Arrhenius Equation
The exponential factor e^{−Ea/RT} describes the fraction of molecular collisions
that have enough energy to overcome the activation barrier.  An Arrhenius plot
(ln k vs 1/T) is linear with slope −Ea/R.

### pH and Natural Logarithm
pH = −log₁₀[H⁺] = −ln[H⁺] / ln(10), so every pH unit represents exactly a
10-fold change in hydrogen ion activity.  Logarithms to any base are natural
logarithms divided by a constant.

### Logistic Growth
Pure exponential growth P₀ e^{rt} is modified by the carrying capacity K via
the logistic equation, which has an exact closed-form solution involving e.

### DNA Melting
The fraction of denatured double-stranded DNA is well described by the
logistic sigmoid F(T) = 1/(1 + e^{−k(T−Tm)}), where Tm increases with
GC content because G–C base pairs have three hydrogen bonds vs. two for A–T.
