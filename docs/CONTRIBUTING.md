# Contributing to the Euler's Number Project

Thank you for your interest in contributing! This project welcomes contributions of all kinds.

## Getting Started

```bash
git clone https://github.com/pkrlfamous/2.71828-euler-s-number.git
cd 2.71828-euler-s-number
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install flake8 pytest
```

## Project Structure

Each module folder (e.g. `07_physics/`) contains:
- Python scripts named after their subject
- A `README.md` explaining the module
- An `outputs/` folder (auto-created) for generated plots

## Adding a New Script

1. **Choose the right module** — pick the folder that best fits your topic
2. **Follow the template:**

```python
"""
Short description of what this script demonstrates.
Formula: <the key formula>
"""
import matplotlib
matplotlib.use('Agg')  # Must be first!
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

# Your computation here
x = np.linspace(-5, 5, 1000)
y = np.exp(x)

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(x, y, color=COLORS['e_gold'], linewidth=2.5, label='eˣ')
ax.set_title('Your Title Here', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
save_plot(fig, 'your_script_name', output_dir=os.path.join(MODULE_DIR, 'outputs'))
plt.close()
```

3. **Use `math.factorial(k)`** — not `np.math.factorial(k)` (deprecated)
4. **Never call `plt.show()`** — all outputs go to the `outputs/` folder
5. **Always use absolute paths** for output directories

## Style Guidelines

- All colors from `COLORS` dict in `utils/plot_style.py`
- Dark theme applied via `apply_euler_style()` at the top
- Every script saves both `.png` and `.svg`
- Line lengths max 120 characters (`flake8 --max-line-length=120`)
- Docstrings for all functions

## Running Tests

```bash
# Core math tests
pytest tests/test_math_helpers.py tests/test_formulas.py -v

# Smoke tests (runs all scripts)
MPLBACKEND=Agg pytest tests/test_modules_importable.py -v
```

## Submitting a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b feature/module-N-script-name`
3. Add your script and test it runs: `python your_module/your_script.py`
4. Run the linter: `flake8 your_module/your_script.py --max-line-length=120`
5. Run the tests: `pytest tests/ -v`
6. Commit and push, then open a PR

## Ideas for Contributions

- Additional physics simulations (quantum harmonic oscillator, etc.)
- More biological models (epidemiology SIR model, etc.)
- Interactive Jupyter notebooks for any module
- Additional games/puzzles about e
- Translations / improved docstrings
- Performance optimizations using mpmath

## Code of Conduct

Be kind, be curious, be mathematically rigorous. This is a learning project — all levels of experience welcome.
