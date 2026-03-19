# Module 03: Euler's Number in Trigonometry

This module explores the deep connection between `e` and the trigonometric
functions through Euler's formula, Euler's identity, and De Moivre's theorem.

## Scripts

| File | Topic | Output |
|------|-------|--------|
| `euler_formula.py` | 3-D helix visualization of e^(iθ) with projections | `outputs/euler_formula_3d.png/.svg` |
| `euler_identity.py` | e^(iπ) + 1 = 0 on the complex plane | `outputs/euler_identity.png/.svg` |
| `sin_cos_from_exp.py` | Deriving sin/cos from complex exponentials | `outputs/sin_cos_from_exp.png/.svg` |
| `de_moivre.py` | De Moivre's theorem — regular polygon roots of unity | `outputs/de_moivre.png/.svg` |
| `unit_circle_animation.py` | 8-frame static view of e^(iθ) on the unit circle | `outputs/unit_circle_frames.png/.svg` |

## Key Formulas

```
Euler's formula:   e^(iθ) = cos(θ) + i·sin(θ)
Euler's identity:  e^(iπ) + 1 = 0
cos from exp:      cos(x) = (e^(ix) + e^(-ix)) / 2
sin from exp:      sin(x) = (e^(ix) - e^(-ix)) / (2i)
De Moivre:         (e^(iθ))^n = cos(nθ) + i·sin(nθ)
```

## Running

```bash
cd 03_trigonometry
python euler_formula.py
python euler_identity.py
python sin_cos_from_exp.py
python de_moivre.py
python unit_circle_animation.py
```

All output files are saved in `03_trigonometry/outputs/` as both `.png` and `.svg`.
