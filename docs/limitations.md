# Known Limitations

This document lists the known limitations of FinFlow (build **FINAL-PRODUCT-V5**), how each one can affect the results, and how the product handles it. Numbers **#1–#26** match section C of *Final Plan v5* and the other documents in this repository (for example, `financial_logic.md` refers to "Limitation #5", "#16" and "#23").

How to read the tables: *Effect* says which way the result may be off. Items marked **leans towards BUY** mean the model is slightly optimistic about buying, so users should read the conclusion together with the sensitivity table.

## 1. Listing data

| # | Limitation | Effect | How it is handled / basis |
|---|---|---|---|
| 1 | Listing data is frozen at 9 Sep 2026 and consists of asking prices, not final sale prices. | Real prices may have changed; asking prices are usually higher than closing prices. | The date is shown in Step 2, Step 3 and "How we check". Team decision. |
| 2 | Data was entered by hand from listings and the team did not correct it: ~14% of rows differ from the source link, ~25 listings are not 2-bedroom, ~10 are "unit-fund" listings, 58 are outdated, and some are duplicates. | Median prices and the similar-unit ranking (B2) may be off for some buildings. | Documented, not corrected (team decision). Checked against the titles of the `source` links in `DATA.xlsx`. |
| 3 | Many buildings have only 1–2 listings (99/235 building × size-band combinations on the BUY side and 47/102 on the RENT side have a single listing). | The price anchor can depend on one asking price. | B2 uses the median; if the target has fewer than 3 units the anchor is the whole size band; if the pool has fewer than 5 units the price criterion is dropped (maximum 55 points). A note is shown in the UI. |
| 4 | RENT suggestions compare the *luxury level of the building* (derived from purchase prices) and use rent per m² only when the building has too few purchase listings (L3). Furnishing status of rental units is not distinguished. | Suggested rentals may differ in rent between units in the same building. | Out of scope (team decision, B2). |
| 10 | House prices use the primary-market series (USD/m²), while the listings are secondary market. | The house-price path may be higher than the secondary market. | PA2 decays towards a long-run rate; sensitivity runs τ = 1 / 3.24 / 6.5 and PA1 (fixed 19%) as an upper bound. |

## 2. Financial assumptions

| # | Limitation | Effect | How it is handled / basis |
|---|---|---|---|
| 5 | The 10.5% reference rate is **extrapolated** from market floating rates; the MB document does not state a value. | BUY results are sensitive to this number. | Team chose 10.5% (8 Oct), with sensitivity 9.5–11.5% and σ = 0.75 percentage points. Sources: Thanh Niên, Dân trí. |
| 6 | σ for the floating rate and for rent growth are estimates with no direct historical series. | The width of the Monte Carlo range is approximate. | Compensated by the sensitivity analysis (B7.1). |
| 8 | Gold: the 11.12% base (Feb 2016–Dec 2024) excludes the 2025 jump (+81.5%) but is still a strong-gold period, and 14.89% runs in sensitivity; the savings rate is the highest on the market; VN-Index covers only ~5 years and excludes dividends. | Investment returns may be inflated, which favours RENT (spare cash is invested). | Gold 14.89% is run in sensitivity. Sources: FiinPro, investing.com. |
| 9 | Income has only n = 6 years, includes 2 COVID years, and is nominal income per person. | σ of income is uncertain. | A sensitivity row tests "income in the first 2 years −1.6%/year". Source: NSO – KSMS 2024. |
| 16 | The age cap of 70 comes from the common range at other banks; the rule "use the older borrower's age" for joint loans is a team assumption. | The maximum loan term for older borrowers may differ from reality. | Sensitivity at 65 / 75. Sources: VIB, Cake, Onlinebank – MB. |
| 18 | Boom / Downturn scenarios are built from periods in the 2016–2026 data; CPI, stocks, gold and holding costs are the same in all three scenarios. | Does not reflect a crisis deeper than anything seen in the last 10 years. | Every scenario number has a source year (sheet `Kich_ban_do_nhay`). |
| 24 | The tiered safety level (40 / 35 / 30 / 25%) creates a "cliff": when real income crosses 35 / 50 / 75 million, the required level drops by 5 points at once. | The safety conclusion can flip when income only just crosses a threshold. | A sensitivity row "smooth safe level" (linear interpolation) is provided. |

## 3. Costs and model scope

| # | Limitation | Effect | How it is handled / basis |
|---|---|---|---|
| 11 | Service fee, fire insurance and selling costs were added. **Still missing:** in-unit repairs (sensitivity only, see #23), depreciation by building age (all units share one price path), and the rental deposit (≈ 30 million VND, costing ~1.8 million VND/year in lost interest). | The missing parts **lean slightly towards BUY**. | Documented. Deposit sources: wiki.batdongsan, Landager. |
| 17 | BUY net worth deducts a 1.5% selling cost (broker) but **not** the 2% personal income tax, assuming a sole home. | If the user owns another home, BUY wealth is higher than reality by about 2% of the house value. | Sensitivity row with a 3.5% selling cost. |
| 19 | Savings are used only for the down payment, the 2.6% purchase costs and the emergency fund; renovation and furnishing costs after purchase are not included. | Real move-in costs are higher than the model; **leans towards BUY**. | Scope decision of the team (7 Oct). |
| 22 | The 10,000 VND/m²/month service fee is a value chosen by the team among press-reported levels, applied to every building, and assumes tenants pay it too. | If the landlord pays the service fee, RENT is cheaper than the model by about 0.8 million VND/month (75 m² unit). | Sensitivity at 16,500 VND/m². Sources: Decision 33/2025/QĐ-UBND; VnExpress 22 Apr 2025. |
| 23 | The main result does **not** include in-unit repair costs (weak source, decided 9 Oct); only a 1%/year-of-price sensitivity runs. | Slight lean towards BUY; for a 6 billion VND unit, 1% repairs cost ~5 million VND more per month and lower "BUY richer" by ~3 points in a test profile. | Sensitivity row "repairs 1%" (source: Metrobank). |
| 26 | The 2% maintenance fee (part of the 2.6% purchase costs) may not apply to resale units: Article 152(1) of the 2023 Housing Law imposes it on buyers and lease-purchasers from the developer; the team's listings are resales, so the real fee may be only ~0.56%. | The down-payment condition may be stricter than reality. | The model keeps 2.6% as a conservative level. *(In Final Plan v5 this item is an unnumbered "Addition"; it is numbered #26 here for easy reference.)* |

## 4. Simulation model and presentation

| # | Limitation | Effect | How it is handled / basis |
|---|---|---|---|
| 7 | By default variables and investment channels are drawn independently (ρ = 0). A one-factor correlation exists but runs only in the ρ = 0.5 sensitivity row; no correlation matrix is estimated from data. | May underestimate BUY tail risk (rates rise while house prices and income fall). | The Downturn scenario acts as a same-direction stress test. |
| 12 | When the emergency fund is exhausted, the shortfall accumulates with no interest; consumer borrowing is not simulated. | Net worth in "ran out of money" runs is slightly higher than reality. | Read together with "% use emergency fund" and "% run out of money". |
| 13 | The CFPB DTI threshold is not equivalent to `safety_margin` because DTI does not subtract living costs. | Qualitative reference only. | Source: CFPB. |
| 20 | The risk labels (below 10% low / 10–25% moderate / above 25% high) and the 0.3 effect threshold used to say "when the risk usually occurs" are team conventions. | Quick-read aid only; the raw percentages are still shown. | Team decision (8 Oct), B9. |
| 21 | Step 3 budget labels are computed with the engine on the Stable scenario and average assumptions; the maximum price on the budget card is for a typical unit (72 m² to buy, 80 m² to rent). | Clicking Boom / Downturn on the result page does not change labels; a "Within budget" unit can still have a high emergency-fund usage rate. | Each unit's own label is still correct because it is computed directly with the engine. |
| 25 | The σ values are estimated from short series over different time windows (sample-size table in B8). | The uncertainty in Monte Carlo is only approximate. | Read Monte Carlo as risk information, not a forecast. |

## 5. Documentation and sources

| # | Limitation | Effect | How it is handled / basis |
|---|---|---|---|
| 14 | The "buy then rent out" branch was dropped (7 Oct). | The product does not compare this option. | **To do:** align the Product Statement / README with this decision. |
| 15 | No source shows that young people use tools to compare BUY and RENT. | Reasoning step by the team, low risk. | Recorded in `data_and_sources.md`. *(Final Plan v5 says "docs/sources.md section 2"; the file in this repository is `data_and_sources.md`.)* |

## Overall direction of the limitations

Most remaining limitations (#11, #17, #19, #22, #23, #26 and part of #8) **lean slightly towards BUY** or inflate investment returns. For this reason the product does not say "you should buy" or "you should rent": the main conclusion is the safety check on average assumptions, Monte Carlo is risk information, and the user decides.

## Limitations beyond the product itself

- Scope: 2-bedroom apartments in Cau Giay, Ha Dong and Tay Ho (the districts in the V5 listing data).
- The data and every financial figure are a snapshot at 9 Sep 2026 and do not update automatically.
- The product supports a decision; it is not personal financial advice.
