# Assumptions — FinFlow (BUY vs RENT, Cau Giay)

## 1. Financial assumptions (`FIN_ASSUMPTIONS` in `finflow.html`)

| Assumption | Current value | Why it's needed | Risk if wrong |
|---|---|---|---|
| Fixed interest rate per phase for the whole loan term (no simulation of the reference rate moving over time) | 8.3%/year for the first 12 months (promo) → 10.5% + 1.5% = 12%/year for months 13–24 → 10.5% + 3.5% = 14%/year from month 25 onward | Keeps the repayment schedule deterministic (declining-balance amortization) without needing a Monte Carlo simulation | The real reference rate can move up or down after the promo period ends — actual borrowing cost could be higher or lower than shown |
| No prepayment fee / early payoff penalty | Not modeled — only principal + interest are calculated | Keeps the formula simple for the demo | Many Vietnamese banks do charge an early-payoff penalty — the demo's numbers are optimistic for a user who intends to pay off early |
| `grace_period_months = 24`: the first 24 months are interest-only, no principal repayment | 24 months | Reflects a grace-period structure common in home-loan products | — |
| `max_loan_to_value_pct = 80%`: if `savings < min_down_payment`, the app returns an explicit error instead of silently shrinking the loan | 80% | Prevents the app from quietly "fixing" the user's input without telling them | A user who doesn't read the error message might think the product is broken rather than understanding they need more savings |
| `buy_closing_costs_pct = 2.6%`: added on top of the LTV-based down payment, paid in cash (not financed into the loan) | 2.6% | `min_down_payment` and the loan itself would otherwise understate what a buyer needs in cash upfront | If the real closing-cost percentage differs, the minimum-savings check will be too strict or too lenient |
| `Loan_term_months = 360` (default, editable by the user in Step 3) | 360 months | Common long-term tenor for a home loan | — |
| `investment_return_pct = 6%/year`: leftover monthly cash (after loan/rent + living costs) is assumed to be invested and compound monthly | 6% | A single number is needed to project net worth over time (Step 4 chart) | This is an **educational** assumption, not tied to any specific investment channel (savings account, stocks, etc.) — it should not be read as investment advice |
| `property_annual_appreciation_pct = 12%/year`: property value is assumed to grow at a flat 12%/year for the entire loan term | 12% | A single number is needed to project `property_value(t)` for the BUY net-worth curve | A flat 30-year growth rate is unrealistic — real estate moves in cycles of growth, plateau, and decline. The in-app disclaimer under the net-worth chart already flags this and cites two sources: [Ministry of Construction, Dec 2025](https://vnexpress.net/bo-xay-dung-gia-nha-o-tang-binh-quan-10-15-moi-nam-4994992.html) (nationwide home prices ~10–15%/year on average) and [Global Property Guide](https://www.globalpropertyguide.com/asia/vietnam/price-history) (+21% primary / +13% secondary) — 12% sits inside that range but is still a simplification |
| Rent growth is not modeled — the rent figure is held constant for the entire comparison period | 0% (no field for this in the current code) | Keeps the RENT net-worth formula a closed-form calculation instead of a month-by-month loop | Real rent typically rises over time (inflation, market pressure) — the demo likely **overstates** RENT's net worth in the later years of the comparison |
| `bedrooms` is fixed at 2.0 when matching listings | 2.0 | Keeps the demo's data scope narrow | The product currently does not serve users looking for apartments with a different bedroom count |
| Listings are matched exactly on `(ward_old, size_band, bedrooms)` — no averaging, ranking, distance tolerance, or "best pick" suggestion | — | Keeps the matching logic simple and predictable | The user has to pick manually from every matching listing instead of being shown a single recommended unit |

## 2. Assumptions about user behavior

| Assumption | Note |
|---|---|
| The user enters financial figures (income, savings, living cost) **accurately and honestly** | The product does not cross-check these against any external source (e.g., a bank statement) — only format is validated (numeric, non-negative), not truthfulness |
| The user understands that all money inputs on the UI are in **million VND** | Every input field states its unit; the conversion to VND happens exactly once, in JavaScript, immediately before the calculation runs |
| A household's income comes from exactly two sources (`income1`, `income2`) | Single-earner households enter `0` for `income2`; households with more than two income sources aren't directly supported |

## 3. Minimum safety-margin threshold (`getSafetyMarginMinPct`)

This is a rule/threshold, tiered by total household income per month:

| Total household income (million VND/month) | `safety_margin_min_pct` |
|---|---|
| < 35 | 40% |
| 35 – < 50 | 35% |
| 50 – < 75 | 30% |
| ≥ 75 | 25% |

`safety_margin = money_remaining / total_income`, where `money_remaining = income1 + income2 − living_cost − existing_debt − monthly_repayment_or_rent`. A result is judged "safe" when `safety_margin ≥ safety_margin_min_pct`.

**Open risk:** the top tier (25%, for households earning ≥75 million VND/month) has not been confirmed against an authoritative source. The [CFPB Ability-to-Repay / Qualified Mortgage rule](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf) can serve as a general reference point for how a debt-to-income-style threshold is reasoned about, but it's a US standard, not a Vietnamese banking benchmark, and its DTI metric isn't computed the same way as `safety_margin` (it doesn't subtract living costs) — so it should not be cited as a direct source for this specific number.

## 4. Design decisions locked into the current logic

1. Listing matching is exact on `(ward_old, size_band, bedrooms)` — no averaging, ranking, tolerance windows, or distance-based (e.g., Haversine) matching.
2. The million-VND → VND conversion happens exactly once, in the JS layer, immediately before the calculation functions are called.
3. Insufficient own capital is never silently patched by shrinking the loan amount — it always surfaces as an explicit error stating the exact shortfall (`"You need at least X more in savings..."`).
