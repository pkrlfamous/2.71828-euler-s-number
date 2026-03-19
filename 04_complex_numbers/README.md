# Module 04: Euler's Number in Complex Analysis

This module ventures into the complex plane, exploring how `e` appears in
domain coloring, the Cornu spiral, the Mandelbrot set, and the Riemann zeta function.

## Scripts

| File | Topic | Output |
|------|-------|--------|
| `complex_exp_map.py` | Domain coloring of w = e^z — strips to annuli | `outputs/complex_exp_map.png/.svg` |
| `euler_spiral.py` | Cornu spiral via Fresnel integrals (scipy) | `outputs/euler_spiral.png/.svg` |
| `mandelbrot_connection.py` | Mandelbrot set with ln-smooth escape-time coloring | `outputs/mandelbrot_connection.png/.svg` |
| `riemann_zeta.py` | ζ(1/2+it) along the critical line (mpmath) | `outputs/riemann_zeta.png/.svg` |

## Key Ideas

**Complex exponential map** — The map `z → e^z` takes vertical lines
`Re(z) = c` to circles of radius `e^c`, and horizontal lines to rays of constant
argument. A vertical strip `0 ≤ Re(z) ≤ 1` maps to the annulus `1 ≤ |w| ≤ e`.

**Cornu / Euler spiral** — The clothoid is parameterized by the Fresnel integrals:
```
C(t) = ∫₀ᵗ cos(πs²/2) ds
S(t) = ∫₀ᵗ sin(πs²/2) ds
```
Its curvature grows linearly: κ = πt — the defining property used in road and
rail design.

**Mandelbrot smooth coloring** — To eliminate banding in escape-time images,
the iteration count is smoothed with:
```
smooth = n + 1 - log(log(|z_n|)) / log(2)
```
The natural logarithm `ln = log_e` appears explicitly here.

**Riemann hypothesis** — The function `ζ(1/2 + it)` oscillates and vanishes
at the non-trivial zeros. All known zeros lie exactly on this critical line.
The first ten zeros are near t ≈ 14.13, 21.02, 25.01, 30.42, 32.93, 37.59,
40.92, 43.33, 48.01, 49.77.

## Running

```bash
cd 04_complex_numbers
python complex_exp_map.py
python euler_spiral.py
python mandelbrot_connection.py   # ~30 s — computes two Mandelbrot grids
python riemann_zeta.py            # ~30–60 s — mpmath high-precision evaluation
```

All output files are saved in `04_complex_numbers/outputs/` as both `.png` and `.svg`.

## Dependencies

Beyond the standard project requirements, `riemann_zeta.py` uses
`mpmath >= 1.3.0` for high-precision zeta evaluation, and `euler_spiral.py`
uses `scipy.special.fresnel`.
