"""
Black-Scholes options pricing: C = S·N(d₁) - K·e^(-rT)·N(d₂)
Plot call price vs stock price for different maturities, show e^(-rT) discount factor.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import norm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def black_scholes_call(S, K, r, sigma, T):
    """European call option price via Black-Scholes."""
    if T <= 0:
        return np.maximum(S - K, 0.0)
    sqrt_T = np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(S, K, r, sigma, T):
    """European put option price via put-call parity."""
    call = black_scholes_call(S, K, r, sigma, T)
    return call - S + K * np.exp(-r * T)


K     = 100.0   # strike price
r     = 0.05    # risk-free rate
sigma = 0.20    # volatility

S = np.linspace(50, 180, 400)

maturities = [0.25, 0.5, 1.0, 2.0, 5.0]
mat_colors  = [COLORS['e_cyan'], COLORS['e_green'], COLORS['e_gold'],
               COLORS['e_orange'], COLORS['e_red']]

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Call price vs stock price for different maturities ───────────────
ax1 = fig.add_subplot(gs[0])

for T, color in zip(maturities, mat_colors):
    C = black_scholes_call(S, K, r, sigma, T)
    ax1.plot(S, C, color=color, lw=2.2, label=f'T = {T}y')

# Intrinsic value (payoff at expiry)
ax1.plot(S, np.maximum(S - K, 0), color=COLORS['text'], lw=1.5, ls=':',
         alpha=0.6, label='Intrinsic value max(S−K, 0)')
ax1.axvline(K, color=COLORS['grid'], lw=1.2, ls='--', alpha=0.8)
ax1.text(K + 1, ax1.get_ylim()[0] + 1, f'K={K}', color=COLORS['text'], fontsize=9)
ax1.fill_between(S, np.maximum(S - K, 0), black_scholes_call(S, K, r, sigma, 1.0),
                 alpha=0.08, color=COLORS['e_gold'], label='Time value (T=1y)')

ax1.set_xlabel('Stock Price S ($)', fontsize=12)
ax1.set_ylabel('Call Option Price C ($)', fontsize=12)
ax1.set_title('Black-Scholes Call Price\nC = S·N(d₁) − K·e⁻ʳᵀ·N(d₂)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.25)

# ── Panel 2: The e^(-rT) discount factor ─────────────────────────────────────
ax2 = fig.add_subplot(gs[1])

T_range = np.linspace(0, 30, 400)
r_rates = [0.02, 0.05, 0.08, 0.12]
r_colors = [COLORS['e_cyan'], COLORS['e_gold'], COLORS['e_orange'], COLORS['e_red']]

for rate, color in zip(r_rates, r_colors):
    discount = np.exp(-rate * T_range)
    ax2.plot(T_range, discount, color=color, lw=2.2, label=f'r = {rate*100:.0f}%')
    # Half-life: T such that e^(-rT) = 0.5  →  T = ln2/r
    half_life = np.log(2) / rate
    ax2.scatter([half_life], [0.5], color=color, s=60, zorder=5)
    ax2.annotate(f'{half_life:.1f}y', (half_life, 0.5),
                 textcoords='offset points', xytext=(5, -12),
                 fontsize=7.5, color=color)

ax2.axhline(0.5, color=COLORS['grid'], lw=1, ls=':', alpha=0.7)
ax2.fill_between(T_range, np.exp(-0.05 * T_range), alpha=0.08, color=COLORS['e_gold'])
ax2.set_xlabel('Time to maturity T (years)', fontsize=12)
ax2.set_ylabel('Discount factor  e⁻ʳᵀ', fontsize=12)
ax2.set_title('e⁻ʳᵀ Discount Factor\nPresent Value of Strike Payment',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.25)

# ── Panel 3: d₁, d₂, and N(d₁), N(d₂) vs stock price ────────────────────────
ax3 = fig.add_subplot(gs[1])  # will be overwritten; redefine:
ax3 = fig.add_subplot(gs[2])

T_fixed = 1.0
d1_vals = (np.log(S / K) + (r + 0.5 * sigma**2) * T_fixed) / (sigma * np.sqrt(T_fixed))
d2_vals = d1_vals - sigma * np.sqrt(T_fixed)

ax3.plot(S, norm.cdf(d1_vals), color=COLORS['e_green'], lw=2.5,
         label='N(d₁)  [delta proxy]')
ax3.plot(S, norm.cdf(d2_vals), color=COLORS['e_cyan'], lw=2.5, ls='--',
         label='N(d₂)  [risk-neutral P(ITM)]')

ax3.axvline(K, color=COLORS['grid'], lw=1.2, ls='--', alpha=0.7, label='Strike K')
ax3.axhline(0.5, color=COLORS['grid'], lw=1, ls=':', alpha=0.5)
ax3.fill_between(S, norm.cdf(d1_vals), norm.cdf(d2_vals),
                 alpha=0.12, color=COLORS['e_gold'], label='N(d₁)−N(d₂) spread')

ax3.set_xlabel('Stock Price S ($)', fontsize=12)
ax3.set_ylabel('Probability', fontsize=12)
ax3.set_title('Risk-Neutral Probabilities\nN(d₁) and N(d₂)  (T=1y)',
              fontsize=13, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)
ax3.set_ylim(-0.02, 1.02)

fig.suptitle(
    'Black-Scholes  C = S·N(d₁) − K·e⁻ʳᵀ·N(d₂)  —  e Powers Options Pricing',
    fontsize=14, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'black_scholes', OUTPUT_DIR)
plt.close(fig)
