# Individual Footprint and Objective Contribution Evidence — Dương Phương Anh

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Dương Phương Anh** |
| **Student ID** | 2413380004 |
| **Main role** | **Coordinator / Repository Owner / Financial Model and Assumptions Lead / Integrator** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `contribution/individuals/Duong_Phuong_Anh.md`. Links to the repository are relative to this folder.
>
> **How to read the links:** `src/index.html#L<number>` points to the line where a function starts in the final V5 build of the product; if the file is edited later, search for the function name instead. External sources are listed once more, grouped by topic, in section 8.

---

## 1. Role in the project and summary of responsibilities

As the **Coordinator and repository owner**, my core responsibility is the financial model behind the BUY and RENT comparison, the assumptions it runs on, and the integration of every member's part into one working product. I also hold the documentation, the final test suite and the repository structure, and, by group decision, the work that had no named owner.

My work covers four layers of FinFlow:

1. **Framework and sources (Weeks 1–5):** the project-master schema, the assumptions table skeleton (FIN_ASSUMPTIONS), the input dictionary, input validation, an early logic test, and the source register; I verified the sources before they were cited.
2. **Financial model (Weeks 6–7):** the BUY and RENT calculation (down payment, loan, holding and selling costs, net worth, safety check) and the key assumptions that drive the result.
3. **Integration and interface (Weeks 6–7):** I merged every member's part into one working build and made the V5 interface changes listed in section 2.5.
4. **Documentation, testing and repository (final build):** the Final Plan, the change log, the list of limitations, the final test suite, and the repository itself.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Assumptions Framework & Sources** | Designed the FIN_ASSUMPTIONS structure and the project-master schema; kept the source register; read each problem-evidence source in full before citing it. | [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv), [data_and_sources.md](../../docs/data_and_sources.md), [assumptions.md](../../docs/assumptions.md), [input-dictionary.md (Week 3)](../../archive/Week%203/input-dictionary.md), [sources-register.md (Week 3)](../../archive/Week%203/sources-register.md) |
| **BUY and RENT Calculation** | Down payment net of fees and emergency fund, loan, holding and selling costs, month-by-month cash flow, net worth, safety check over the whole term. | [src/index.html](../../src/index.html): [`loanCalc`](../../src/index.html#L1580), [`evaluateBuy`](../../src/index.html#L1757), [`evaluateRent`](../../src/index.html#L1976), [`buyRunningCostAt`](../../src/index.html#L1469), [`rentRunningCostAt`](../../src/index.html#L1476), [`stepPortfolio`](../../src/index.html#L1418), [`getSafetyMarginMinPct`](../../src/index.html#L1746), [`findBreakEven`](../../src/index.html#L2315); [financial_logic.md](../../docs/financial_logic.md) |
| **Key Assumptions** | Chose and sourced the assumptions that drive the result: house-price path, rent growth, age cap, reference rate. | [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv); [`propertyGrowthPctForYear`](../../src/index.html#L1327); [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf); source links in section 8 |
| **Integration & Interface Parts** | Merged the members' parts into one offline `index.html`; V5 interface changes (see 2.5) on top of the deep-gradient layout by Sơn and Khánh An. | [src/index.html](../../src/index.html); [user_flow.md](../../docs/user_flow.md); commit links in [evidence_links.png](../evidence/Duong_Phuong_Anh/evidence_links.png) |
| **Documentation & Testing** | Final Plan, change log, limitations; final test suite of 123 cases, all passed. | [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20%28Midterm%20to%20Final%29.pdf), [limitations.md](../../docs/limitations.md), [testing.md](../../docs/testing.md), [revision_summary.md](../../docs/revision_summary.md), [FinFlow_Test_Cases_V5.xlsx](../../tests/FinFlow_Test_Cases_V5.xlsx) |
| **Repository & Coordination** | Repository structure following the course guide; group contribution map and individual files. | [README.md](../../README.md), [contribution_map.md](../contribution_map.md) |

---

## 2. Technical evidence and implementation details

### 2.1 Down payment and loan (`loanCalc`, `financial_logic.md`)

Code: [`loanCalc`](../../src/index.html#L1580) in [src/index.html](../../src/index.html). Logic description: [financial_logic.md](../../docs/financial_logic.md).

The 27 September version treated buying as cheap. In the final model the down payment is net of purchase fees and the emergency fund:

```text
Down payment = Savings − 2.6% × Price − Emergency fund
Loan         = Price − Down payment
```

- The 2.6% purchase fee = 2% maintenance fee + 0.5% registration tax + about 0.06% notary fee (sources in [data_and_sources.md](../../docs/data_and_sources.md)). Legal basis for each part:
  - 2% maintenance fund: [Article 152, Law on Housing 2023](https://hethongphapluat.com/law-no-27-2023-qh15-dated-december-27-2023-on-housing/dieu-152); explanation of who pays: [Thư viện Pháp luật](https://thuvienphapluat.vn/phap-luat-nha-dat/nguoi-mua-can-ho-chung-cu-co-bat-buoc-phai-dong-phi-bao-tri-chung-cu-khong-8987.html).
  - 0.5% registration tax: [Thư viện Pháp luật — cases of exemption and rate](https://thuvienphapluat.vn/phap-luat-nha-dat/toan-bo-19-truong-hop-duoc-mien-le-phi-truoc-ba-nha-dat-2026-14320.html); [declaration under Decree 373/2025](https://thuvienphapluat.vn/phap-luat-nha-dat/ho-so-khai-le-phi-truoc-ba-nha-dat-moi-nhat-2026-chuan-nghi-dinh-373-2025-nd-cp-14436.html).
  - Notary fee about 0.05–0.07%: [LuatVietnam](https://luatvietnam.vn/hanh-chinh/muc-phi-cong-chung-moi-nhat-570-21497-article.html).
- Eligibility: savings ≥ 20% of price + 2.6% of price + emergency fund.
- **Worked example:** price 5 billion VND, savings 1.5 billion, living cost 15 million/month (6-month fund = 90 million): 1.5 billion − 130 million − 90 million = **1.28 billion** down payment; loan **3.72 billion** (it was 3.5 billion in the 27 September version).
- **How to check:** the same steps are worked out for other prices in [financial_logic.md](../../docs/financial_logic.md) (A3 and D4), and the formulas are in `loanCalc`.
- In `loanCalc` my part is the down payment, purchase fees, schedule and net worth. The age-based term (`calcLoanTerm`) and the prepayment-fee rule (`getPrepaymentFeePct`) are Sơn's and are passed into this function.

### 2.2 Monthly cash flow and safety check (`evaluateBuy`, `evaluateRent`, `getSafetyMarginMinPct`)

Code: [`evaluateBuy`](../../src/index.html#L1757), [`evaluateRent`](../../src/index.html#L1976), [`getSafetyMarginMinPct`](../../src/index.html#L1746), [`buyRunningCostAt`](../../src/index.html#L1469), [`rentRunningCostAt`](../../src/index.html#L1476).

- **Spare money (BUY)** = income − living cost − existing debt − bank payment − holding costs. **Spare money (RENT)** = income − living cost − existing debt − rent − service fee.
- Income grows 5.56% a year, living cost 3.09%, rent 6% (sources in 2.4).
- Holding costs: service fee 10,000 VND/m²/month (both sides) and fire insurance 0.05% of price a year (BUY side), both growing with inflation. Sources:
  - Service fee: Hanoi's price framework of 1,200–16,500 VND/m²/month for buildings with a lift — [Thời báo Tài chính](https://thoibaotaichinhvietnam.vn/gia-dich-vu-quan-ly-van-hanh-chung-cu-tai-ha-noi-tu-700-dong-16500-dongm-thang-175052.html) and [VnExpress](https://vnexpress.net/ha-noi-tiep-tuc-ap-tran-gia-dich-vu-chung-cu-16-500-dong-mot-m2-4877080.html). The 10,000 level is the group's choice between observed building fees and sits below the cap.
  - Fire insurance 0.05%: [Luật Minh Khuê](https://luatminhkhue.vn/muc-phi-bao-hiem-chay-no-chung-cu-moi-nhat-va-cach-tinh.aspx); the compulsory-insurance rule for apartment buildings: [LSVN](https://lsvn.vn/tu-01-7-chung-cu-nha-o-tap-the-tu-05-tang-tro-len-phai-mua-bao-hiem-chay-no-bat-buoc-a158203.html).
  - In-unit repairs (1% rule, sensitivity row only): [Metrobank](https://www.metrobank.com.ph/articles/learn/home-maintenance-budget).
- **Safety level:** the share of income that must stay free is 40 / 35 / 30 / 25% for income below 35 / 35–49 / 50–74 / 75 million and above, looked up in today's money for every month; both BUY and RENT are checked over the whole term. The "worst month" is the month with the smallest gap between the free share and the required level. The tiers are the group's proposal (the 25% top tier is interpolated); [CFPB Ability-to-Repay rule](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf) and [DNSE on debt-to-income](https://www.dnse.com.vn/hoc/ty-le-no-tren-thu-nhap) are qualitative references only, because a debt-to-income ratio does not subtract living costs.
- Existing debt has a "months left" field; promo packages of 6 / 12 / 18 / 24 months; break-even year is rounded up ([`findBreakEven`](../../src/index.html#L2315)).

### 2.3 Net worth (`evaluateBuy`, `stepPortfolio`)

Code: [`evaluateBuy`](../../src/index.html#L1757), [`stepPortfolio`](../../src/index.html#L1418).

- **BUY:** house value − 1.5% selling cost − remaining debt − prepayment fee if settled that month (fee rule by Sơn) + invested money. The year-0 point already deducts purchase and selling costs (selling cost is 75 million on a 5 billion unit), so net worth at year 0 is lower than savings. Sources for the selling cost: broker commission of 1–2% — [wiki.batdongsan](https://wiki.batdongsan.com.vn/wiki/phi-moi-gioi-nha-dat-109150); personal income tax of 2% on a sale — [Thư viện Pháp luật](https://thuvienphapluat.vn/ma-so-thue/phap-luat-thue/ban-nha-o-can-ho-chung-cu-nop-thue-tncn-bao-nhieu-phan-tram-127913-218677.html), with the exemption for the only home owned — [Báo Pháp luật](https://baophapluat.vn/ban-can-nha-duy-nhat-co-phai-nop-thue-thu-nhap-ca-nhan-khong.html) (the model applies 0%; 3.5% runs as a sensitivity row).
- **RENT:** initial savings and monthly spare money invested in 4 channels (savings, bonds, gold, stocks) at the user's mix, rebalanced every 12 months; the emergency fund stays in savings. Return and volatility of each channel come from the series collected by Khánh An and Nam Phương ([Deposit_Rates.csv](../../data/financial_assumptions/Deposit_Rates.csv), [Gov_Bond_Yields.csv](../../data/financial_assumptions/Gov_Bond_Yields.csv), [Gold_Price_SJC.csv](../../data/financial_assumptions/Gold_Price_SJC.csv), [VNIndex_Returns.csv](../../data/financial_assumptions/VNIndex_Returns.csv)); see their files in this folder.
- Shortfalls draw on the 4 channels proportionally, then on the emergency fund; when that is empty the shortfall accumulates without interest.

### 2.4 Key assumptions and their sources (`propertyGrowthPctForYear`, `Assumptions_Summary.csv`)

Code: [`FIN_ASSUMPTIONS`](../../src/index.html#L1204), [`propertyGrowthPctForYear`](../../src/index.html#L1327), [`calcLoanTerm`](../../src/index.html#L1546). Values with status and source: [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv). Cross-check of the workbook against the code (48 parameters compared, no mismatches): [Code_Cross_Check.csv](../../data/financial_assumptions/Code_Cross_Check.csv).

- **House-price path (base case):** a decaying path instead of a fixed 19%, where k is the year of the projection and k = 1 is the first year (this is how `propertyGrowthPctForYear` counts):

  ```text
  g(k) = 8.38% + (20.43% − 8.38%) × e^(−(k − 1) / 3.24)
  ```

  Here 8.38% is the long-run growth rate, 20.43% is the growth in the first year (k = 1), and τ = 3.24 years (the number under the "/") is chosen so the next 10 years average the last 10 (12.66%). A 5 billion VND unit becomes about 84 billion after 30 years (×16.8); the old fixed 19% gave ×185.
  - Sources: starting rate (2020–2025 compound growth of primary prices) — [CafeF](https://cafef.vn/nhin-lai-10-nam-bds-ha-noi-gia-can-ho-tang-gan-300-thi-truong-chuan-bi-da-cuc-hoa-18826042315173533.chn) and [Cushman & Wakefield](https://cloud.comm.cushmanwakefield.com/Hanoi_realestate_market_review?); long-run rate 8.38% = CPI 3.09% + real GDP per person 5.29% — [World Bank CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2025&locations=VN&start=2016&view=chart) and [World Bank GDP per person](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?end=2025&locations=VN&start=2016). Data: [Property_Price_Growth.csv](../../data/financial_assumptions/Property_Price_Growth.csv), [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv).
- **Rent growth:** 6% a year, sensitivity 3 / 7 / 10%; income 5.56% and living cost 3.09% always switch on together with it. Sources: [VnExpress — rising apartment rents](https://vnexpress.net/chat-vat-vi-gia-thue-chung-cu-leo-thang-4927114.html) (2025: 10–15% for many apartments, 5–10% in some projects) and [Vietnambiz — rental yields falling](https://vietnambiz.vn/loi-suat-cho-thue-chung-cu-dang-giam-dan-202541323742923.htm) (flat rents for 3 years); income growth: [NSO Living Standards Survey 2024](https://www.nso.gov.vn/wp-content/uploads/2026/03/Sach-Khao-sat-muc-song-dan-cu-2024.pdf), data in [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv). The VnExpress sources were found by Khánh An; the value of 6% was chosen by me. Reasoning for choosing 6%: [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf), section B3.
- **Age cap:** 70 at settlement, sensitivity 65 and 75 (sources: [VIB](https://www.vib.com.vn/vn/cam-nang/vay/vay-bat-dong-san/vay-mua-nha-duoc-bao-nhieu-nam), [Cake](https://cake.vn/tin-tuc/tai-chinh/vay-the-chap-toi-da-duoc-bao-nhieu-nam), [Onlinebank – MB](https://onlinebank.com.vn/sp/vay-mua-nha-du-an-mb/), [Standard Chartered](https://www.sc.com/vn/loans/mortgage/)). The value and its sources are mine; the rule in the code (`calcLoanTerm`) is Sơn's.
- **Reference rate:** 10.5% = market floating rate 13–15% minus the MB margin of 3.5% (midpoint of 9.5–11.5%); with MB's margins the floating rate is 12% in the first year after the promo and 14% afterwards. Sources: [Thanh Niên, 25/08/2026](https://thanhnien.vn/nguoi-vay-mua-nha-dang-chiu-lai-suat-bao-nhieu-185260825101722042.htm) and [Dân trí, 24/08/2026](https://dantri.com.vn/kinh-doanh/lai-suat-tha-noi-tren-14nam-ngan-hang-giam-cho-vay-mua-nha-20260823171410442.htm). The MB rate sheet itself gives margins but no reference value: [mb_bank_rate.jpg](../../data/financial_assumptions/mb_bank_rate.jpg); data: [Reference_Rate.csv](../../data/financial_assumptions/Reference_Rate.csv), [Mortgage_Rates_Market.csv](../../data/financial_assumptions/Mortgage_Rates_Market.csv).
- **Workbook corrections:** the change log records the corrections #15–#26 made to the assumptions workbook; the series were collected by Khánh An and Nam Phương, who also found several of the errors (see their files). **[CONFIRM: who applied each correction]**

### 2.5 Integration and interface parts (`src/index.html`)

- Merged into one `index.html` with embedded data, no server and no internet connection: listings (Tuấn: Cau Giay; Sơn: Ha Dong and Tay Ho), financial series and workbook figures (Khánh An, Nam Phương), Monte Carlo and dashboard framework (Tuấn), relevance engine, loan term and prepayment fee (Sơn). Commit links: [evidence_links.png](../evidence/Duong_Phuong_Anh/evidence_links.png). (The repository has no pull requests; the evidence is in commits.)
- V5 interface changes credited to me: two-line unit cards with "Show details"; shorter wording of the "Your budget" card (the card and labels are Sơn's); spare-money table in Step 4; "What is varied" in the Monte Carlo section as two tables (the simulation itself is Tuấn's: [`runMonteCarlo`](../../src/index.html#L2187), [`MC_SETTINGS`](../../src/index.html#L2061)); monthly cash-flow table in short rows; regrouping of the assumptions box into 5 groups with the shared list of 32 source links ([`renderLoanAssumptionsBox`](../../src/index.html#L3464), first built by Sơn; the file contains 32 source addresses, listed in section 8); right-column summary box and scroll to the conclusion after Calculate (the conclusion block [`buildConclusionHTML`](../../src/index.html#L4254) is Sơn's design on Tuấn's first dashboard).
- These parts sit under the deep-gradient layout designed by Sơn and Khánh An, which is built on the version I made.

### 2.6 Documentation and final test suite

- Final Plan (v2 to v5, written from Khánh An's initial idea; the final product follows it): [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf); change log (batches 1–11): [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20%28Midterm%20to%20Final%29.pdf); limitations: [limitations.md](../../docs/limitations.md); and the summaries in `docs/` ([revision_summary.md](../../docs/revision_summary.md), [financial_logic.md](../../docs/financial_logic.md), [assumptions.md](../../docs/assumptions.md), [user_flow.md](../../docs/user_flow.md)).
- Test suite: 88 calculation cases, 28 input-error cases, 7 filter cases (123 in total); expected values are the V5 baseline ([testing.md](../../docs/testing.md); workbook [FinFlow_Test_Cases_V5.xlsx](../../tests/FinFlow_Test_Cases_V5.xlsx)).
- Results of running the suite: **123 of 123 cases passed** (88/88 calculation, 28/28 input-error, 7/7 filter), run by hand in Microsoft Edge and Google Chrome on a laptop on 9 Oct 2026. Two cosmetic wording issues (negative-savings and negative-debt messages, LI.09 and LI.10) remain open; details in [testing.md](../../docs/testing.md), section 5.2.
- The expected values are the V5 baseline of 9 Oct. The later deep-gradient interface was checked by Sơn for layout and script errors (see his file); **[CONFIRM: calculation results unchanged after the interface change, and who reran which cases]**.

---

## 3. What I did, by phase

### 3.1 Framework, sources and early logic (Weeks 1–5)

- Refined the initial HTML financial-simulator concept and coordinated group discussions and project development (week 1, recorded in the credit table: [Week 1 README](../../archive/Week%201/README.md)).
- Project-master schema and listing-filtering logic; the FIN_ASSUMPTIONS table skeleton ([assumptions.md, Week 3](../../archive/Week%203/assumptions.md)).
- Input dictionary listing and describing every input ([input-dictionary.md, Week 3](../../archive/Week%203/input-dictionary.md)).
- Co-authored the **data-flow diagram** Source → Input → Validation → Process → Output, with Phạm Thị Khánh An and Nguyễn Hải Sơn ([data-flow.md](../../archive/Week%203/data-flow.md)).
- Input validation in the Calculate-button handler ([Input Validation & Early Logic Test.md, section 1](../../archive/Week%203/Input%20Validation%20%26%20Early%20Logic%20Test.md)).
- **Early logic test:** designed test cases, calculated them by hand and cross-checked them against the code ([Input Validation & Early Logic Test.md](../../archive/Week%203/Input%20Validation%20%26%20Early%20Logic%20Test.md), later extended in the Week 4 [Sample Calculation & Logic Test.md](../../archive/Week%204/Sample%20Calculation%20%26%20Logic%20Test.md)).
- Declining-balance repayment method, with Phạm Nam Phương and Phạm Thị Khánh An ([financial-logic.md, Week 4](../../archive/Week%204/financial-logic.md)).
- **Two-point safety-margin rule** and the rule that adds closing costs to the minimum-savings check, designed with Nguyễn Minh Tuấn; implemented together with interface text updates and the auto-generated assumptions box (AI-assisted).
- **Source register:** ([sources-register.md, Week 3](../../archive/Week%203/sources-register.md))
  - CFPB Ability-to-Repay reference (qualitative support for the safety-margin idea): [CFPB final rule](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf).
  - State Bank of Vietnam deposit-rate report: [div.gov.vn](https://div.gov.vn/lai-suat-tiet-kiem-tang-trong-tam-kiem-soat-mt-bang-cho-vay-du-kien-tiep-tuc-on-dinh); floating-rate sources behind the 10.5% reference rate (with An): [Thanh Niên](https://thanhnien.vn/nguoi-vay-mua-nha-dang-chiu-lai-suat-bao-nhieu-185260825101722042.htm), [Dân trí](https://dantri.com.vn/kinh-doanh/lai-suat-tha-noi-tren-14nam-ngan-hang-giam-cho-vay-mua-nha-20260823171410442.htm).
  - Three legal citations behind the 2.6% closing costs (registration tax, maintenance fund, notary fee): see 2.1.
  - I read the four problem-evidence sources in full and confirmed the exact figures and links before citing them (with An): [sources-register.md, section 2](../../archive/Week%203/sources-register.md).
- Evidence for this phase: [contribution.md, Week 5](../../archive/Week%205/contribution.md); commit links in [evidence_links.png](../evidence/Duong_Phuong_Anh/evidence_links.png).

### 3.2 BUY and RENT calculation upgrade (Weeks 6–7)

- Down payment net of the 2.6% purchase fees and a 6-month emergency fund; loan = price − down payment (worked example in 2.1).
- Income +5.56%, living cost +3.09% and rent +6% each year.
- Holding costs: service fee and fire insurance (see 2.2).
- Selling cost 1.5% deducted from BUY net worth, including year 0.
- RENT wealth tracked month by month across 4 investment channels, rebalanced every year; RENT safety checked over the whole term.
- Existing debt with a "months left" field; promo packages of 6 / 12 / 18 / 24 months; break-even year rounded up.
- Functions: [`loanCalc`](../../src/index.html#L1580), [`evaluateBuy`](../../src/index.html#L1757), [`evaluateRent`](../../src/index.html#L1976), [`buyRunningCostAt`](../../src/index.html#L1469), [`rentRunningCostAt`](../../src/index.html#L1476), [`stepPortfolio`](../../src/index.html#L1418), [`findBreakEven`](../../src/index.html#L2315), [`getSafetyMarginMinPct`](../../src/index.html#L1746) in [src/index.html](../../src/index.html).

### 3.3 Key assumptions (Weeks 6–7)

- House-price path 20.43% → 8.38%, τ = 3.24 years; rent growth 6%; age cap 70; reference rate 10.5% (details and sources in 2.4).
- Evidence: [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv); [`FIN_ASSUMPTIONS`](../../src/index.html#L1204) table and [`propertyGrowthPctForYear`](../../src/index.html#L1327) in [src/index.html](../../src/index.html); [financial_logic.md](../../docs/financial_logic.md); [assumptions.md](../../docs/assumptions.md); [Code_Cross_Check.csv](../../data/financial_assumptions/Code_Cross_Check.csv).

### 3.4 Integration, interface, documentation and repository (Weeks 6–7 and final build)

- Integration and interface parts: see 2.5.
- Documentation and final test suite: see 2.6.
- Repository structure following the course guide: README, docs/, contribution/, src/, data/, tests/ ([repository](https://github.com/FTU-Legacy-63/G04)).
- Group contribution map and the individual footprint files: [contribution_map.md](../contribution_map.md); root [README.md](../../README.md).

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **Assumptions framework** | FIN_ASSUMPTIONS skeleton, project-master schema, input dictionary | [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv); [assumptions.md](../../docs/assumptions.md); [input-dictionary.md (Week 3)](../../archive/Week%203/input-dictionary.md) | Every assumption in the sheet has a value, a status and a source |
| **Source register** | CFPB, deposit-rate report, floating-rate sources, three legal citations | [data_and_sources.md](../../docs/data_and_sources.md); [sources-register.md (Week 3)](../../archive/Week%203/sources-register.md); source links in section 8 | Open each cited link and compare the figure |
| **Down payment and loan** | Savings − 2.6% fee − emergency fund; loan = price − down payment | [`loanCalc`](../../src/index.html#L1580) in [src/index.html](../../src/index.html); [financial_logic.md](../../docs/financial_logic.md) | Price 5 billion, savings 1.5 billion, living cost 15 million → loan 3.72 billion |
| **Holding and selling costs** | Service fee, fire insurance, 1.5% selling cost | [`buyRunningCostAt`](../../src/index.html#L1469), [`rentRunningCostAt`](../../src/index.html#L1476), [`evaluateBuy`](../../src/index.html#L1757) | Net worth at year 0 is lower than savings by the purchase and selling costs |
| **RENT portfolio** | 4 channels, yearly rebalancing, safety over the whole term | [`stepPortfolio`](../../src/index.html#L1418), [`evaluateRent`](../../src/index.html#L1976) | Change the mix in Step 4: RENT net worth changes, BUY does not |
| **House-price path** | 20.43% → 8.38%, τ = 3.24 | [`propertyGrowthPctForYear`](../../src/index.html#L1327); [Property_Price_Growth.csv](../../data/financial_assumptions/Property_Price_Growth.csv) | First-year growth 20.43% (k = 1); 10-year average 12.66% |
| **Other key assumptions** | Rent 6%, age cap 70 (value and sources), reference rate 10.5% | [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv); [financial_logic.md](../../docs/financial_logic.md); [Reference_Rate.csv](../../data/financial_assumptions/Reference_Rate.csv) | Assumption box in Step 1 shows the same values |
| **Workbook-to-code check** | Compared the assumptions workbook with the code | [Code_Cross_Check.csv](../../data/financial_assumptions/Code_Cross_Check.csv) | 48 parameters compared; no mismatch |
| **Integration** | One offline `index.html` | [src/index.html](../../src/index.html); [evidence_links.png](../evidence/Duong_Phuong_Anh/evidence_links.png) | Open the file without internet and run a full case |
| **V5 interface changes** | Two-line unit cards, spare-money table, "What is varied", cash-flow table, assumptions-box regrouping and source links, summary box | [src/index.html](../../src/index.html); [user_flow.md](../../docs/user_flow.md) | Compare each element with the description in the user flow |
| **Documentation** | Final Plan, change log, limitations | [FinFlow - Final Plan.pdf](../../docs/FinFlow%20-%20Final%20Plan.pdf); [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20%28Midterm%20to%20Final%29.pdf); [revision_summary.md](../../docs/revision_summary.md); [limitations.md](../../docs/limitations.md) | Numbers in these files match the web page and the workbook |
| **Final test suite** | 88 + 28 + 7 = 123 cases, all passed | [FinFlow_Test_Cases_V5.xlsx](../../tests/FinFlow_Test_Cases_V5.xlsx); [testing.md](../../docs/testing.md) | Enter a case's inputs and compare the expected columns |

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
   [`src/index.html`](../../src/index.html), [`data/financial_assumptions/Assumptions_Summary.csv`](../../data/financial_assumptions/Assumptions_Summary.csv), [`docs/`](../../docs/) (Final Plan, change log, `financial_logic.md`, `limitations.md`, `testing.md`), [`tests/`](../../tests/), [`contribution/`](../).
4. **How my output supports the group product:**
   - It gives **Tuấn** the calculation that the Monte Carlo reruns 1,000 times ([`runMonteCarlo`](../../src/index.html#L2187)), and the assumptions around which the scenarios shift ([`SCENARIOS`](../../src/index.html#L2086)).
   - It gives **An and Nam Phương** the structure in which their series become assumptions (CPI, income, VN-Index, gold, LTV).
   - It passes **Sơn's** age-based term ([`calcLoanTerm`](../../src/index.html#L1546)) and prepayment fee through the loan calculation, and uses his relevance engine in Step 3 ([`muaCalc`](../../src/index.html#L2653), [`thueCalc`](../../src/index.html#L2655)).
   - It puts all of these into the one file users open.
5. **Remaining limitation:** see section 7.

---

## 7. Remaining limitations

- **Model scope:** repairs inside the unit (sensitivity only), building depreciation, rental deposit and furnishing costs are not in the main result; the 2% income tax on a sale is not applied; when the whole emergency fund runs out, the shortfall accumulates without interest ([limitations.md](../../docs/limitations.md), #11, #12, #17, #19, #23).
- **Assumptions:** τ rests on the idea that the next 10 years grow like the last 10; rent growth of 6% is a reasoned judgment, not a measurement, because there is no historical rent series; the 10.5% reference rate is extrapolated because the MB document gives no value; "use the older borrower's age" is a group assumption ([limitations.md](../../docs/limitations.md), #5, #10, #16).
- **Maintenance fee:** 2% may not apply to resale units (about 0.56%); the model keeps 2.6% as a conservative level ([limitations.md](../../docs/limitations.md), #26; in the Final Plan this appears only as an unnumbered addendum under section C, and `limitations.md` numbers it #26 for easy reference). Source: [Article 152, Law on Housing 2023](https://hethongphapluat.com/law-no-27-2023-qh15-dated-december-27-2023-on-housing/dieu-152) — the 2% obligation is set for buyers from the investor.
- **Build:** Boom / Downturn on the result screen do not update the budget labels in Step 3; the code still contains an unused Chart.js loader and old comments (for example the comment at `buy_closing_costs_pct` still says "~0.1% notary" while the documents use about 0.06%).

---

## 8. Source and evidence index

### 8.1 External sources used by my parts of the model

| Topic | Source |
| :--- | :--- |
| Purchase fees (2.6%) | [Article 152, Law on Housing 2023](https://hethongphapluat.com/law-no-27-2023-qh15-dated-december-27-2023-on-housing/dieu-152) · [maintenance fee explained](https://thuvienphapluat.vn/phap-luat-nha-dat/nguoi-mua-can-ho-chung-cu-co-bat-buoc-phai-dong-phi-bao-tri-chung-cu-khong-8987.html) · [registration tax](https://thuvienphapluat.vn/phap-luat-nha-dat/toan-bo-19-truong-hop-duoc-mien-le-phi-truoc-ba-nha-dat-2026-14320.html) · [declaration, Decree 373/2025](https://thuvienphapluat.vn/phap-luat-nha-dat/ho-so-khai-le-phi-truoc-ba-nha-dat-moi-nhat-2026-chuan-nghi-dinh-373-2025-nd-cp-14436.html) · [notary fee](https://luatvietnam.vn/hanh-chinh/muc-phi-cong-chung-moi-nhat-570-21497-article.html) |
| Service fee | [Thời báo Tài chính](https://thoibaotaichinhvietnam.vn/gia-dich-vu-quan-ly-van-hanh-chung-cu-tai-ha-noi-tu-700-dong-16500-dongm-thang-175052.html) · [VnExpress](https://vnexpress.net/ha-noi-tiep-tuc-ap-tran-gia-dich-vu-chung-cu-16-500-dong-mot-m2-4877080.html) |
| Fire insurance | [Luật Minh Khuê](https://luatminhkhue.vn/muc-phi-bao-hiem-chay-no-chung-cu-moi-nhat-va-cach-tinh.aspx) · [LSVN](https://lsvn.vn/tu-01-7-chung-cu-nha-o-tap-the-tu-05-tang-tro-len-phai-mua-bao-hiem-chay-no-bat-buoc-a158203.html) |
| In-unit repairs (sensitivity) | [Metrobank](https://www.metrobank.com.ph/articles/learn/home-maintenance-budget) |
| Selling cost and tax | [wiki.batdongsan — broker fee](https://wiki.batdongsan.com.vn/wiki/phi-moi-gioi-nha-dat-109150) · [Thư viện Pháp luật — personal income tax](https://thuvienphapluat.vn/ma-so-thue/phap-luat-thue/ban-nha-o-can-ho-chung-cu-nop-thue-tncn-bao-nhieu-phan-tram-127913-218677.html) · [Báo Pháp luật — only home exemption](https://baophapluat.vn/ban-can-nha-duy-nhat-co-phai-nop-thue-thu-nhap-ca-nhan-khong.html) |
| Safety-margin concept (qualitative) | [CFPB Ability-to-Repay](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf) · [DNSE](https://www.dnse.com.vn/hoc/ty-le-no-tren-thu-nhap) |
| House-price path | [CafeF](https://cafef.vn/nhin-lai-10-nam-bds-ha-noi-gia-can-ho-tang-gan-300-thi-truong-chuan-bi-da-cuc-hoa-18826042315173533.chn) · [Cushman & Wakefield](https://cloud.comm.cushmanwakefield.com/Hanoi_realestate_market_review?) · [World Bank CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2025&locations=VN&start=2016&view=chart) · [World Bank GDP per person](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?end=2025&locations=VN&start=2016) |
| Rent growth and rental yield | [VnExpress](https://vnexpress.net/chat-vat-vi-gia-thue-chung-cu-leo-thang-4927114.html) · [Vietnambiz](https://vietnambiz.vn/loi-suat-cho-thue-chung-cu-dang-giam-dan-202541323742923.htm) · [Global Property Guide](https://www.globalpropertyguide.com/asia/vietnam/rental-yields) |
| Income growth | [NSO Living Standards Survey 2024](https://www.nso.gov.vn/wp-content/uploads/2026/03/Sach-Khao-sat-muc-song-dan-cu-2024.pdf) |
| Age cap 70 | [VIB](https://www.vib.com.vn/vn/cam-nang/vay/vay-bat-dong-san/vay-mua-nha-duoc-bao-nhieu-nam) · [Cake](https://cake.vn/tin-tuc/tai-chinh/vay-the-chap-toi-da-duoc-bao-nhieu-nam) · [Onlinebank – MB](https://onlinebank.com.vn/sp/vay-mua-nha-du-an-mb/) · [Standard Chartered](https://www.sc.com/vn/loans/mortgage/) |
| Reference rate 10.5% | [Thanh Niên](https://thanhnien.vn/nguoi-vay-mua-nha-dang-chiu-lai-suat-bao-nhieu-185260825101722042.htm) · [Dân trí](https://dantri.com.vn/kinh-doanh/lai-suat-tha-noi-tren-14nam-ngan-hang-giam-cho-vay-mua-nha-20260823171410442.htm) |
| Savings rate (SBV report, Week 3 source register) | [div.gov.vn](https://div.gov.vn/lai-suat-tiet-kiem-tang-trong-tam-kiem-soat-mt-bang-cho-vay-du-kien-tiep-tuc-on-dinh) · [trolyluat.vn](https://trolyluat.vn/tien-ich/bieu-do-lai-suat-tiet-kiem) |

### 8.2 Evidence inside the repository

| Evidence | Link |
| :--- | :--- |
| Final product | [src/index.html](../../src/index.html) |
| Financial assumptions (one CSV per sheet) | [data/financial_assumptions/](../../data/financial_assumptions/) |
| Workbook-to-code check | [Code_Cross_Check.csv](../../data/financial_assumptions/Code_Cross_Check.csv) |
| Change log of the assumptions workbook | [Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) |
| MB Bank rate sheet | [mb_bank_rate.jpg](../../data/financial_assumptions/mb_bank_rate.jpg) |
| Listing data | [data/sample_data/](../../data/sample_data/) |
| Documentation | [docs/](../../docs/) |
| Weekly records (Weeks 1–5) | [archive/](../../archive/) |
| Tests | [tests/](../../tests/) |
| Group contribution map | [contribution_map.md](../contribution_map.md) |
| Commit links with a note on what each commit shows | [evidence_links.png](../evidence/Duong_Phuong_Anh/evidence_links.png) |
