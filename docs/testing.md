# Testing

**Product tested:** FINAL-PRODUCT-V5 (single HTML file, runs in the browser)
**Test workbook:** [`tests/FinFlow_Test_Cases_V5.xlsx`](../tests/FinFlow_Test_Cases_V5.xlsx)
**Run conditions:** Stable scenario, Monte Carlo 1,000 runs, fixed random seed (20260909), data snapshot of 9 Sep 2026
**Related documents:** [financial_logic.md](financial_logic.md) · [data_and_sources.md](data_and_sources.md) · [limitations.md](limitations.md) · [revision_summary.md](revision_summary.md)

---

## 1. What we test and why

FinFlow answers one question: *with the money I have, should I buy or rent a 2-bedroom apartment in Tay Ho, Cau Giay or Ha Dong?* A wrong answer here is not a visual glitch; it can push a user toward a loan they cannot carry. So testing focuses on four things:

1. **The safety check is correct.** The label (Comfortable / Tight / Not safe) and the banner (Both pass / Only BUY / Only RENT / Neither) must follow the rules in `financial_logic.md`.
2. **The loan rules are applied correctly.** Loan term by age, grace period, promotional-rate package, savings needed for the down payment.
3. **Bad input is caught.** The tool must refuse impossible input with a clear message and must not show a result.
4. **The Step 2–3 listing filters behave.** Project lists and unit cards must follow the filters the user chose.

## 2. Two layers of testing

| Layer | Who / when | What it covers | Evidence |
|---|---|---|---|
| **A. Developer checks during the build** | Group, 27 Sep – 9 Oct 2026, after each version (V1 → V5) | Regression: a new version must give the same results as the old one when new features are switched off. Consistency: labels on the cards must equal the live safety check. | [revision_summary.md](revision_summary.md) (sections on V2–V5) |
| **B. Structured test workbook** | Built from V5, 9 Oct 2026 | 123 written cases with inputs, expected output, and a place to record the actual output and Pass / Fail | `tests/FinFlow_Test_Cases_V5.xlsx` |

### Layer A: checks already done by the developers

| Version | Check | Result recorded |
|---|---|---|
| V2 vs V1 | Same profile and same pair of units | Same conclusion, same safety margin, same break-even year |
| V2 | Budget label vs direct safety check on all 756 BUY and 277 RENT listings | Labels match 100% |
| V2 | Relevance score across 337 project × size-band combinations | Score is always non-increasing with rank |
| V3 | All new costs (service fee, fire insurance, selling cost, repairs) set to 0 | Output equals V2 (same conclusion, margin, final wealth, % BUY wins) |
| V3 | Budget label vs direct check on 756 + 277 listings | Labels match 100% |
| V3 | Sensitivity table | All 17 rows run; page shows no error |
| V3 | Excel assumptions file recalculated | Only the intentional error in cell C65 of the VN-Index sheet remains |
| V4 | "In today's money" switch | Conclusion unchanged; % BUY wins = 91% in both modes; choice persists when scenario or N changes |
| V4 | Sensitivity rows | Base 86%, repairs-1% row 83%, as expected |
| V4 | Excel assumptions file v6 recalculated (504 formulas) | Only the intentional error in cell C65 of the VN-Index sheet remains |
| V5 | Presentation-only release | Formulas unchanged (compared at build); test workbook built from this version |
| All | Monte Carlo with standard deviation set to 0 | Every run equals the average path |
| All | Correlation set to 0 | Result equals V2 |

## 3. Layer B: the test workbook

The workbook has six sheets.

| Sheet | Purpose | Cases |
|---|---|---|
| `Đọc trước` (Read first) | How to use the workbook, default settings, test profiles, progress table | n/a |
| `Case test` | Calculation cases: inputs → expected output → actual output | **88** |
| `Căn nhà` (Units) | The 33 listings used by the cases, with the exact clicks to select each one in the interface | n/a |
| `Lỗi nhập liệu` (Input errors) | Invalid or edge-case input and the expected message | **28** |
| `Lọc Bước 2-3` (Step 2–3 filters) | Filter and project-list behaviour | **7** |
| `Lưu ý` (Notes) | How to read results; known by-design behaviours; what is not covered | n/a |

**Default settings** when a case does not say otherwise: 12-month promotional package, 100% savings mix, 6-month emergency fund, Stable scenario, compare at 10 years, nominal money.

**Test profiles.** Profile A: income 25 + 15 million VND/month, savings 2,000 million, minimum living cost 8 million, no debt, ages 32 and 30. Profile R2: income 20 million, savings 800 million, living cost 8 million, age 30, no second borrower.

### 3.1 Calculation cases (88)

| Group | What it checks | Cases |
|---|---|---|
| G1 Conclusion | Every banner type (Both pass, Only BUY, Only RENT, Neither) and every label combination | 10 |
| G2 Emergency fund, BUY side | Rising BUY price (3.30 → 5.90 billion VND) against a fixed RENT unit: the share of simulated futures that need the emergency fund must rise | 10 |
| G3 Emergency fund, RENT side | Rising rent (6 → 32 million/month) against a fixed BUY unit | 11 |
| G4 Pass but still uses fund | A side that passes the safety check but still dips into the fund in a small share of futures (Stable and Downturn) | 2 |
| G5 Months of emergency fund | 0 / 3 / 6 / 12 months, on both the BUY and the RENT side | 8 |
| G6 Income thresholds | Income 34 / 35 / 49 / 50 / 74 / 75 million, around the points where the required safety level changes | 6 |
| G7 Age and loan term | Ages 28 to 67, and two borrowers of different ages (older age sets the term) | 7 |
| G8 Existing debt | No debt; 5 million with unknown months, 36 months, 12 months; 10 million | 5 |
| G9 Promotional package | 6 / 12 / 18 / 24 months (tightest month moves from 25 to 37) | 4 |
| G10 Investment mix | 100% savings; savings + bonds; four-way split; 100% stocks; 100% gold | 5 |
| G11 Scenario | Boom / Stable / Downturn on the same four BUY units | 12 |
| G12 Savings larger than price | Savings 10,000 million against a 2.05 billion unit (savings only, and 100% stocks) | 2 |
| G13 Compare-at year and money display | 10 years, 20 years, end of loan × nominal / today's money | 6 |

**Worked example (case G1.02).** Profile A, BUY unit BHD0175 (PCC1 Complex, 67 m², 3.2 billion VND), RENT unit RCG0117 (Discovery Complex, 100 m², 15 million/month). Expected: banner **Both pass**; BUY **Tight** (month 25 is the tightest: 15.7 million VND left, only 0.1 million above the safe level); RENT **Comfortable**; both use the emergency fund in 0% of futures.

### 3.2 Input-error cases (28)

| Type | Examples | Expected behaviour |
|---|---|---|
| Missing required field (LI.01–04, 21) | Income 1, savings, living cost or age 1 left blank | "Please fill in Income 1, Savings, Minimum living cost, and Age 1." |
| Impossible value (LI.05–12) | Total income 0; living cost 0, equal to or above income; negative savings or debt; age 0 | A specific message naming the field; no result shown |
| Debt months and fund months (LI.13–15) | 2.5 or −1 months left on a debt; negative emergency fund | Message asking for a whole number of months (0 or more) |
| Investment mix (LI.16–18) | Mix totals 90 or 110, or has a negative box | "must be 0 or more in each box and add up to 100%" |
| Age rules (LI.19, 20, 25–28) | Older borrower aged 68, 69, 70; two borrowers 30 and 70 | Age 70 or more: "Not eligible for a loan due to age". Term of 24 months or less: message that the term must exceed the 24-month grace period |
| Valid edge cases (LI.22–24) | Income 1 = 0 with income 2 = 40; blank emergency fund; blank debt | No error; the tool runs normally (blank is treated as 0) |

### 3.3 Step 2–3 filter cases (7)

| ID | Action | Expected (V5) |
|---|---|---|
| S.01 | Profile A, no filter | BUY: 170 projects, 29 cards; RENT: 81 projects, 10 cards |
| S.02 | BUY district = Cau Giay | BUY project list drops to 69 |
| S.03 | Cau Giay, Vinhomes D'Capitale, Medium | "33 target units"; 59 cards, first one marked TARGET |
| S.04 | RENT: tick "Same filters as Buy" | RENT district jumps to Cau Giay; 34 RENT projects |
| S.05 | Building name = "Chelsea" | 2 projects (Chelsea Park, Chelsea Residences); 15 cards |
| S.06 | Building name = "zzzz" | "No project matches these filters"; 0 cards |
| S.07 | Sorting and "Only within budget" | No expected numbers yet; tester records observed behaviour |

## 4. Results

> **Status: to be completed by the team.** The workbook records the expected output of V5 for every case. The "actual result" columns (banner, labels, % using the fund, Pass / Fail) are filled in as each case is run in the browser. In the workbook version reviewed for this document, no case had been run yet.

| Group | Cases | Pass | Fail | Not yet run |
|---|---|---|---|---|
| Calculation (G1–G13) | 88 | | | 88 |
| Input errors | 28 | | | 28 |
| Step 2–3 filters | 7 | | | 7 |
| **Total** | **123** | | | **123** |

**Pass rule.** Labels and banner must match exactly. Percentages may differ by at most 1 percentage point, because the interface shows whole percentages.

**Important about "expected".** The expected values are what V5 itself returned, so they are a **baseline for regression** (they catch future changes), not an independent answer key. A few values were also checked by hand: the safety level by income band, the loan term by age, and the shortfall in case G1.07. V4 and V5 gave identical results across 48 comparison runs.

## 5. Findings

### 5.1 Behaviours that look odd but are by design

| Observation | Why it is not a bug |
|---|---|
| A side marked *Not safe* can still show 0% fund use (G1.06, G1.08) | "Safe every month" and "needs the emergency fund in a random future" are two separate signals |
| A side that passes the safety check almost never needs the fund: in 5,678 extra random combinations tried by the team, only about 0–1% of futures did (G4). The Moderate and High risk chips appeared only on the Not safe side | Passing the check on average assumptions leaves a buffer; the risk chip is information, not a second verdict |
| More emergency-fund months → "uses fund" goes **up**, "runs out" goes **down** (G5: BUY 4.9 billion, 52% → 68% and 52% → 44%) | The two figures count different things: touching the fund versus emptying it |
| BUY ends richer than RENT in 92–99% of futures at 10 years even when only RENT passes (G2). It drops to 42–66% only in Downturn (G11) | Net worth and monthly safety measure different risks; the result page shows both rather than merging them |
| Income 34 → 35 million flips RENT from Not safe to pass (G6) | The required safety level changes in steps (40% → 35%). This is a known design limit; the sensitivity table has a "smooth" option |
| The conclusion sentence shows whole percentages | Display rounding; the check allows 1 point |

### 5.2 Issues found

| # | Issue | Severity | Status |
|---|---|---|---|
| 1 | Error messages for negative savings (LI.09) and negative debt (LI.10) show raw variable names (`savings`, `existing_debt`) instead of the field labels | Cosmetic (wording only) | Open |

No critical bug is recorded in the workbook at the time of writing. Bugs found while running the cases in Section 4 should be added to this table.

## 6. What is not covered

- Mobile layout for each case (the page was only checked for errors on desktop and phone-size view during the V2 build)
- Sorting options and the "Only within budget" button in Step 3 (case S.07)
- The detailed BUY / RENT cards (monthly payment bar chart)
- Real-money accuracy: the tool is a simulation on assumptions, so tests check that rules are applied correctly, not that the future will match. See [limitations.md](limitations.md).

## 7. How to reproduce a test

1. Open the final HTML file in a browser (no internet needed; the data is embedded).
2. Open `tests/FinFlow_Test_Cases_V5.xlsx`, sheet `Case test`, and pick a row.
3. Enter the blue input columns in Step 1 (income, savings, living cost, debt, emergency fund, ages, promotional package).
4. Select the BUY and RENT units. The sheet `Căn nhà` gives the exact clicks for each unit ID.
5. In Step 4, set the investment mix if the case says so, then press **Calculate**.
6. Read the conclusion block at the top of Step 5 and compare it with the expected columns.
7. Record the actual result in the yellow columns and mark Pass or Fail.

Because the random seed is fixed, the same input always gives the same numbers. If a number differs from the workbook, the code or the data has changed.
