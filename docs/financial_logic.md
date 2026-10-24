# Financial Logic

**Product:** FinFlow (FINAL-PRODUCT-V5), a buy-versus-rent simulator for a 2-bedroom apartment in Hanoi
**Companion documents:** [data_and_sources.md](data_and_sources.md) (where every number comes from) · [testing.md](testing.md) · [limitations.md](limitations.md) · [user_flow.md](user_flow.md)

Rates are stored as fractions in the model (0.083 = 8.3%). Money is in VND; "million" and "billion" mean million and billion VND. Every number in this document is the value used in the final HTML file; where a number is a judgement call rather than a measured fact, the text says so and points to [limitations.md](limitations.md).

**Contents**

- [Part A. The problem and the two tests](#part-a-the-problem-and-the-two-tests)
- [Part B. The loan](#part-b-the-loan)
- [Part C. How home prices grow](#part-c-how-home-prices-grow)
- [Part D. Monthly cash flow, costs and the safety check](#part-d-monthly-cash-flow-costs-and-the-safety-check)
- [Part E. Investing the spare money and net worth](#part-e-investing-the-spare-money-and-net-worth)
- [Part F. Scenarios, sensitivity and Monte Carlo](#part-f-scenarios-sensitivity-and-monte-carlo)
- [Part G. All assumptions at a glance](#part-g-all-assumptions-at-a-glance)

---

## Part A. The problem and the two tests

### A1. The problem and the user

**Problem.** A young household in Hanoi with some savings wants a 2-bedroom apartment in Tay Ho, Cau Giay or Ha Dong. Buying needs a large down payment and a 20–30 year loan. Renting keeps the savings free. Most people compare only the monthly payment, which hides two questions: *can I carry this every month?* and *who is richer after many years?*

**User task.** Decide between buying one specific apartment and renting another, using their own income, savings, age and debts.

**Input → process → output.**

- *Input:* income, age, savings, living cost, existing debt, one BUY unit and one RENT unit from real listings (batdongsan.com.vn, snapshot of 9 Sep 2026).
- *Process:* simulate both paths month by month for the whole loan term, then repeat 1,000 times with random market changes (Monte Carlo).
- *Output:* a safety verdict for each side, a net worth comparison over time, and a risk summary. The tool does not tell the user what to choose; "the decision is yours".

### A2. The two tests

Both paths start from the **same savings**.

| | BUY | RENT |
|---|---|---|
| Savings are used for | Down payment, purchase fees (2.6% of price), emergency fund | Emergency fund, and the rest invested in four channels (savings, bonds, gold, stocks) |
| Monthly cost | Loan payment + service fee + fire insurance | Rent + service fee |
| Wealth after N years | House value − selling cost (1.5%) − remaining loan − early-repayment fee + investments | Investments |

**Test 1: Safety check (can I carry it?).** Every month of the loan term, the money left after all costs must stay above a minimum share of income. The share is 40%, 35%, 30% or 25% depending on income. Each side is labelled **Comfortable** (passes with at least 5 percentage points of income to spare), **Tight** (passes with less) or **Not safe** (at least one month below the line). Details in Part D.

**Test 2: Net worth (who is richer?).** *Net worth* means everything you own minus what you owe. Both paths are compared at 10 years by default (the user can choose 20 years or the end of the loan). Details in Part E.

The two tests can disagree: BUY may end richer while failing the safety check. The tool shows both rather than merging them into one verdict, and Monte Carlo is shown as risk information, not as the decision rule.

### A3. Worked example (illustrative numbers)

Buy a 4.0 billion apartment with 2,000 million savings and 8 million/month living cost. Emergency fund = 6 months × 8 = 48 million.

| Step | Calculation | Result |
|---|---|---|
| Purchase fees | 4,000 × 2.6% | 104 million |
| Down payment | 2,000 − 104 − 48 | 1,848 million |
| Loan | 4,000 − 1,848 | 2,152 million |
| Minimum savings to be allowed to borrow | 20% × 4,000 + 104 + 48 | 952 million |

Income 40 million → the 35% band → in month 1 the user must keep at least 40 × 35% = **14 million** after all costs.

---

## Part B. The loan

The loan follows one real product: **MBBank, Van Phuc branch** (rate sheet received from the branch; see [data_and_sources.md](data_and_sources.md)). The model uses the sheet's terms, except the age limit (B3), which comes from other banks.

### B1. Loan terms used

| Item | Value in the model | Note |
|---|---|---|
| Promotional rate (user picks the package) | 6 months 7.7% · 12 months 8.3% · 18 months 8.5% · 24 months 9.0% | Default: 12 months |
| Floating rate after the promotion | Reference rate + margin | See B2 |
| Reference rate | 10.5% | Extrapolated, not stated by MB (see limitation #5) |
| Margin | +1.5% for the first 12 months after the promotion, +3.5% afterwards | From the MB sheet |
| Grace period (interest only) | 24 months | From the MB sheet |
| Repayment method | Equal principal, interest on the declining balance | After the grace period |
| Prepayment fee | 1% of the amount repaid in years 1–5, free from year 6 | Matters only when the comparison year N is 5 or less |
| Maximum loan-to-value (LTV) | 80% (Stable and Boom), 70% (Downturn) | LTV = loan ÷ price |
| Maximum term | 360 months | MB's other 35-year "young people" product is not used |

### B2. How the interest rate moves

Take the 12-month package. The rate is a step function:

| Months | Rate | How it is built |
|---|---|---|
| 1–12 | 8.3% | Promotional rate |
| 13–24 | 12.0% | Reference 10.5% + 1.5% margin |
| 25 onward | 14.0% | Reference 10.5% + 3.5% margin |

Each month, interest = opening balance × annual rate ÷ 12.

**Why the reference rate is 10.5%.** The MB sheet gives the margin but not the reference rate. Press reports (Thanh Nien 25 Aug 2026, Dan Tri 24 Aug 2026) put market floating rates at 13–15%. Subtracting MB's 3.5% margin gives 9.5–11.5%, and the team used the midpoint. In Monte Carlo the reference rate varies by ±0.75 percentage points (one standard deviation).

### B3. The loan term depends on age

The bank will not lend past age 70 at the **payoff date**. The tool takes the **older** of the two borrowers, as a cautious assumption (no bank states how it treats co-borrowers).

> Maximum term = min( (70 − age of the older borrower) × 12 , 360 ) months

| Age of the older borrower | Maximum term | Limited by |
|---|---|---|
| 30 | 360 months | The bank |
| 40 | 360 months | The bank (70 − 40 = 30 years) |
| 45 | 300 months | Age |
| 50 | 240 months | Age |
| 60 | 120 months | Age |
| 68 | 24 months | Blocked: equals the grace period, so no principal months remain |
| 70 or more | none | Not eligible |

An older borrower gets a shorter term, so the monthly principal is higher and the safety margin is lower. Ages 65 and 75 are tested as sensitivities.

### B4. Can the user borrow at all?

Three conditions must hold, otherwise the BUY side shows "Not enough savings" or "No loan available" and no BUY result is calculated:

1. **Savings are enough for the down payment.** Savings ≥ (1 − LTV) × price + 2.6% × price + emergency fund. At 80% LTV this is price × 22.6% + emergency fund.
2. **Age.** The older borrower is under 70, and the maximum term is more than 24 months.
3. **LTV.** Loan ÷ price does not exceed 80% (70% in Downturn).

**Purchase fees (2.6% of price)** = maintenance fund 2% + registration fee 0.5% + notary about 0.06%. They are paid on day one, so BUY net worth starts below the savings figure by exactly the fees.

If savings exceed the price, the loan is zero and the excess is invested from day one.

### B5. Worked example: why month 25 is the hardest month

Continue the example from A3: loan 2,152 million, borrowers aged 32 and 30, 12-month package.

- Term: older age 32 → (70 − 32) × 12 = 456 months, capped at 360.
- Principal after the grace period: 2,152 ÷ (360 − 24) = **6.4 million per month**.

| Month | Rate | Interest | Principal | Loan payment |
|---|---|---|---|---|
| 1 | 8.3% | 2,152 × 8.3% ÷ 12 = 14.9 million | 0 (grace) | **14.9 million** |
| 13 | 12.0% | 2,152 × 12% ÷ 12 = 21.5 million | 0 (grace) | **21.5 million** |
| 25 | 14.0% | 2,152 × 14% ÷ 12 = 25.1 million | 6.4 million | **31.5 million** |

In month 25 two things happen at once: the grace period ends (principal starts) and the margin rises from 1.5% to 3.5%. The payment more than doubles compared with month 1. This is why the "tightest month" in the test cases is usually month 25 (see [testing.md](testing.md)). With an 18-month package the jump moves to month 31, and with 24 months to month 37.

**Early repayment.** If the user compares at year 5 or earlier, the model deducts a 1% fee on the remaining balance from BUY net worth. From year 6 there is no fee.

---

## Part C. How home prices grow

Home price growth is the assumption that moves BUY net worth the most, so the model does not use one flat number.

### C1. The curve (called PA2)

Growth in year k (k = 1 is the first year) starts high and cools toward a long-run level:

> g(k) = 8.38% + (20.43% − 8.38%) × e^( −(k − 1) / 3.24 )

Think of a car that is going fast now and slows down gradually toward cruising speed.

| Parameter | Value | Why |
|---|---|---|
| Start g₀ | 20.43% | Compound annual growth of Hanoi primary-market prices 2020–2025 (CafeF, Cushman & Wakefield data in the group's file) |
| Long-run g∞ | 8.38% | CPI average 3.09% + real GDP per capita growth average 5.29%, 2016–2025 (World Bank). Reasoning: in the long run house prices cannot outgrow incomes forever |
| Cooling speed τ | 3.24 years | Chosen so the average growth over the next 10 years equals the last 10 years: 12.66% (CAGR 2016–2025) |

| Year | 1 | 2 | 3 | 4 | 5 | 10 | 15 | 30 |
|---|---|---|---|---|---|---|---|---|
| Growth in that year | 20.4% | 17.2% | 14.9% | 13.2% | 11.9% | 9.1% | 8.5% | 8.4% |

Within a year the value is compounded at that year's rate and pro-rated by month.

**Worked example.** A 4.0 billion apartment: after 10 years the price factor is ×3.29 (about 13.2 billion; average 12.66% a year); after 30 years ×16.8 (about 67 billion; average 9.86% a year).

### C2. Why not a flat 19%?

An earlier plan used a flat 19% a year (called PA1). It is kept only as an optimistic sensitivity because:

- It stretches the hottest period (2020–2025) over 30 years, while 2016–2020 grew only 3.6% a year in the same data.
- A 5 billion apartment would become about 923 billion (×185) after 30 years.
- The rental yield would shrink to about 0.12%, meaning house prices would have run far beyond what rents can justify.
- It uses primary-market prices, while the group's listings are resale (Global Property Guide: about +13% resale).
- It makes BUY win almost always, so the tool would be biased from the start.

### C3. The rental-yield reality check

Rental yield = a year of rent ÷ price. If prices grow faster than rents, the yield falls:

> yield after t years = yield today × ( (1 + rent growth) / (1 + price growth) )^t

Example with today's yield 3.74% (Global Property Guide, 2-bedroom Hanoi, Q3 2025) and rent growth 6%: after 10 years the yield is 3.74% × 1.06¹⁰ ÷ 3.29 = **2.03%**. The result page shows this as the "Reality check" card, with the group's own median yield from the data (2.3%) as a second reference point and the cost of money (savings 6.5%, mortgage 12% then 14%) for comparison. If the yield is below both the savings rate and the mortgage rate the card says "That's low".

| Home price path | Yield after 10 years / 30 years (start 3.74%) |
|---|---|
| Flat 19% (PA1) | 1.18% / 0.12% |
| Flat 12.66% | 2.03% / 0.60% |
| **PA2 (base)** | **2.03% / 1.28%** |

PA2 and a flat 12.66% agree at year 10 (by construction) but only PA2 keeps the yield sensible at year 30.

---

## Part D. Monthly cash flow, costs and the safety check

### D1. What changes each year

Growth is applied in steps once a year, starting in year 2. The three rates must be switched on together; turning on only rent growth would make RENT look worse than it is.

| Item | Growth per year | Source |
|---|---|---|
| Household income | 5.56% | Red River Delta income per capita, NSO living standards survey 2024, 2019–2024 |
| Living cost | 3.09% (CPI) | World Bank CPI average 2016–2025 |
| Rent | 6% (decided 9 Oct 2026; sensitivity 3% / 7% / 10%) | Anchored between income growth (5.56%) and the 5–15% rises seen in press reports for 2025 (short-term, in some projects only) |
| Service fee, fire insurance | 3.09% (CPI) | Follows living cost |
| Existing debt payment | None | Fixed amount, stops after the number of months the user enters (blank = whole term) |

**Why 6% for rent.** There is no history of apartment rents. At 6% the rent-to-income ratio rises only slightly over 30 years (30% to 34%); at 7% it would reach 45% and at 10% it would exceed income. The 3% and 10% cases are used in Downturn and Boom.

### D2. Costs of living in the home

| Cost | BUY | RENT | Rule |
|---|---|---|---|
| Service (management) fee | Yes | Yes | 10,000 VND per m² per month × floor area, grows with CPI. Hanoi's official range for buildings with lifts is 1,200–16,500 VND/m² (Decision 33/2025); real buildings quoted 5,000–14,000. The person living in the unit pays, and rent listings usually exclude it |
| Fire insurance (compulsory) | 0.05% of price per year | No | Decree 67/2023 and 105/2025. Applied to price, which is an upper bound |
| Repairs inside the unit | 0 in the base case | No | Weakest-sourced item; 1% of price per year is run only as a sensitivity |
| Selling cost | 1.5% of home value, deducted from BUY net worth every year (also year 0) | No | Broker fee 1–2%. The 2% income tax is exempt for a sole home held 183+ days (3.5% total in the sensitivity) |
| Rental deposit | Not modelled | Not modelled | About 2 months of rent; a small effect (see limitation #11) |

### D3. The safety check, step by step

For every month t of the loan term:

1. **Income** = (income 1 + income 2) × growth factor for that year.
2. **Money left** = income − living cost − existing debt − housing payment (loan payment, or rent) − running costs.
3. **Required amount** = safe share × income in month t.
4. **Slack** = money left ÷ income − safe share.
5. The **tightest month** is the month with the smallest slack. The side **passes** if the slack is 0 or more in every month.

**Which safe share?** It depends on income **in today's money** (nominal income divided by cumulative CPI), so that ordinary inflation does not lower the bar:

| Income in today's money | Share that must be kept |
|---|---|
| Under 35 million | 40% |
| 35 to under 50 million | 35% |
| 50 to under 75 million | 30% |
| 75 million or more | 25% |

The share has a cliff at each boundary (income 34 → 35 million flips a verdict, see testing group G6). The sensitivity table includes a version with straight lines between the bands.

**Labels.** *Not safe* = fails in at least one month. *Tight* = passes, but the slack in the tightest month is under 5 percentage points of income. *Comfortable* = slack of 5 points or more. The labels are only a way to present the numbers; pass or fail is the rule above.

### D4. Worked example that reproduces a test case

Test case G1.02: profile A (income 25 + 15 million, savings 2,000 million, living cost 8 million, ages 32 and 30, no debt), BUY unit BHD0175 (PCC1 Complex, 67 m², 3.2 billion), 12-month package. The tool reports that month 25 is the tightest: 15.7 million left, 0.1 million above the safe level. Recomputing by hand:

| Step | Calculation | Result |
|---|---|---|
| Fees, down payment, loan | fees 3,200 × 2.6% = 83.2; down payment 2,000 − 83.2 − 48 = 1,868.8; loan 3,200 − 1,868.8 | 1,331.2 million |
| Principal per month | 1,331.2 ÷ (360 − 24) | 3.96 million |
| Interest, month 25 (year 3) | 1,331.2 × 14% ÷ 12 | 15.53 million |
| Income, month 25 | 40 × 1.0556² | 44.57 million |
| Living cost, month 25 | 8 × 1.0309² | 8.50 million |
| Running costs, month 25 | (67 m² × 10,000 + 3,200 million × 0.05% ÷ 12) × 1.0309² | 0.85 million |
| **Money left** | 44.57 − 8.50 − (3.96 + 15.53) − 0.85 | **15.72 million** |
| Safe level | income in today's money = 44.57 ÷ 1.0309² = 41.9 → 35% band; 35% × 44.57 | 15.60 million |
| Slack | 15.72 − 15.60 | 0.12 million (0.3 points of income) → **Tight** |

This matches the tool's output (15.7 left, 0.1 above the safe level), so the written rules and the code agree.

---

## Part E. Investing the spare money and net worth

### E1. Four investment channels

Money that is not needed for housing is invested in four channels. The user chooses the split in Step 4 (default: 100% savings deposits, because no appetite for risk is assumed).

| Channel | Average return per year | Source and note |
|---|---|---|
| Savings deposits | 6.50% | FiinPro, highest 6–12 month deposit rate 2016–2026, so an upper bound |
| Government bonds | 4.02% | FiinPro, 10-year yield 2016–2026 |
| Gold (SJC) | 11.12% | FiinPro, February 2016 – December 2024. The 2025 spike (+81.5%) is excluded on purpose; including it gives 14.89%, run as a sensitivity |
| Stocks (VN-Index) | 7.99% | investing.com, May 2021 – August 2026, dividends not included |

Each channel earns its yearly return. In Monte Carlo the rate used for a year can differ from the average (Part F3).

### E2. Two pockets and the rules for moving money

Each side (BUY and RENT) holds two pockets:

- **Reserve pocket**: the emergency fund, always in savings deposits. Target = months chosen by the user (default 6) × that month's living cost, so it rises with CPI.
- **Investment pocket**: the four channels, split by the user's mix.

Each month:

1. **Surplus** (money left is positive): first repay any unfunded shortfall, then top up the reserve to its target, then split the rest across the four channels by the mix.
2. **Deficit** (money left is negative): take the shortfall from the four channels in proportion to the mix. Only when the four channels are empty is the reserve used.
3. If the reserve is also empty, the remaining gap becomes an **unfunded shortfall** (no interest charged) that is subtracted from net worth.
4. Every 12 months the four channels are rebalanced back to the user's mix.

Two signals come out of these rules:

- **Uses the emergency fund** (main signal): in what share of simulated futures the four channels run dry and the reserve is touched.
- **Runs out of money** (secondary): in what share the reserve also reaches zero.

### E3. Net worth formulas

| Side | Net worth at year t |
|---|---|
| BUY | Home value (Part C) − selling cost 1.5% − remaining loan − early-repayment fee (years 1–5 only) + reserve + investments − unfunded shortfall |
| RENT | Reserve + investments − unfunded shortfall |

At year 0: RENT = savings; BUY = savings − purchase fees − selling cost.

The **break-even year** is the first year BUY net worth rises above RENT net worth (median path), rounded up to a whole year. The page can show values in today's money by dividing year t by (1 + CPI)^t (about ÷1.36 at year 10 and ÷2.5 at year 30). This changes the display only; the conclusion, the percentages and the break-even year do not change because both sides are divided by the same number.

**Choosing the comparison year N.** Default 10 years (or the loan term if shorter). The user can pick 20 years or the end of the loan, never longer than the loan. A note warns that longer horizons favour BUY because home prices compound and long-run assumptions are less certain. Changing N does not rerun Monte Carlo; it only reads the results at that year. The safety check and the risk sentences always cover the whole loan term, because the debt must be paid until the end.

---

## Part F. Scenarios, sensitivity and Monte Carlo

The tool uses three layers that share one engine and differ only in the inputs fed to it.

| Layer | What changes | Question answered |
|---|---|---|
| Monte Carlo | Random good and bad years around the average | Because of luck alone, within what range does the result fall? |
| Scenarios (Boom, Stable, Downturn) | Several variables move together, like a real period in 2016–2026 data | What if the market runs hot or cools off? |
| Sensitivity | One variable at a time, others stay Stable | Which assumption does the result depend on most? |

### F1. The three scenarios

Principles: (1) each scenario mirrors a period that actually happened in the 2016–2026 data, so every number has a source year; (2) scenarios move the averages only, the standard deviations stay as in Monte Carlo; (3) variables that do not follow the housing cycle in the data (CPI, stocks, gold, running costs) stay the same in all three. Loan term does not change with the scenario.

| Variable | Boom | **Stable (base)** | Downturn | Basis |
|---|---|---|---|---|
| Reference interest rate | 9.75% | **10.5%** | 11.25% | ±1 standard deviation (0.75) |
| Loan-to-value | 80% | **80%** | 70% | MB allows at most 80%; Downturn = banks tighten (VCB package at 70%) |
| Home price growth: start → long-run, τ | 20.43% → 8.38%, τ 6.5 | **20.43% → 8.38%, τ 3.24** | 3.64% → 8.38%, τ 3.24 | Boom: the 2020–25 surge cools twice as slowly. Downturn: a repeat of 2016–2020 |
| Rent growth | 10% | **6%** | 3% | Upper end of press range; about CPI |
| Income growth | 9.29% | **5.56%** | 3.09% | Boom: average 2022–2024. Downturn: equals CPI (real income flat) |
| Savings deposit rate | 5.85% | **6.50%** | 7.60% | Boom: 2020–21 low rates. Downturn: 2022 |
| Government bond yield | 2.40% | **4.02%** | 5.04% | Same periods |
| CPI, stocks, gold, running costs | same | same | same | No link to the housing cycle in the data |

The resulting home price paths: the price multiple after 30 years is ×23.7 in Boom, ×16.8 in Stable and ×9.5 in Downturn, and the average growth over the first 10 years is 14.98%, 12.66% and 6.67%.

### F2. The sensitivity table

Each row changes one thing from the Stable case and runs 500 random futures. The table opens only when the user clicks (so the page stays fast): 17 rows, the base plus these 16 changes.

| Group | Levels tested | Reason |
|---|---|---|
| Home price cooling speed | τ = 1 and τ = 6.5 | Fast and slow cooling |
| Home price upper bound | Flat 19% (PA1) | The old, optimistic plan |
| Rent growth | 3%, 7%, 10% | Press range |
| Maximum age at loan end | 65, 75 | Range across banks |
| Loan-to-value | 70% | Banks tighten |
| Gold return | 14.89% | Includes the 2025 spike |
| Income shock | −1.6% a year in years 2 and 3 | COVID-like shock right after buying |
| Service fee | 16,500 VND/m² | Hanoi ceiling |
| Repairs inside the unit | 1% of price a year | Not in the base case |
| Selling cost | 3.5% | Adds 2% income tax (not the only home) |
| Shocks move together | Correlation 0.5 | One common "bad times" factor: rates up, prices, income and stocks down |
| Safe level | Straight lines between bands | Removes the cliff |

### F3. Monte Carlo

The tool runs **1,000 simulated futures**. A random number generator with a fixed seed (20260909) is used, so the same input always gives the same output.

| Variable | Standard deviation | Drawn | Meaning |
|---|---|---|---|
| Reference interest rate | 0.75 points | once per future | Uncertainty about the long-run level |
| Home price growth | 4 points | once per future, added to every year of the PA2 path | See below |
| Rent growth | 1.25 points | once per future | About (10% − 5%) ÷ 4 from press ranges |
| Savings rate | 0.82 points | once per future | Uncertainty of the average rate |
| Bond yield | 1.37 points | once per future | Same |
| Income growth | 5.71 points | new draw every year | Year-to-year swings, Red River Delta 2019–2024 |
| Gold | 14.13 points | new draw every year | Yearly swings (whole series) |
| Stocks | 19.30 points | new draw every year | Yearly swings, 64 monthly prices |
| CPI (living cost) | none | fixed | Not randomised |

**Why home price uses 4 points, not 14.** In the data, yearly price growth swings about 14%. But the model draws one growth shift per future and keeps it for 30 years, so what matters is the uncertainty of the 30-year **average**: about 14% ÷ √30 ≈ 2.6 points. The group rounded up to 4 for caution.

**Checks built into the design.** With every standard deviation set to 0, every run equals the average path. With correlation 0 the results equal the earlier version without that option.

**Outputs shown on the result page.** Share of futures in which BUY ends richer than RENT at year N (and the part where it never touches the emergency fund); for each side the share that uses the emergency fund and the share that runs out of money; P10 / P50 / P90 net worth (a bad, a middle and a good future); median break-even year; share of futures that stay above the safe level every month. Risk labels are a team convention: under 10% low, 10–25% moderate, above 25% high.

**Reading the result.** The conclusion rests on the safety check using average assumptions. Monte Carlo adds how often things go wrong and when (up to two variables that differ most between futures that touch the reserve and those that do not). If more than 95% of futures use the fund, the tool says the problem is the monthly budget, not bad luck.

---

## Part G. All assumptions at a glance

| Assumption | Value (base) | Status | Where explained |
|---|---|---|---|
| Promotional rate, 6/12/18/24 months | 7.7 / 8.3 / 8.5 / 9.0% | From the MB sheet | B1 |
| Margin after promotion | +1.5% for 12 months, then +3.5% | From the MB sheet | B2 |
| Reference rate | 10.5% | Extrapolated, team decision (08 Oct) | B2 |
| Grace period | 24 months | From the MB sheet | B1 |
| Maximum LTV | 80% (Downturn 70%) | From the MB sheet and VCB | B1 |
| Maximum term | 360 months | From the MB sheet | B1 |
| Maximum age at payoff | 70 (sensitivity 65 / 75) | Other banks; older borrower rule is a team assumption | B3 |
| Purchase fees | 2.6% (2% + 0.5% + about 0.06%) | Legal sources | B4 |
| Early-repayment fee | 1%, years 1–5 | From the MB sheet | B5 |
| Home price growth | 20.43% → 8.38%, τ = 3.24 | Calibrated from data | C1 |
| Income growth | 5.56% | NSO survey | D1 |
| CPI | 3.09% | World Bank | D1 |
| Rent growth | 6% | Reasoned judgement (09 Oct) | D1 |
| Service fee | 10,000 VND/m²/month | Team choice within the legal range | D2 |
| Fire insurance | 0.05% of price a year | Decrees 67/2023, 105/2025 | D2 |
| Repairs | 0 (sensitivity 1%) | Team decision | D2 |
| Selling cost | 1.5% | Broker fee range | D2 |
| Safe share of income | 40 / 35 / 30 / 25% by income band | Team proposal | D3 |
| Emergency fund | 6 months of living cost (user can change) | Team decision | E2 |
| Savings / bonds / gold / stocks | 6.50 / 4.02 / 11.12 / 7.99% | FiinPro, investing.com | E1 |
| Monte Carlo | 1,000 futures, seed 20260909 | Team design | F3 |

Sources, dates and links for each row are in [data_and_sources.md](data_and_sources.md). Judgement calls and their possible effect are listed in [limitations.md](limitations.md).
