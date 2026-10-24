# Individual Footprint — Phạm Thị Khánh An

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Phạm Thị Khánh An** |
| **Student ID** | [add student ID] |
| **Main role** | **Macro and Market Data / Workbook Reviewer / Final Layout Co-designer** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `docs/individual/khanh-an.md`. Links to the repository are relative to this folder.

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
   The rate document from MB Bank – Van Phuc branch confirms 6 of the 7 loan values: promo rates for 6 / 12 / 18 / 24 months (7.7 / 8.3 / 8.5 / 9.0%), the margins after the promo period, the 3-month rate adjustment, the 24-month grace period, 80% LTV, the 360-month term and the 1% prepayment fee.

3. **A corrected assumptions workbook.**
   In the review, the income growth was corrected from 16.3% ± 16.6% to **5.56% ± 5.71%** (the old column divided across rows, so growth over 2 years had been counted as 1 year), units were made consistent so no figure is off by a factor of 100, two sheets were added, and all 504 formulas were recalculated with only one intentional error left.

---

## 3. What I actually did

### 3.1. Idea, sources and data flow (Weeks 1–5)
- Drafted the initial Purchase or Lease web-tool concept and proposed Candidate 3 (week 1, recorded in the credit table). The initial rough idea is what the Final Plan was written from.
- Found and saved the MB Bank – Van Phuc branch document.
- Found the VnExpress / Ministry of Construction source for the property-appreciation assumption and the VnExpress source for rent growth.
- With Dương Phương Anh: the State Bank of Vietnam deposit-rate report, the floating-rate sources behind the 10.5% reference rate, and the reading of the four problem-evidence sources (figures and links confirmed before citing).
- Co-authored the **data-flow diagram**, with Phương Anh and Nguyễn Hải Sơn ([data-flow.md](../../archive/Week%203/data-flow.md)), and the declining-balance repayment formula, with Phương Anh and Phạm Nam Phương.

### 3.2. Data collection and returns (Weeks 6–7)

| Series | Period | Result in the final assumptions | Where it is used |
| :--- | :---: | :--- | :--- |
| Inflation (CPI) | 2016–2025 | average 3.09% (σ 0.54%) | growth of living costs; part of the long-run house-price rate |
| GDP per person | 2016–2025 | real growth 5.29% on average | with CPI, the long-run house-price rate 8.38% |
| SJC gold price | 2016–2026 | return and σ of the gold channel (11.12% a year, σ 14.13% in the final version) | gold channel of the investment mix |
| Government bond prices | 2016–2026 | 10-year yield 4.02% ± 1.37% | government-bond channel |
| Deposit rates | 2016–2026 | 6.50% ± 0.82% | savings channel |
| Household income, Red River Delta | 2010–2024 | income growth 5.56% ± 5.71% (final version) | growth of income in every projection |
| Property purchase prices | 2016–2025 | growth (CAGR) 12.66% over 2016–2025; 20.43% over 2020–2025 | start and calibration of the house-price path |

### 3.3. Workbook review (Weeks 6–7)
- Income: 16.3% ± 16.6% corrected to 5.56% ± 5.71% (growth over 2010–2018 had been treated as one year).
- Inflation and GDP converted to fractions (2.67 becomes 0.0267) so that no figure is read 100 times too large.
- Added the sheet of reference rates and the sheet of scenarios.
- Recalculated all 504 formulas; the only error left is the intentional one in cell C65 of the VN-Index sheet.
- Evidence: [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv), [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv), [Assumptions_Summary.csv](../../data/financial_assumptions/Assumptions_Summary.csv), [Reference_Rate.csv](../../data/financial_assumptions/Reference_Rate.csv), [Scenarios_Sensitivity.csv](../../data/financial_assumptions/Scenarios_Sensitivity.csv); the change log ([Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) and [FinFlow - Change log (Midterm to Final).pdf](https://github.com/FTU-Legacy-63/G04/blob/main/docs/FinFlow%20-%20Change%20log%20(Midterm%20to%20Final).pdf) records each corrected cell with its reason.

### 3.4. Layout of the final product (final build)
- Credited with Nguyễn Hải Sơn for the layout design of the final product, built on top of the version made by Dương Phương Anh. The list of layout components is in [Sơn's file](https://github.com/FTU-Legacy-63/G04/blob/main/contribution/individuals/Nguyen_Hai_Son.md), section 3.6. My specific components: **[TO ADD: list the layout components you built, with function or commit]**.

### 3.5. Test of the web demo (after the midterm)
- Tested the web demo after the midterm (recorded in the credit table). Cases tested and bugs found: **[FILE NEEDED: `web_demo_test_log.md` → put in `tests/`]** (An's section).

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **MB Bank document** | Rate document confirming 6 of 7 loan values | [mb_bank_rate.jpg](../../data/financial_assumptions/mb_bank_rate.jpg); [data_and_sources.md](../data_and_sources.md) | Promo rates 7.7 / 8.3 / 8.5 / 9.0% appear in the promo-package choice in Step 1 |
| **Macro and market series** | Inflation, GDP, gold, bonds, deposit rates, income, property prices | [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv), [Gold_Price_SJC.csv](../../data/financial_assumptions/Gold_Price_SJC.csv), [Gov_Bond_Yields.csv](../../data/financial_assumptions/Gov_Bond_Yields.csv), [Deposit_Rates.csv](../../data/financial_assumptions/Deposit_Rates.csv), [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv), [Property_Price_Growth.csv](../../data/financial_assumptions/Property_Price_Growth.csv) | Open each file: the series and the computed statistic match section 3.2 |
| **Long-run house-price rate** | CPI 3.09% + GDP per person 5.29% = 8.38% | [financial_logic.md](https://github.com/FTU-Legacy-63/G04/blob/main/docs/financial_logic.md) | The house-price path ends at 8.38% |
| **Income correction** | 16.3% ± 16.6% to 5.56% ± 5.71% | [Household_Income.csv](../../data/financial_assumptions/Household_Income.csv); [Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) | `Household_Income.csv` shows 5.56% ± 5.71% |
| **Unit consistency** | Percentages stored as fractions | [CPI_Inflation.csv](../../data/financial_assumptions/CPI_Inflation.csv), [GDP_Per_Capita.csv](../../data/financial_assumptions/GDP_Per_Capita.csv) | `CPI_Inflation.csv` stores 0.0267, not 2.67 |
| **Formula check** | 504 formulas recalculated | [Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) | The workbook (v6, exported to these CSV files) was recalculated: only cell C65 of its VN-Index sheet shows an error, left on purpose |
| **Layout co-design** | Final layout with Sơn, on Phương Anh's version | [src/index.html](../../src/index.html); [Sơn's file](https://github.com/FTU-Legacy-63/G04/blob/main/contribution/individuals/Nguyen_Hai_Son.md) | Open the page and compare with the component list |

---

## 5. Evidence by project phase

| Phase | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **Weeks 1–5** | Initial idea; MB document; sources; data-flow diagram | [data-flow.md](../../archive/Week%203/data-flow.md); [contribution.md](../../archive/Week%205/contribution.md) | The starting idea and the loan terms the model uses |
| **Weeks 6–7** | Data collection and returns; workbook review | `data/financial_assumptions/` (CSV files); `Change_Log_v6.csv` | The figures the model runs on, and their correction |
| **Final** | Layout co-design; test of the web demo | [src/index.html](../../src/index.html) | The version the group presents |

---

## 6. Remaining limitations

- **Income:** only 6 yearly observations, including 2 COVID years; it is nominal income per person, so σ is uncertain [limitations.md](https://github.com/FTU-Legacy-63/G04/blob/main/docs/limitations.md), #9).
- **Gold and savings:** 11.12% still comes from a strong period for gold (14.89% runs only in sensitivity); the savings rate is the highest on the market, so it is an upper bound (#8).
- **House prices:** the series is primary-market, while the group's listings are secondary market (#10).
- **Bank terms:** the MB document gives no date and no value for the reference rate, so 10.5% is extrapolated (#5).
