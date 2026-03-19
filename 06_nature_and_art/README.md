# Module 06 — Nature and Art

Euler's number *e* and the logarithmic spiral pervade the natural world — from nautilus shells and galaxy arms to sunflower seeds and spider webs. This module visualizes ten phenomena where exponential growth and the spiral r = e^(aθ) appear.

## Scripts

| Script | Description | Output |
|--------|-------------|--------|
| `logarithmic_spiral.py` | Self-similar spiral r=e^(aθ), a=0.1/0.2/0.3, annotated constant-angle property | `outputs/logarithmic_spiral.png/svg` |
| `golden_spiral_vs_log.py` | Golden spiral (φ-based) vs e-based spiral — identical growth rate | `outputs/golden_spiral_vs_log.png/svg` |
| `phyllotaxis.py` | Sunflower seed packing: golden angle vs off-angle vs rational angle | `outputs/phyllotaxis.png/svg` |
| `nautilus_shell.py` | Chambered nautilus cross-section with filled septa and siphuncle | `outputs/nautilus_shell.png/svg` |
| `galaxy_spiral.py` | Spiral galaxy: 4 logarithmic arms + central bulge + background stars | `outputs/galaxy_spiral.png/svg` |
| `fractal_trees.py` | Recursive fractal tree; branch length scaled by e^(−0.3) ≈ 0.74 | `outputs/fractal_trees.png/svg` |
| `flower_petals.py` | Polar rose r=cos(nθ) for Fibonacci petal counts 3,5,8,13,21 | `outputs/flower_petals.png/svg` |
| `spider_web.py` | Orb-weaver web: radial threads + logarithmic capture spiral + dew drops | `outputs/spider_web.png/svg` |
| `horn_growth.py` | Ram horn cross-section + radius vs angle exponential growth curve | `outputs/horn_growth.png/svg` |
| `population_nature.py` | P(t)=P₀·e^(rt) for multiple rates; exponential vs logistic; phase plane | `outputs/population_nature.png/svg` |

## Key Mathematical Concepts

- **Logarithmic spiral**: r = e^(aθ) — found in nautilus shells, galaxy arms, ram horns, spider webs, and hurricane arms. Its defining property is that the angle between the tangent and radial direction is constant: α = arctan(1/a).
- **Golden angle**: 2π(1 − 1/φ) ≈ 137.508° — the most irrational rotation, guaranteeing no two seeds overlap optimally in phyllotaxis.
- **Golden spiral**: r = φ^(2θ/π) is identical in shape to r = e^(aθ) with a = ln(φ)/(π/2) ≈ 0.3063.
- **Fractal scaling**: e^(−0.3) ≈ 0.7408 is a natural contraction ratio linking recursion depth to exponential decay.
- **Population growth**: P(t) = P₀·e^(rt) is the fundamental model; logistic growth P(t) = K / (1 + ((K−P₀)/P₀)·e^(−rt)) adds a carrying capacity K.

## Running

```bash
cd 06_nature_and_art
python logarithmic_spiral.py
python golden_spiral_vs_log.py
python phyllotaxis.py
python nautilus_shell.py
python galaxy_spiral.py
python fractal_trees.py
python flower_petals.py
python spider_web.py
python horn_growth.py
python population_nature.py
```

All outputs are saved to `06_nature_and_art/outputs/` as both PNG and SVG.
