# Data Flow — FinFlow (BUY vs RENT, Cau Giay)

| Source | Input | Validation | Process | Output |
|---|---|---|---|---|
| BUY_LISTINGS / RENT_LISTINGS (embedded in the page's `<script>`) | `ward_old`, `size_band` (chosen in Step 1) | Must match one of the unique values loaded from the data at page load | Listings filtered on exact `(ward_old, size_band, bedrooms=2.0)` | Card list of matching BUY/RENT listings (Step 2) |
| Card list (above) | `buy_listing`, `rent_listing` (chosen in Step 2) | Must have `total_price_vnd` / `rent_monthly_vnd > 0` | User clicks to select exactly one BUY and one RENT card | Two selected listing objects |
| User types manually (Step 3, in million VND) | `income1`, `income2`, `savings`, `living_cost`, `existing_debt`, `loan_term_months` | Must be valid, non-negative numbers; `loan_term_months` (if entered) must be a whole number > 0 | Values are multiplied by 1,000,000 exactly once, right before the calculation is called | income/savings/etc. in VND (converted from the million-VND UI unit) |
| All of the above | `evaluateBuyVsRent(...)` | `income1 + income2 > 0` (guards against dividing by zero in `safety_margin`) | `loanCalc()` runs the declining-balance amortization and, in the same pass, builds the BUY net-worth series → `evaluateBuy()` / `evaluateRent()` compute `safety_margin` against the income-tiered threshold (see `assumptions.md` §3) → `netWorthRentSchedule()` (closed-form formula, no loop needed) → `findBreakEven()` locates the crossover month, if any → `decide()` picks BUY / RENT / NEITHER | `result = { buy, rent, decision, reason, net_worth: { buy_series, rent_series, break_even_month, break_even_year } }` |
| result (above) | `buildNetWorthTimeline()` | — | Monthly series re-sampled into yearly points (`t = 12, 24, 36, ...`) | Step 4: two result cards (with safety badges) + the yearly net-worth chart (break-even marked if one exists) |

## Worked example

This traces the exact same input used in `validation-and-early-logic-test.md`'s Case A, end to end through the pipeline above:

BUY_LISTINGS / RENT_LISTINGS (embedded data)

→ user picks a BUY unit priced at 3,000,000,000 VND

→ user picks a RENT unit priced at 30,000,000 VND/month

→ user enters income1=40M, income2=25M, savings=1,000M, living_cost=15M, loan_term=360 (all in million VND)

→ validation passes (savings 1,000M ≥ min_down_payment 678M)

→ loanCalc(): required_loan = 2,000,000,000; monthly_repayment (month 1) = 13,833,333

→ evaluateBuyVsRent(): decision = "BUY", reason = "BUY meets the safety threshold. (Note: BUY and RENT have fairly close safety margins — consider other factors beyond this model.)"

→ buildNetWorthTimeline(): 30 yearly points; net_worth_buy at year 30 ≈ 119,778,517,547 VND

**### Input validation**

The full list of validation checks (required fields, number format, negative values, the insufficient-savings business rule, etc.) is documented once, in validation-and-early-logic-test.md §1, to avoid duplicating it here — this file only shows where validation sits in the pipeline (the step right after Step 3, before evaluateBuyVsRent() is called).

For a static, human-readable snapshot of the same source data used in Source above, see data.md §6.
