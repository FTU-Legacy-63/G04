# Individual Footprint — Phạm Nam Phương

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Phạm Nam Phương** |
| **Student ID** | [add student ID] |
| **Main role** | **Stock and Bank-Loan Data / Workbook Reviewer (gold, VN-Index) / Input Flow and Filters Developer** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `docs/individual/nam-phuong.md`. Links to the repository are relative to this folder.

---

## 1. Role in the project

My work covers three layers of FinFlow:

1. **First concepts and assumptions (Weeks 1–5):** proposed project candidates, researched Vietcombank rates as a cross-check source, and contributed to the first working set of assumptions.
2. **Stock and bank-loan data (Weeks 6–7):** VN-Index returns, bank loan-to-value levels and mortgage rates, and the correction of the gold and VN-Index sheets in the assumptions workbook.
3. **Input flow and filters (Weeks 6–7):** the five-step order (finances first, units later) and the filters of the project step.

---

## 2. Personal footprint in the product

1. **The stock channel and the loan-to-value scenarios.**
   VN-Index from May 2021 to August 2026 (64 monthly prices) gives the stock channel: mean **7.99% a year**, σ **19.30%**, growth over the whole period 6.32%, dividends not included. The bank LTV levels (VCB has both a 70% and a 100% package; BIDV and Vietinbank 100%; MB Van Phuc 80%) are the basis for the scenarios: Boom 80%, Stable 80%, Downturn 70%.

2. **Two corrected series in the assumptions workbook.**
   Gold was corrected from −2.9% to **11.12% a year (σ 14.13%)**: the old formula used a single cell, the new one takes the monthly mean × 12 over Feb 2016–Dec 2024 and leaves out the 2025 jump (+81.5%); 14.89% (with 2025) is kept for a sensitivity row. VN-Index dates were repaired (labels such as "MmmYY" had been read as dates).

3. **An input flow that follows the way people decide.**
   Finances first, units later: a five-step flow in which Step 4 holds the Calculate button, filters for district, beltway zone, ward and building name, and a **"Same filters as Buy"** option that locks the RENT filters to the BUY filters and relaxes them step by step if no rental project matches.

---

## 3. What I actually did

### 3.1. Concepts and cross-check (Weeks 1–5)
- Drafted the initial HTML financial-simulator concept and proposed Candidates 1 and 2 (week 1, recorded in the credit table).
- Researched Vietcombank published rates as an alternative or cross-check source; not adopted in the final numbers.
- Declining-balance repayment formula, with Dương Phương Anh and Phạm Thị Khánh An.
- First working set of assumption values, with An (to be confirmed by the group) ([contribution.md](../../archive/Week%205/contribution.md)).

### 3.2. Stock and bank-loan data (Weeks 6–7)
- **VN-Index** May 2021 – Aug 2026 (64 monthly prices): mean 7.99% a year, σ 19.30%, growth over the period 6.32%.
- **LTV of banks:** VCB has both a 70% and a 100% package; BIDV and Vietinbank 100%; MB Van Phuc 80%. The "5 billion" cell for Agribank is a limit, not an LTV.
- **Mortgage rates for Q3/2026** of BIDV, VCB and Agribank.
- Evidence: [VNIndex_Returns.csv](../../data/financial_assumptions/VNIndex_Returns.csv), [Bank_LTV_Products.csv](../../data/financial_assumptions/Bank_LTV_Products.csv), [Mortgage_Rates_Market.csv](../../data/financial_assumptions/Mortgage_Rates_Market.csv).

### 3.3. Workbook review: gold and VN-Index (Weeks 6–7)
- **Gold (SJC):** −2.9% corrected to 11.12% a year, σ 14.13%; monthly mean × 12 over Feb 2016–Dec 2024; the 2025 jump is excluded; 14.89% kept for sensitivity.
- **VN-Index:** date error repaired; yearly mean 7.99%, σ 19.30%.
- The hand-typed 14.2% with no source and the regression block with a number-format error were marked "not used".
- Evidence: [Gold_Price_SJC.csv](../../data/financial_assumptions/Gold_Price_SJC.csv), [VNIndex_Returns.csv](../../data/financial_assumptions/VNIndex_Returns.csv); the change log ([Change_Log_v6.csv](../../data/financial_assumptions/Change_Log_v6.csv) and the change log PDF) records each corrected cell with its reason.

### 3.4. Five-step flow and filters (Weeks 6–7)
- Five-step flow, finances first; Step 4 "How you invest spare money" holds the Calculate button.
- Filters for district, beltway zone, ward and building name in the project step.
- "Same filters as Buy": when ticked, the RENT filters lock and follow the BUY filters; if no rental project matches, they relax in the order building name, ward, beltway zone, district, and the page says what was relaxed.
- Functions: `readProjectFilter`, `fillFilterSelects`, `syncRentFilters`, `resetSelections` in [src/index.html](../../src/index.html); [user_flow.md](../user_flow.md).

### 3.5. Test of the web demo (after the midterm)
- Tested the web demo after the midterm (recorded in the credit table). Cases tested and bugs found: **[FILE NEEDED: `web_demo_test_log.md` → put in `tests/`]** (Nam Phương's section).

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **VN-Index data** | 64 monthly prices; mean, σ, growth over the period | `VNIndex_Returns.csv` | File shows 7.99%, 19.30%, 6.32% |
| **Bank LTV table** | VCB 70% / 100%, BIDV and Vietinbank 100%, MB 80% | `Bank_LTV_Products.csv`; [data_and_sources.md](../data_and_sources.md) | Scenario buttons use 80 / 80 / 70% |
| **Mortgage rates Q3/2026** | BIDV, VCB, Agribank | `Mortgage_Rates_Market.csv` | Used only as a cross-check of the MB rates |
| **Gold correction** | −2.9% to 11.12%, σ 14.13% | `Gold_Price_SJC.csv`; `Change_Log_v6.csv` | `Gold_Price_SJC.csv` shows 11.12% as the base and 14.89% as sensitivity |
| **VN-Index correction** | Date error; unsourced cell and faulty block marked "not used" | `VNIndex_Returns.csv`; `Change_Log_v6.csv` | Dates read as month and year; the unsourced cell and the regression block are recorded as "not used" in the change log |
| **Five-step flow** | Finances first; Calculate in Step 4 | [src/index.html](../../src/index.html); [user_flow.md](../user_flow.md) | Edit Step 1 after a result: the result is cleared, selected units are kept |
| **Project filters** | District, beltway zone, ward, building name | `readProjectFilter`, `fillFilterSelects` | Filter BUY by district Cau Giay: the project list shrinks (test case S.02 in [testing.md](../testing.md)) |
| **"Same filters as Buy"** | Locks RENT filters to BUY and relaxes if empty | `syncRentFilters`, `resetSelections` | Tick the box with BUY on Cau Giay: RENT jumps to Cau Giay (test case S.04) |

---

## 5. Evidence by project phase

| Phase | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **Weeks 1–5** | Candidates 1 and 2; VCB research; repayment formula; first assumptions | [contribution.md](../../archive/Week%205/contribution.md) | Early concepts and a cross-check source |
| **Weeks 6–7** | VN-Index, LTV and mortgage-rate data; gold and VN-Index correction; five-step flow and filters | `data/financial_assumptions/` (CSV files); [src/index.html](../../src/index.html) | The stock channel, the loan scenarios and the way users move through the tool |
| **Final** | Test of the web demo | [testing.md](../testing.md) | Checking the version the group presents |

---

## 6. Remaining limitations

- **Stocks:** VN-Index covers only about 5 years and excludes dividends ([limitations.md](../limitations.md), #8).
- **Gold:** 11.12% still comes from a strong period for gold; 14.89% runs only in sensitivity (#8); cell C65 of the VN-Index sheet still shows a divide-by-zero error, left on purpose and commented.
- **Loan rates:** rates of BIDV, VCB and Agribank could not be identified as promo or floating rates, so they are used only to compare; some VCB figures (7.5%, 6.2%) cannot serve as the reference rate because they are an average lending rate or an expired package (#5).
- **Filters:** they only narrow the building list and do not limit the similar units suggested later, which can mislead users; when the RENT side relaxes its filters on its own, results may be wider than the filters the user chose.
- **Build:** there is no deployment link yet.
