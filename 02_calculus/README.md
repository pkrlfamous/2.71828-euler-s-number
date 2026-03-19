# Module 02 — Calculus with Euler's Number e

This module demonstrates the central role Euler's number **e** plays in
differential and integral calculus: its exponential function is its own
derivative and antiderivative, the natural logarithm has the uniquely simple
derivative 1/x, and the limit definition ties to compound interest.

---

## Scripts

### 1. `derivative_equals_self.py`
**Theorem:** $\dfrac{d}{dx} e^x = e^x$

- Left panel: overlays the exact curve $e^x$ with its central-difference
  numerical derivative — they are indistinguishable.
- Right panel: log-scale error confirming the match is limited only by
  floating-point precision (~10⁻¹²).

**Output:** `outputs/derivative_equals_self.png / .svg`

---

### 2. `integral_ex.py`
**Theorem:** $\int e^x\,dx = e^x + C$

- Single panel with $e^x$ plotted over $[-2.5, 3]$.
- Area from $x=-1$ to $x=2$ shaded and annotated with the exact value
  $e^2 - e^{-1}$.
- Simpson's rule numerical value shown for verification.

**Output:** `outputs/integral_ex.png / .svg`

---

### 3. `taylor_series.py`
**Formula:** $e^x = \sum_{k=0}^{\infty} \dfrac{x^k}{k!}$

Six-panel static figure showing polynomial approximations $P_n(x)$ for
$n = 1, 2, 3, 5, 8, 12$ terms, each overlaid with the exact $e^x$ curve.
The valid approximation range is shaded per panel.

**Output:** `outputs/taylor_series.png / .svg`

---

### 4. `ax_vs_ex.py`
Reproduction of the classic Wikipedia comparison graph:

| Curve | Style |
|-------|-------|
| $2^x$ | blue dotted |
| $e^x$ | blue solid |
| $4^x$ | blue dashed |
| $y = x+1$ | red solid (tangent) |

All three exponentials pass through $(0, 1)$; only $e^x$ has the tangent
$y = x+1$ (slope exactly 1).

**Output:** `outputs/ax_vs_ex_wikipedia.png / .svg`

---

### 5. `tangent_line_slope1.py`
**Key fact:** $\dfrac{d}{dx} a^x \big|_{x=0} = \ln a$, and $\ln e = 1$.

- Left panel: $2^x$, $e^x$, $4^x$ zoomed near origin with their tangent lines
  at $x=0$ drawn.
- Right panel: bar chart comparing the three slopes, with $e^x$ highlighted as
  the special case where slope $= 1$.

**Output:** `outputs/tangent_line_slope1.png / .svg`

---

### 6. `natural_log_derivative.py`
**Theorem:** $\dfrac{d}{dx} \ln x = \dfrac{1}{x}$

- Left panel: $\ln x$ with tangent lines drawn at several points, each labeled
  with its slope $= 1/x$.
- Right panel: $1/x$ overlaid with the numerical derivative of $\ln x$ —
  confirming they match to floating-point precision.

**Output:** `outputs/natural_log_derivative.png / .svg`

---

### 7. `ln_integral.py`
**Theorem / Definition:** $\ln x \equiv \int_1^x \dfrac{1}{t}\,dt$, so $\int_1^e \dfrac{1}{t}\,dt = 1$

- $1/t$ plotted from $t=0.1$ to $4$.
- Area from $1$ to $e$ shaded in green and annotated "Area = 1 exactly!"
- Both the exact value and the Simpson's rule numerical result are displayed.

**Output:** `outputs/ln_integral.png / .svg`

---

### 8. `limit_definition_plot.py`
**Visual explanation of** $(1+1/n)^n \to e$

- Top panel: compound-interest growth curves $(1+1/n)^{nt}$ for $n=1,2,5,10,100$,
  plus the continuous limit $e^t$, over $t \in [0,1]$.
- Bottom panel: number line showing each approximation approaching $e$ from below.

**Output:** `outputs/limit_definition_plot.png / .svg`

---

## Running the Scripts

```bash
# From the repo root
python 02_calculus/derivative_equals_self.py
python 02_calculus/integral_ex.py
python 02_calculus/taylor_series.py
python 02_calculus/ax_vs_ex.py
python 02_calculus/tangent_line_slope1.py
python 02_calculus/natural_log_derivative.py
python 02_calculus/ln_integral.py
python 02_calculus/limit_definition_plot.py
```

All outputs are written to `02_calculus/outputs/`.

## Dependencies

- `numpy`, `matplotlib`, `mpmath`
- `utils/plot_style.py`, `utils/math_helpers.py` (shared utilities)
