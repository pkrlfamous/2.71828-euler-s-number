# Complete Formula Reference — Euler's Number e

> e = 2.71828182845904523536028747135266249775724709369995...

---

## 1. Definitions of e

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 1 | `e = lim(n→∞) (1 + 1/n)^n` | Bernoulli's limit — compound interest origin | `01_computing_e/limit_definition.py` |
| 2 | `e = Σ(k=0→∞) 1/k! = 1 + 1 + 1/2 + 1/6 + 1/24 + ...` | Factorial series | `01_computing_e/factorial_series.py` |
| 3 | `e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, ...]` | Continued fraction | `01_computing_e/continued_fraction.py` |
| 4 | `∫₁ᵉ (1/t) dt = 1` | Integral definition of e | `02_calculus/ln_integral.py` |
| 5 | `e = lim(n→∞) n·(n^(1/n) - 1)` | Alternative limit | — |

---

## 2. Calculus Properties

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 6 | `d/dx(eˣ) = eˣ` | Self-derivative — THE defining property | `02_calculus/derivative_equals_self.py` |
| 7 | `∫eˣ dx = eˣ + C` | Self-integral | `02_calculus/integral_ex.py` |
| 8 | `d/dx(aˣ) = aˣ · ln(a)` | General exponential derivative | `02_calculus/ax_vs_ex.py` |
| 9 | `d/dx(ln x) = 1/x` | Natural log derivative | `02_calculus/natural_log_derivative.py` |
| 10 | `eˣ = Σ(n=0→∞) xⁿ/n! = 1 + x + x²/2! + x³/3! + ...` | Taylor / Maclaurin series | `02_calculus/taylor_series.py` |
| 11 | `ln(eˣ) = x` | Inverse relationship | — |

---

## 3. Complex Analysis — Euler's Formula

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 12 | `e^(iθ) = cos(θ) + i·sin(θ)` | **Euler's Formula** | `03_trigonometry/euler_formula.py` |
| 13 | `e^(iπ) + 1 = 0` | **Euler's Identity** — "most beautiful equation" | `03_trigonometry/euler_identity.py` |
| 14 | `sin(x) = (e^(ix) - e^(-ix)) / 2i` | Sine from exponentials | `03_trigonometry/sin_cos_from_exp.py` |
| 15 | `cos(x) = (e^(ix) + e^(-ix)) / 2` | Cosine from exponentials | `03_trigonometry/sin_cos_from_exp.py` |
| 16 | `(e^(iθ))^n = e^(inθ) = cos(nθ) + i·sin(nθ)` | De Moivre's theorem | `03_trigonometry/de_moivre.py` |
| 17 | `\|e^(iθ)\| = 1` | Unit modulus — traces unit circle | `03_trigonometry/unit_circle_animation.py` |

---

## 4. Hyperbolic Functions (all via e)

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 18 | `cosh(x) = (eˣ + e⁻ˣ) / 2` | Hyperbolic cosine | `05_coordinate_systems/hyperbolic_functions.py` |
| 19 | `sinh(x) = (eˣ - e⁻ˣ) / 2` | Hyperbolic sine | `05_coordinate_systems/hyperbolic_functions.py` |
| 20 | `tanh(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ)` | Hyperbolic tangent | `05_coordinate_systems/hyperbolic_functions.py` |
| 21 | `cosh²(x) - sinh²(x) = 1` | Pythagorean identity for hyperbola | `05_coordinate_systems/hyperbolic_functions.py` |
| 22 | `y = a·cosh(x/a)` | Catenary (hanging chain) | `05_coordinate_systems/catenary_curve.py` |

---

## 5. Geometry — Logarithmic Spiral

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 23 | `r = e^(aθ)` or `r = r₀·e^(aθ)` | Logarithmic spiral in polar coordinates | `05_coordinate_systems/polar_exponential.py` |
| 24 | `max of x^(1/x) occurs at x = e` | Steiner problem | `12_games_puzzles/steiner_problem.py` |

---

## 6. Physics

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 25 | `N(t) = N₀·e^(-λt)` | Radioactive decay | `07_physics/radioactive_decay.py` |
| 26 | `V(t) = V₀(1 - e^(-t/RC))` | Capacitor charging | `07_physics/capacitor_charge.py` |
| 27 | `x(t) = A·e^(-γt)·cos(ωt + φ)` | Damped harmonic oscillation | `07_physics/damped_oscillation.py` |
| 28 | `T(t) = Tₑ + (T₀-Tₑ)·e^(-kt)` | Newton's law of cooling | `07_physics/heat_equation.py` |
| 29 | `P(E) ∝ e^(-E/kT)` | Boltzmann distribution | `07_physics/boltzmann_distribution.py` |
| 30 | `ψ = A·e^(ikx - iωt)` | Quantum wave function | `07_physics/schrodinger.py` |
| 31 | `B(ν,T) = (2hν³/c²) · 1/(e^(hν/kT) - 1)` | Planck's radiation law | `07_physics/blackbody_radiation.py` |

---

## 7. Chemistry & Biology

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 32 | `k = A·e^(-Ea/RT)` | Arrhenius equation — reaction rate | `08_chemistry_biology/arrhenius_equation.py` |
| 33 | `[A](t) = [A]₀·e^(-kt)` | First-order chemical kinetics | `08_chemistry_biology/chemical_kinetics.py` |
| 34 | `P(t) = P₀·e^(rt)` | Bacterial exponential growth | `08_chemistry_biology/bacterial_growth.py` |
| 35 | `P(t) = K / (1 + Ce^(-rt))` | Logistic growth with carrying capacity | `08_chemistry_biology/logistic_growth.py` |
| 36 | `C(t) = C₀·e^(-kt)` | Drug metabolism (pharmacokinetics) | `08_chemistry_biology/drug_metabolism.py` |
| 37 | `N(t) = N₀·e^(-t·ln2/5730)` | Carbon-14 dating | `08_chemistry_biology/carbon_dating.py` |

---

## 8. Machine Learning & AI

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 38 | `σ(x) = 1 / (1 + e^(-x))` | **Sigmoid activation function** | `09_computer_science_ml/sigmoid_function.py` |
| 39 | `softmax(xᵢ) = e^(xᵢ) / Σⱼ e^(xⱼ)` | Softmax — output layer of classifiers | `09_computer_science_ml/softmax_function.py` |
| 40 | `L = -Σ yᵢ · ln(ŷᵢ)` | Cross-entropy loss (natural log = base e) | `09_computer_science_ml/cross_entropy_loss.py` |
| 41 | `lr(t) = lr₀ · e^(-λt)` | Exponential learning rate decay | `09_computer_science_ml/learning_rate_decay.py` |
| 42 | `H = -Σ pᵢ · ln(pᵢ)` | Shannon entropy in nats (base e) | `09_computer_science_ml/information_entropy.py` |
| 43 | `Attention = softmax(QKᵀ/√d) · V` | Transformer attention | `09_computer_science_ml/attention_mechanism.py` |

---

## 9. Finance & Economics

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 44 | `A = P·e^(rt)` | Continuous compounding | `10_finance/compound_interest.py` |
| 45 | `A = P(1 + r/n)^(nt) → Pe^(rt)` | Discrete → continuous limit | `10_finance/continuous_compounding.py` |
| 46 | `PV = FV · e^(-rt)` | Present value (continuous discounting) | `10_finance/present_value.py` |
| 47 | `C = S·N(d₁) - K·e^(-rT)·N(d₂)` | Black-Scholes call option | `10_finance/black_scholes.py` |

---

## 10. Probability & Statistics

| # | Formula | Description | Script |
|---|---------|-------------|--------|
| 48 | `f(x) = (1/σ√2π)·e^(-(x-μ)²/2σ²)` | Normal (Gaussian) distribution | `11_probability_statistics/normal_distribution.py` |
| 49 | `P(k; λ) = (λᵏ · e^(-λ)) / k!` | Poisson distribution | `11_probability_statistics/poisson_distribution.py` |
| 50 | `f(x; λ) = λ·e^(-λx)` | Exponential distribution (waiting times) | `11_probability_statistics/exponential_distribution.py` |
| 51 | `P(derangement) → 1/e ≈ 0.3679` | Hat-check problem | `11_probability_statistics/derangement_problem.py` |
| 52 | `Optimal stop at r = ⌊n/e⌋` | Secretary / optimal stopping problem | `11_probability_statistics/secretary_problem.py` |
| 53 | `(1 - 1/n)^n → 1/e` | Bernoulli trials convergence | `11_probability_statistics/bernoulli_trials.py` |
| 54 | `n! ≈ √(2πn) · (n/e)^n` | Stirling's approximation | `11_probability_statistics/stirling_approximation.py` |

---

## Key Properties Summary

| Property | Statement |
|----------|-----------|
| Self-derivative | d/dx(eˣ) = eˣ — unique among all functions |
| Base of natural log | ln(e) = 1, ln(eˣ) = x |
| Limit definition | (1 + 1/n)^n → e (discovered by Bernoulli, 1683) |
| Irrationality | e is irrational (proved by Euler, 1737) |
| Transcendence | e is transcendental (proved by Hermite, 1873) |
| Euler's identity | e^(iπ) + 1 = 0 (connects e, π, i, 1, 0) |
| Steiner's problem | x^(1/x) is maximized at x = e |
| Hat-check | Probability all items deranged → 1/e |
| Secretary | Optimal look-then-leap threshold is n/e |

---

*e was first discovered by Jacob Bernoulli in 1683 while studying compound interest.*
*Leonhard Euler introduced the notation 'e' in 1731.*
