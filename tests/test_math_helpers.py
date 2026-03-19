"""
Tests for utils/math_helpers.py

Tests cover:
- compute_e_limit: convergence, edge cases, ValueError
- compute_e_series: convergence, edge cases, ValueError
- compute_e_digits: string format, precision, ValueError
- numerical_derivative: accuracy on known functions
- numerical_integral: accuracy on known integrals
- e_continued_fraction_coeffs: known pattern
- e_continued_fraction_convergent: known values
- sigmoid, softmax, normal_pdf, poisson_pmf
"""
import math
import sys
import os
import pytest
import numpy as np

# Add repo root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.math_helpers import (
    compute_e_limit,
    compute_e_series,
    compute_e_digits,
    numerical_derivative,
    numerical_integral,
    e_continued_fraction_coeffs,
    e_continued_fraction_convergent,
    sigmoid,
    softmax,
    normal_pdf,
    poisson_pmf,
)

E = math.e  # 2.718281828459045...


class TestComputeELimit:
    def test_large_n_close_to_e(self):
        approx = compute_e_limit(1_000_000)
        assert abs(approx - E) < 1e-5

    def test_n_equals_1(self):
        # (1 + 1/1)^1 = 2
        assert compute_e_limit(1) == pytest.approx(2.0)

    def test_n_equals_10(self):
        approx = compute_e_limit(10)
        # Should be within 5% of e
        assert abs(approx - E) / E < 0.05

    def test_n_equals_100(self):
        # (1+1/100)^100 ≈ 2.7048, within 0.02 of e
        approx = compute_e_limit(100)
        assert abs(approx - E) < 0.02

    def test_raises_on_zero(self):
        with pytest.raises((ValueError, ZeroDivisionError)):
            compute_e_limit(0)

    def test_raises_on_negative(self):
        with pytest.raises((ValueError, ZeroDivisionError)):
            compute_e_limit(-5)

    def test_monotone_increasing(self):
        # (1+1/n)^n is monotonically increasing toward e
        vals = [compute_e_limit(n) for n in [1, 10, 100, 1000, 10000]]
        for i in range(len(vals) - 1):
            assert vals[i] < vals[i + 1]

    def test_never_exceeds_e(self):
        # By definition, (1+1/n)^n < e for all finite n
        for n in [10, 100, 1000, 100000]:
            assert compute_e_limit(n) < E + 1e-10


class TestComputeESeries:
    def test_zero_terms(self):
        # Σ 1/k! for k=0 only = 1.0
        assert compute_e_series(0) == pytest.approx(1.0)

    def test_one_term(self):
        # 1/0! + 1/1! = 2.0
        assert compute_e_series(1) == pytest.approx(2.0)

    def test_two_terms(self):
        # 1 + 1 + 0.5 = 2.5
        assert compute_e_series(2) == pytest.approx(2.5)

    def test_convergence_5_terms(self):
        approx = compute_e_series(5)
        assert abs(approx - E) < 0.01

    def test_convergence_15_terms(self):
        approx = compute_e_series(15)
        assert abs(approx - E) < 1e-10

    def test_raises_on_negative(self):
        with pytest.raises(ValueError):
            compute_e_series(-1)

    def test_monotone_increasing(self):
        vals = [compute_e_series(n) for n in range(10)]
        for i in range(len(vals) - 1):
            assert vals[i] < vals[i + 1]

    def test_never_exceeds_e_significantly(self):
        # Series is always <= e (alternating series argument doesn't apply here,
        # but all terms positive so it approaches from below then levels off)
        for n in range(20):
            assert compute_e_series(n) <= E + 1e-10


class TestComputeEDigits:
    def test_starts_with_2_point(self):
        digits = compute_e_digits(10)
        assert digits.startswith('2.')

    def test_known_digits(self):
        # e = 2.71828182845904523536...
        digits = compute_e_digits(20)
        assert digits.startswith('2.71828182845')

    def test_raises_on_zero(self):
        with pytest.raises(ValueError):
            compute_e_digits(0)

    def test_raises_on_negative(self):
        with pytest.raises(ValueError):
            compute_e_digits(-1)

    def test_100_digits_start(self):
        digits = compute_e_digits(50)
        assert digits.startswith('2.718281828459045')


class TestNumericalDerivative:
    def test_exp_derivative(self):
        # d/dx(e^x) = e^x
        for x in [-2, -1, 0, 1, 2]:
            deriv = numerical_derivative(np.exp, x)
            assert abs(deriv - np.exp(x)) < 1e-5, f"Failed at x={x}"

    def test_sin_derivative(self):
        # d/dx(sin x) = cos x
        for x in [0, 0.5, 1.0, 1.5, 2.0]:
            deriv = numerical_derivative(np.sin, x)
            assert abs(deriv - np.cos(x)) < 1e-5

    def test_x_squared_derivative(self):
        # d/dx(x^2) = 2x
        f = lambda x: x ** 2
        for x in [-3, -1, 0, 1, 3]:
            deriv = numerical_derivative(f, x)
            assert abs(deriv - 2 * x) < 1e-5

    def test_constant_derivative(self):
        # d/dx(5) = 0
        f = lambda x: 5.0
        for x in [-1, 0, 1]:
            deriv = numerical_derivative(f, x)
            assert abs(deriv) < 1e-5

    def test_ln_derivative(self):
        # d/dx(ln x) = 1/x
        for x in [0.5, 1.0, 2.0, 5.0]:
            deriv = numerical_derivative(np.log, x)
            assert abs(deriv - 1.0 / x) < 1e-5


class TestNumericalIntegral:
    def test_exp_integral(self):
        # ∫₀¹ e^x dx = e - 1
        result = numerical_integral(np.exp, 0, 1)
        assert abs(result - (E - 1)) < 1e-6

    def test_constant_integral(self):
        # ∫₀¹ 1 dx = 1
        result = numerical_integral(lambda x: np.ones_like(x) if hasattr(x, '__len__') else 1.0, 0, 1)
        assert abs(result - 1.0) < 1e-6

    def test_ln_integral_definition_of_e(self):
        # ∫₁ᵉ (1/t) dt = 1  (this is the integral definition of e)
        result = numerical_integral(lambda x: 1.0 / x, 1, E)
        assert abs(result - 1.0) < 1e-4

    def test_sin_integral(self):
        # ∫₀^π sin(x) dx = 2
        result = numerical_integral(np.sin, 0, math.pi)
        assert abs(result - 2.0) < 1e-6

    def test_raises_on_invalid_bounds(self):
        with pytest.raises(ValueError):
            numerical_integral(np.exp, 1, 0)  # a > b

    def test_raises_on_equal_bounds(self):
        with pytest.raises(ValueError):
            numerical_integral(np.exp, 1, 1)  # a == b


class TestContinuedFraction:
    def test_known_coefficients(self):
        # e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, ...]
        coeffs = e_continued_fraction_coeffs(13)
        assert coeffs[0] == 2
        assert coeffs[1] == 1
        assert coeffs[2] == 2
        assert coeffs[3] == 1
        assert coeffs[4] == 1
        assert coeffs[5] == 4
        assert coeffs[6] == 1
        assert coeffs[7] == 1
        assert coeffs[8] == 6

    def test_convergent_0(self):
        coeffs = e_continued_fraction_coeffs(10)
        h, k = e_continued_fraction_convergent(coeffs, 0)
        assert h / k == pytest.approx(2.0)

    def test_convergent_1(self):
        # After [2; 1], convergent = 2 + 1/1 = 3/1
        coeffs = e_continued_fraction_coeffs(10)
        h, k = e_continued_fraction_convergent(coeffs, 1)
        assert h / k == pytest.approx(3.0)

    def test_convergents_approach_e(self):
        coeffs = e_continued_fraction_coeffs(20)
        errors = []
        for i in range(len(coeffs)):
            h, k = e_continued_fraction_convergent(coeffs, i)
            errors.append(abs(h / k - E))
        # Errors should generally decrease
        assert errors[-1] < errors[0]
        assert errors[-1] < 1e-6


class TestSigmoid:
    def test_at_zero(self):
        assert sigmoid(0) == pytest.approx(0.5)

    def test_large_positive(self):
        assert sigmoid(100) == pytest.approx(1.0, abs=1e-10)

    def test_large_negative(self):
        assert sigmoid(-100) == pytest.approx(0.0, abs=1e-10)

    def test_symmetry(self):
        # sigmoid(-x) = 1 - sigmoid(x)
        for x in [0.5, 1.0, 2.0]:
            assert sigmoid(-x) == pytest.approx(1 - sigmoid(x), rel=1e-6)

    def test_steepness(self):
        # Higher k means sharper transition
        s1 = sigmoid(1.0, k=1)
        s5 = sigmoid(1.0, k=5)
        assert s5 > s1  # Both > 0.5, but s5 is closer to 1


class TestSoftmax:
    def test_sums_to_one(self):
        logits = [1.0, 2.0, 3.0]
        probs = softmax(logits)
        assert abs(sum(probs) - 1.0) < 1e-10

    def test_order_preserved(self):
        logits = [1.0, 3.0, 2.0]
        probs = softmax(logits)
        # Highest logit should have highest probability
        assert probs[1] > probs[2] > probs[0]

    def test_uniform_for_equal_logits(self):
        logits = [1.0, 1.0, 1.0]
        probs = softmax(logits)
        for p in probs:
            assert p == pytest.approx(1 / 3, rel=1e-6)

    def test_temperature_sharpens(self):
        logits = [1.0, 2.0, 0.0]
        probs_cold = softmax(logits, temperature=0.1)
        probs_hot = softmax(logits, temperature=10.0)
        # Cold (low temp) should have higher peak
        assert max(probs_cold) > max(probs_hot)


class TestNormalPDF:
    def test_standard_normal_peak(self):
        # Peak at x=0 = 1/sqrt(2π) ≈ 0.3989
        expected = 1.0 / math.sqrt(2 * math.pi)
        assert normal_pdf(0) == pytest.approx(expected, rel=1e-6)

    def test_symmetric(self):
        for x in [0.5, 1.0, 2.0]:
            assert normal_pdf(x) == pytest.approx(normal_pdf(-x), rel=1e-10)

    def test_1sigma_value(self):
        # At x = σ, PDF = (1/√2π)·e^(-1/2) ≈ 0.2420
        expected = math.exp(-0.5) / math.sqrt(2 * math.pi)
        assert normal_pdf(1.0) == pytest.approx(expected, rel=1e-6)

    def test_different_mean(self):
        # N(2, 1): peak at x=2
        assert normal_pdf(2.0, mu=2.0) > normal_pdf(2.5, mu=2.0)

    def test_different_sigma(self):
        # Wider distribution has lower peak
        peak_narrow = normal_pdf(0.0, sigma=0.5)
        peak_wide = normal_pdf(0.0, sigma=2.0)
        assert peak_narrow > peak_wide


class TestPoissonPMF:
    def test_known_value(self):
        # P(X=0 | λ=1) = e^(-1) ≈ 0.3679
        p = poisson_pmf(0, 1)
        assert abs(p - math.exp(-1)) < 1e-10

    def test_sum_to_one(self):
        # Sum over large k range should be close to 1
        lam = 3
        total = sum(poisson_pmf(k, lam) for k in range(30))
        assert abs(total - 1.0) < 1e-6

    def test_mode_at_lambda(self):
        # For integer λ, mode is at λ (and λ-1)
        lam = 5
        mode_val = poisson_pmf(lam, lam)
        for k in [0, 1, 2, 7, 10]:
            assert poisson_pmf(k, lam) <= mode_val + 1e-10
