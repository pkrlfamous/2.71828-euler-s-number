# Module 05 — Coordinate Systems

Euler's number *e* expressed through polar, parametric, spherical, and curvilinear coordinates.

## Scripts

| Script | Description | Output |
|--------|-------------|--------|
| `polar_exponential.py` | Logarithmic spiral r = e^(aθ) for a = 0.05–0.3 | `outputs/polar_exponential.png/svg` |
| `parametric_curves.py` | Four parametric curves involving e^t with color gradients | `outputs/parametric_curves.png/svg` |
| `spherical_coordinates.py` | 3D radial decay e^(−r), unit sphere intensity, 2D contour | `outputs/spherical_coordinates.png/svg` |
| `catenary_curve.py` | Catenary y = a·cosh(x/a) for a = 0.5–3; hanging chain illustration | `outputs/catenary_curve.png/svg` |
| `hyperbolic_functions.py` | sinh/cosh/tanh, identity proof, unit hyperbola, vs circular functions | `outputs/hyperbolic_functions.png/svg` |

## Key Mathematical Concepts

- **Logarithmic spiral**: r = e^(aθ) — equal-angle property; each radial ray cuts the curve at the same angle.
- **Parametric forms**: Expanding helices, damped Lissajous figures, and Maclaurin's butterfly all involve e^t.
- **Radial decay**: f(ρ) = e^(−ρ/2) is the canonical spherically symmetric decay function in physics.
- **Catenary**: y = a·cosh(x/a) = a(e^(x/a) + e^(−x/a))/2 — the shape of a hanging chain under gravity.
- **Hyperbolic functions**: sinh, cosh, tanh defined directly through e; obey cosh² − sinh² = 1 (analogous to the Pythagorean identity on the unit hyperbola x² − y² = 1).

## Running

```bash
cd 05_coordinate_systems
python polar_exponential.py
python parametric_curves.py
python spherical_coordinates.py
python catenary_curve.py
python hyperbolic_functions.py
```

All outputs are saved to `05_coordinate_systems/outputs/` as both PNG and SVG.
