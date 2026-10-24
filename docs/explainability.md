# Explainability: how the screen shows its reasoning

Logic: [financial_logic.md](financial_logic.md). Values: [assumptions.md](assumptions.md).
This file covers only how inputs, outputs and reasoning are **presented** in V5.

## 1. Input presentation

| Checklist item | V5 |
|---|---|
| Label and unit | Every field has a label and a unit (million VND, years, months, %) |
| Defaults | Emergency fund 6 months, promo package 12 months, investment mix 100% savings, comparison horizon 10 years, existing debt months blank = whole loan term |
| Required vs optional | [VERIFY in UI: marking of required fields]. Income 1, Savings, Minimum living cost and Age 1 are required |
| Budget feedback before choosing | The "Your budget" card updates as the user types: maximum safe price, maximum rent, number of units in reach |
| Error messages | Specific plain-English messages (blank fields, income ≤ living costs, negative values, mix not 100%, age/loan-term rules). Two messages still show raw variable names (`savings`, `existing_debt`) |

## 2. Output presentation (Step 5)

| Item | V5 |
|---|---|
| Main result | One-line safety verdict at the top: Both pass / Only BUY passes / Only RENT passes / Neither passes |
| Per-option label | Comfortable / Tight / Not safe, one per option |
| Reason in numbers | The tightest month, money left, and the gap to the safe level (for example "Month 25 is the tightest: 15.7 million VND left, 0.1 million VND above the safe level") |
| Risk | Share of 1,000 simulated futures that use the emergency fund or run out, with a low / moderate / high label |
| Comparison | Net-worth chart (P10 / P50 / P90 band), break-even year, bad / middle / good table, monthly cash flow at two points |
| Context | "Reality check: rent vs price" card compares the rental yield with the market median, savings rate and loan rate |
| Limitations | "How we check" panel states the rule, the labels, the risk convention, "the decision is yours" and the data source and date |
| Next action | Change scenario, comparison horizon, nominal or today's-money view, or go back and change units |

## 3. What makes the reasoning visible

- **Assumptions box** in Step 1 groups every loan and projection number with a source link next to it. The safety table is read directly from the function that performs the check, so the box cannot disagree with the result.
- **Two-line explanation** above the unit list, with the full scoring rule behind "Show details".
- **Budget labels** on every unit: Within budget / Payment too tight / Not enough savings (with the shortfall).
- **Scenario buttons and sensitivity table** show which assumption moves the result most.

## 4. Things the output does not make obvious by itself

| Point | Why it matters | Handling |
|---|---|---|
| Safety and wealth can point in opposite directions | A user can see "Only RENT passes" while the chart shows BUY ahead in 92–99% of futures after 10 years | Mentioned in the "How we check" text; worth saying aloud in a demo |
| Longer horizons favour BUY | Compounding of the home price assumption | A note appears when the horizon is longer than 10 years |
| Safe-level cliffs at income 35 / 50 / 75 million | Income 34 vs 35 can flip RENT from Not safe to pass | Smooth-threshold sensitivity row |
| Emergency-fund use is not the same as the safety check | A Not safe option can show 0% fund use | Risk line shows both separately |
| Risk label thresholds | Team convention, not a standard | Stated in "How we check" |

## 5. Not yet tested

Whether a first-time user, without the documentation, can read Step 5 and explain why the result came out as it did. Planned: a quick test with 2–3 people before submission. [RESULT TO BE ADDED]
