# Input Dictionary — FinFlow (BUY vs RENT, Cau Giay)

Per the guide's Week 3 §3, inputs are grouped into 4 categories: **user-entered**, **product information**, **scenario information**, and **assumptions**.

## A. User-entered input (Step 1–3 on the UI)

| Input name | Meaning | Type | Unit | Example | Valid range | Missing-value handling | Source |
|---|---|---|---|---|---|---|---|
| `ward_old` | The (pre-2025-merger) ward the user wants to search in | string (dropdown, populated from the data) | — | `"Trung Hoa"` | Must be one of the 9 unique ward values found across the embedded listings | Defaults to the first ward in the list on page load — never actually blank | user |
| `size_band` | Apartment size bracket | string (fixed dropdown) | — | `"Medium"` | One of `Small` (45–59 m²), `Medium` (60–79 m²), `Large` (80–100 m²) | Defaults to `Medium` on page load | user |
| Selected BUY listing (`selectedBuy`) | The specific BUY unit the user picks in Step 2 (a whole object, not a single number) | object | — | `{ listing_id: "BCG0156", total_price_vnd: 3780000000, ... }` | Must be one of the cards shown after filtering by `ward_old`/`size_band` | The Calculate button stays disabled until both a BUY and a RENT unit are selected — hint shown: "Select a BUY and a RENT unit in Step 2 first." | user |
| Selected RENT listing (`selectedRent`) | The specific RENT unit the user picks in Step 2 | object | — | `{ listing_id: "RCG0037", rent_monthly_vnd: 16500000, ... }` | Same as above | Same as above | user |
| `income1` | Monthly income of the first household earner | number | **million VND** (converted to VND once, right before calculation — see §D) | `25` | ≥ 0 | Required — blank triggers "Please fill in Income 1, Income 2, Savings, and Minimum living cost." | user |
| `income2` | Monthly income of the second household earner (enter `0` if single-earner) | number | million VND | `15` | ≥ 0 | Required (enter `0`, not blank, if not applicable) | user |
| `savings` | Total savings available as a down payment | number | million VND | `2000` (= 2 billion VND) | ≥ 0 | Required | user |
| `living_cost` | Minimum monthly living cost (food, transport, etc. — excludes housing) | number | million VND | `10` | ≥ 0 | Required | user |
| `existing_debt` | Other existing monthly debt payments (consumer loans, car installments, etc.) | number | million VND | `0` | ≥ 0 | Optional — defaults to `0` if left blank | user |
| `loan_term_months` | User-adjustable loan tenor (Step 3) | integer | months | `360` | > 0 (whole number) | Optional — defaults to `FIN_ASSUMPTIONS.Loan_term_months` (360) if left blank | user |

Additional cross-field rule: if `income1 + income2 ≤ 0`, the app shows "Income 1 + Income 2 must be greater than 0 to calculate the safety margin." (this guards the division in `safety_margin`).

## B. Product information (listing attributes — not typed by the user)

These come from the listing object the user selected in Step 2 (see `data.md` for the full schema and provenance):

| Input name | Meaning | Type | Unit | Example | Valid range | Source |
|---|---|---|---|---|---|---|
| `total_price_vnd` | Full sale price of the BUY unit | number | VND | `3,780,000,000` | > 0 | Embedded `BUY_LISTINGS` |
| `price_m2_vnd` | Price per m² (display only — not used in any financial formula) | number | VND/m² | `84,000,000` | > 0 | Embedded `BUY_LISTINGS` |
| `rent_monthly_vnd` | Monthly rent of the RENT unit | number | VND/month | `16,500,000` | > 0 | Embedded `RENT_LISTINGS` |
| `area_m2`, `bedrooms`, `bathrooms` | Apartment attributes shown on the card | number | m², count | `45.0`, `2.0`, `1.0` | > 0 | Embedded listings |
| `beltway_zone` | Distance band from the city's ring-road system | string | — | `"2.5-3"` | Format `"X-Y"` | Embedded listings |
| `address_street` | Street name (joined onto the listing by `project_id`) | string | — | `"Nguyen Chanh"` | — | Embedded listings |

## C. Scenario information / assumptions (`FIN_ASSUMPTIONS`)

These are not user-entered, but they directly shape the output, so they're listed here too. Full rationale and sourcing for each is in `assumptions.md`.

| Input name | Meaning | Type | Unit | Current value |
|---|---|---|---|---|
| `interest_rate_promo_pct` | Promotional interest rate for the first months | number | %/year | `8.3` |
| `promo_period_months` | Number of months the promo rate applies | integer | months | `12` |
| `interest_rate_float_ref_pct` | Reference floating rate (fixed for the demo, not simulated as time-varying) | number | %/year | `10.5` |
| `float_rate_margin_year1_pct` | Margin added in the first floating-rate year | number | % | `1.5` |
| `float_rate_margin_from_year2_pct` | Margin added from the second floating-rate year onward | number | % | `3.5` |
| `grace_period_months` | Interest-only grace period | integer | months | `24` |
| `max_loan_to_value_pct` | Maximum loan-to-value ratio | number | % | `80` |
| `buy_closing_costs_pct` | Closing costs added to the required down payment (paid in cash, not financed) | number | % | `2.6` |
| `investment_return_pct` | Assumed return on leftover monthly cash | number | %/year | `6` |
| `property_annual_appreciation_pct` | Assumed flat property appreciation rate | number | %/year | `12` |
| `Loan_term_months` | Default loan tenor (overridable by `loan_term_months`) | integer | months | `360` |

## D. Validation & unit notes

- Every money field the user types is in **million VND**; conversion to VND happens **exactly once**, in JavaScript, immediately before `evaluateBuyVsRent()` is called.
- All listing data (`total_price_vnd`, `rent_monthly_vnd`, etc.) is already stored in full VND — no further conversion needed there.
- The full validation rulebook (invalid numbers, negative values, the insufficient-savings business rule, etc.) is documented once, in `validation-and-early-logic-test.md` §1, to avoid duplicating it here.
