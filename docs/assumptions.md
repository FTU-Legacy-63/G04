# Assumptions: FinFlow V5

Every number the engine uses, with its source and status. The values are kept in
[Assumptions_Summary.csv](../data/financial_assumptions/Assumptions_Summary.csv)
and cross-checked against the code in [`src/index.html`](../src/index.html):
**48 parameters + 13 listing figures compared, 0 mismatches**
([Code_Cross_Check.csv](../data/financial_assumptions/Code_Cross_Check.csv)).
Scenario and sensitivity numbers with their base year are in
[Scenarios_Sensitivity.csv](../data/financial_assumptions/Scenarios_Sensitivity.csv).
Links to sources: [data_and_sources.md](data_and_sources.md). How the numbers are used in formulas: [financial_logic.md](financial_logic.md). What can go wrong: [limitations.md](limitations.md).

**Status:** CONFIRMED = has a source or a team decision; PROPOSED = calculated by the team, not independently confirmed.
All rates are stored as fractions (0.083 = 8.3%).

## 1. Loan (MB Bank, Van Phuc Branch rate sheet)

Every loan parameter comes from the MB Van Phuc rate sheet (photo: [mb_bank_rate.jpg](../data/financial_assumptions/mb_bank_rate.jpg)), except the two values the sheet does not give (reference rate, maximum age).

| Assumption | Value | Status | Note |
|---|---|---|---|
| Promo rate (user picks 6 / 12 / 18 / 24 months) | 7.7 / **8.3** / 8.5 / 9.0% | CONFIRMED | Default 12 months |
| Floating margin after promo | +1.5% for 12 months, then +3.5% | CONFIRMED | |
| Floating reference rate | 10.5% (sensitivity 9.5–11.5%) | CONFIRMED (team decision 08/10) | **Extrapolated**: the MB sheet gives no value. Market floating rate 13–15% (Thanh Niên 25/08/2026, Dan Tri 24/08/2026) minus the 3.5% margin. VCB 7.5% and the State Bank 6.96% are average lending rates for all loans, so they are shown only as a cross-check |
| Rate adjustment frequency | 3 months | CONFIRMED | Not simulated; the rate is fixed within each phase |
| Interest-only grace period | 24 months | CONFIRMED | |
| Early repayment fee | 1% in years 1–5, 0% from year 6 | CONFIRMED | |
| Max LTV (loan-to-value: loan as a share of the home price) | 80% base and Boom; 70% Downturn | CONFIRMED | 80% is the MB maximum. Boom does **not** use the 100% packages of VCB/BIDV because every other loan number comes from MB. Downturn 70% = VCB "Nhà mới thành đạt" package (banks tighten) |
| Max term | min(360 months, (70 − older borrower's age) × 12) | CONFIRMED | Older age is used when two borrowers (team assumption, prudent) |
| Max borrower age at payoff | 70 (sensitivity 65 / 75) | CONFIRMED (team decision 08/10) | Main source VIB, plus Cake, Onlinebank–MB, Standard Chartered. Blocked if the older borrower is ≥ 70 or the max term is ≤ 24 months |
| Repayment method | Equal principal after grace, interest on declining balance | n/a | |
| Down payment | savings − 2.6% buying costs − emergency fund; loan = price − down payment | CONFIRMED (07/10) | Eligible only if savings ≥ 20% of price + 2.6% of price + emergency fund |

## 2. One-off and recurring costs

| Assumption | Value | Status | Note |
|---|---|---|---|
| Buying costs | 2.6% of price (2% maintenance fund + 0.5% registration tax + ~0.06% notary) | CONFIRMED | Paid in cash, not financed. Legal basis: Law on Housing 2023 Art. 152 (2%), Decree 10/2022 as amended by 175/2025 (0.5%), Circular 257/2016 (notary). The 2% may not apply to resale units (about 0.56% then); kept as prudent |
| Emergency fund | 6 months of living costs (user input) | CONFIRMED | Always held in savings; same rule for BUY and RENT; the floor grows with living costs |
| Service fee | 10,000 VND/m²/month × unit area, grows with CPI; **paid by both** BUY and RENT | CONFIRMED (team choice 09/10) | Hanoi cap for lift buildings is 16,500 (Decision 33/2025/QĐ-UBND), used as sensitivity. Real buildings: about 5,000 to 14,000 |
| Fire insurance | 0.05% of price per year, grows with CPI; BUY only | CONFIRMED | Decrees 67/2023 and 105/2025. The law uses rebuilding cost, the model uses price, so this is an upper bound |
| In-unit repairs | 0 in the main result; sensitivity 1% of price per year | CONFIRMED (excluded from main result) | Weakest-sourced item (Metrobank 1% rule, halved because the maintenance fund and service fee already cover shared parts) |
| Selling cost | 1.5% of home value (broker) subtracted from BUY net worth every year, including year 0 | CONFIRMED (team choice 09/10) | Broker fee 1–2%. Sensitivity 3.5% |
| Personal income tax on sale | 0% | CONFIRMED | Assumes the only home owned and held at least 183 days. In the code it is folded into the selling cost (3.5% = 1.5% + 2% tax in the sensitivity row) |
| Broker fee when renting | 0 | CONFIRMED | Normally paid by the landlord |
| Rental deposit | **Not modelled** (about 2 months of rent) | Market practice | About 1.8 million VND of lost interest a year; listed as a limitation |

## 3. Growth assumptions

| Assumption | Value | Status | Source |
|---|---|---|---|
| Home price growth (PA2, base) | starts 20.43%, eases to 8.38%: g(t) = 8.38% + (20.43% − 8.38%) × e^(−t/3.24) | CONFIRMED | Start: 2020–2025 CAGR (compound annual growth rate) of primary prices (CafeF, Cushman & Wakefield). Long-run: CPI 3.09% + real GDP per capita 5.29% (World Bank). τ (cooling time) = 3.24 so that the next 10 years average 12.66%, like 2016–2025. Result: about ×17 after 30 years |
| Home price growth, upper bound | PA1: 19% fixed | Reference only | Kept as an optimistic sensitivity (×185 after 30 years, not realistic as a base) |
| Rent growth | 6% per year (sensitivity 3 / 7 / 10%) | CONFIRMED (09/10) | VnExpress 08/2025, Vietnambiz 04/2025. Close to income growth, so rent/income stays near 30–34% over 30 years (7% would reach 45%, 10% would exceed 100%) |
| Income growth | 5.56% per year (σ 5.71) | CONFIRMED | NSO household living standards survey 2024 (Red River Delta), p. 283, 2019–2024, nominal |
| Living cost growth (CPI) | 3.09% per year | PROPOSED | World Bank CPI 2016–2025 |

Income, living costs and rent growth are always switched on together; enabling only rent growth would make RENT look worse than it is.

**Rent-yield check (not an input to the engine).** Year-0 rental yield (yearly rent ÷ price) is 2.3% (median of the 71 buildings that have both a sale and a rent listing, team data) to 3.74% (Global Property Guide, 2-bedroom Hanoi, Q3/2025). PROPOSED. It feeds only the "Reality check" card on the result page. It is the reason PA2 was chosen over PA1: with PA1 the yield falls to about 0.1% after 30 years.

## 4. Investment channels (spare cash and RENT's initial savings)

Default mix is 100% savings; the user can change it in Step 4. Rebalanced every 12 months. Withdrawals when short are taken pro rata across channels, then from the emergency fund.

| Channel | Return | σ | Draw | Status | Source |
|---|---|---|---|---|---|
| Savings | 6.50% | 0.82% | once per path | PROPOSED | FiinPro deposit rates 6–12 months (highest rate 2016–2026, so an upper bound); DIV 01/2026 |
| Stocks | 7.99% | 19.30% | each year | PROPOSED | VN-Index 05/2021–08/2026 (investing.com), price only, no dividends |
| Bonds | 4.02% | 1.37% | once per path | PROPOSED | 10-year government bond, FiinPro; σ is that of the yield level |
| Gold | 11.12% | 14.13% | each year | CONFIRMED (07/10) | SJC 02/2016–12/2024 (monthly mean × 12); the +81.5% year of 2025 is excluded; 14.89% with 2025 is a sensitivity |

## 5. Safety rule

| Item | Value |
|---|---|
| Safe level (share of income that must remain after living costs, debts and housing costs) | 40% / 35% / 30% / 25% for income under 35 / 35–49 / 50–74 / 75+ million VND (income in today's money) |
| Checked | Every month of the loan, for BUY and RENT; the tightest month is reported |
| Existing debt | Same monthly amount, stops after the number of months the user enters (blank = whole term) |
| Comfortable / Tight / Not safe | Passes with at least 5 points above the safe level / passes with less / below the safe level in at least one month |
| Running out of savings | Main measure: the emergency fund has to be used. Secondary: money runs out completely; the shortfall then accumulates without interest |
| Optional smooth thresholds | Off. Linear interpolation (40% @ 35M, 35% @ 50M, 30% @ 75M, 25% @ 100M) runs as a sensitivity row |
| Risk label | Share of 1,000 futures that touch the emergency fund: under 10% low, 10–25% moderate, over 25% high (team convention) |

Source of the tiers: team proposal; the 25% top tier is interpolated. CFPB and DNSE are qualitative references only (a DTI ratio, debt-to-income, does not subtract living costs).

## 6. Monte Carlo

| Setting | Value |
|---|---|
| Runs | **1,000** (fixed; the same input always gives the same result) |
| Random generator | mulberry32, seed 20260909 |
| Sensitivity | 17 rows (base + 16), 500 runs per row, computed on click |
| Shocks (σ) | Reference rate 0.75 pt, home price 4 pt (one draw per path), rent growth 1.25 pt (one draw per path), income 5.71 pt per year, savings 0.82 (per path), bonds 1.37 (per path), gold 14.13 (per year), stocks 19.30 (per year). CPI is not random |
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

Each scenario copies a real period in 2016–2026 data (for example Boom = the 2020–2025 surge cooling twice as slowly; Downturn = a repeat of 2016–2020 and of 2022 deposit and bond yields). Only the means move; σ stays as in section 6. CPI, stocks, gold and holding/selling costs stay the same in all three. The loan term does not change with the scenario.

## 8. Sensitivity rows (one variable at a time, others at Stable)

Home-price cooling τ = 1 / 6.5 · PA1 19% fixed · rent growth 3 / 7 / 10% · max age 65 / 75 · LTV 70% · gold 14.89% · income −1.6% in years 2–3 (like 2020–21) · service fee 16,500 · repairs 1% · selling cost 3.5% · correlation ρ = 0.5 · smooth safe level.

## 9. Modelling and user-behaviour assumptions

1. Date zero is 2026-09-09; listing data is a static snapshot of asking prices, not closing prices.
2. The data holds 205 buildings, 756 sale listings and 277 rent listings, all 2-bedroom apartments in Tay Ho, Cau Giay and Ha Dong. Median unit: 72 m² (sale) and 80 m² (rent); median rent 15 million VND a month. The tool uses these figures for the budget card; they were recomputed from the data embedded in `index.html` and match the plan.
3. The user enters honest figures; only format and basic ranges are validated.
4. Shortfalls after the emergency fund is empty accumulate without interest (no consumer loan is modelled).
5. Buy-to-let was dropped on 07/10; there is no rental income for the BUY side.
6. The comparison horizon N defaults to 10 years (or the loan term if shorter); the user can pick 20 years or the full term. Changing N reads the same Monte Carlo result, it does not rerun it, and safety is still checked for the whole loan term.
7. Money is shown in nominal terms by default. The "In today's money" button divides year t by (1 + CPI)^t (about ÷1.36 at year 10 and ÷2.5 at year 30); the conclusion does not change because BUY and RENT are divided by the same number.
8. Budget labels on the unit cards (Within budget, Payment too tight, Not enough savings, No loan available) use the Stable scenario and the chosen promo package; they do not change when the user clicks Boom or Downturn.
