"""
Euler's Number Project — Shared Utilities
"""
from .plot_style import apply_euler_style, save_plot, COLORS
from .math_helpers import (
    compute_e_limit,
    compute_e_series,
    compute_e_digits,
    numerical_derivative,
    numerical_integral,
)

__all__ = [
    "apply_euler_style",
    "save_plot",
    "COLORS",
    "compute_e_limit",
    "compute_e_series",
    "compute_e_digits",
    "numerical_derivative",
    "numerical_integral",
]
