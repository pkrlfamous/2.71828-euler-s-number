"""
Common math utilities used across all modules.
Pure Python + NumPy + mpmath implementations.
"""
import math
import numpy as np
from mpmath import mp, mpf, e as mp_e


def compute_e_limit(n):
    """
    Compute e using the limit definition: (1 + 1/n)^n.

    Args:
        n (float): The value of n (should be large for good approximation).

    Returns:
        float: Approximation of e.

    Raises:
        ValueError: If n <= 0.
    """
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    return (1 + 1 / n) ** n


def compute_e_series(terms):
    """
    Compute e using the factorial series: sum(1/k! for k in 0..terms).

    Args:
        terms (int): Number of terms to sum (0-indexed upper bound).

    Returns:
        float: Approximation of e.

    Raises:
        ValueError: If terms < 0.
    """
    if terms < 0:
        raise ValueError(f"terms must be >= 0, got {terms}")
    return sum(1.0 / math.factorial(k) for k in range(terms + 1))


def compute_e_digits(num_digits):
    """
    Compute e to arbitrary precision using mpmath.

    Args:
        num_digits (int): Number of significant digits to compute.

    Returns:
        str: String representation of e with the requested digits.

    Raises:
        ValueError: If num_digits < 1.
    """
    if num_digits < 1:
        raise ValueError(f"num_digits must be >= 1, got {num_digits}")
    mp.dps = num_digits + 5
    return mp.nstr(mp_e, num_digits, strip_zeros=False)


def numerical_derivative(f, x, h=1e-8):
    """
    Compute derivative using central difference approximation.

    Args:
        f (callable): Function to differentiate.
        x (float): Point at which to evaluate derivative.
        h (float): Step size (default 1e-8).

    Returns:
        float: Approximate derivative f'(x).
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_integral(f, a, b, n=10000):
    """
    Compute integral using Simpson's rule.

    Args:
        f (callable): Function to integrate. Must accept numpy arrays.
        a (float): Lower bound.
        b (float): Upper bound.
        n (int): Number of intervals (must be even, default 10000).

    Returns:
        float: Approximate integral.

    Raises:
        ValueError: If n is odd or a >= b.
    """
    if n % 2 != 0:
        n += 1  # Make n even
    if a >= b:
        raise ValueError(f"a must be < b, got a={a}, b={b}")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([float(f(xi)) for xi in x])
    return h / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]))


def e_continued_fraction_coeffs(n_terms):
    """
    Generate the continued fraction coefficients for e.
    e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, ...]
    Pattern: a(3k-1) = 2k, rest are 1, starting with a0 = 2.

    Args:
        n_terms (int): Number of coefficients to generate.

    Returns:
        list[int]: Continued fraction coefficients.
    """
    coeffs = [2]
    for i in range(1, n_terms):
        # index i in coeffs (1-based position i)
        # positions 2, 5, 8, 11, ... (i.e., i % 3 == 2) get 2*(i//3 + 1)
        if i % 3 == 2:
            coeffs.append(2 * (i // 3 + 1))
        else:
            coeffs.append(1)
    return coeffs


def e_continued_fraction_convergent(coeffs, index):
    """
    Compute the p/q convergent of the continued fraction at a given index.

    Args:
        coeffs (list[int]): Continued fraction coefficients.
        index (int): Which convergent to compute (0-indexed).

    Returns:
        tuple[int, int]: (numerator, denominator) of the convergent.
    """
    h_prev, h_curr = 1, coeffs[0]
    k_prev, k_curr = 0, 1
    for j in range(1, index + 1):
        h_prev, h_curr = h_curr, coeffs[j] * h_curr + h_prev
        k_prev, k_curr = k_curr, coeffs[j] * k_curr + k_prev
    return h_curr, k_curr


def sigmoid(x, k=1.0):
    """Logistic sigmoid: 1 / (1 + e^(-k*x))."""
    return 1.0 / (1.0 + np.exp(-k * x))


def softmax(logits, temperature=1.0):
    """Numerically stable softmax with temperature scaling."""
    scaled = np.array(logits, dtype=float) / temperature
    shifted = scaled - np.max(scaled)
    exp_vals = np.exp(shifted)
    return exp_vals / np.sum(exp_vals)


def normal_pdf(x, mu=0.0, sigma=1.0):
    """Gaussian probability density function."""
    return (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def poisson_pmf(k, lam):
    """Poisson probability mass function: e^(-lambda) * lambda^k / k!"""
    return np.exp(-lam) * (lam ** k) / math.factorial(int(k))
