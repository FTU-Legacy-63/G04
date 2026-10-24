# Individual Footprint — Dương Phương Anh

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Dương Phương Anh** |
| **Student ID** | [add student ID] |
| **Main role** | **Coordinator / Repository Owner / Financial Model and Assumptions Lead / Integrator** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `docs/individual/phuong-anh.md`. Links to the repository are relative to this folder.

---

## 1. Role in the project

My work covers four layers of FinFlow:

1. **Framework and sources (Weeks 1–5):** the project-master schema, the assumptions table skeleton (FIN_ASSUMPTIONS), the input dictionary, input validation, an early logic test, and the source register; I verified the sources before they were cited.
2. **Financial model (Weeks 6–7):** the BUY and RENT calculation (down payment, loan, holding and selling costs, net worth, safety check) and the key assumptions that drive the result.
3. **Integration and interface (Weeks 6–7):** I merged every member's part into one working build and credited interface parts that no other member claimed.
4. **Documentation, testing and repository (final build):** the Final Plan, the revision log, the list of limitations, the final test suite, and the repository itself. Under the group's decision, work that had no named owner is credited to me.

---

## 2. Personal footprint in the product

1. **A BUY and RENT model that carries the real costs.**
   The 27 September version treated buying as cheap. In the final model the down payment is net of purchase fees and the emergency fund:

   $$\text{Down payment} = \text{Savings} - 2.6\% \times \text{Price} - \text{Emergency fund}, \qquad \text{Loan} = \text{Price} - \text{Down payment}$$

   Example: price 5 billion VND, savings 1.5 billion, living cost 15 million/month (6-month fund = 90 million): 1.5 billion − 130 million − 90 million = **1.28 billion** down payment, so the loan is **3.72 billion** (it was 3.5 billion before). Holding costs reduce monthly spare money, and a 1.5% selling cost reduces BUY net worth in every year, including year 0 (75 million on a 5 billion unit).

2. **The assumptions that decide the answer, each with a source.**
   House prices follow a decaying path instead of a fixed 19%:

   $$g(t) = 8.38\% + (20.43\% - 8.38\%)\, e^{-t/3.24}$$

   A 5 billion VND unit becomes about 84 billion after 30 years (×16.8), against ×185 under the old fixed rate. I also set rent growth at 6% a year (sensitivity 3 / 7 / 10%), the age cap at 70 (sensitivity 65 and 75), and the reference rate at 10.5% (market floating rate 13–15% minus the MB margin of 3.5%).

3. **One working product and one organized repository.**
   I merged the data and figures of An and Nam Phương, the Monte Carlo and dashboard of Tuấn, and the relevance engine, loan term and loan calculation of Sơn into a single `index.html` that runs without a server or internet connection, and kept the repository structured so a reviewer can find the evidence.

---

## 3. What I actually did

### 3.1. Framework, sources and early logic (Weeks 1–5)
- Refined the initial HTML financial-simulator concept and coordinated group discussions and project development (week 1, recorded in the credit table).
- Project-master schema and listing-filtering logic; the FIN_ASSUMPTIONS table skeleton.
- Input dictionary listing and describing every input (**[FILE NEEDED: `input_dictionary.md` → put in `docs/`]**).
- Co-authored the **data-flow diagram** Source → Input → Validation → Process → Output, with Phạm Thị Khánh An and Nguyễn Hải Sơn ([data-flow.md](../../archive/Week%203/data-flow.md)).
- Input validation in the Calculate-button handler.
- **Early logic test:** designed test cases, calculated them by hand and cross-checked them against the code (**[FILE NEEDED: `validation_and_early_logic_test.md` → put in `docs/`]**).
- Declining-balance repayment method, with Phạm Nam Phương and Phạm Thị Khánh An.
- **Two-point safety-margin rule** and the rule that adds closing costs to the minimum-savings check, designed with Nguyễn Minh Tuấn; implemented together with interface text updates and the auto-generated assumptions box (AI-assisted).
- **Source register:** CFPB Ability-to-Repay reference (qualitative support for the safety-margin idea); State Bank of Vietnam deposit-rate report and the floating-rate sources behind the 10.5% reference rate (with An); three legal citations behind the 2.6% closing costs (registration tax, maintenance fund, notary fee). I read the four problem-evidence sources in full and confirmed the exact figures and links before citing them (with An).
- Final Plan ([FinFlow - Final Plan.pdf](../FinFlow%20-%20Final%20Plan.pdf)), written from Khánh An's initial idea; the final product follows it.

### 3.2. BUY and RENT calculation upgrade (Weeks 6–7)
- Down payment net of the 2.6% purchase fees and a 6-month emergency fund; loan = price − down payment (worked example in section 2).
- Income +5.56%, living cost +3.09% and rent +6% each year.
- Holding costs: service fee 10,000 VND/m²/month (both sides) and fire insurance 0.05% a year (BUY side).
- Selling cost 1.5% deducted from BUY net worth, including year 0.
- RENT wealth tracked month by month across 4 investment channels, rebalanced every year; RENT safety is checked over the whole term.
- Existing debt with a "months left" field; promo packages of 6 / 12 / 18 / 24 months; break-even year rounded up.
- Functions: `loanCalc`, `evaluateBuy`, `evaluateRent`, `buyRunningCostAt`, `rentRunningCostAt`, `stepPortfolio`, `findBreakEven`, `getSafetyMarginMinPct` in [src/index.html](../../src/index.html).

### 3.3. Key assumptions (Weeks 6–7)
- House-price path 20.43% → 8.38%, τ = 3.24 years, calibrated so the next 10 years average the last 10 (12.66%); rent growth 6%; age cap 70 (sources: VIB, Cake, Onlinebank – MB); reference rate 10.5%.
- Evidence: [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv); `FIN_ASSUMPTIONS` table and `propertyGrowthPctForYear` in [src/index.html](../../src/index.html); [financial_logic.md](../financial_logic.md).

### 3.4. Integration of the final build (Weeks 6–7)
- Merged: data and figures (An, Nam Phương); Monte Carlo and dashboard framework (Tuấn); relevance engine, loan term and loan calculation (Sơn).
- Result: one `index.html`, data embedded, no internet needed. Commit / pull-request links: **[FILE NEEDED: `evidence_links.md` → put in `contribution/`]**.

### 3.5. Interface parts credited to me
- Two-line unit cards, with the detailed rules behind "Show details".
- A shorter "Your budget" card.
- The spare-money table in Step 4.
- "What is varied" in the Monte Carlo section, split into two tables.
- Monthly cash-flow table split into short rows.
- 32 source links placed next to the numbers.
- Right-column summary box, and the page scroll to the conclusion block after Calculate.
- These parts sit under the deep-gradient layout designed by Sơn and Khánh An, which is built on the version I made.

### 3.6. Documentation and final test suite (final build)
- Final Plan ([FinFlow - Final Plan.pdf](../FinFlow%20-%20Final%20Plan.pdf), versions v2 to v5), the change log ([FinFlow - Change log (Midterm to Final).pdf](../FinFlow%20-%20Change%20log%20(Midterm%20to%20Final).pdf), batches 1–11) and the list of limitations ([limitations.md](../limitations.md)).
- Final test suite: 88 calculation cases, 28 input-error cases and 7 filter cases (`tests/FinFlow_Test_Cases_V5.xlsx` **[FILE NEEDED: `FinFlow_Test_Cases_V5.xlsx` → put in `tests/`]**; summary in [testing.md](../testing.md)).

### 3.7. Repository and coordination
- Repository structure following the course guide: README, docs/, contribution/, src/, data/, tests/.
- Group contribution map and the individual footprint files; root **[FILE NEEDED: `README.md` → put in `repository root`]**.

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **Assumptions framework** | FIN_ASSUMPTIONS skeleton, project-master schema, input dictionary | `Assumptions_Summary.csv` in `data/financial_assumptions/`; [assumptions.md](../assumptions.md); **[FILE NEEDED: `input_dictionary.md` → put in `docs/`]** | Every assumption in the sheet has a value, a status and a source |
| **Source register** | CFPB, deposit-rate report, floating-rate sources, three legal citations | [data_and_sources.md](../data_and_sources.md) | Open each cited link and compare the figure |
| **Down payment and loan** | Savings − 2.6% fee − emergency fund; loan = price − down payment | `loanCalc` in [src/index.html](../../src/index.html); [financial_logic.md](../financial_logic.md) | Price 5 billion, savings 1.5 billion, living cost 15 million → loan 3.72 billion |
| **Holding and selling costs** | Service fee, fire insurance, 1.5% selling cost | `buyRunningCostAt`, `rentRunningCostAt`, `evaluateBuy` | Net worth at year 0 is lower than savings by the purchase and selling costs |
| **RENT portfolio** | 4 channels, yearly rebalancing, safety over the whole term | `stepPortfolio`, `evaluateRent` | Change the mix in Step 4: RENT net worth changes, BUY does not |
| **House-price path** | 20.43% → 8.38%, τ = 3.24 | `propertyGrowthPctForYear` | Year-1 growth 20.43%; 10-year average 12.66% |
| **Other key assumptions** | Rent 6%, age cap 70, reference rate 10.5% | `Assumptions_Summary.csv`; [financial_logic.md](../financial_logic.md) | Assumption box in Step 1 shows the same values |
| **Integration** | One offline `index.html` | [src/index.html](../../src/index.html) | Open the file without internet and run a full case |
| **Interface parts** | Unit cards, budget card, spare-money table, "What is varied", cash-flow table, source links, summary box | [src/index.html](../../src/index.html); [user_flow.md](../user_flow.md) | Compare each element with the description in the user flow |
| **Documentation** | Final Plan, revision log, limitations | [FinFlow - Final Plan.pdf](../FinFlow%20-%20Final%20Plan.pdf); [FinFlow - Change log (Midterm to Final).pdf](../FinFlow%20-%20Change%20log%20(Midterm%20to%20Final).pdf); [revision_summary.md](../revision_summary.md); [limitations.md](../limitations.md) | Numbers in these files match the web page and the workbook |
| **Final test suite** | 88 + 28 + 7 cases | `tests/FinFlow_Test_Cases_V5.xlsx` **[FILE NEEDED: `FinFlow_Test_Cases_V5.xlsx` → put in `tests/`]**; [testing.md](../testing.md) | Enter a case's inputs and compare the expected columns |

---

## 5. Evidence by project phase

| Phase | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **Weeks 1–5** | Concept refinement, schema, assumptions skeleton, input dictionary, data-flow diagram, validation, early logic test, source register, Final Plan | [data-flow.md](../../archive/Week%203/data-flow.md); [contribution.md](../../archive/Week%205/contribution.md) | Framework and sources the model is built on |
| **Weeks 6–7** | Calculation upgrade, key assumptions, integration | [src/index.html](../../src/index.html) | The financial logic of the final product and the merged build |
| **Final** | Interface parts, documentation, test suite, repository | [src/index.html](../../src/index.html); [testing.md](../testing.md); [revision_summary.md](../revision_summary.md) | The documented, tested and organized version the group submits |

---

## 6. Remaining limitations

- **Model scope:** repairs inside the unit (sensitivity only), building depreciation, rental deposit and furnishing costs are not in the main result; the 2% income tax on a sale is not applied; when the whole emergency fund runs out, the shortfall accumulates without interest ([limitations.md](../limitations.md), #11, #12, #17, #19, #23).
- **Assumptions:** τ rests on the idea that the next 10 years grow like the last 10; rent growth of 6% is a reasoned judgment, not a measurement, because there is no historical rent series; the 10.5% reference rate is extrapolated because the MB document gives no value; "use the older borrower's age" is a group assumption (#5, #10, #16).
- **Maintenance fee:** 2% may not apply to resale units (about 0.56%); the model keeps 2.6% as a conservative level (#26).
- **Build:** Boom / Downturn on the result screen do not update the budget labels in Step 3; the code still contains an unused Chart.js loader and old comments; there is no deployment link yet.

> **Note on AI assistance:** the implementation of the safety-margin and closing-cost rules was produced with AI assistance at my request and under my direction.
