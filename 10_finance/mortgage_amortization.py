"""
Mortgage amortization: exponential decay of principal.
M = P·(r/12) / (1 − (1 + r/12)^(-n))
Shows how e^x connects to the amortization formula.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

apply_euler_style()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def amortization_schedule(P, annual_rate, years):
    """Return arrays of remaining principal, interest paid, and principal paid per month."""
    r_monthly = annual_rate / 12
    n_months  = years * 12
    # Monthly payment formula
    M = P * r_monthly / (1 - (1 + r_monthly) ** (-n_months))
    principal_remaining = [P]
    interest_paid       = [0]
    cumulative_interest = [0]
    cumulative_principal= [0]
    monthly_interest    = []
    monthly_principal   = []

    bal = P
    cum_int = 0.0
    cum_pri = 0.0
    for _ in range(n_months):
        interest   = bal * r_monthly
        principal  = M - interest
        bal       -= principal
        bal        = max(bal, 0)
        cum_int   += interest
        cum_pri   += principal
        principal_remaining.append(bal)
        cumulative_interest.append(cum_int)
        cumulative_principal.append(cum_pri)
        monthly_interest.append(interest)
        monthly_principal.append(principal)

    months = np.arange(n_months + 1)
    return (months,
            np.array(principal_remaining),
            np.array(cumulative_interest),
            np.array(cumulative_principal),
            M,
            np.array(monthly_interest),
            np.array(monthly_principal))


P_loan = 400_000   # $400,000 mortgage
rate   = 0.065     # 6.5% annual
years  = 30

months, principal, cum_interest, cum_principal, M, mo_interest, mo_principal = \
    amortization_schedule(P_loan, rate, years)

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.42)

# ── Panel 1: Remaining principal over time ────────────────────────────────────
ax1 = fig.add_subplot(gs[0])

ax1.plot(months / 12, principal / 1e3, color=COLORS['e_gold'], lw=2.8,
         label='Remaining principal')

# Overlay continuous exponential approximation
# The principal decays faster than pure exponential but we can show the e connection
# Exponential approximation: P·e^(-λt) where λ chosen to match final payoff
# Pure exponential decay line for comparison
t_cont = np.linspace(0, years, 400)
lam_approx = math.log(2) / (years * 0.55)   # visual approximation
ax1.plot(t_cont, P_loan * np.exp(-lam_approx * t_cont) / 1e3,
         color=COLORS['e_cyan'], lw=1.8, ls='--', alpha=0.7,
         label=f'Approx P·e⁻λᵗ')

ax1.fill_between(months / 12, principal / 1e3, alpha=0.12, color=COLORS['e_gold'])

# Mark halfway point
idx_half = np.argmin(np.abs(principal - P_loan / 2))
ax1.scatter([months[idx_half] / 12], [principal[idx_half] / 1e3],
            color=COLORS['e_red'], s=100, zorder=5,
            label=f'50% paid off at {months[idx_half]/12:.1f}y')

ax1.set_xlabel('Time (years)', fontsize=12)
ax1.set_ylabel('Principal Remaining ($000s)', fontsize=12)
ax1.set_title(f'$400k Mortgage @ {rate*100:.1f}%, 30 Years\nM = ${M:,.2f}/month',
              fontsize=12, color=COLORS['e_gold'], pad=10)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.25)

# ── Panel 2: Cumulative interest vs principal paid ────────────────────────────
ax2 = fig.add_subplot(gs[1])

ax2.stackplot(months / 12, cum_principal / 1e3, cum_interest / 1e3,
              colors=[COLORS['e_green'], COLORS['e_red']],
              alpha=0.75, labels=['Cumulative principal paid', 'Cumulative interest paid'])
ax2.axhline(P_loan / 1e3, color=COLORS['text'], lw=1.2, ls=':', alpha=0.7,
            label=f'Original loan ${P_loan/1e3:.0f}k')
ax2.axhline((cum_interest[-1] + P_loan) / 1e3, color=COLORS['e_orange'],
            lw=1.2, ls='--', alpha=0.8,
            label=f'Total paid ${(cum_interest[-1]+P_loan)/1e3:.0f}k')

ax2.set_xlabel('Time (years)', fontsize=12)
ax2.set_ylabel('Cumulative Amount ($000s)', fontsize=12)
ax2.set_title(f'Cumulative Payments\nTotal interest = ${cum_interest[-1]/1e3:.0f}k',
              fontsize=12, color=COLORS['e_gold'], pad=10)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.25)

# ── Panel 3: Exponential connection & monthly breakdown ──────────────────────
ax3 = fig.add_subplot(gs[2])

# Show how the closed-form formula uses e
# M = P·r/(1 − e^(−r·n)) in the continuous limit (r→continuous)
# Plot monthly interest vs principal payment over time
t_years = months[1:] / 12
ax3.plot(t_years, mo_interest / M * 100, color=COLORS['e_red'], lw=2.2,
         label='% of payment = interest')
ax3.plot(t_years, mo_principal / M * 100, color=COLORS['e_green'], lw=2.2,
         label='% of payment = principal')
ax3.fill_between(t_years, mo_interest / M * 100, alpha=0.12, color=COLORS['e_red'])
ax3.fill_between(t_years, mo_principal / M * 100, alpha=0.12, color=COLORS['e_green'])
ax3.axhline(50, color=COLORS['grid'], lw=1, ls='--', alpha=0.7)

# Mark crossover point (when principal payment > interest payment)
crossover = np.argmax(mo_principal > mo_interest)
ax3.axvline(crossover / 12, color=COLORS['e_gold'], lw=1.5, ls='--',
            label=f'Crossover at {crossover/12:.1f}y')

ax3.set_xlabel('Time (years)', fontsize=12)
ax3.set_ylabel('% of Monthly Payment', fontsize=12)
ax3.set_title('Monthly Payment Breakdown\nInterest Decays Exponentially',
              fontsize=12, color=COLORS['e_gold'], pad=10)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.25)
ax3.set_ylim(0, 100)

fig.suptitle('Mortgage Amortization  M = P·(r/12)/(1−(1+r/12)⁻ⁿ)  —  Exponential Decay of Debt',
             fontsize=13, color=COLORS['e_gold'], y=1.02, fontweight='bold')

save_plot(fig, 'mortgage_amortization', OUTPUT_DIR)
plt.close(fig)
