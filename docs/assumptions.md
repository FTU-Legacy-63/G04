# Assumptions: FinFlow V5

Every number the engine uses, with its source and status. Values are stored in
[data/Supporting_data_for_fin_assumptions_v6_1.xlsx](../data/Supporting_data_for_fin_assumptions_v6_1.xlsx)
(sheet `FIN_ASSUMPTIONS_tong_hop`) and cross-checked against `src/index.html`:
48 parameters compared, 0 mismatches (sheet `Doi_chieu_index_html`).
Links to sources: [data_and_sources.md](data_and_sources.md). What can go wrong: [limitations.md](limitations.md).

**Status:** CONFIRMED = has a source or a team decision; PROPOSED = calculated by the team, not independently confirmed.
All rates are stored as fractions (0.083 = 8.3%).

## 1. Loan (MB Bank, Van Phuc Branch rate sheet)

| Assumption | Value | Status | Note |
|---|---|---|---|
| Promo rate (user picks 6 / 12 / 18 / 24 months) | 7.7 / **8.3** / 8.5 / 9.0% | CONFIRMED | Default 12 months |
| Floating margin after promo | +1.5% for 12 months, then +3.5% | CONFIRMED | |
| Floating reference rate | 10.5% (sensitivity 9.5–11.5%) | CONFIRMED (team decision 08/10) | **Extrapolated**: the MB sheet gives no value. Market floating rate 13–15% minus 3.5% margin |
| Rate adjustment frequency | 3 months | CONFIRMED | Not simulated; rate is fixed per phase |
| Interest-only grace period | 24 months | CONFIRMED | |
| Early repayment fee | 1% in years 1–5, 0% from year 6 | CONFIRMED | |
| Max LTV | 80% base; 100% Boom; 70% Downturn | CONFIRMED | Boom / Downturn from VCB, BIDV, Vietinbank products |
| Max term | min(360 months, (70 − older borrower's age) × 12) | CONFIRMED | Older age is used when two borrowers (team assumption) |
| Max borrower age at payoff | 70 (sensitivity 65 / 75) | CONFIRMED (team decision 08/10) | Blocked if the older borrower is ≥ 70 or max term ≤ 24 months |
| Repayment method | Equal principal after grace, interest on declining balance | n/a | |

## 2. One-off and recurring costs

| Assumption | Value | Status | Note |
|---|---|---|---|
| Buying costs | 2.6% of price (2% maintenance fund + 0.5% registration tax + ~0.06% notary) | CONFIRMED | Paid in cash, not financed. The 2% may not apply to resale units (about 0.56% then); kept as prudent |
| Emergency fund | 6 months of living costs (user input) | CONFIRMED | Always held in savings; same rule for BUY and RENT |
| Service fee | 10,000 VND/m²/month × unit area, grows with CPI; **paid by both** BUY and RENT | CONFIRMED (team choice 09/10) | Hanoi cap for lift buildings is 16,500 (sensitivity) |
| Fire insurance | 0.05% of price per year, grows with CPI; BUY only | CONFIRMED | |
| In-unit repairs | 0 in main result; sensitivity 1% of price per year | CONFIRMED (excluded from main result) | Weakest-sourced item |
| Selling cost | 1.5% of home value (broker) subtracted from BUY net worth every year, incl. year 0 | CONFIRMED (team choice 09/10) | Sensitivity 3.5% |
| Personal income tax on sale | 0% | CONFIRMED | Assumes the only home owned and held > 183 days |
| Rental deposit | **Not modelled** (about 2 months of rent) | Market practice | Small effect, listed as limitation |

## 3. Growth assumptions

| Assumption | Value | Status | Source |
|---|---|---|---|
| Home price growth (PA2, base) | starts 20.43%, eases to 8.38%: g(t) = 8.38% + (20.43% − 8.38%) × e^(−t/3.24) | CONFIRMED | Start: 2020–2025 CAGR of primary prices (CafeF, Cushman & Wakefield). Long-run: CPI 3.09% + real GDP/capita 5.29% (World Bank). τ = 3.24 so that the next 10 years average 12.66% like 2016–2025 |
| Home price growth, upper bound | PA1: 19% fixed | Reference only | Kept as optimistic sensitivity |
| Rent growth | 6% per year (sensitivity 3 / 7 / 10%) | CONFIRMED (09/10) | VnExpress 08/2025, Vietnambiz 04/2025; close to income growth so rent/income stays near 30–34% over 30 years |
| Income growth | 5.56% per year (σ 5.71) | CONFIRMED | NSO household survey 2024 (Red River Delta), 2019–2024 |
| Living cost growth (CPI) | 3.09% per year | PROPOSED | World Bank CPI 2016–2025 |

Income, living costs and rent growth are always switched on together; enabling only rent growth would make RENT look worse than it is.

## 4. Investment channels (spare cash and RENT's initial savings)

Default mix is 100% savings; the user can change it in Step 4. Rebalanced every 12 months. Withdrawals when short are taken pro rata across channels, then from the emergency fund.

| Channel | Return | σ | Draw | Status | Source |
|---|---|---|---|---|---|
| Savings | 6.50% | 0.82% | once per path | PROPOSED | FiinPro deposit rates (highest 2016–2026, upper bound); DIV 01/2026 |
| Stocks | 7.99% | 19.30% | each year | PROPOSED | VN-Index 05/2021–08/2026 (investing.com), price only, no dividends |
| Bonds | 4.02% | 1.37% | once per path | PROPOSED | 10-year government bond, FiinPro |
| Gold | 11.12% | 14.13% | each year | CONFIRMED (07/10) | SJC 02/2016–12/2024; the +81.5% year of 2025 is excluded; 14.89% with 2025 is a sensitivity |

## 5. Safety rule

| Item | Value |
|---|---|
| Safe level (share of income that must remain after living costs, debts and housing costs) | 40% / 35% / 30% / 25% for income under 35 / 35–49 / 50–74 / 75+ million VND (income in today's money) |
| Checked | Every month of the loan, for BUY and RENT; the tightest month is reported |
| Comfortable / Tight / Not safe | Passes with at least 5 points above the safe level / passes with less / below the safe level in at least one month |
| Optional smooth thresholds | Off. Linear interpolation (40% @ 35M, 35% @ 50M, 30% @ 75M, 25% @ 100M) runs as a sensitivity row |
| Risk label | Share of 1,000 futures that touch the emergency fund: under 10% low, 10–25% moderate, over 25% high (team convention) |

Source of the tiers: team proposal; the 25% top tier is interpolated. CFPB and DNSE are qualitative references only (a DTI ratio does not subtract living costs).

## 6. Monte Carlo

| Setting | Value |
|---|---|
| Runs | **1,000** (fixed; the same input always gives the same result) |
| Random generator | mulberry32, seed 20260909 |
| Sensitivity | 17 rows (base + 16), 500 runs per row, computed on click |
| Shocks (σ) | Reference rate 0.75 pt, home price 4 pt (one draw per path), rent growth 1.25 pt, income 5.71 pt per year, savings 0.82, bonds 1.37, gold 14.13, stocks 19.30 |
| Correlation ρ | 0 by default; 0.5 only as a stress-test row |

σ of home price is 4 points, not 14: one draw covers a 30-year path, so the relevant uncertainty is the average growth (about 14% ÷ √30 ≈ 2.6, rounded up). Several σ come from short series (5–10 observations); see [limitations.md](limitations.md).

## 7. Scenarios (same engine, different inputs)

| Variable | Boom | Stable (base) | Downturn |
|---|---|---|---|
| Reference rate | 9.75% | 10.5% | 11.25% |
| LTV | 80% | 80% | 70% |
| Home price growth | 20.43% → 8.38%, τ = 6.5 | τ = 3.24 | starts 3.64%, τ = 3.24 |
| Rent growth | 10% | 6% | 3% |
| Income growth | 9.29% | 5.56% | 3.09% |
| Savings / bond return | 5.85% / 2.40% | 6.50% / 4.02% | 7.60% / 5.04% |

Each scenario copies a real period in 2016–2026 data. CPI, stocks, gold and holding/selling costs stay the same in all three.

## 8. Sensitivity rows (one variable at a time, others at Stable)

Home-price cooling τ = 1 / 6.5 · PA1 19% fixed · rent growth 3 / 7 / 10% · max age 65 / 75 · LTV 70% · gold 14.89% · income −1.6% in years 2–3 · service fee 16,500 · repairs 1% · selling cost 3.5% · correlation ρ = 0.5 · smooth safe level.

## 9. Modelling and user-behaviour assumptions

1. Date zero is 2026-09-09; listing data is a static snapshot of asking prices.
2. All listings are 2-bedroom apartments in Tay Ho, Cau Giay and Ha Dong.
3. The user enters honest figures; only format and basic ranges are validated.
4. Shortfalls after the emergency fund is empty accumulate without interest (no consumer loan is modelled).
5. Buy-to-let was dropped on 07/10; there is no rental income for the BUY side.
