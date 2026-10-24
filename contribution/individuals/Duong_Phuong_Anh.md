# Individual Footprint and Objective Contribution Evidence — Dương Phương Anh

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Dương Phương Anh** |
| **Student ID** | 2413380004 |
| **Main role** | **Coordinator / Repository Owner / Financial Model and Assumptions Lead / Integrator** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Technology Applications in Finance and Banking (NHA408E) - FTU 2026 |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `contribution/individual/Duong_Phuong_Anh.md`. Links to the repository are relative to this folder.

---

## 1. Role in the project and summary of responsibilities

As the **Coordinator and repository owner**, my core responsibility is the financial model behind the BUY and RENT comparison, the assumptions it runs on, and the integration of every member's part into one working product. I also hold the documentation, the final test suite and the repository structure, and, by group decision, the work that had no named owner.

My work covers four layers of FinFlow:

1. **Framework and sources (Weeks 1–5):** the project-master schema, the assumptions table skeleton (FIN_ASSUMPTIONS), the input dictionary, input validation, an early logic test, and the source register; I verified the sources before they were cited.
2. **Financial model (Weeks 6–7):** the BUY and RENT calculation (down payment, loan, holding and selling costs, net worth, safety check) and the key assumptions that drive the result.
3. **Integration and interface (Weeks 6–7):** I merged every member's part into one working build and credited interface parts that no other member claimed.
4. **Documentation, testing and repository (final build):** the Final Plan, the change log, the list of limitations, the final test suite, and the repository itself.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Assumptions Framework & Sources** | Designed the FIN_ASSUMPTIONS structure and the project-master schema; kept the source register; read each problem-evidence source in full before citing it. | [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv), [data_and_sources.md](../../docs/data_and_sources.md), [assumptions.md](../../docs/assumptions.md), **[FILE NEEDED: `input_dictionary.md` → put in `docs/`]** |
| **BUY and RENT Calculation** | Down payment net of fees and emergency fund, loan, holding and selling costs, month-by-month cash flow, net worth, safety check over the whole term. | [src/index.html](../../src/index.html): `loanCalc`, `evaluateBuy`, `evaluateRent`, `buyRunningCostAt`, `rentRunningCostAt`, `stepPortfolio`, `getSafetyMarginMinPct`, `findBreakEven`; [financial_logic.md](../../docs/financial_logic.md) |
| **Key Assumptions** | Chose and sourced the assumptions that drive the result: house-price path, rent growth, age cap, reference rate. | `Assumptions_Summary.csv`; `propertyGrowthPctForYear`; [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf) |
| **Integration & Interface Parts** | Merged the members' parts into one offline `index.html`; credited with the interface parts no other member claimed. | [src/index.html](../../src/index.html); [user_flow.md](../../docs/user_flow.md) |
| **Documentation & Testing** | Final Plan, change log, limitations; final test suite of 123 cases. | [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20(Midterm%20to%20Final).pdf), [limitations.md](../../docs/limitations.md), [testing.md](../../docs/testing.md), [revision_summary.md](../../docs/revision_summary.md), `tests/FinFlow_Test_Cases_V5.xlsx` **[FILE NEEDED: `FinFlow_Test_Cases_V5.xlsx` → put in `tests/`]** |
| **Repository & Coordination** | Repository structure following the course guide; group contribution map and individual files. | **[FILE NEEDED: `README.md` → put in `repository root`]**, [contribution_map.md](../contribution_map.md) |

---

## 2. Technical evidence and implementation details

### 2.1 Down payment and loan (`loanCalc`, `financial_logic.md`)

The 27 September version treated buying as cheap. In the final model the down payment is net of purchase fees and the emergency fund:

$$\text{Down payment} = \text{Savings} - 2.6\% \times \text{Price} - \text{Emergency fund}, \qquad \text{Loan} = \text{Price} - \text{Down payment}$$

- The 2.6% purchase fee = 2% maintenance fee + 0.5% registration tax + about 0.06% notary fee (sources in `data_and_sources.md`).
- Eligibility: savings ≥ 20% of price + 2.6% of price + emergency fund.
- **Worked example:** price 5 billion VND, savings 1.5 billion, living cost 15 million/month (6-month fund = 90 million): 1.5 billion − 130 million − 90 million = **1.28 billion** down payment; loan **3.72 billion** (it was 3.5 billion in the 27 September version).

### 2.2 Monthly cash flow and safety check (`evaluateBuy`, `evaluateRent`, `getSafetyMarginMinPct`)

- **Spare money (BUY)** = income − living cost − existing debt − bank payment − holding costs. **Spare money (RENT)** = income − living cost − existing debt − rent − service fee.
- Income grows 5.56% a year, living cost 3.09%, rent 6%.
- Holding costs: service fee 10,000 VND/m²/month (both sides) and fire insurance 0.05% of price a year (BUY side), both growing with inflation.
- **Safety level:** the share of income that must stay free is 40 / 35 / 30 / 25% for income below 35 / 35–49 / 50–74 / 75 million and above, looked up in today's money for every month; both BUY and RENT are checked over the whole term. The "worst month" is the month with the smallest gap between the free share and the required level.
- Existing debt has a "months left" field; promo packages of 6 / 12 / 18 / 24 months; break-even year is rounded up (`findBreakEven`).

### 2.3 Net worth (`evaluateBuy`, `stepPortfolio`)

- **BUY:** house value − 1.5% selling cost − remaining debt − prepayment fee if settled that month + invested money. The year-0 point already deducts purchase and selling costs (selling cost is 75 million on a 5 billion unit), so net worth at year 0 is lower than savings.
- **RENT:** initial savings and monthly spare money invested in 4 channels (savings, bonds, gold, stocks) at the user's mix, rebalanced every 12 months; the emergency fund stays in savings.
- Shortfalls draw on the 4 channels proportionally, then on the emergency fund; when that is empty the shortfall accumulates without interest.

### 2.4 Key assumptions and their sources (`propertyGrowthPctForYear`, `Assumptions_Summary.csv`)

- **House-price path (base case):** a decaying path instead of a fixed 19%:
  $$g(t) = 8.38\% + (20.43\% - 8.38\%)\, e^{-t/3.24}$$
  with τ = 3.24 years chosen so the next 10 years average the last 10 (12.66%). A 5 billion VND unit becomes about 84 billion after 30 years (×16.8); the old fixed 19% gave ×185.
- **Rent growth:** 6% a year, sensitivity 3 / 7 / 10%; income 5.56% and living cost 3.09% always switch on together with it.
- **Age cap:** 70 at settlement, sensitivity 65 and 75 (sources: VIB, Cake, Onlinebank – MB).
- **Reference rate:** 10.5% = market floating rate 13–15% minus the MB margin of 3.5% (midpoint of 9.5–11.5%); with MB's margins the floating rate is 12% in the first year after the promo and 14% afterwards.

### 2.5 Integration and interface parts (`src/index.html`)

- Merged into one `index.html` with embedded data, no server and no internet connection: listings and figures (An, Nam Phương), Monte Carlo and dashboard framework (Tuấn), relevance engine, loan term and loan calculation (Sơn). Commit / pull-request links: **[FILE NEEDED: `evidence_links.md` → put in `contribution/`]**.
- Interface parts credited to me: two-line unit cards with "Show details" (the detailed rules sit behind it); shorter "Your budget" card; spare-money table in Step 4; "What is varied" in the Monte Carlo section as two tables; monthly cash-flow table in short rows; 32 source links beside the numbers; right-column summary box and scroll to the conclusion after Calculate.
- These parts sit under the deep-gradient layout designed by Sơn and Khánh An, which is built on the version I made.

### 2.6 Documentation and final test suite

- Final Plan (v2 to v5, written from Khánh An's initial idea; the final product follows it), change log (batches 1–11), limitations ([limitations.md](../../docs/limitations.md)) and the summaries in `docs/`.
- Test suite: 88 calculation cases, 28 input-error cases, 7 filter cases (123 in total); expected values are the V5 baseline ([testing.md](../../docs/testing.md)).

---

## 3. What I did, by phase

### 3.1 Framework, sources and early logic (Weeks 1–5)

- Refined the initial HTML financial-simulator concept and coordinated group discussions and project development (week 1, recorded in the credit table).
- Project-master schema and listing-filtering logic; the FIN_ASSUMPTIONS table skeleton.
- Input dictionary listing and describing every input (**[FILE NEEDED: `input_dictionary.md` → put in `docs/`]**).
- Co-authored the **data-flow diagram** Source → Input → Validation → Process → Output, with Phạm Thị Khánh An and Nguyễn Hải Sơn ([data-flow.md](../../archive/Week%203/data-flow.md)).
- Input validation in the Calculate-button handler.
- **Early logic test:** designed test cases, calculated them by hand and cross-checked them against the code (**[FILE NEEDED: `validation_and_early_logic_test.md` → put in `docs/`]**).
- Declining-balance repayment method, with Phạm Nam Phương and Phạm Thị Khánh An.
- **Two-point safety-margin rule** and the rule that adds closing costs to the minimum-savings check, designed with Nguyễn Minh Tuấn; implemented together with interface text updates and the auto-generated assumptions box (AI-assisted).
- **Source register:** CFPB Ability-to-Repay reference (qualitative support for the safety-margin idea); State Bank of Vietnam deposit-rate report and the floating-rate sources behind the 10.5% reference rate (with An); three legal citations behind the 2.6% closing costs (registration tax, maintenance fund, notary fee). I read the four problem-evidence sources in full and confirmed the exact figures and links before citing them (with An).

### 3.2 BUY and RENT calculation upgrade (Weeks 6–7)

- Down payment net of the 2.6% purchase fees and a 6-month emergency fund; loan = price − down payment (worked example in 2.1).
- Income +5.56%, living cost +3.09% and rent +6% each year.
- Holding costs: service fee and fire insurance (see 2.2).
- Selling cost 1.5% deducted from BUY net worth, including year 0.
- RENT wealth tracked month by month across 4 investment channels, rebalanced every year; RENT safety checked over the whole term.
- Existing debt with a "months left" field; promo packages of 6 / 12 / 18 / 24 months; break-even year rounded up.
- Functions: `loanCalc`, `evaluateBuy`, `evaluateRent`, `buyRunningCostAt`, `rentRunningCostAt`, `stepPortfolio`, `findBreakEven`, `getSafetyMarginMinPct` in [src/index.html](../../src/index.html).

### 3.3 Key assumptions (Weeks 6–7)

- House-price path 20.43% → 8.38%, τ = 3.24 years; rent growth 6%; age cap 70; reference rate 10.5% (details and sources in 2.4).
- Evidence: [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv); `FIN_ASSUMPTIONS` table and `propertyGrowthPctForYear` in [src/index.html](../../src/index.html); [financial_logic.md](../../docs/financial_logic.md).

### 3.4 Integration, interface, documentation and repository (Weeks 6–7 and final build)

- Integration and interface parts: see 2.5.
- Documentation and final test suite: see 2.6.
- Repository structure following the course guide: README, docs/, contribution/, src/, data/, tests/.
- Group contribution map and the individual footprint files; root **[FILE NEEDED: `README.md` → put in `repository root`]**.

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **Assumptions framework** | FIN_ASSUMPTIONS skeleton, project-master schema, input dictionary | `Assumptions_Summary.csv` in `data/financial_assumptions/`; [assumptions.md](../../docs/assumptions.md); **[FILE NEEDED: `input_dictionary.md` → put in `docs/`]** | Every assumption in the sheet has a value, a status and a source |
| **Source register** | CFPB, deposit-rate report, floating-rate sources, three legal citations | [data_and_sources.md](../../docs/data_and_sources.md) | Open each cited link and compare the figure |
| **Down payment and loan** | Savings − 2.6% fee − emergency fund; loan = price − down payment | `loanCalc` in [src/index.html](../../src/index.html); [financial_logic.md](../../docs/financial_logic.md) | Price 5 billion, savings 1.5 billion, living cost 15 million → loan 3.72 billion |
| **Holding and selling costs** | Service fee, fire insurance, 1.5% selling cost | `buyRunningCostAt`, `rentRunningCostAt`, `evaluateBuy` | Net worth at year 0 is lower than savings by the purchase and selling costs |
| **RENT portfolio** | 4 channels, yearly rebalancing, safety over the whole term | `stepPortfolio`, `evaluateRent` | Change the mix in Step 4: RENT net worth changes, BUY does not |
| **House-price path** | 20.43% → 8.38%, τ = 3.24 | `propertyGrowthPctForYear` | Year-1 growth 20.43%; 10-year average 12.66% |
| **Other key assumptions** | Rent 6%, age cap 70, reference rate 10.5% | `Assumptions_Summary.csv`; [financial_logic.md](../../docs/financial_logic.md) | Assumption box in Step 1 shows the same values |
| **Integration** | One offline `index.html` | [src/index.html](../../src/index.html) | Open the file without internet and run a full case |
| **Interface parts** | Unit cards, budget card, spare-money table, "What is varied", cash-flow table, source links, summary box | [src/index.html](../../src/index.html); [user_flow.md](../../docs/user_flow.md) | Compare each element with the description in the user flow |
| **Documentation** | Final Plan, change log, limitations | [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf); [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20(Midterm%20to%20Final).pdf); [revision_summary.md](../../docs/revision_summary.md); [limitations.md](../../docs/limitations.md) | Numbers in these files match the web page and the workbook |
| **Final test suite** | 88 + 28 + 7 = 123 cases | `tests/FinFlow_Test_Cases_V5.xlsx` **[FILE NEEDED: `FinFlow_Test_Cases_V5.xlsx` → put in `tests/`]**; [testing.md](../../docs/testing.md) | Enter a case's inputs and compare the expected columns |

---

## 5. Evidence by project phase

| Phase | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **Weeks 1–5** | Concept refinement, schema, assumptions skeleton, input dictionary, data-flow diagram, validation, early logic test, source register, Final Plan | [data-flow.md](../../archive/Week%203/data-flow.md); [contribution.md](../../archive/Week%205/contribution.md) | Framework and sources the model is built on |
| **Weeks 6–7** | Calculation upgrade, key assumptions, integration | [src/index.html](../../src/index.html) | The financial logic of the final product and the merged build |
| **Final** | Interface parts, documentation, test suite, repository | [src/index.html](../../src/index.html); [testing.md](../../docs/testing.md); [revision_summary.md](../../docs/revision_summary.md) | The documented, tested and organized version the group submits |

---

## 6. Individual footprint self-check (final readiness checklist)

1. **My main responsibility:**
   The financial model (loan, costs, cash flow, net worth, safety check), the key assumptions with their sources, and the integration of the final build; plus documentation, testing and the repository.
2. **My most important output:**
   The BUY and RENT calculation in `src/index.html` with the assumptions in `Assumptions_Summary.csv`, and the merged offline `index.html`.
3. **Where the evidence is located:**
   `src/index.html`, `data/financial_assumptions/Assumptions_Summary.csv`, `docs/` (Final Plan, change log, `financial_logic.md`, `limitations.md`, `testing.md`), `tests/`, `contribution/`.
4. **How my output supports the group product:**
   - It gives **Tuấn** the calculation that the Monte Carlo reruns 1,000 times, and the assumptions around which the scenarios shift.
   - It gives **An and Nam Phương** the structure in which their series become assumptions (CPI, income, VN-Index, gold, LTV).
   - It passes **Sơn's** age-based term and prepayment fee through the loan calculation, and uses his relevance engine in Step 3.
   - It puts all of these into the one file users open.
5. **Remaining limitation:** see section 7.

---

## 7. Remaining limitations

- **Model scope:** repairs inside the unit (sensitivity only), building depreciation, rental deposit and furnishing costs are not in the main result; the 2% income tax on a sale is not applied; when the whole emergency fund runs out, the shortfall accumulates without interest ([limitations.md](../../docs/limitations.md), #11, #12, #17, #19, #23).
- **Assumptions:** τ rests on the idea that the next 10 years grow like the last 10; rent growth of 6% is a reasoned judgment, not a measurement, because there is no historical rent series; the 10.5% reference rate is extrapolated because the MB document gives no value; "use the older borrower's age" is a group assumption (#5, #10, #16).
- **Maintenance fee:** 2% may not apply to resale units (about 0.56%); the model keeps 2.6% as a conservative level (#26).
- **Build:** Boom / Downturn on the result screen do not update the budget labels in Step 3; the code still contains an unused Chart.js loader and old comments; there is no deployment link yet.
