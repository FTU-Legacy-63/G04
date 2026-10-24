# User Flow

This document describes exactly what the final product (`src/index.html`) does. Button names and labels in quotation marks are the text shown in the interface. The calculation logic is in [`financial_logic.md`](financial_logic.md) and the data sources are in [`data_and_sources.md`](data_and_sources.md).

## 1. Target user and decision supported

- **Target user:** young couples or single people in Hanoi who are deciding whether to buy or rent a 2-bedroom apartment.
- **Question answered:** "Buy or rent a 2-bedroom apartment in Hanoi?" The tool checks two things: (1) after housing payments, holding costs and living costs, is there enough money left each month to stay above the safe level; (2) after many years, which option leaves higher net worth.
- **Scope:** 2-bedroom apartments in Cau Giay, Ha Dong and Tay Ho. The data are listings from batdongsan.com.vn as of 9 Sep 2026.
- **How to run:** open the HTML file in a browser. The data and the engine are embedded, so no server is needed and no data is sent anywhere. (Only the page's web fonts are fetched from Google Fonts when online; without them the browser uses default fonts.)

## 2. Flow overview

```
Step 1            Step 2               Step 3                Step 4                  Step 5
Your finances --> Choose a project --> Choose a BUY unit --> How you invest      --> Result
                  & size (BUY/RENT)    and a RENT unit       spare money             (its own screen)
   |                                   (budget labels)       (optional) + Calculate
   +-- the "Your budget" card updates as the user types
```

Steps 1–4 are on one scrolling page (on desktop a preview rail stays fixed on the right; on mobile a preview card appears between steps). Step 5 is a separate screen that opens after the user clicks **Calculate**.

## 3. Step by step

### Step 1. Your finances

| Field | Notes |
|---|---|
| Income 1 | million VND / month, required |
| Income 2 | optional; blank = applying alone |
| Savings | million VND |
| Minimum living cost | million VND / month |
| Existing monthly debt payment | default 0 |
| Months left on this debt | optional; blank = the debt lasts the whole loan term |
| Emergency fund to keep | months of living cost, default 6; always held in savings, not used for the down payment |
| Age 1 | required, 18–100 |
| Age 2 | optional; blank = applying alone |
| Fixed-rate promo package | MB Bank – Van Phuc branch: fixed for 6 / 12 / 18 / 24 months, then floating |

Also in this step:
- A box shows the **maximum loan term**, worked out from the older borrower's age (age cap 70, at most 360 months). There is no separate loan-term input: the calculation uses this maximum term.
- "Loan & projection assumptions (click to view)" lists the loan, cost, growth and safety-level assumptions, with source links next to the numbers.
- The **"Your budget"** card updates as the user types: maximum safe purchase price, maximum rent, number of units within budget, and a district × size table. Until Income 1, Savings, Minimum living cost and Age 1 are filled in, the card only asks the user to fill them in.

### Step 2. Choose a project & size

- The **Buy** column and the **Rent** column are chosen independently: each side has its own project and size band (Small 45–59, Medium 60–79, Large 80–100 m²). For example, a user can compare "buy small" with "rent large".
- Filters on each side: district, beltway zone, ward, building name. The filters only narrow the list of buildings; they do **not** limit the units suggested in Step 3.
- The **"Same filters as Buy"** checkbox in the Rent column locks the Rent filters and makes them follow the Buy filters; if no rental project matches, the system relaxes them step by step (building name, ward, beltway zone, district) and says what was relaxed.
- Data note: listings and prices from batdongsan.com.vn as of 9 Sep 2026, which may have changed since.

### Step 3. Choose a BUY unit and a RENT unit

- Each side shows a list of units: units in the selected project and size (the target) plus similar units in other buildings, ranked by relevance (score out of 100). The default view shows the target, all high-relevance units and up to 8 medium-relevance units; "Show details" explains the scoring rules.
- **Sorting:** Relevance, Within budget first, Price low → high / high → low, Name A → Z / Z → A, Area large → small / small → large. There is an **"Only within budget"** checkbox and a **"Load more"** button.
- Each unit card has a **budget label**, computed with the same engine as Step 5 for that exact unit:

| Label | Applies to | Meaning |
|---|---|---|
| Within budget | BUY, RENT | Enough for the down payment and passes the safety check over the whole term |
| Payment too tight / Rent too tight | BUY / RENT | At least one month where money left is below the safe level |
| Not enough savings | BUY | Savings are below the minimum down payment (shows the shortfall and a suggested price) |
| No loan available | BUY | The older borrower is 70 or more, or the maximum term leaves no principal-repayment months |

- Labels are warnings only and **do not block** selection. The user picks exactly one unit to buy and one unit to rent (they can be in different buildings and size bands).

### Step 4. How you invest spare money (optional)

- A spare-money table for BUY and RENT, computed for the two selected units: starting money to invest, spare money in month 1, and spare money in the tightest month. The numbers match "Money left over" in Step 5.
- **Your mix:** how each month's spare money is split across 4 channels (Savings deposits, Government bonds, Gold (SJC), Stocks (VN-Index)); the total must be 100%. The default is 100% savings. Each box shows the channel's average return and its source. The mix applies to both sides; the emergency fund always stays in savings.
- The **Calculate** button is in this step. It is disabled until Step 1 is valid and one BUY unit and one RENT unit are selected. After a result exists, **"View last result →"** reopens the latest result.

### Step 5. Result (its own screen)

The **"← Edit inputs"** button returns to Steps 1–4. Blocks from top to bottom:

1. **Conclusion block.** One line: BOTH PASS / ONLY BUY / ONLY RENT / NEITHER OPTION PASSES THE SAFETY CHECK. Each side (Buy, Rent) has a **Comfortable / Tight / Not safe** label, a line giving the tightest month, and a Monte Carlo risk line. The collapsed **"How we check"** section explains the method. The conclusion is a check on average assumptions, not advice; the user decides.
2. **Scenario buttons** Boom / Stable / Downturn (default Stable). Clicking one recalculates the whole page.
3. **"Reality check: rent vs price".** Gross rental yield per m², years of rent needed to equal the price, yield in year 10, compared with market references of 2.3% and 3.74%.
4. **"Net worth over time".** BUY vs RENT net worth chart (P50 line and P10–P90 band) and the break-even year. Buttons choose the comparison horizon: "10 years" (default), "20 years", or "End of loan (N years)". The **Nominal / In today's money** buttons change how money is displayed.
5. **"1,000 simulated futures".** % of scenarios where BUY net worth is higher than RENT, % that need the emergency fund, % that run out of money, and P10 / P50 / P90 final net worth.
6. **"What drives the result? (sensitivity)".** Collapsed by default and run only on click; changes one assumption at a time to show which assumptions the result depends on most.
7. **Detailed Buy and Rent cards:** monthly cash flow by phase, holding costs, money left over, safety label.

## 4. What happens when the user edits inputs

| User action | System response |
|---|---|
| Edits any field in Step 1 | Re-labels the units, **keeps** the selected units, **clears** the result; the user must click Calculate again |
| Edits Step 2 (project, size) | The unit selection in Step 3 is cleared |
| Changes the 4-channel mix or the promo package | Go back to Step 4 or Step 1 and click Calculate again |
| Changes the scenario in Step 5 | Recalculates the safety check, chart and Monte Carlo; keeps the chosen horizon N and money display |
| Changes the horizon N in Step 5 | Only reads the result at that year; Monte Carlo is not rerun; the safety check still covers the whole loan term |

Invalid or missing input shows a specific message and no result, for example "Please fill in Income 1, Savings, Minimum living cost, and Age 1.", "Check income, living cost and age in Step 1.", "Not eligible for a loan due to age", or "The maximum loan term by age is only … months, but the loan term must be longer than the … months grace period". These cases are covered by the test suite (see [`testing.md`](testing.md)).

## 5. Input, process, output

| | Content |
|---|---|
| **Input** | Financial profile (Step 1), one BUY unit and one RENT unit (Steps 2–3), 4-channel investment mix (Step 4) |
| **Process** | Loan eligibility and month-by-month safety check over the whole term; BUY vs RENT net worth by year; Monte Carlo with 1,000 runs; scenarios and sensitivity |
| **Output** | Safety conclusion for each side, net worth and break-even year, Monte Carlo outcome distribution, the assumptions that matter most |

## 6. Example use case

Sample profile used in Final Plan v5: Income 1 = 30, Income 2 = 20 (million VND / month), Savings = 1,500 million VND, Minimum living cost = 15 million VND / month, Age 1 = 32, 6-month emergency fund, 12-month promo package, default 100% savings mix. Enter this profile in Step 1, pick a project and size in Step 2, pick one BUY unit and one RENT unit in Step 3, then click Calculate in Step 4 to see the result in Step 5.
