# Sample Calculation & Logic Test — FinFlow

The cases below are **identical** to the ones used in `../week3/validation-and-early-logic-test.md` — restated here in the Week 4 "sample calculation" format (input → expected calculation → expected output → actual output → status), focused specifically on verifying the **financial logic**, without repeating the input-validation section.

**Methodology:** the `loanCalc`, `evaluateBuy`, `evaluateRent`, `decide`, and `findBreakEven` functions were taken verbatim from `finflow.html` and run in Node.js with specific inputs, cross-checked against hand calculations using the formulas in `03-formulas-rules-scoring.md`.

## Case A — BUY wins

**Input:** BUY unit priced at 3,000,000,000 VND; RENT unit priced at 30,000,000 VND/month; income1 = 40,000,000; income2 = 25,000,000; savings = 1,000,000,000; living_cost = 15,000,000; existing_debt = 0; loan_term_months = 360 (default).

| Step | Expected calculation | Expected output | Actual output (running the real code) | Status |
|---|---|---|---|---|
| `min_down_payment` | 3.0B × 20% + 3.0B × 2.6% | 678,000,000 VND | 677,999,999.99 VND (floating-point rounding, negligible) | ✅ Match |
| `required_loan` | 3.0B − 1.0B | 2,000,000,000 VND | 2,000,000,000 VND | ✅ Match |
| `monthly_repayment_grace` (month 1, 8.3%/year, interest-only) | 2B × 8.3%/12 | 13,833,333 VND | 13,833,333.33 VND | ✅ Match |
| `monthly_repayment_post_grace` (month 25, 14%/year) | principal 2B/336 + interest 2B×14%/12 | 5,952,381 + 23,333,333 = 29,285,714 VND | 29,285,714.29 VND | ✅ Match |
| `safety_margin_grace` / `safety_margin_post_grace` | (65M−15M−repayment)/65M | 55.64% / 31.87% | 55.64% / 31.87% | ✅ Match |
| `safety_margin` (headline, BUY) | MIN(55.64%, 31.87%) | 31.87% | 31.87% | ✅ Match, `is_safe`=true |
| RENT `safety_margin` | (65M−15M−30M)/65M | 30.77% | 30.77% | ✅ Match, `is_safe`=true (lower than BUY) |
| `decide()` | RENT safe but margin ≤ BUY's; BUY safe | BUY, "BUY meets the safety threshold. (Note: BUY and RENT have fairly close safety margins — consider other factors beyond this model.)" | Matches exactly | ✅ Match |

## Case B — RENT wins because of the post-grace safety check

**Input:** BUY unit priced at 7,200,000,000 VND; RENT unit priced at 16,000,000 VND/month; income1 = 45,000,000; income2 = 20,000,000; savings = 3,000,000,000; living_cost = 15,000,000; existing_debt = 0.

| Step | Expected calculation | Expected output | Actual output | Status |
|---|---|---|---|---|
| `min_down_payment` | 7.2B × 20% + 7.2B × 2.6% | 1,627,200,000 VND | 1,627,199,999.99 VND | ✅ Match |
| `monthly_repayment_grace` (month 1, 8.3%) | 4.2B × 8.3%/12 | 29,050,000 VND | 29,050,000.00 VND | ✅ Match |
| `monthly_repayment_post_grace` (month 25, 14%) | principal + interest on 4.2B | 61,500,000 VND | 61,500,000.00 VND | ✅ Match |
| `safety_margin_grace` / `safety_margin_post_grace` | (65M−15M−repayment)/65M | 32.23% / −17.69% | 32.23% / −17.69% | ✅ Match |
| `safety_margin` (headline, BUY) | MIN(32.23%, −17.69%) | −17.69% | −17.69% | ✅ Match, `is_safe`=false |
| RENT `safety_margin` | (65M−15M−16M)/65M | 52.31% | 52.31% | ✅ Match, `is_safe`=true |
| `decide()` | RENT safe, BUY unsafe | RENT, "RENT meets the safety threshold and has a higher safety margin than BUY." | Matches exactly | ✅ Match |

This is the direct real-number illustration of why `evaluateBuy()` checks two points in time: checking the grace-period month alone would have wrongly reported BUY as "safe" (32.23% ≥ 30%).

## Case C — NEITHER (insufficient savings, RENT also fails the threshold)

**Input:** same BUY/RENT listings as Case B; income1 = 30,000,000; income2 = 15,000,000; savings = 1,500,000,000; living_cost = 15,000,000; existing_debt = 0.

| Step | Expected calculation | Expected output | Actual output | Status |
|---|---|---|---|---|
| Savings vs. `min_down_payment` | 1.5B < 1.6272B, short by 127.2M | Error: "You need at least 127.2M VND more in savings to qualify for this loan (max LTV 80%)." | Matches exactly | ✅ Match |
| RENT `safety_margin` | (45M−15M−16M)/45M | 31.11% | 31.11% | ✅ Match, `is_safe`=false (45M income → 35% threshold) |
| `decide()` | BUY error, RENT unsafe | NEITHER, "BUY not viable due to insufficient savings, and RENT also does not meet the safety threshold." | Matches exactly | ✅ Match |

## Scenario D — net worth over 30 years, and where the safety decision and the wealth outcome diverge

**Input:** BUY unit priced at 3,780,000,000 VND (45 m²); RENT unit priced at 18,000,000 VND/month; income1 = 50,000,000; income2 = 30,000,000; savings = 2,000,000,000; living_cost = 10,000,000; existing_debt = 0; loan_term = 360 months.

**Actual output (running the real code):**

- `min_down_payment` = 854,280,000 VND → savings (2.0B) more than sufficient, no error.
- `required_loan` = 1,780,000,000 VND.
- `monthly_repayment_grace` (month 1) = 12,311,667 VND; `safety_margin_grace` = 72.11%.
- `monthly_repayment_post_grace` (month 25) = 26,064,286 VND; `safety_margin_post_grace` = 54.92%.
- Headline `safety_margin` (BUY) = MIN(72.11%, 54.92%) = **54.92%** — still comfortably above the 25% threshold for this income tier (≥75M total) → `is_safe` = true.
- RENT `safety_margin` = 65.00% → also safe, and **higher** than BUY's 54.92%.
- `decide()` → **RENT**, "RENT meets the safety threshold and has a higher safety margin than BUY."

**Net worth over time (from the same calculation):**

| Year | Net worth BUY (VND) | Net worth RENT (VND) | Difference (BUY−RENT) |
|---|---|---|---|
| 1 | 3,165,218,034 | 2,764,804,867 | +400,413,167 |
| 5 | 8,516,528,843 | 6,325,741,892 | +2,190,786,951 |
| 10 | 18,455,740,314 | 12,160,519,502 | +6,295,220,812 |
| 30 | 165,473,527,754 | 64,279,932,632 | +101,193,595,122 |

`findBreakEven()` returns `(null, null)` — BUY's net worth leads from year 1 and the gap only widens, so the two lines never cross.

**Why this matters:** in this scenario, FinFlow recommends **RENT** on safety grounds (RENT leaves more breathing room against monthly income), while the net-worth chart simultaneously shows **BUY** building dramatically more long-term wealth (largely driven by the 12%/year flat property-appreciation assumption compounding over 30 years). These are two different questions — "which is safer to commit to today" vs. "which builds more wealth if the assumptions hold for 30 years" — and the product answers both, but a user skimming only the top banner could misread the wealth chart as contradicting the recommendation. This is worth calling out explicitly when presenting the product, and is a candidate addition to `04-explainability.md`'s list of things the output does not automatically make obvious.

## `findBreakEven()` — branch coverage (synthetic test data)

These four scenarios use hand-constructed net-worth series (not real listings) to directly test the crossover-detection function itself, verified by calling `findBreakEven()` in Node.js:

| Scenario | Expected | Actual | Status |
|---|---|---|---|
| BUY starts below RENT, crosses above | `month=24, year=2` | `month=24, year=2` | ✅ Match |
| BUY starts above RENT, crosses below | `month=27, year=2` | `month=27, year=2` | ✅ Match |
| The two series never cross | `(null, null)` | `(null, null)` | ✅ Match |
| BUY has no series (loan error, nothing to compare) | `(null, null)` | `(null, null)` | ✅ Match |

Note: an earlier version of this test used "Case B on the real dataset (savings 1.5B)" as a real-world example of the fourth branch. Under the current code, that specific input errors out on insufficient savings for a different, but consistent, reason — the branch behavior itself (`null, null` when BUY has no series) is unchanged and independently confirmed above.

## Conclusion

Four real cases (A, B, C, D) plus a 4-branch synthetic test of `findBreakEven()` were run against the current code and matched hand calculations exactly — covering all three final decisions (BUY/RENT/NEITHER), the two-point safety check, the long-term net-worth projection, and break-even detection. The financial logic is ready to be presented at the midterm checkpoint. Scenario D's safety-vs-wealth divergence (above) is flagged as a presentation talking point, not a bug.
