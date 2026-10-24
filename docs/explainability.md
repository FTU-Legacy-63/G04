# Explainability: how the screen shows its reasoning

Logic: [financial_logic.md](financial_logic.md). Values: [assumptions.md](assumptions.md). Tests: [testing.md](testing.md).
This file covers only how inputs, outputs and reasoning are **presented** in V5.

## 1. Input presentation

| Checklist item | V5 |
|---|---|
| Label and unit | Every field has a label and a unit (million VND, million VND / month, years, months, %) |
| Defaults | Emergency fund 6 months, promo package 12 months, investment mix 100% savings, comparison horizon 10 years, existing debt 0, months left on the debt blank = whole loan term |
| Required vs optional | Marked on the label only for some fields: Age 1 says "(years, required)"; Age 2 and "Months left on this debt" say "(optional)"; Income 2 carries the hint "Leave blank if you're applying alone". Income 1, Savings and Minimum living cost have no marker on the label, but the hint at the top of Step 1 and the error message name them as the four needed fields (Income 1, Savings, Minimum living cost, Age 1) |
| Budget feedback before choosing | The "Your budget" card updates as the user types: maximum safe price, maximum rent, number of units in reach. Until the four needed fields are filled it says which ones are missing |
| Live check of the investment mix | Below the four boxes the tool shows "Total: x%" and adds "must be 100%" in red when the total is wrong |
| Error messages | Specific plain-English messages (blank fields, income ≤ living costs, negative values, mix not 100%, age and loan-term rules). One group of messages still shows raw variable names: "not a valid number" and "cannot be negative" print the internal field name (`savings` and `existing_debt` were seen in tests LI.09 and LI.10; the same code also covers `income1`, `income2` and `living_cost`). Wording only, no effect on results |

## 2. Output presentation (Step 5)

| Item | V5 |
|---|---|
| Main result | One-line safety verdict at the top: Both pass / Only BUY passes / Only RENT passes / Neither passes |
| Per-option label | Comfortable / Tight / Not safe, one per option |
| Reason in numbers | The tightest month, money left, and the gap to the safe level (for example "Month 25 is the tightest: 15.7 million VND left, 0.1 million VND above the safe level (15.6 million VND)", test G1.02) |
| Risk | Share of 1,000 simulated futures that use the emergency fund or run out, with a low / moderate / high label |
| Comparison | Net-worth chart (P10 / P50 / P90 band; P10 = bad case, P50 = middle, P90 = good case), break-even year, bad / middle / good table, monthly cash flow at two points |
| Context | "Reality check: rent vs price" card compares the rental yield with the market median, savings rate and loan rate, and adds "That's low" when the yield is below both |
| Limitations | "How we check" panel states the rule, the labels, the risk convention, "the decision is yours" and the data source and date (batdongsan.com.vn, 9 Sep 2026) |
| Next action | Change scenario, comparison horizon, nominal or today's-money view, or go back and change units |

## 3. What makes the reasoning visible

- **Assumptions box** in Step 1 groups every loan and projection number with a source link next to it. The safety table is read directly from the function that performs the check, so the box cannot disagree with the result.
- **Two-line explanation** above the unit list, with the full scoring rule behind "Show details".
- **Budget labels** on every unit: Within budget / Payment too tight / Not enough savings (with the shortfall) / No loan available.
- **Scenario buttons and sensitivity table** show which assumption moves the result most.
- **Spare-money table** in Step 4 (starting money, spare money in month 1 and in the tightest month) uses the same engine as Step 5, so its numbers match "Money left over".

## 4. Things the output does not make obvious by itself

| Point | Why it matters | Handling |
|---|---|---|
| Safety and wealth can point in opposite directions | A user can see "Only RENT passes" while the chart shows BUY ahead of RENT in 92–99% of futures after 10 years (test group G2). Only in Downturn does BUY fall back, to 42–66% (G11) | Mentioned in the "How we check" text; worth saying aloud in a demo |
| Longer horizons favour BUY | Compounding of the home price assumption | A note appears when the horizon is longer than 10 years: the further out, the more the result leans toward buying, and 10 years is the horizon the price assumptions are calibrated on |
| Safe-level cliffs at income 35 / 50 / 75 million | Income 34 vs 35 can flip RENT from Not safe to pass because the safe level drops from 40% to 35% (test G6) | Smooth-threshold sensitivity row |
| Emergency-fund use is not the same as the safety check | A Not safe option can show 0% fund use (G1.06, G1.08); in the random profiles tested, the option that passes uses the fund in only about 0–1% of futures | Risk line shows both separately |
| More emergency-fund months: "uses the fund" goes up, "runs out" goes down | Example G5: BUY at 4.9 billion, fund 0 to 12 months: uses fund 52% to 68%, runs out 52% to 44%. It is a counting difference (touching the fund vs emptying it), not an error | Both numbers are shown |
| Risk label thresholds | Team convention, not a standard | Stated in "How we check" |
| Rounding | The conclusion sentences show whole percentages (for example "In 16% of 1,000 futures…") | Test sheet allows a 1-point tolerance |

## 5. Not yet tested

Whether a first-time user, without the documentation, can read Step 5 and explain why the result came out as it did. Planned: a quick test with 2–3 people before submission. [RESULT TO BE ADDED]
