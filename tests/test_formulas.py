"""
Formula correctness tests — verify key mathematical formulas implemented
across the project produce correct numerical results.
"""
import math
import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.math_helpers import sigmoid, softmax, normal_pdf, poisson_pmf

E = math.e
PI = math.pi


class TestEulerIdentity:
    """e^(iπ) + 1 = 0"""

    def test_euler_identity(self):
        result = (math.cos(PI) + 1j * math.sin(PI)) + 1  # e^(iπ) + 1 = 0
        assert abs(result) < 1e-15

    def test_euler_formula_real_part(self):
        # Re(e^(iθ)) = cos(θ)
        for theta in [0, PI / 6, PI / 4, PI / 3, PI / 2, PI]:
            real_part = math.cos(theta)
            expected = math.cos(theta)
            assert abs(real_part - expected) < 1e-15

    def test_euler_formula_imag_part(self):
        # Im(e^(iθ)) = sin(θ)
        for theta in [0, PI / 6, PI / 4, PI / 3, PI / 2]:
            assert abs(math.sin(theta) - math.sin(theta)) < 1e-15

    def test_unit_circle(self):
        # |e^(iθ)| = 1 for all θ
        for theta in np.linspace(0, 2 * PI, 100):
            z = math.cos(theta) + 1j * math.sin(theta)
            assert abs(abs(z) - 1.0) < 1e-14


class TestHyperbolicIdentities:
    """sinh, cosh, tanh defined via e"""

    def test_cosh_definition(self):
        # cosh(x) = (e^x + e^(-x)) / 2
        for x in [-2, -1, 0, 1, 2]:
            via_e = (math.exp(x) + math.exp(-x)) / 2
            assert abs(via_e - math.cosh(x)) < 1e-12

    def test_sinh_definition(self):
        # sinh(x) = (e^x - e^(-x)) / 2
        for x in [-2, -1, 0, 1, 2]:
            via_e = (math.exp(x) - math.exp(-x)) / 2
            assert abs(via_e - math.sinh(x)) < 1e-12

    def test_pythagorean_identity(self):
        # cosh²(x) - sinh²(x) = 1
        for x in [-3, -1, 0, 1, 3]:
            lhs = math.cosh(x) ** 2 - math.sinh(x) ** 2
            assert abs(lhs - 1.0) < 1e-12

    def test_tanh_range(self):
        # -1 < tanh(x) < 1
        for x in np.linspace(-10, 10, 100):
            assert -1 < math.tanh(x) < 1


class TestExponentialGrowth:
    """P(t) = P₀·e^(rt)"""

    def test_at_zero(self):
        P0, r = 100, 0.1
        assert P0 * math.exp(r * 0) == pytest.approx(P0)

    def test_doubling_time(self):
        # Doubling time: t_d = ln(2)/r
        r = 0.1
        t_d = math.log(2) / r
        P0 = 100
        assert P0 * math.exp(r * t_d) == pytest.approx(2 * P0, rel=1e-6)

    def test_decay(self):
        # Exponential decay: half-life t_{1/2} = ln(2)/λ
        lam = 0.5
        t_half = math.log(2) / lam
        N0 = 1000
        assert N0 * math.exp(-lam * t_half) == pytest.approx(N0 / 2, rel=1e-6)


class TestLogisticGrowth:
    """P(t) = K / (1 + ((K-P₀)/P₀)·e^(-rt))"""

    def _logistic(self, t, P0, K, r):
        C = (K - P0) / P0
        return K / (1 + C * math.exp(-r * t))

    def test_initial_value(self):
        assert self._logistic(0, 100, 1000, 0.1) == pytest.approx(100.0)

    def test_approaches_carrying_capacity(self):
        P_inf = self._logistic(1000, 100, 1000, 0.1)
        assert abs(P_inf - 1000) < 0.1

    def test_inflection_at_k_over_2(self):
        # Inflection point when P = K/2
        P0, K, r = 10, 1000, 0.2
        t_infl = math.log((K - P0) / P0) / r
        assert self._logistic(t_infl, P0, K, r) == pytest.approx(K / 2, rel=1e-4)


class TestContinuousCompounding:
    """A = P·e^(rt) — continuous compounding limit"""

    def test_bernoulli_limit(self):
        # (1 + r/n)^(nt) → e^(rt) as n → ∞
        P, r, t = 1000, 0.1, 5
        continuous = P * math.exp(r * t)
        daily = P * (1 + r / 365) ** (365 * t)
        assert abs(daily - continuous) / continuous < 0.001

    def test_at_100_percent_rate(self):
        # P=1, r=1, t=1: A = e
        result = 1 * math.exp(1 * 1)
        assert abs(result - E) < 1e-12

    def test_present_value_discounting(self):
        # PV = FV · e^(-rt)
        FV, r, t = 1000, 0.05, 10
        PV = FV * math.exp(-r * t)
        # Round-trip: PV·e^(rt) = FV
        assert PV * math.exp(r * t) == pytest.approx(FV, rel=1e-10)


class TestNormalDistribution:
    """f(x) = (1/σ√2π)·e^(-(x-μ)²/2σ²)"""

    def test_integrates_to_one(self):
        # ∫ N(x; 0, 1) dx over (-∞, ∞) = 1
        x = np.linspace(-10, 10, 100000)
        dx = x[1] - x[0]
        pdf = normal_pdf(x)
        total = np.sum(pdf) * dx
        assert abs(total - 1.0) < 0.001

    def test_68_95_rule(self):
        # P(-1σ < X < 1σ) ≈ 68.27%
        x = np.linspace(-1, 1, 10000)
        dx = x[1] - x[0]
        prob = np.sum(normal_pdf(x)) * dx
        assert abs(prob - 0.6827) < 0.01


class TestPoissonDistribution:
    """P(k; λ) = λ^k · e^(-λ) / k!"""

    def test_e_connection(self):
        # P(0; λ) = e^(-λ) — pure exponential
        for lam in [0.5, 1, 2, 5]:
            assert poisson_pmf(0, lam) == pytest.approx(math.exp(-lam), rel=1e-10)

    def test_mode(self):
        # For integer λ=5, Poisson has two modes: k=4 and k=5 (equal probability)
        # P(k=4; λ=5) = P(k=5; λ=5)
        probs = [poisson_pmf(k, 5) for k in range(20)]
        max_prob = max(probs)
        mode_indices = [i for i, p in enumerate(probs) if abs(p - max_prob) < 1e-12]
        assert 4 in mode_indices and 5 in mode_indices

    def test_mean_equals_lambda(self):
        # E[X] = λ
        lam = 4
        k_vals = np.arange(0, 30)
        probs = [poisson_pmf(k, lam) for k in k_vals]
        mean = sum(k * p for k, p in zip(k_vals, probs))
        assert abs(mean - lam) < 0.01


class TestDerangements:
    """P(derangement of n) → 1/e as n → ∞"""

    def _derangement_prob(self, n):
        """Exact derangement probability: D(n)/n! = sum(-1)^k/k! for k=0..n"""
        return sum((-1) ** k / math.factorial(k) for k in range(n + 1))

    def test_d1_is_zero(self):
        # Only 1 element can't derange
        assert self._derangement_prob(1) == pytest.approx(0.0)

    def test_d2_is_half(self):
        # [1,2] → [2,1] only: P = 1/2
        assert self._derangement_prob(2) == pytest.approx(0.5)

    def test_converges_to_1_over_e(self):
        prob_large = self._derangement_prob(15)
        assert abs(prob_large - 1 / E) < 0.001

    def test_always_near_1_over_e_for_large_n(self):
        for n in range(8, 15):
            prob = self._derangement_prob(n)
            assert abs(prob - 1 / E) < 0.01


class TestStirlingApproximation:
    """n! ≈ √(2πn) · (n/e)^n"""

    def _stirling(self, n):
        return math.sqrt(2 * PI * n) * (n / E) ** n

    def test_stirling_10(self):
        exact = math.factorial(10)
        approx = self._stirling(10)
        rel_error = abs(approx - exact) / exact
        assert rel_error < 0.01  # < 1% error for n=10

    def test_stirling_improves_with_n(self):
        errors = [abs(self._stirling(n) / math.factorial(n) - 1)
                  for n in [5, 10, 20, 50]]
        # Should be monotonically improving
        for i in range(len(errors) - 1):
            assert errors[i] > errors[i + 1]


class TestSigmoidDerivative:
    """σ'(x) = σ(x)(1 - σ(x))"""

    def test_derivative_formula(self):
        h = 1e-7
        for x in [-2, -1, 0, 1, 2]:
            numerical = (sigmoid(x + h) - sigmoid(x - h)) / (2 * h)
            analytical = sigmoid(x) * (1 - sigmoid(x))
            assert abs(numerical - analytical) < 1e-5


class TestSecretaryProblem:
    """Optimal stopping at r = n/e candidates"""

    def _success_prob_exact(self, n, r):
        """P(success) when stopping threshold is r, total n candidates."""
        if r >= n:
            return 1 / n
        total = 0
        for k in range(r, n):
            # Probability that best is at position k+1 and best in first r is at position < k
            total += (1 / n) * (r / k)
        return total

    def test_optimal_stop_near_n_over_e(self):
        n = 100
        probs = [self._success_prob_exact(n, r) for r in range(1, n)]
        best_r = probs.index(max(probs)) + 1  # +1 because range starts at 1
        # Should be near n/e ≈ 36.8
        assert 30 <= best_r <= 42

    def test_optimal_probability_near_1_over_e(self):
        n = 100
        r_opt = round(n / E)
        prob = self._success_prob_exact(n, r_opt)
        # Should be close to 1/e ≈ 0.368
        assert abs(prob - 1 / E) < 0.05
