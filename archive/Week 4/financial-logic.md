# Financial Logic — FinFlow

## 1. Project Logic Chain

| Stage                  | Description                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Problem**            | Young people and households in Hanoi struggle to compare the real cost of BUYING vs. RENTING a home — the two options use different time units and cost structures (a long-term amortizing loan with changing interest rates vs. a fixed monthly rent), making them hard to reduce to one comparable measure. See `../week3/source-register.md` §2 for real evidence that this problem exists. |
| **Target user**        | People aged 25–40 with a stable income, considering their first home purchase in the Cau Giay area of Hanoi, who have some savings but aren't sure whether it's enough — or whether they should put it all toward a home purchase at all.                                                                                                                                                      |
| **User task**          | Enter their own income, savings, and living costs, then pick one specific BUY unit and one specific RENT unit (same area, same size band) to compare directly.                                                                                                                                                                                                                                 |
| **Difficulty**         | Can't work out a declining-balance repayment schedule by hand across changing interest-rate phases (promo → floating year 1 → floating from year 2); doesn't know whether the money left over each month after paying for housing is actually a safe amount; can't visualize how differently BUY vs. RENT would grow their net worth over 5, 10, or 30 years.                                  |
| **Technology support** | A client-side web app (plain HTML/JS, no framework, no backend) that calculates instantly as the user types — nothing is sent to a bank or a server.                                                                                                                                                                                                                                           |
| **Input**              | See `../week3/input-dictionary.md` (user-entered + product information + assumptions).                                                                                                                                                                                                                                                                                                         |
| **Financial logic**    | Declining-balance loan amortization + income-tiered safety-margin thresholds + net-worth projection (BUY: month-by-month accumulation; RENT: closed-form formula) + break-even detection + a BUY/RENT/NEITHER decision rule. Full details in §3 below.                                                                                                                                         |
| **Output**             | Two result cards (BUY/RENT: monthly cost, money left over, a safety progress bar) + one final decision banner + one net-worth-over-time chart (marking the break-even point, if one exists).                                                                                                                                                                                                   |
| **User action**        | Decide whether to BUY or RENT the selected unit, or go back to Step 1–2 to try a different combination (ward, size band, listing).                                                                                                                                                                                                                                                             |

## Self-check

* **Is the input actually relevant to the task?** Yes — every input (income, savings, living cost, home price, rent, loan term) is used directly in a formula; there's no "decorative" input that goes unused.
* **Does the logic use the input?** Yes — see the full mapping in §2 below.
* **Does the output reflect the logic?** Yes — every displayed number (monthly cost, money left over, safety margin %, net worth by year) traces back to exactly one calculation in `finflow.html`.
* **Can the user act on the output?** Yes — the BUY/RENT/NEITHER decision, plus a way to go back and pick a different listing.
* **Is technology's role clear?** Yes — the web app recalculates instantly whenever the user changes an input, instead of requiring a 360-row repayment schedule to be worked out by hand.

## 2. Input → Logic → Output Mapping

| Input                                                                                                              | Financial meaning                                                                                      | Rule / calculation / process                                                                                                                                                                                                                                               | Output                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `total_price_vnd` (BUY), `savings`, `max_loan_to_value_pct`, `buy_closing_costs_pct`                               | Whether the user has enough own capital to qualify for the loan                                        | `min_down_payment = total_price_vnd × (1 − max_loan_to_value_pct/100) + total_price_vnd × (buy_closing_costs_pct/100)`; if `savings < min_down_payment` → BUY is not viable                                                                                                | A clear error message stating exactly how much more is needed — the loan amount is never silently reduced       |
| `total_price_vnd − savings`, the rate schedule, `grace_period_months`                                              | Monthly borrowing cost, which changes over time (grace period → promo ends → floating rate)            | Declining-balance amortization: principal is fixed each month after the grace period, interest is computed on the outstanding balance                                                                                                                                      | `monthly_repayment` for each month (a 360-row schedule)                                                         |
| `income1+income2`, `living_cost`, `existing_debt`, `monthly_repayment`/`monthly_rent`                              | How much money is left over each month after housing costs                                             | `money_remaining = income1+income2 − living_cost − existing_debt − (repayment or rent)`                                                                                                                                                                                    | `money_remaining` (VND/month)                                                                                   |
| `money_remaining`, `income1+income2`                                                                               | Financial safety, judged against a threshold that depends on income level                              | `safety_margin = money_remaining / total_income`; compared against `safety_margin_min_pct` for that income tier (see `../week3/assumptions.md` §3)                                                                                                                         | `safety_margin` (%) + `is_safe` (true/false) + a progress bar                                                   |
| BUY's `safety_margin`/`is_safe` at 2 points in time (grace period and right after)                                 | Whether BUY's affordability holds up once principal repayment begins, not just during the grace period | Evaluate at both points; headline `safety_margin` = the worse (minimum) of the two; headline `is_safe` = both points safe                                                                                                                                                  | Headline `safety_margin`/`is_safe` for BUY, plus the two separate grace/post-grace values shown on the BUY card |
| `safety_margin`/`is_safe` for both BUY and RENT                                                                    | Which option to recommend                                                                              | `decide()`: prefer RENT if RENT is safe AND its margin is higher than BUY's; otherwise BUY if BUY is safe; otherwise RENT if RENT is safe; otherwise NEITHER — plus a "fairly close margins" note appended when both are safe and within 5 percentage points of each other | `decision` (`BUY`/`RENT`/`NEITHER`) + `reason` (an English explanation string)                                  |
| Monthly `money_remaining`, `investment_return_pct`, `property_annual_appreciation_pct`, the remaining loan balance | Net worth accumulated over time if BUYing                                                              | `net_worth_buy(t) = property_value(t) − remaining_loan_balance(t) + invested_balance_buy(t)`, accumulated month by month                                                                                                                                                   | `net_worth_buy` for every month → re-sampled by year for the chart                                              |
| `savings`, `money_remaining` for RENT (constant), `investment_return_pct`                                          | Net worth accumulated over time if RENTing                                                             | `net_worth_rent(t) = savings×(1+r)^t + money_remaining×[((1+r)^t−1)/r]` (closed-form, no loop needed)                                                                                                                                                                      | `net_worth_rent` for every month → re-sampled by year for the chart                                             |
| The two monthly net-worth series                                                                                   | Whether, and when, one option overtakes the other                                                      | `findBreakEven()`: locates the first month where the two series cross (in either direction)                                                                                                                                                                                | `break_even_month`/`break_even_year` (or `null` if they never cross)                                            |

## 3. Formula / Rule / Classification

FinFlow uses **formulas + rules/thresholds + a priority decision rule**. The product does **not** use a weighted scoring model — noted explicitly here to avoid confusion when presenting.

### Formula — monthly interest rate

```text
if t ≤ promo_period_months:                              rate = interest_rate_promo_pct
if promo_period_months < t ≤ promo_period_months + 12:   rate = interest_rate_float_ref_pct + float_rate_margin_year1_pct
otherwise:                                                rate = interest_rate_float_ref_pct + float_rate_margin_from_year2_pct
```

With current values: 8.3% (first 12 months) → 12% (months 13–24) → 14% (from month 25).

### Formula — repayment schedule (declining-balance method)

```text
min_down_payment = purchasePrice × (1 − max_loan_to_value_pct/100)
                  + purchasePrice × (buy_closing_costs_pct/100)

required_loan     = purchasePrice − savings
                    (excludes closing costs — paid in cash)

Each month t (1..loan_term_months):
  if t ≤ grace_period_months:
      principal_payment = 0
      interest_payment  = balance_start × monthly_rate

  otherwise:
      principal_payment = required_loan / (loan_term_months − grace_period_months) (fixed)
      interest_payment  = balance_start × monthly_rate

  monthly_repayment = principal_payment + interest_payment
  balance_end       = balance_start − principal_payment
```

### Formula — financial safety at one point in time (shared by BUY & RENT)

```text
money_remaining = income1 + income2 − living_cost − existing_debt − (monthly_repayment | monthly_rent)

safety_margin   = money_remaining / (income1 + income2)

is_safe         = safety_margin ≥ safety_margin_min_pct
```

### Rule — minimum safety threshold by household income

| Total household income/month | Minimum threshold |
| ---------------------------- | ----------------: |
| < 35 million VND             |               40% |
| 35 – 49 million VND          |               35% |
| 50 – 74 million VND          |               30% |
| ≥ 75 million VND             |               25% |

### Rule — BUY's headline safety margin at 2 points in time

```text
point a = the month within the grace period (default: month 1)
point b = grace_period_months + 1   (the first month right after the grace period)

safety_margin (headline) = MIN(safety_margin at point a, safety_margin at point b)

is_safe (headline)       = is_safe at point a AND is_safe at point b
```

This is **not** a weighted, multi-indicator scoring model — it's simply taking the worse value between two independent safety calculations, to prevent a loan that "looks safe" during the grace period from masking risk. See the real worked example in `sample-calculation-and-logic-test.md`.

### Rule — priority decision

```text
if BUY has an error (insufficient capital):
    if RENT is safe → RENT
    otherwise       → NEITHER

otherwise:
    if RENT is safe AND margin(RENT) > margin(BUY) → RENT
    otherwise if BUY is safe                        → BUY
    otherwise if RENT is safe                        → RENT
    otherwise                                        → NEITHER

    if both BUY and RENT are safe AND |margin(BUY) − margin(RENT)| < 0.05 (5 percentage points):
        append to "reason": "(Note: BUY and RENT have fairly close safety margins —
        consider other factors beyond this model.)"
```

This is a **priority-rule classification**, not scoring — the decision always lands on exactly one of 3 labels: BUY / RENT / NEITHER, based on sequential branching conditions, not a multi-criteria weighted sum.

### Formula — long-term net worth & break-even

```text
Net worth BUY(t) = property_value(t) − balance_end(t) + invested_balance_buy(t)

  property_value(t)        = purchase_price × (1 + property_annual_appreciation_pct/100)^(t/12)

  invested_balance_buy(t)  = invested_balance_buy(t−1) × (1 + investment_return_pct/100/12) + money_remaining_buy(t)

  money_remaining_buy(t)   = income1 + income2 − living_cost − existing_debt − monthly_repayment(t)


Net worth RENT(t) = savings × (1+r)^t + money_remaining_rent × ((1+r)^t − 1) / r

  r = investment_return_pct/100/12
      (if r = 0: = savings + money_remaining_rent × t)

  money_remaining_rent = income1 + income2 − living_cost − existing_debt − rent_monthly_vnd
                         (constant every month)

Break-even = the first month where (Net worth BUY − Net worth RENT) flips sign compared to the previous month
```

### Why a weighted scoring model isn't needed

The product only compares **two specific options** (one unit to buy, one unit to rent) on the same financial yardsticks (safety margin as a % of income, and net worth in VND) — there's no need to combine several unrelated criteria (e.g., location, amenities, legal risk) into a single composite score.

If the product were later extended to compare multiple apartments at once across many criteria, that's when scoring would be worth considering — but it's outside the current MVP scope.

## 4. Explainability

An explainable output should answer: what is the result, why did this result appear, which inputs influenced it, which assumptions were used, how should the user interpret the output, and what does the output NOT claim.

### 4.1 What FinFlow already does to make its output explainable

| UI mechanism                                                                                                      | Which question it answers                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The "loan assumptions" box auto-generated from `FIN_ASSUMPTIONS` (Step 3)                                         | "Which assumptions were used?" — shows the exact promotional/floating rate, grace period, and LTV currently in effect, **before** the user clicks Calculate                        |
| Two "Monthly cost" lines split by phase (grace period / post-grace period), each with its own Safe/Not-safe badge | "What is the result?" and "Which inputs influenced it?" — the user immediately sees how the repayment and safety level change once the grace period ends, not just a single number |
| The `reason` inside the decision banner                                                                           | "Why did this result appear?" — a BUY/RENT/NEITHER label is always accompanied by a plain-language explanation                                                                     |
| The income-tier safety threshold caption in the banner                                                            | "How should the user interpret the output?" — explains why a 30% (or 40%/35%/25%) threshold is used, so the user doesn't assume it's an arbitrary number                           |
| The disclaimer below the net worth chart (12%/year and 6%/year assumptions, with cited sources)                   | "Which assumptions were used?" and "What does the output NOT claim?" — clarifies this is a simplified assumption, not a guaranteed 30-year forecast                                |
| The "fairly close safety margins" note when the two options are near each other                                   | "What does the output NOT claim?" — prevents the user from reading a small difference as a decisive one                                                                            |

### 4.2 A worked example with real numbers

**Input/result verified in `sample-calculation-and-logic-test.md`, Case B — Recommendation: RENT.**

> "The BUY option has a 32.2% safety margin during the first 24-month grace period (enough to clear the 30% threshold required at a 65-million/month income level), but that drops to −17.7% the very first month after the grace period ends — because the monthly repayment jumps from 29.05 million to 61.5 million as the bank begins collecting principal and applies the 14%/year floating rate. Since this result is based on the worse of the two points checked, the BUY option is judged **not safe** overall. The RENT option has a 52.3% margin — much higher than BUY — so it is recommended. This conclusion does not account for factors outside the model, such as future income changes, actual floating-rate movements, or home repair/maintenance costs."

This is a direct illustration of the value of assessing at 2 points in time: if only one point during the grace period were checked, the system would have reported "safe" for a loan that is, in reality, unsustainable.

### 4.3 Open gap before midterm: `reason` is a fixed string, not a generated sentence

The explanation above (§4.2) was written by hand, pulling the real numbers out of the calculation results.

In the actual UI, `decide()` only returns a small set of **fixed** English sentences (e.g., `"BUY meets the safety threshold."`, `"RENT meets the safety threshold and has a higher safety margin than BUY."`) — it does not interpolate the specific percentages, thresholds, or VND amounts into the sentence shown to the user.

This means the on-screen `reason` currently cannot say something like *"BUY's safety margin is −17.7%, below the 30% threshold required for a 65M/month household"* — a user has to cross-reference the two "Monthly cost" lines and their badges to reconstruct that story themselves.

Before the midterm presentation, the team should decide whether to invest in generating a dynamic sentence (inserting the real `safety_margin`, threshold, and repayment figures into the reason string) or to keep the fixed strings and rely on the surrounding UI (badges, the assumptions box) to carry that detail instead.

### 4.4 Limitations that should be communicated to the user

* Does not include repair costs, building management fees, or home insurance.
* Does not simulate the reference interest rate changing over time (assumed fixed for the entire floating-rate period).
* Does not verify actual income or repayment capacity with a bank — all input is self-reported.
* Home price/rent data is a real but static snapshot, not real-time market listing prices at the time of use (see `../week3/source-register.md`).
* Only applies to 2-bedroom apartments in the Cau Giay (old) area within the current dataset.
* The BUY/RENT/NEITHER recommendation is based on near-term financial safety, not on which option builds more long-term wealth — the two can diverge (see `sample-calculation-and-logic-test.md`, Scenario D).

## 5. Sample Calculation & Logic Test

Kept as its own file, `sample-calculation-and-logic-test.md`, since it's a distinct kind of evidence (an Input/Expected/Actual/Status table with real cases run against the code) shared between this file's logic and the technical-readiness checkpoint.

