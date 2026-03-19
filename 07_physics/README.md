# Module 07 — Physics

Euler's number **e** appears throughout physics wherever a quantity changes
proportionally to itself — from radioactive nuclei decaying at a rate
proportional to their count, to photons following the Planck distribution.

## Scripts

| Script | Physics Law | Key Formula |
|---|---|---|
| `radioactive_decay.py` | Radioactive decay | N(t) = N₀ e^{−λt} |
| `capacitor_charge.py` | RC circuit | V(t) = V₀(1 − e^{−t/RC}) |
| `damped_oscillation.py` | Damped SHM | x(t) = A e^{−γt} cos(ω_d t) |
| `heat_equation.py` | Newton's cooling | T(t) = T_e + (T₀−T_e) e^{−kt} |
| `wave_attenuation.py` | Wave propagation | A(x) = A₀ e^{−αx} cos(kx) |
| `boltzmann_distribution.py` | Statistical mechanics | P(E) ∝ √E · e^{−E/k_BT} |
| `schrodinger.py` | Quantum mechanics | ψ = A e^{ikx}, ψ_n ∝ H_n(x) e^{−x²/2} |
| `blackbody_radiation.py` | Planck's law | B(λ,T) = (2hc²/λ⁵) / (e^{hc/λk_BT} − 1) |
| `relativity_rapidity.py` | Special relativity | v/c = tanh(φ), φ = atanh(v/c) |

## Running All Scripts

```bash
cd 07_physics
for script in *.py; do python "$script"; done
```

Outputs (PNG + SVG) are written to `07_physics/outputs/`.

## Key Physics Concepts

### Exponential Decay
Any system where the rate of change is proportional to the current value
obeys dN/dt = −λN, solved by N(t) = N₀ e^{−λt}.  Half-life t₁/₂ = ln 2 / λ.

### RC Circuits
The time constant τ = RC is the time for the capacitor to reach 1 − 1/e ≈ 63.2%
of full charge (or discharge to 1/e ≈ 36.8%).

### Boltzmann Factor
The probability of a state with energy E at temperature T is suppressed by
the Boltzmann factor e^{−E/k_BT}.  This is the fundamental reason high-energy
states are exponentially rare.

### Planck's Law
The denominator e^{hν/k_BT} − 1 prevents the ultraviolet catastrophe of
classical physics and gives the correct blackbody spectrum.

### Rapidity
Because tanh = (e^φ − e^{−φ}) / (e^φ + e^{−φ}), rapidity φ = atanh(v/c)
is the "natural" velocity parameter in special relativity — rapidities simply
add under boosts, while velocities do not.
