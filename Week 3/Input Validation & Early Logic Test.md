# Input Validation & Early Logic Test — FinFlow

## 1. Validation implemented in code

Location: the `click` event of `#calculate-btn` (Step 3), which runs **before** the calculation engine is called.

| Check type (per the guide) | Present in FinFlow? | How it's checked in code | Error message |
|---|---|---|---|
| Required input | ✅ | `income1Raw/income2Raw/savingsRaw/livingCostRaw` must not be blank | "Please fill in Income 1, Income 2, Savings, and Minimum living cost." |
| Number format | ✅ | `Number(...)` then checks `Number.isNaN(value)` | `"<field>" is not a valid number.` |
| Negative value | ✅ | `value < 0` for income1, income2, savings, living_cost, existing_debt | `"<field>" cannot be negative.` |
| Impossible range | ✅ (basic level) | `income1 + income2 > 0` (both cannot be zero); `loan_term_months > 0` if entered | "Income 1 + Income 2 must be greater than 0..." / "Loan term (months) must be a valid number greater than 0." |
| Missing value | ✅ | `existing_debt` left blank → defaults to 0 (not required); `loan_term_months` left blank → uses the default `Loan_term_months` (360) from `FIN_ASSUMPTIONS` | — |
| Invalid category | ⚠️ Indirect | `ward_old`/`size_band` are `<select>` elements, so the user cannot enter a value outside the list; the Calculate button also stays disabled until one BUY + one RENT unit are both selected (`updateCalculateButton()`) | Hint: "Select a BUY and a RENT unit in Step 2 first." |
| Unit mismatch | ✅ | The million-VND → VND conversion happens exactly once, right after validation (see `data-flow.md`) | — |
| Business-specific rule: insufficient own capital | ✅ | `loanCalc()`: if `savings < min_down_payment` (LTV portion + `buy_closing_costs_pct`) → returns an `error`, does not throw | "You need at least Xm VND more in savings to qualify for this loan (max LTV 80%)." |
| Business-specific rule: grace period ≥ loan tenure | ✅ | `loanCalc()`: if `loanTermMonths - gracePeriod ≤ 0` → returns an `error` | "grace_period_months must be less than Loan_term_months (invalid input)." |

## 2. Verification methodology

Rather than reading the code and assuming it's correct, the team extracted `loanCalc`, `evaluateBuy`, `evaluateRent`, and `decide` directly from `finflow.html` and ran them in a standalone Node.js environment with specific numeric inputs, then cross-checked the output against hand calculations using the formulas in `../week4/formulas-rules-scoring.md`. This matches guide section 11: *"enter one sample data row; calculate one output by hand; check the classification rule."*

Three cases were designed to exercise the three possible final decisions (BUY, RENT, NEITHER) and, in particular, the Week 4 two-point safety check.

## 3. Case A — BUY wins

**Input:** BUY unit priced at 3,000,000,000 VND; RENT unit priced at 30,000,000 VND/month; income1 = 40,000,000; income2 = 25,000,000; savings = 1,000,000,000; living_cost = 15,000,000; existing_debt = 0; loan_term_months = 360 (default).

**Hand calculation (checked against the code's actual output):**

- `min_down_payment` = 3.0B × (1 − 0.8) + 3.0B × 0.026 = 600,000,000 + 78,000,000 = **678,000,000 VND** → savings (1.0B) comfortably cover it, no error.
- `required_loan` = 3.0B − 1.0B = **2,000,000,000 VND**.
- Month 1 (grace period, promo rate 8.3%/year, interest-only): `monthly_repayment_grace` = 2,000,000,000 × (8.3%/12) = **13,833,333 VND**.
- Month 25 (right after the grace period, rate = 10.5% + 3.5% = 14%/year): principal = 2,000,000,000 / (360 − 24) = 5,952,381; interest = 2,000,000,000 × (14%/12) = 23,333,333 → `monthly_repayment_post_grace` = **29,285,714 VND**.
- `safety_margin_grace` = (65,000,000 − 15,000,000 − 13,833,333) / 65,000,000 = **55.64%** → safe.
- `safety_margin_post_grace` = (65,000,000 − 15,000,000 − 29,285,714) / 65,000,000 = **31.87%** → income tier 65M falls in the 50–74M band → threshold 30% → still **safe**.
- Headline `safety_margin` (BUY) = MIN(55.64%, 31.87%) = **31.87%**; `is_safe` (BUY) = **true**.
- RENT: `safety_margin` = (65,000,000 − 15,000,000 − 30,000,000) / 65,000,000 = **30.77%** → also safe, but lower than BUY's 31.87%.
- `decide()`: RENT is safe but its margin (30.77%) is **not** higher than BUY's (31.87%), and BUY is safe → **Recommendation: BUY**, reason "BUY meets the safety threshold. (Note: BUY and RENT have fairly close safety margins — consider other factors beyond this model.)"

| Input | Expected process | Expected output | Actual (running the real code) | Status |
|---|---|---|---|---|
| Case A (above) | `evaluateBuy()` (both points safe) → `evaluateRent()` → `decide()` | BUY safe at both points, margin 31.87%; RENT safe at 30.77%; Decision = BUY, with the close-margin note appended | **100% matches** | ✅ |

## 4. Case B — RENT wins because of the post-grace safety check

**Input:** BUY unit priced at 7,200,000,000 VND; RENT unit priced at 16,000,000 VND/month; income1 = 45,000,000; income2 = 20,000,000; savings = 3,000,000,000; living_cost = 15,000,000; existing_debt = 0.

**Hand calculation:**

- `min_down_payment` = 7.2B × 0.2 + 7.2B × 0.026 = 1,440,000,000 + 187,200,000 = **1,627,200,000 VND** → savings (3B) are enough, no error.
- `required_loan` = 7.2B − 3B = **4,200,000,000 VND**.
- `monthly_repayment_grace` (month 1, 8.3%) = **29,050,000 VND**; `safety_margin_grace` = (65M − 15M − 29.05M)/65M = **32.23%** → safe.
- `monthly_repayment_post_grace` (month 25, 14%) = **61,500,000 VND**; `safety_margin_post_grace` = (65M − 15M − 61.5M)/65M = **−17.69%** → not safe.
- Headline `safety_margin` (BUY) = MIN(32.23%, −17.69%) = **−17.69%**; `is_safe` (BUY) = **false**.
- RENT: `safety_margin` = (65M − 15M − 16M)/65M = **52.31%** → safe.
- `decide()`: RENT is safe and its margin is higher than BUY's → **Recommendation: RENT**, reason "RENT meets the safety threshold and has a higher safety margin than BUY."

| Input | Expected process | Expected output | Actual (running the real code) | Status |
|---|---|---|---|---|
| Case B (above) | BUY safe during the grace period but unsafe right after → headline unsafe; RENT safe | Decision = RENT | **100% matches** — this is the direct real-number illustration of why `evaluateBuy()` checks two points in time: checking the grace-period month alone would have wrongly reported BUY as "safe" (32.23% ≥ 30%). | ✅ |

## 5. Case C — NEITHER (insufficient savings, and RENT also fails the threshold)

**Input:** same BUY/RENT listings as Case B; income1 = 30,000,000; income2 = 15,000,000; savings = 1,500,000,000; living_cost = 15,000,000; existing_debt = 0.

**Hand calculation:**

- `min_down_payment` is still 1,627,200,000 VND (independent of income) → savings (1.5B) fall short by **127,200,000 VND**.
- BUY returns an `error`: "You need at least 127.2M VND more in savings to qualify for this loan (max LTV 80%)." No repayment schedule or margin is computed.
- RENT: `safety_margin` = (45M − 15M − 16M)/45M = **31.11%** → income tier 45M falls in the 35–49M band → threshold 35% → **not safe**.
- `decide()`: BUY has an error, RENT is also not safe → **Recommendation: NEITHER**, reason "BUY not viable due to insufficient savings, and RENT also does not meet the safety threshold."

| Input | Expected process | Expected output | Actual (running the real code) | Status |
|---|---|---|---|---|
| Case C (above) | `loanCalc()` returns an error before BUY reaches the safety check; RENT computed and found unsafe | Decision = NEITHER | **100% matches** | ✅ |

## 6. Conclusion

All three possible final decisions (BUY, RENT, NEITHER) were exercised with concrete numbers and matched the hand calculations exactly, including the error branch (insufficient savings) and the branch that motivated the Week 4 two-point safety check (a loan that looks safe during the grace period but becomes unsafe the moment it ends). The input validation, safety-margin, and decision logic are ready to build on. Full formula details are in `../week4/formulas-rules-scoring.md`.
