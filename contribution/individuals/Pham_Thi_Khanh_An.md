# Individual Footprint — Phạm Thị Khánh An

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Phạm Thị Khánh An** |
| **Student ID** | 2412380003 |
| **Main role** | **Macro and Market Data / Workbook Reviewer / Final Layout Co-designer** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `contribution/individuals/Pham_Thi_Khanh_An.md`. Links to the repository are relative to this folder.

---

## 1. Role in the project

My work covers three layers of FinFlow:

1. **Idea and bank sources (Weeks 1–5):** the initial idea the Final Plan was written from, and the MB Bank document that supplies the loan terms.
2. **Macro and market data (Weeks 6–7):** the series for inflation, GDP, gold, bonds, deposit rates, income and property prices, and the returns computed from them.
3. **Workbook review and layout (Weeks 6–7 and final build):** reviewing and correcting the assumptions workbook, and co-designing the layout of the final product with Sơn, on top of the version made by Dương Phương Anh.

---

## 2. Personal footprint in the product

1. **The data behind the assumptions.**
   Seven series I collected turn into the numbers the model runs on. For example, long-run house-price growth is the sum of two of them:

   $$g_\infty = \text{CPI} + \text{real GDP per person} = 3.09\% + 5.29\% = 8.38\%$$

   Income growth of 5.56% ± 5.71% sets how income grows in every projection, and the 2020–2025 property growth of 20.43% is the starting point of the house-price path.

2. **The MB Bank document.**
   The rate document from MB Bank – Van Phuc branch confirms 7 of the 9 loan parameters of the model: promo rates for 6 / 12 / 18 / 24 months (7.7 / 8.3 / 8.5 / 9.0%), the margins after the promo period, the 3-month rate adjustment, the 24-month grace period, 80% LTV, the 360-month term and the 1% prepayment fee. The two values it does not give are the reference rate (10.5%, extrapolated) and the age limit (70, from other banks).

3. **A reviewed assumptions workbook.**
   In the review, the income growth was corrected from 16.3% ± 16.6% to **5.56% ± 5.71%** (the old column divided across rows, so growth over 2 years had been counted as 1 year), units were made consistent so no figure is off by a factor of 100, two sheets were added, and all 504 formulas were recalculated; the one error found (VN-Index cell C65, whose oldest month has no previous month) was left blank and enters no statistic.

---

## 3. What I actually did

### 3.1. Idea, sources and data flow (Weeks 1–5)
- Drafted the initial Purchase or Lease web-tool concept and proposed Candidate 3 (week 1, recorded in the credit table). The initial rough idea is what the Final Plan was written from.
- Found and saved the MB Bank – Van Phuc branch document.
- Found the VnExpress / Ministry of Construction article (17/12/2025: home prices up 10–15% a year) used as a cross-check for home-price growth (change log, item 30b), and the VnExpress source for rent growth (15/08/2025).
- With Dương Phương Anh: the State Bank of Vietnam deposit-rate report, the floating-rate sources behind the 10.5% reference rate, and the reading of the four problem-evidence sources (figures and links confirmed before citing).
- Co-authored the **data-flow diagram**, with Phương Anh and Nguyễn Hải Sơn ([data-flow.md](../../archive/Week%203/data-flow.md)), and the declining-balance repayment formula, with Phương Anh and Phạm Nam Phương.

### 3.2. Data collection and returns (Weeks 6–7)

| Series | Period | Result in the final assumptions | Where it is used |
| :--- | :---: | :--- | :--- |
| Inflation (CPI) | 2016–2025 | average 3.09% (σ 0.54%) | growth of living costs; part of the long-run house-price rate |
| GDP per person | 2016–2025 | real growth 5.29% on average | with CPI, the long-run house-price rate 8.38% |
| SJC gold price | Jan 2016 – Sep 2026 | yearly mean 14.89%, σ 14.13% for the whole series (sensitivity row); the base value 11.12% uses Feb 2016 – Dec 2024 without the 2025 jump (set in the review, see Phạm Nam Phương's file) | gold channel of the investment mix |
| Government bond prices | 2016–2026 | 10-year yield 4.02% ± 1.37% | government-bond channel |
| Deposit rates | 2016–2026 | 6.50% ± 0.82% | savings channel |
| Household income, Red River Delta | series 2010–2024; the final statistic uses 2019–2024 | income growth 5.56% ± 5.71% | growth of income in every projection |
| Property purchase prices | 2016–2025 | growth (CAGR) 12.66% over 2016–2025; 20.43% over 2020–2025 | start and calibration of the house-price path |

### 3.3. Workbook review (Weeks 6–7)
- Income: 16.3% ± 16.6% corrected to 5.56% ± 5.71% (growth over 2010–2018 had been treated as one year).
- Inflation and GDP converted to fractions (2.67 becomes 0.0267) so that no figure is read 100 times too large.
- Added the sheet of reference rates and the sheet of scenarios (the scenario values in the code, `SCENARIOS`, are Nguyễn Minh Tuấn's; the 10.5% reference rate was chosen with Dương Phương Anh).
- Recalculated all 504 formulas; the only error found, cell C65 of the VN-Index sheet (no previous month for the oldest month), is left blank and is not used by any statistic.
- Evidence: [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv), [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv), [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv), [Reference_Rate.csv](../../data/financial_assumptions/Reference_Rate.csv), [Scenarios_Sensitivity.csv](../../data/financial_assumptions/Scenarios_Sensitivity.csv); the change log ([Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) and [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20%28Midterm%20to%20Final%29.pdf)) records each corrected cell with its reason.

### 3.4. Layout of the final product (final build)
- Credited with Nguyễn Hải Sơn for the layout design of the final product (deep gradient version), built on top of the version made by Dương Phương Anh. The list of layout components is in [Sơn's file](./Nguyen_Hai_Son.md), section 3.6. 

### 3.5. Test of the web demo (after the midterm)
- Tested the web demo after the midterm (recorded in the credit table). Cases tested and bugs found: [web_demo_test_log.md](https://github.com/FTU-Legacy-63/G04/blob/main/testings/web_demo_test_log.docx)

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **MB Bank document** | Rate document confirming 7 of the 9 loan parameters | [mb_bank_rate.jpg](../../data/financial_assumptions/mb_bank_rate.jpg); [data_and_sources.md](../../docs/data_and_sources.md) | Promo rates 7.7 / 8.3 / 8.5 / 9.0% appear in the promo-package choice in Step 1 |
| **Macro and market series** | Inflation, GDP, gold, bonds, deposit rates, income, property prices | [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv), [Gold_Price_SJC.csv](../../data/financial_assumptions/Gold_Price_SJC.csv), [Gov_Bond_Yields.csv](../../data/financial_assumptions/Gov_Bond_Yields.csv), [Deposit_Rates.csv](../../data/financial_assumptions/Deposit_Rates.csv), [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv), [Property_Price_Growth.csv](../../data/financial_assumptions/Property_Price_Growth.csv) | Open each file: the series and the computed statistic match section 3.2 |
| **Long-run house-price rate** | CPI 3.09% + GDP per person 5.29% = 8.38% | [financial_logic.md](../../docs/financial_logic.md) | The house-price path ends at 8.38% |
| **Income correction** | 16.3% ± 16.6% to 5.56% ± 5.71% | [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv); [Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) | `Household_Income.csv` shows 5.56% ± 5.71% |
| **Unit consistency** | Percentages stored as fractions | [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv) | `CPI_Inflation.csv` stores 0.0267, not 2.67 |
| **Formula check** | 504 formulas recalculated | [Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) | The v6 workbook (exported to these CSV files) was recalculated; the only error found, cell C65 of its VN-Index sheet, is left blank and is not used by any statistic |
| **Layout co-design** | Final layout with Sơn, on Phương Anh's version | [src/index.html](../../src/index.html); [Sơn's file](./Nguyen_Hai_Son.md) | Open the page and compare with the component list |

---

## 5. Evidence by project phase

| Phase | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **Weeks 1–5** | Initial idea; MB document; sources; data-flow diagram | [data-flow.md](../../archive/Week%203/data-flow.md); [contribution.md](../../archive/Week%205/contribution.md) | The starting idea and the loan terms the model uses |
| **Weeks 6–7** | Data collection and returns; workbook review | [data/financial_assumptions/](../../data/financial_assumptions/) (CSV files); [Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv); [FinFlow - Change log (Midterm to Final).pdf](../../docs/FinFlow%20-%20Change%20log%20%28Midterm%20to%20Final%29.pdf) | The figures the model runs on, and their correction |
| **Final** | Layout co-design; test of the web demo | [src/index.html](../../src/index.html) | The version the group presents |

---

## 6. Remaining limitations

- **Income:** only 6 yearly observations, including 2 COVID years; it is nominal income per person, so σ is uncertain (see [limitations.md](../../docs/limitations.md), #9).
- **Gold and savings:** 11.12% still comes from a strong period for gold (14.89% runs only in sensitivity); the savings rate is the highest on the market, so it is an upper bound (#8).
- **House prices:** the series is primary-market, while the group's listings are secondary market (#10).
- **Bank terms:** the MB document gives no date and no value for the reference rate, so 10.5% is extrapolated (#5).
