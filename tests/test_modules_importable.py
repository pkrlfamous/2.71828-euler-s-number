"""
Smoke tests: verify every module script can be imported without errors.
All scripts use matplotlib.use('Agg') so no display is needed.
These tests ensure no syntax errors, missing imports, or crash-on-import issues.
"""
import os
import sys
import importlib.util
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Collect all .py scripts (excluding utils, tests, and game scripts that need stdin)
ALL_SCRIPTS = []
MODULES = [
    '01_computing_e',
    '02_calculus',
    '03_trigonometry',
    '04_complex_numbers',
    '05_coordinate_systems',
    '06_nature_and_art',
    '07_physics',
    '08_chemistry_biology',
    '09_computer_science_ml',
    '10_finance',
    '11_probability_statistics',
    '12_games_puzzles',
]

for module_dir in MODULES:
    module_path = os.path.join(REPO_ROOT, module_dir)
    if os.path.isdir(module_path):
        for fname in sorted(os.listdir(module_path)):
            if fname.endswith('.py') and fname != '__init__.py':
                ALL_SCRIPTS.append(os.path.join(module_path, fname))


def run_script(script_path):
    """Execute a script file in isolation."""
    spec = importlib.util.spec_from_file_location("_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    # Add repo root and script's parent to sys.path
    parent = os.path.dirname(script_path)
    original_path = sys.path.copy()
    original_argv = sys.argv.copy()
    sys.path.insert(0, REPO_ROOT)
    sys.path.insert(0, parent)
    sys.argv = [script_path]
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path = original_path
        sys.argv = original_argv


# Parametrize by relative path for clear test names
@pytest.mark.parametrize("script_path", ALL_SCRIPTS, ids=[
    os.path.relpath(p, REPO_ROOT) for p in ALL_SCRIPTS
])
def test_script_runs(script_path):
    """Each script should run without raising an exception."""
    run_script(script_path)
