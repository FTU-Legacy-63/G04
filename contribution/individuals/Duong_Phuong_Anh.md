# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Finance and Banking (NHA408E) - FTU 2026  
**Project:** FinFlow - Buy vs Rent (Group 04, G04)  
**Member:** Dương Phương Anh  
**Student ID:** [add student ID]  
**Assigned Role:** Coordinator - Financial Model and Integration Lead  

---

## 1. Executive Summary of Responsibilities

As the **Coordinator and repository owner**, my core responsibility is the financial model behind the BUY and RENT comparison, the assumptions it runs on, and the integration of every member's part into one working product. I also hold the documentation, the final test suite and the repository structure, and, by group decision, the work that had no named owner.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Assumptions Framework & Sources** | Designed the FIN_ASSUMPTIONS structure and the project-master schema; kept the source register; read each problem-evidence source in full before citing it. | [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv), [data_and_sources.md](../../docs/data_and_sources.md), [assumptions.md](../../docs/assumptions.md), **[FILE NEEDED: `input_dictionary.md` → put in `docs/`]** |
| **BUY and RENT Calculation** | Down payment net of fees and emergency fund, loan, holding and selling costs, month-by-month cash flow, net worth, safety check over the whole term. | [src/index.html](../../src/index.html): `loanCalc`, `evaluateBuy`, `evaluateRent`, `buyRunningCostAt`, `rentRunningCostAt`, `stepPortfolio`, `getSafetyMarginMinPct`, `findBreakEven`; [financial_logic.md](../../docs/financial_logic.md) |
| **Key Assumptions** | Chose and sourced the assumptions that drive the result: house-price path, rent growth, age cap, reference rate. | `Assumptions_Summary.csv`; `propertyGrowthPctForYear`; [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf) |
| **Integration & Interface Parts** | Merged the members' parts into one offline `index.html`; credited with the interface parts no other member claimed. | [src/index.html](../../src/index.html); [user_flow.md](../../docs/user_flow.md) |
| **Documentation & Testing** | Final Plan, change log, limitations; final test suite of 123 cases. | [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20(Midterm%20to%20Final).pdf), [limitations.md](../../docs/limitations.md), [testing.md](../../docs/testing.md), `tests/FinFlow_Test_Cases_V5.xlsx` **[FILE NEEDED: `FinFlow_Test_Cases_V5.xlsx` → put in `tests/`]** |
| **Repository & Coordination** | Repository structure following the course guide; group contribution map and individual files. | **[FILE NEEDED: `README.md` → put in `repository root`]**, [contribution_map.md](../contribution_map.md) |

---

## 2. Technical Evidence & Implementation Details

### 2.1 Down payment and loan (`loanCalc`, `financial_logic.md`)
- **Down payment and loan:**
  $$\text{Down payment} = \text{Savings} - 2.6\% \times \text{Price} - \text{Emergency fund}, \qquad \text{Loan} = \text{Price} - \text{Down payment}$$
- The 2.6% purchase fee = 2% maintenance fee + 0.5% registration tax + about 0.06% notary fee (sources in `data_and_sources.md`).
- Eligibility: savings ≥ 20% of price + 2.6% of price + emergency fund.
- **Worked example:** price 5 billion VND, savings 1.5 billion, living cost 15 million/month (6-month fund = 90 million): 1.5 billion − 130 million − 90 million = 1.28 billion; loan 3.72 billion (it was 3.5 billion in the 27 September version).

### 2.2 Monthly cash flow and safety check (`evaluateBuy`, `evaluateRent`, `getSafetyMarginMinPct`)
- **Spare money (BUY)** = income − living cost − existing debt − bank payment − holding costs. **Spare money (RENT)** = income − living cost − existing debt − rent − service fee.
- Income grows 5.56% a year, living cost 3.09%, rent 6%.
- Holding costs: service fee 10,000 VND/m²/month (both sides) and fire insurance 0.05% of price a year (BUY side), both growing with inflation.
- **Safety level:** the share of income that must stay free is 40 / 35 / 30 / 25% for income below 35 / 35–49 / 50–74 / 75 million and above, looked up in today's money for every month; both BUY and RENT are checked over the whole term. The "worst month" is the month with the smallest gap between the free share and the required level.

### 2.3 Net worth (`evaluateBuy`, `stepPortfolio`)
- **BUY:** house value − 1.5% selling cost − remaining debt − prepayment fee if settled that month + invested money; the year-0 point already deducts purchase and selling costs.
- **RENT:** initial savings and monthly spare money invested in 4 channels (savings, bonds, gold, stocks) at the user's mix, rebalanced every 12 months; the emergency fund stays in savings.
- Shortfalls draw on the 4 channels proportionally, then on the emergency fund; when that is empty the shortfall accumulates without interest.

### 2.4 Key assumptions and their sources (`propertyGrowthPctForYear`, `Assumptions_Summary.csv`)
- **House-price path (base case):**
  $$g(t) = 8.38\% + (20.43\% - 8.38\%)\, e^{-t/3.24}$$
  with τ = 3.24 years chosen so the next 10 years average the last 10 (12.66%). A 5 billion VND unit becomes about 84 billion after 30 years (×16.8); the old fixed 19% gave ×185.
- **Rent growth:** 6% a year, sensitivity 3 / 7 / 10%; income 5.56% and living cost 3.09% always switch on together with it.
- **Age cap:** 70 at settlement, sensitivity 65 and 75 (sources: VIB, Cake, Onlinebank – MB).
- **Reference rate:** 10.5% = market floating rate 13–15% minus the MB margin of 3.5% (midpoint of 9.5–11.5%); with MB's margins the floating rate is 12% in the first year after the promo and 14% afterwards.

### 2.5 Integration and interface parts (`src/index.html`)
- Merged into one `index.html` with embedded data, no server and no internet connection: listings and figures (An, Nam Phương), Monte Carlo and dashboard (Tuấn), relevance engine, loan term and loan calculation (Sơn). Commit / pull-request links: **[FILE NEEDED: `evidence_links.md` → put in `contribution/`]**.
- Interface parts credited to me: two-line unit cards with "Show details"; shorter "Your budget" card; spare-money table in Step 4; "What is varied" as two tables; monthly cash-flow table in short rows; 32 source links beside the numbers; right-column summary box and scroll to the conclusion after Calculate.

### 2.6 Documentation and final test suite
- Final Plan (v2 to v5), change log (batches 1–11), limitations ([limitations.md](../../docs/limitations.md)) and the summaries in `docs/`.
- Test suite: 88 calculation cases, 28 input-error cases, 7 filter cases; expected values are the V5 baseline ([testing.md](../../docs/testing.md)).

---

## 3. Individual Footprint Self-Check (Final Readiness Checklist)

1. **My Main Responsibility:**  
   The financial model (loan, costs, cash flow, net worth, safety check), the key assumptions with their sources, and the integration of the final build; plus documentation, testing and the repository.
2. **My Most Important Output:**  
   The BUY and RENT calculation in `src/index.html` with the assumptions in `Assumptions_Summary.csv`, and the merged offline `index.html`.
3. **Where the Evidence is Located:**  
   `src/index.html`, `data/financial_assumptions/Assumptions_Summary.csv`, `docs/` (Final Plan, change log, `financial_logic.md`, `limitations.md`, `testing.md`), `tests/`, `contribution/`.
4. **How My Output Supports the Group Product:**
   - It gives **Tuấn** the calculation that the Monte Carlo reruns 1,000 times, and the assumptions around which the scenarios shift.
   - It gives **An and Nam Phương** the structure in which their series become assumptions (CPI, income, VN-Index, gold, LTV).
   - It passes **Sơn's** age-based term and prepayment fee through the loan calculation, and uses his relevance engine in Step 3.
   - It puts all of these into the one file users open.
5. **Remaining Limitation:**  
   Repairs inside the unit (sensitivity only), building depreciation, rental deposit and furnishing costs are not in the main result; the 2% maintenance fee may not apply to resale units; τ rests on the idea that the next 10 years grow like the last 10; rent growth of 6% is a reasoned judgment, not a measurement; there is no deployment link yet ([limitations.md](../../docs/limitations.md), #5, #10, #11, #19, #23, #26).
