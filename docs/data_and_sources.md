# Data and Sources

**Product:** FinFlow (FINAL-PRODUCT-V5)
**Files covered:** `data/DATA.xlsx` (apartment listings) and `data/Supporting_data_for_fin_assumptions_v6.xlsx` (financial assumptions)
**Companion documents:** [financial_logic.md](financial_logic.md) (how the numbers are used) · [limitations.md](limitations.md) · [revision_summary.md](revision_summary.md)

This document answers three questions for a reviewer: **where does each number come from, how much should it be trusted, and what was fixed along the way.** Every source name in the tables is a clickable link; the full list is in Section 8.

---

## 1. How to read this document

### 1.1 Reliability grades

Every source below is given one grade (column **g**).

| Grade | Meaning | Examples |
|---|---|---|
| **A** | Primary document or law | MB Bank rate sheet, Housing Law 2023, decrees, Decision 33/2025 |
| **B** | Official statistics, international body or paid database | NSO survey, World Bank, FiinPro, investing.com |
| **C** | Press or industry report (numbers quoted second-hand) | Thanh Nien, VnExpress, CafeF, Cushman & Wakefield, Global Property Guide |
| **D** | Team judgement or extrapolation built on the sources above | Reference rate 10.5%, rent growth 6%, service fee 10,000 VND/m² |

### 1.2 Status

**Decided** means the team fixed the value (date given). **Proposed** means calculated and accepted as a working value but not formally closed. Nothing in the final product is "open".

### 1.3 Two data files

| File | Content | Who uses it |
|---|---|---|
| `DATA.xlsx` | 205 buildings, 756 resale listings for sale, 277 listings for rent | Embedded inside the HTML product, so the page works offline |
| `Supporting_data_for_fin_assumptions_v6.xlsx` | All financial assumptions with sources, raw series, scenarios, a code cross-check | Source of every constant in the HTML code |

The sheet `FIN_ASSUMPTIONS_tong_hop` of the v6 workbook is the master table: one row per assumption with value, standard deviation for Monte Carlo, status and source. All other sheets are raw series or working sheets feeding it.

---

## 2. Apartment listing data

### 2.1 What the data is

| Item | Value |
|---|---|
| Source | batdongsan.com.vn, one link per listing (column `source`) |
| Snapshot date | **9 Sep 2026**. The data does not update itself; prices are asking prices, not closing prices |
| Area | Three districts: Tay Ho, Cau Giay, Ha Dong |
| Property | 2-bedroom apartments, resale market |
| Size bands | Small 45–59 m², Medium 60–79 m², Large 80–100 m² |
| Size | 205 buildings · 756 sale listings · 277 rental listings |
| Typical values | Median area 72 m² (sale) and 80 m² (rent); median rent 15 million VND a month; median price about 85 million VND/m²; median rent about 190,000 VND/m²/month |

### 2.2 Fields

| Table | Fields |
|---|---|
| Building master (`PROJECT_MASTER`) | `project_id`, `project_name`, `district_old`, `ward_old`, `ward_2025`, `beltway_zone` (kept as text), `address_street`, `latitude`, `longitude` |
| Sale listings (`BUY_RAW`) | `listing_id`, `project_id`, location fields, `area_m2`, `size_band`, `bedrooms`, `bathrooms` (may be blank), `total_price_vnd`, `price_m2_vnd`, `source`, `project_name` |
| Rental listings (`RENT_RAW`) | Same, with `rent_monthly_vnd` instead of the price fields |

Removed from the schema: `listing_status`, `status_updated_date`, `collection_date` (the whole file is treated as prices on 9 Sep 2026). Listing IDs start with `BCG`, `BHD`, `BTH` (sale) and `RCG`, `RHD`, `RTH` (rent) for Cau Giay, Ha Dong and Tay Ho.

### 2.3 Where listing data is used

| Use | Detail |
|---|---|
| Choosing the BUY and RENT unit | Steps 2–3 of the user flow |
| Suggesting similar units | Score out of 100: price within tolerance 45, same district 30, same ring road 25 |
| Price anchor | Median price per m² of the target building; if it has fewer than 3 listings, the median of the whole size band |
| Budget labels | Every listing is checked with the same engine as the result page (1,033 units, about 0.3 seconds) |
| Rental yield check | Median yield 2.3% from the 71 buildings that have both sale and rental listings |

### 2.4 Known data quality problems (decision: not corrected)

The team chose **not to clean** the listing file and to keep it frozen at 9 Sep 2026. The problems are known and documented (limitations #1–#3):

| Problem | Size |
|---|---|
| Rows that differ from the original listing link | about 14% |
| Listings that are not 2-bedroom | about 25 |
| "Fund unit" listings (not a normal resale) | about 10 |
| Old listings | 58 |
| Duplicates | some |
| Buildings × size bands with only 1 sale listing | 99 of 235 |
| Buildings × size bands with only 1 rental listing | 47 of 102 |

The repository also keeps a fix for three buildings (HD072–HD074) that shared the same coordinates (`data/project_master_fixes.json`); the product applies it automatically.

---

## 3. Source register for financial assumptions

**g** = reliability grade (Section 1.1).

### 3.1 The loan (MB Bank, Van Phuc branch)

| Number | Value | Source | g | Status |
|---|---|---|---|---|
| Promotional rate | 7.7% (6 months), 8.3% (12), 8.5% (18), 9.0% (24) | Photo of the branch's own rate sheet (`docs/assets/mb-bank-rate-sheet.png`). The sheet has no date; recorded as Q3/2026 | A | Decided |
| Margin after promotion | +1.5% for the first 12 months, then +3.5% | Same sheet | A | Decided |
| Grace period, prepayment fee, maximum LTV, term | 24 months; 1% in years 1–5 and none from year 6; 80%; 360 months | Same sheet. MB's separate 35-year "young people" product ([MB Bank](https://www.mbbank.com.vn/26/37/113/Chi-tiet/mua-nha-dat-tho-cu-chung-cu-du-an-cho-nguoi-tre-2024-6-5-17-58-30)) is not used | A | Decided |
| Rate review every 3 months | 3 months | Same sheet. Recorded, but the model keeps the reference rate constant in each simulated future, so only the margin steps change the rate | A | Decided |
| **Reference rate** | **10.5%** | Not on the sheet. Market floating rates 13–15% ([Thanh Nien, 25 Aug 2026](https://thanhnien.vn/nguoi-vay-mua-nha-dang-chiu-lai-suat-bao-nhieu-185260825101722042.htm)) and 12–14% per SSI, commonly 13–15% ([Dan Tri, 24 Aug 2026](https://dantri.com.vn/kinh-doanh/lai-suat-tha-noi-tren-14nam-ngan-hang-giam-cho-vay-mua-nha-20260823171410442.htm)), minus MB's 3.5% margin = 9.5–11.5%; midpoint used. Cross-checks that are **not** substitutes: VCB average lending rate 7.5% ([VCB notice, June 2026](https://www.vietcombank.com.vn/-/media/Project/VCB-Sites/VCB/Tin-tuc/2026/Vietcombank/Vietcombank_202607/Vietcombank_20260721/20260729_Thong-bao-lai-suat-2026-thang-6.pdf?ts=20260729065709)); State Bank average new-loan rate 6.96%, Nov 2025 ([DIV, 27 Jan 2026](https://div.gov.vn/lai-suat-tiet-kiem-tang-trong-tam-kiem-soat-mt-bang-cho-vay-du-kien-tiep-tuc-on-dinh)) | C → D | Decided 8 Oct |
| Maximum LTV by scenario | Stable 80%, Boom 80%, Downturn 70% | 80%: MB sheet. 70%: [VCB "Nha moi thanh dat"](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Nha-moi-thanh-dat). Other packages offer 100% ([VCB home and land](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Vay-mua-nha-dat), [VCB project apartments](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Vay-mua-nha-du-an), [BIDV](https://bidv.com.vn/vn/ca-nhan/san-pham-dich-vu/vay-ca-nhan/vay-nhu-cau-nha-o), [Vietinbank](https://www.vietinbank.vn/ca-nhan/san-pham-dich-vu/cho-vay/cho-vay-nhan-quyen-su-dung-dat-mua-xay-dung-sua-chua-nha-va-hoac-cong-trinh-xay-dung-30-html)), which the team does not use because all loan terms come from the MB sheet | A | Decided |
| Market range of mortgage rates (context only) | 3.6–9.6% early 2026 | [Vietnambiz](https://vietnambiz.vn/dau-nam-2026-lai-suat-vay-mua-nha-ngan-hang-nao-thap-nhat-2026223101939632.htm); [wiki.batdongsan](https://wiki.batdongsan.com.vn/tin-tuc/lai-suat-vay-mua-nha-ngan-hang-nao-thap-nhat-103041). Q3/2026 bank rate checks kept in the workbook: [BIDV "first home" package](https://bidv.com.vn/bidv/ca-nhan/khuyen-mai/san-pham-vay/bidv-trien-khai-goi-vay-uu-dai-ngoi-nha-dau-tien-danh-cho-khach-hang-ca-nhan), [Agribank](https://www.agribank.com.vn/vn/lai-suat-cho-vay-agribank) (rate type unconfirmed, so not used) | C | Reference |

### 3.2 Age limit

| Number | Value | Source | g | Status |
|---|---|---|---|---|
| Maximum age at payoff | 70 | [VIB](https://www.vib.com.vn/vn/cam-nang/vay/vay-bat-dong-san/vay-mua-nha-duoc-bao-nhieu-nam) (main source: total of age and term not above 65–70), [Cake](https://cake.vn/tin-tuc/tai-chinh/vay-the-chap-toi-da-duoc-bao-nhieu-nam) (60–70), [Onlinebank – MB](https://onlinebank.com.vn/sp/vay-mua-nha-du-an-mb/) (70), [Standard Chartered](https://www.sc.com/vn/loans/mortgage/) (70 for business owners) | C | Decided 8 Oct |
| Sensitivity values | 65 and 75 | [VPBank](https://www.vpbank.com.vn/bi-kip-va-chia-se/retail-story-and-tips/loans-category/kinh-nghiem-vay-ngan-hang-mua-nha) (65), [PVcomBank](https://www.pvcombank.com.vn/tin-tuc/cam-nang-tai-chinh/vay-mua-nha-tra-gop) and [NCB](https://www.ncb-bank.vn/vi/ca-nhan/cho-vay-mua-nha-o-dat-o-xay-dung-sua-chua-nha--p1697) (75) | C | Sensitivity |
| Rule "use the older borrower's age" | n/a | No bank states how co-borrowers are treated; **team assumption** | D | Decided |

### 3.3 Purchase fees, running costs and selling costs

| Number | Value | Source | g | Status |
|---|---|---|---|---|
| Maintenance fund | 2% of price | [Article 152(1), Housing Law 2023](https://hethongphapluat.com/law-no-27-2023-qh15-dated-december-27-2023-on-housing/dieu-152) (effective 1 Aug 2024); explained in [Thuvienphapluat](https://thuvienphapluat.vn/phap-luat-nha-dat/nguoi-mua-can-ho-chung-cu-co-bat-buoc-phai-dong-phi-bao-tri-chung-cu-khong-8987.html) and [Thu vien Nha dat](https://thuviennhadat.vn/phap-ly-nha-dat/nguoi-mua-chung-cu-phai-dong-2-kinh-phi-bao-tri-chung-cu-dung-khong-633637.html). Old Decree 99/2015 expired 1 Aug 2024 and was replaced by Decree 95/2024 ([Decision 99/QD-BXD](https://caselaw.vn/van-ban-phap-luat/506072-quyet-dinh-so-99-qd-bxd-ngay-24-01-2025-cua-bo-truong-bo-xay-dung-cong-bo-danh-muc-van-ban-quy-pham-phap-luat-het-hieu-luc-toan-bo-hoac-mot-phan-thuoc-linh-vuc-quan-ly-nha-nuoc-cua-bo-xay-dung-nam-2024)). **Caveat:** the article obliges buyers from the developer; listings here are resale, so the real fee may be about 0.56% in total. The model keeps 2.6% as a cautious value | A | Decided |
| Registration fee | 0.5% | Article 8(1), Decree 10/2022, amended by Decree 175/2025 ([Thuvienphapluat – exemptions](https://thuvienphapluat.vn/phap-luat-nha-dat/toan-bo-19-truong-hop-duoc-mien-le-phi-truoc-ba-nha-dat-2026-14320.html)); filing under Decree 373/2025 ([Thuvienphapluat – filing](https://thuvienphapluat.vn/phap-luat-nha-dat/ho-so-khai-le-phi-truoc-ba-nha-dat-moi-nhat-2026-chuan-nghi-dinh-373-2025-nd-cp-14436.html)) | A | Decided |
| Notary fee | about 0.05–0.07% (0.06% used) | Circular 257/2016 amended by 111/2017 ([LuatVietnam](https://luatvietnam.vn/hanh-chinh/muc-phi-cong-chung-moi-nhat-570-21497-article.html)) | A | Decided |
| **Total purchase fees** | **2.6%** | Sum of the three rows above (2.56% rounded) | A/D | Decided |
| Service fee | 10,000 VND/m²/month, both sides, grows with CPI | Hanoi range 1,200–16,500 VND/m² for buildings with lifts, Decision 33/2025/QD-UBND ([Vietnam Finance Times](https://thoibaotaichinhvietnam.vn/gia-dich-vu-quan-ly-van-hanh-chung-cu-tai-ha-noi-tu-700-dong-16500-dongm-thang-175052.html); ceiling also in [VnExpress, 22 Apr 2025](https://vnexpress.net/ha-noi-tiep-tuc-ap-tran-gia-dich-vu-chung-cu-16-500-dong-mot-m2-4877080.html)). Real examples in the same VnExpress article: Xuan Mai Complex about 5,000; Mandarin Garden about 14,000; Vinhomes Smart City 13,000–23,000. 10,000 is a team choice between them. Payer: whoever lives in the unit (Housing Law 2023, Circular 05/2024/TT-BXD; [Thuvienphapluat](https://thuvienphapluat.vn/phap-luat-nha-dat/cac-chi-phi-phai-tra-khi-thue-nha-chung-cu-nam-2026-duoc-quy-dinh-ra-sao-14924.html)) | A/C/D | Decided 9 Oct |
| Fire insurance | 0.05% of price a year, BUY only | Decrees 67/2023 and 105/2025 ([Luat Minh Khue](https://luatminhkhue.vn/muc-phi-bao-hiem-chay-no-chung-cu-moi-nhat-va-cach-tinh.aspx), [LSVN](https://lsvn.vn/tu-01-7-chung-cu-nha-o-tap-the-tu-05-tang-tro-len-phai-mua-bao-hiem-chay-no-bat-buoc-a158203.html)). The law uses rebuild cost; price is an upper bound | A | Decided |
| Repairs inside the unit | 0 in base, 1% a year in sensitivity | "1% of home value a year" rule ([Metrobank](https://www.metrobank.com.ph/articles/learn/home-maintenance-budget)), halved because the maintenance fund and service fee already cover shared parts. Weakest source, so excluded from the base case | C/D | Decided 9 Oct |
| Selling cost | 1.5% | Broker fee 1–2% ([wiki.batdongsan](https://wiki.batdongsan.com.vn/wiki/phi-moi-gioi-nha-dat-109150), June 2023). Personal income tax 2% (PIT Law 2025, Art. 14; [Thuvienphapluat](https://thuvienphapluat.vn/ma-so-thue/phap-luat-thue/ban-nha-o-can-ho-chung-cu-nop-thue-tncn-bao-nhieu-phan-tram-127913-218677.html)) is waived for a sole home held 183+ days (Art. 4(2); Decree 253/2026 Art. 19; [Bao Phap Luat](https://baophapluat.vn/ban-can-nha-duy-nhat-co-phai-nop-thue-thu-nhap-ca-nhan-khong.html)), so 0 in base; total 3.5% in sensitivity | A/C | Decided 9 Oct |
| Rental deposit (not modelled) | about 2 months of rent | Market practice ([wiki.batdongsan](https://wiki.batdongsan.com.vn/wiki/tien-coc-thue-nha-la-gi-cdk-109669), [Landager](https://landager.com/vi/property-compliance/vietnam/national/security-deposits)); no law sets an amount | C | Excluded |

**What is *not* in the cost model:** furniture and renovation after purchase, depreciation by building age, and rental deposit. See limitations #11 and #19.

### 3.4 Growth rates

| Number | Value | Source | g | Status |
|---|---|---|---|---|
| Home price: starting growth | 20.43% | CAGR of average Hanoi **primary-market** price 2020–2025: 1,500 → 3,800 USD/m² ([CafeF](https://cafef.vn/nhin-lai-10-nam-bds-ha-noi-gia-can-ho-tang-gan-300-thi-truong-chuan-bi-da-cuc-hoa-18826042315173533.chn); [Cushman & Wakefield](https://cloud.comm.cushmanwakefield.com/Hanoi_realestate_market_review?)) | C | Decided |
| Home price: long-run growth | 8.38% | CPI mean 3.092% ([World Bank – CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2025&locations=VN&start=2016&view=chart)) + real GDP per capita growth mean 5.29% ([World Bank – GDP per capita](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?end=2025&locations=VN&start=2016)), 2016–2025 | B | Decided |
| Home price: cooling speed τ | 3.24 years | **Calibrated by the team** so the next 10 years average 12.66%, the 2016–2025 CAGR of the same series | D | Decided |
| Home price: yearly swing | 14.3% (std of YoY 2017–2025); σ in Monte Carlo 4 points | Same series; divided by √30 because one shift is drawn per future (see financial_logic.md, F3) | D | Decided |
| Home price cross-checks (not used in formulas) | +27% primary Q2/2026 (Savills via [Mekong Asean](https://mekongasean.vn/thi-truong-nha-o-ha-noi-vang-bong-can-ho-so-cap-duoi-70-trieu-dongm2-58416.html)); about 26% a year 2019–2024 (Savills via [HouseNow](https://www.housenow.com.vn/news/gia-chung-cu-ha-noi-tang-hon-200-sau-5-nam-xu-huong-2026-va-khu-vuc-tiem-nang-212)); +21% primary and +13% resale Q2/2026, resale down about 3% on the quarter ([Global Property Guide – price history](https://www.globalpropertyguide.com/asia/vietnam/price-history)); 10–15% a year ([Ministry of Construction via VnExpress, 17 Dec 2025](https://vnexpress.net/bo-xay-dung-gia-nha-o-tang-binh-quan-10-15-moi-nam-4994992.html)); apartment prices up 30–50% in a year ([Thanh Tra](https://thanhtra.com.vn/nha-dat-57A4B2310/gia-chung-cu-ha-noi-tang-3050-chi-sau-mot-nam-hang-loat-du-an-vuot-moc-100-trieu-fd59f5bb8.html)) | CafeF/C&W figures are primary-market; the group's listings are resale, which grows slower | C | Reference |
| Income growth | 5.56% a year, σ 5.71 | Red River Delta monthly income per capita, [NSO Living Standards Survey 2024](https://www.nso.gov.vn/wp-content/uploads/2026/03/Sach-Khao-sat-muc-song-dan-cu-2024.pdf), p. 283; 6 data points 2019–2024; nominal; includes two COVID years. Nationwide check: 4.87% ± 5.68% | B | Decided |
| CPI | 3.09% a year (σ 0.54) | [World Bank – CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2025&locations=VN&start=2016&view=chart), 2016–2025 | B | Proposed |
| Rent growth | 6% a year, σ 1.25; sensitivity 3 / 7 / 10% | No history of apartment rents exists. Evidence conflicts: [VnExpress, 15 Aug 2025](https://vnexpress.net/chat-vat-vi-gia-thue-chung-cu-leo-thang-4927114.html) (10–15% for many apartments, 5–10% for some projects, from Batdongsan and VARS data) and [Vietnambiz, 14 Apr 2025](https://vietnambiz.vn/loi-suat-cho-thue-chung-cu-dang-giam-dan-202541323742923.htm) (rent flat about 13 million over 3 years). 6% sits between income growth (5.56%) and the press range | C/D | Decided 9 Oct |
| Rental yield today | 3.74% ([Global Property Guide – rental yields](https://www.globalpropertyguide.com/asia/vietnam/rental-yields), 2-bedroom Hanoi, Q3 2025); 2.3% (group data, median of 71 buildings) | Used only for the "Reality check" card and for choosing the price curve | C | Proposed |

### 3.5 Investment channels

| Channel | Return | σ | Source | g | Status |
|---|---|---|---|---|---|
| Savings deposits | 6.50% | 0.82 | FiinPro, highest 6–12 month deposit rate at year-end 2016–2026 (11 points). **Upper bound**, since it is the best rate in the market. Cross-check: leading banks 7.0–7.2% ([DIV, 27 Jan 2026](https://div.gov.vn/lai-suat-tiet-kiem-tang-trong-tam-kiem-soat-mt-bang-cho-vay-du-kien-tiep-tuc-on-dinh)); [trolyluat rate chart](https://trolyluat.vn/tien-ich/bieu-do-lai-suat-tiet-kiem) | B | Proposed |
| Government bonds | 4.02% | 1.37 | FiinPro, 10-year yield at year-end 2016–2026 (11 points). The σ is that of the yield level, acceptable if bonds are held to maturity. 5-year bond (3.23% ± 1.64) not used | B | Proposed |
| Gold (SJC) | 11.12% | 14.13 | FiinPro, SJC selling price, monthly, Feb 2016 – Dec 2024 (107 monthly returns, mean × 12). The 2025 jump (+81.5%) is excluded on purpose; the full series (Jan 2016 – Sep 2026) gives 14.89%, kept as a sensitivity. σ is taken from the whole series | B | Decided 7 Oct |
| Stocks | 7.99% | 19.30 | [investing.com – VN-Index](https://vn.investing.com/indices/vn-historical-data), monthly, May 2021 – Aug 2026 (64 prices). CAGR 6.32%. Dividends not included; only about 5 years | B | Proposed |

FiinPro is a paid database with no public link; the workbook records the series name and download date.

### 3.6 Scenarios

All scenario numbers sit in sheet `Kich_ban_do_nhay`, each tied to a year in the data (for example Boom income growth 9.29% = average of 2022–2024; Downturn deposit rate 7.6% = 2022). The table with values and reasons is in [financial_logic.md](financial_logic.md), Part F.

### 3.7 Team conventions (no external source)

| Item | Value | Note |
|---|---|---|
| Safe share of income | 40 / 35 / 30 / 25% by income band | Team proposal. [CFPB](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf) and [DNSE](https://www.dnse.com.vn/hoc/ty-le-no-tren-thu-nhap) debt-to-income ratios were read only as qualitative references (they do not subtract living costs) |
| Comfortable / Tight margin | 5 percentage points | Presentation only |
| Risk labels | Under 10% low, 10–25% moderate, above 25% high | Team convention |
| Emergency fund | 6 months of living cost | User can change it |
| Monte Carlo | 1,000 runs for the page; 500 per sensitivity row; fixed seed 20260909 | Team design |

---

## 4. Corrections made to the raw data

These fixes were made to `Supporting_data_for_fin_assumptions` between 2 and 9 Oct 2026 (full list in [revision_summary.md](revision_summary.md)). Original sheets were kept; fixed cells are highlighted and carry comments.

| # | Sheet | Problem | Fix | Effect |
|---|---|---|---|---|
| 15 | Household income | Growth between survey years 2 years apart was treated as one year | Growth converted to per-year: (B_t ÷ B_t−1)^(1/years) − 1 | Mean 5.56% ± 5.71% (before: 16.3% ± 16.6%) |
| 17 | Gold | Formula read one cell only (−2.9%); monthly figures mixed with yearly model | Added CAGR and yearly mean/σ (monthly × 12, × √12) | CAGR 14.88%, mean 14.89%, σ 14.13% |
| 18 | VN-Index | Month labels were read as dates in the wrong year; 14.2% typed by hand with no source; a regression block with corrupt number format | Dates rebuilt; statistics recomputed; old cells marked "not used" | Mean 7.99%, σ 19.30%, CAGR 6.32% |
| 19 | Loan value | "5 billion" in the Agribank row is a loan limit, not an LTV; MB Van Phuc missing | Moved to a note; added MB Van Phuc row | Boom / base / downturn LTV tied to specific bank packages |
| 20 | Deposit rate | All three columns are the market's highest rates | Added mean/σ for 6–12 months and a note "upper bound" | 6.50% ± 0.82% |
| 21 | Mortgage rate | MB (the base bank) was missing; promotional and floating rates mixed | Added four MB rows and a "rate type" column | 7.7 / 8.3 / 8.5 / 9.0% |
| 22 | Inflation, GDP | Stored as 2.67 in two sheets and 0.056 in the others | All divided by 100 | All rates are fractions |
| 23 | Bonds | σ of the yield level mixed up with σ of return | Added mean/σ for 5 and 10 years with a note | 10-year 4.02% ± 1.37% |
| 24 | Home price | Unit missing; primary versus resale not distinguished | Added "USD/m², primary", YoY growth and σ, secondary cross-checks | σ of YoY 14.3% |
| 26 | Reference rate | Two different unsourced numbers in the repo and the MVP | New sheet `Lai_tham_chieu` with three options; 10.5% chosen on 8 Oct | See 3.1 |
| v6 | VN-Index | Cell C65 held a divide-by-zero from the oldest month | Left blank (statistics only use C2:C64) | No change in numbers |

Source figures that were **checked and rejected** (not used anywhere): a "3.5% first year, 1.5% afterwards" margin (reversed relative to the MB sheet); a 7.5% floating rate and 3.6% step (these were VCB's average lending rate and a spread); a 6.2% 60-month promotion (really an 18-month fixed package, expired 31 Mar 2025); a 3.34% rent growth (a rental yield); a 24.33% home price growth (not found on the cited page); a 50–90% debt-to-income rule (no source).

---

## 5. Check that the code matches the workbook

The workbook has a sheet `Doi_chieu_index_html` that compares the final HTML with the Excel assumptions:

| Check | Count | Mismatches |
|---|---|---|
| Parameters in the code (`FIN_ASSUMPTIONS`, `MC_SETTINGS`, `SCENARIOS`) against the Excel value in the same unit | 48 | **0** |
| Listing statistics recomputed from the data embedded in the HTML against the numbers in the plan (counts, medians, 235 / 99 / 102 / 47 building-size combinations, 71 buildings with both sale and rent, median yield 2.3%) | 13 | **0** |

---

## 6. Where to find each number

| To check | Open |
|---|---|
| Any assumption, its σ, status and source | `FIN_ASSUMPTIONS_tong_hop` |
| Scenario values and their base years | `Kich_ban_do_nhay` |
| Raw series | `Inflation - kan`, `GDP per capita - kan`, `Giá vàng SJC - kan`, `Return Bond (kan)`, `VNIndex return - npp`, `Lãi huy động (kan)`, `Biến động thu nhập household`, `Lạm phát giá mua bds - kan` |
| Loan packages and LTVs | `Loan value - npp`, `Lãi suất vay nhà - npp` |
| Reference rate options | `Lai_tham_chieu` |
| Changes between v4 and v6 | `Nhat_ky_v6` |
| Code versus workbook | `Doi_chieu_index_html` |

---

## 7. What a reader should keep in mind

- The MB rate sheet is a photo of a branch document with no date; the reference rate behind its floating rate is not stated. The 10.5% is an extrapolation and the results are sensitive to it (limitation #5).
- Home price growth uses a primary-market series for a resale-market listing set (limitation #10).
- Several inputs come from short series (income 6 points, stocks about 5 years, rates 11 points), so the Monte Carlo ranges are approximate (limitation #25).
- Savings, gold and stocks returns lean optimistic: the deposit rate is the market's highest, and gold excludes 2025 but still covers a strong decade.

---

## 8. Full link list

Links are taken from the hyperlinks in the Final Plan v5 (56 links). FiinPro (paid database) and the MB rate sheet (a photo in `docs/assets/`) have no public link.

### Loans, rates and banks

| Source | Used for |
|---|---|
| [Thanh Nien, 25 Aug 2026](https://thanhnien.vn/nguoi-vay-mua-nha-dang-chiu-lai-suat-bao-nhieu-185260825101722042.htm) | Floating rate 13–15% (reference rate) |
| [Dan Tri, 24 Aug 2026](https://dantri.com.vn/kinh-doanh/lai-suat-tha-noi-tren-14nam-ngan-hang-giam-cho-vay-mua-nha-20260823171410442.htm) | Floating rate 12–14%, commonly 13–15% |
| [Vietnambiz, early 2026 mortgage rates](https://vietnambiz.vn/dau-nam-2026-lai-suat-vay-mua-nha-ngan-hang-nao-thap-nhat-2026223101939632.htm) | Market range of mortgage rates |
| [wiki.batdongsan, lowest mortgage rates](https://wiki.batdongsan.com.vn/tin-tuc/lai-suat-vay-mua-nha-ngan-hang-nao-thap-nhat-103041) | Market range of mortgage rates |
| [VCB interest-rate notice, June 2026](https://www.vietcombank.com.vn/-/media/Project/VCB-Sites/VCB/Tin-tuc/2026/Vietcombank/Vietcombank_202607/Vietcombank_20260721/20260729_Thong-bao-lai-suat-2026-thang-6.pdf?ts=20260729065709) | Cross-check: average lending rate 7.5% |
| [DIV, 27 Jan 2026](https://div.gov.vn/lai-suat-tiet-kiem-tang-trong-tam-kiem-soat-mt-bang-cho-vay-du-kien-tiep-tuc-on-dinh) | Cross-checks: deposit rates 7.0–7.2%, State Bank lending rate 6.96% |
| [MB Bank "young people" package](https://www.mbbank.com.vn/26/37/113/Chi-tiet/mua-nha-dat-tho-cu-chung-cu-du-an-cho-nguoi-tre-2024-6-5-17-58-30) | Product not used (35 years) |
| [VCB – home and land loan](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Vay-mua-nha-dat) | LTV 100% (not used) |
| [VCB – project apartment loan](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Vay-mua-nha-du-an) | LTV 100% (not used) |
| [VCB – "Nha moi thanh dat"](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Nha-moi-thanh-dat) | LTV 70% (Downturn) |
| [BIDV – housing need loan](https://bidv.com.vn/vn/ca-nhan/san-pham-dich-vu/vay-ca-nhan/vay-nhu-cau-nha-o) | LTV 100% (not used) |
| [Vietinbank – land, house purchase loan](https://www.vietinbank.vn/ca-nhan/san-pham-dich-vu/cho-vay/cho-vay-nhan-quyen-su-dung-dat-mua-xay-dung-sua-chua-nha-va-hoac-cong-trinh-xay-dung-30-html) | LTV 100% (not used) |
| [BIDV – "first home" package](https://bidv.com.vn/bidv/ca-nhan/khuyen-mai/san-pham-vay/bidv-trien-khai-goi-vay-uu-dai-ngoi-nha-dau-tien-danh-cho-khach-hang-ca-nhan) | Q3/2026 rate check (unconfirmed rate type) |
| [Agribank – lending rates](https://www.agribank.com.vn/vn/lai-suat-cho-vay-agribank) | Q3/2026 rate check (unconfirmed rate type) |

### Age limit

| Source | Used for |
|---|---|
| [VIB](https://www.vib.com.vn/vn/cam-nang/vay/vay-bat-dong-san/vay-mua-nha-duoc-bao-nhieu-nam) | Main source for age 70 |
| [Cake](https://cake.vn/tin-tuc/tai-chinh/vay-the-chap-toi-da-duoc-bao-nhieu-nam) | Age 60–70 |
| [Onlinebank – MB](https://onlinebank.com.vn/sp/vay-mua-nha-du-an-mb/) | Age 70 (MB) |
| [Standard Chartered](https://www.sc.com/vn/loans/mortgage/) | Age 70 |
| [VPBank](https://www.vpbank.com.vn/bi-kip-va-chia-se/retail-story-and-tips/loans-category/kinh-nghiem-vay-ngan-hang-mua-nha) | Sensitivity 65 |
| [PVcomBank](https://www.pvcombank.com.vn/tin-tuc/cam-nang-tai-chinh/vay-mua-nha-tra-gop) | Sensitivity 75 |
| [NCB](https://www.ncb-bank.vn/vi/ca-nhan/cho-vay-mua-nha-o-dat-o-xay-dung-sua-chua-nha--p1697) | Sensitivity 75 |

### Purchase fees, running costs, selling costs

| Source | Used for |
|---|---|
| [Article 152, Housing Law 2023](https://hethongphapluat.com/law-no-27-2023-qh15-dated-december-27-2023-on-housing/dieu-152) | Maintenance fund 2% |
| [Thuvienphapluat – maintenance fee](https://thuvienphapluat.vn/phap-luat-nha-dat/nguoi-mua-can-ho-chung-cu-co-bat-buoc-phai-dong-phi-bao-tri-chung-cu-khong-8987.html) | Maintenance fund 2% |
| [Thu vien Nha dat – maintenance fee](https://thuviennhadat.vn/phap-ly-nha-dat/nguoi-mua-chung-cu-phai-dong-2-kinh-phi-bao-tri-chung-cu-dung-khong-633637.html) | Maintenance fund 2% |
| [Decision 99/QD-BXD (list of expired documents)](https://caselaw.vn/van-ban-phap-luat/506072-quyet-dinh-so-99-qd-bxd-ngay-24-01-2025-cua-bo-truong-bo-xay-dung-cong-bo-danh-muc-van-ban-quy-pham-phap-luat-het-hieu-luc-toan-bo-hoac-mot-phan-thuoc-linh-vuc-quan-ly-nha-nuoc-cua-bo-xay-dung-nam-2024) | Decree 99/2015 expired |
| [Thuvienphapluat – registration fee exemptions](https://thuvienphapluat.vn/phap-luat-nha-dat/toan-bo-19-truong-hop-duoc-mien-le-phi-truoc-ba-nha-dat-2026-14320.html) | Registration fee 0.5% |
| [Thuvienphapluat – registration fee filing](https://thuvienphapluat.vn/phap-luat-nha-dat/ho-so-khai-le-phi-truoc-ba-nha-dat-moi-nhat-2026-chuan-nghi-dinh-373-2025-nd-cp-14436.html) | Registration fee, Decree 373/2025 |
| [LuatVietnam – notary fees](https://luatvietnam.vn/hanh-chinh/muc-phi-cong-chung-moi-nhat-570-21497-article.html) | Notary fee |
| [Vietnam Finance Times – service fee range](https://thoibaotaichinhvietnam.vn/gia-dich-vu-quan-ly-van-hanh-chung-cu-tai-ha-noi-tu-700-dong-16500-dongm-thang-175052.html) | Service fee 1,200–16,500 VND/m² |
| [VnExpress, 22 Apr 2025](https://vnexpress.net/ha-noi-tiep-tuc-ap-tran-gia-dich-vu-chung-cu-16-500-dong-mot-m2-4877080.html) | Service fee ceiling, real building examples |
| [Thuvienphapluat – costs of renting an apartment](https://thuvienphapluat.vn/phap-luat-nha-dat/cac-chi-phi-phai-tra-khi-thue-nha-chung-cu-nam-2026-duoc-quy-dinh-ra-sao-14924.html) | Who pays the service fee |
| [Luat Minh Khue](https://luatminhkhue.vn/muc-phi-bao-hiem-chay-no-chung-cu-moi-nhat-va-cach-tinh.aspx) | Fire insurance |
| [LSVN](https://lsvn.vn/tu-01-7-chung-cu-nha-o-tap-the-tu-05-tang-tro-len-phai-mua-bao-hiem-chay-no-bat-buoc-a158203.html) | Compulsory fire insurance |
| [Metrobank – home maintenance budget](https://www.metrobank.com.ph/articles/learn/home-maintenance-budget) | Repairs 1% rule |
| [wiki.batdongsan – brokerage fees](https://wiki.batdongsan.com.vn/wiki/phi-moi-gioi-nha-dat-109150) | Selling cost 1–2% |
| [Thuvienphapluat – income tax on selling a home](https://thuvienphapluat.vn/ma-so-thue/phap-luat-thue/ban-nha-o-can-ho-chung-cu-nop-thue-tncn-bao-nhieu-phan-tram-127913-218677.html) | PIT 2% |
| [Bao Phap Luat – sole home exemption](https://baophapluat.vn/ban-can-nha-duy-nhat-co-phai-nop-thue-thu-nhap-ca-nhan-khong.html) | PIT exemption |
| [wiki.batdongsan – rental deposit](https://wiki.batdongsan.com.vn/wiki/tien-coc-thue-nha-la-gi-cdk-109669) | Deposit 2 months (excluded) |
| [Landager – security deposits](https://landager.com/vi/property-compliance/vietnam/national/security-deposits) | No legal deposit amount |

### Growth rates and markets

| Source | Used for |
|---|---|
| [CafeF – 10 years of Hanoi apartment prices](https://cafef.vn/nhin-lai-10-nam-bds-ha-noi-gia-can-ho-tang-gan-300-thi-truong-chuan-bi-da-cuc-hoa-18826042315173533.chn) | Primary price series 2016–2025 |
| [Cushman & Wakefield – Hanoi market review](https://cloud.comm.cushmanwakefield.com/Hanoi_realestate_market_review?) | Primary price series |
| [Mekong Asean (Savills)](https://mekongasean.vn/thi-truong-nha-o-ha-noi-vang-bong-can-ho-so-cap-duoi-70-trieu-dongm2-58416.html) | Cross-check +27% Q2/2026 |
| [HouseNow (Savills)](https://www.housenow.com.vn/news/gia-chung-cu-ha-noi-tang-hon-200-sau-5-nam-xu-huong-2026-va-khu-vuc-tiem-nang-212) | Cross-check about 26% a year |
| [Global Property Guide – price history](https://www.globalpropertyguide.com/asia/vietnam/price-history) | Cross-check +21% primary, +13% resale |
| [VnExpress – Ministry of Construction, 17 Dec 2025](https://vnexpress.net/bo-xay-dung-gia-nha-o-tang-binh-quan-10-15-moi-nam-4994992.html) | Cross-check 10–15% a year |
| [Thanh Tra – Hanoi apartment prices](https://thanhtra.com.vn/nha-dat-57A4B2310/gia-chung-cu-ha-noi-tang-3050-chi-sau-mot-nam-hang-loat-du-an-vuot-moc-100-trieu-fd59f5bb8.html) | Cross-check (press) |
| [NSO – Living Standards Survey 2024](https://www.nso.gov.vn/wp-content/uploads/2026/03/Sach-Khao-sat-muc-song-dan-cu-2024.pdf) | Income growth |
| [World Bank – CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2025&locations=VN&start=2016&view=chart) | CPI and long-run growth |
| [World Bank – GDP per capita growth](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?end=2025&locations=VN&start=2016) | Long-run growth |
| [VnExpress, 15 Aug 2025](https://vnexpress.net/chat-vat-vi-gia-thue-chung-cu-leo-thang-4927114.html) | Rent growth |
| [Vietnambiz, 14 Apr 2025](https://vietnambiz.vn/loi-suat-cho-thue-chung-cu-dang-giam-dan-202541323742923.htm) | Rent growth, yield falling |
| [Global Property Guide – rental yields](https://www.globalpropertyguide.com/asia/vietnam/rental-yields) | Yield 3.74% |

### Investment channels and conventions

| Source | Used for |
|---|---|
| [trolyluat – savings rate chart](https://trolyluat.vn/tien-ich/bieu-do-lai-suat-tiet-kiem) | Deposit rate cross-check |
| [investing.com – VN-Index history](https://vn.investing.com/indices/vn-historical-data) | Stocks |
| [CFPB – ability-to-repay rule](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf) | Qualitative reference only |
| [DNSE – debt-to-income ratio](https://www.dnse.com.vn/hoc/ty-le-no-tren-thu-nhap) | Qualitative reference only |
