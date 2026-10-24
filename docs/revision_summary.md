# Revision Summary

This document summarizes the main revisions made to FinFlow between the original plan (9 Sep 2026) and the final build **FINAL-PRODUCT-V5** (9 Oct 2026). The full item-by-item record (what changed, how, why, and the source) is in the revision log, *FinFlow – Nhật ký sửa* (batches 1–11). This file only gives the overview.

## 1. Version chain

| Artifact | Versions | Final version used for assessment |
|---|---|---|
| Product (HTML, runs offline) | MVP 27 Sep → MVP steps 1–5 (7 Oct) → FINAL-PRODUCT V1 → V2 → V3 → V4 → V5 | `FinFlow-deep-gradient-2.html` (FINAL-PRODUCT-V5) |
| Plan | Original plan → Final Plan v2 → v3 → v5 | Final Plan v5 |
| Assumptions workbook | Original → v3 → v5 → v6 | `Supporting_data_for_fin_assumptions_v6.xlsx` |
| Test cases | Built from V5 | `FinFlow_Test_Cases_V5.xlsx` |

Where documents disagree, the final product HTML is the reference.

## 2. Timeline of main revisions

| Date | Batch | Main changes | Why |
|---|---|---|---|
| 2 Oct | 1 | **Assumptions workbook corrected** (items 15, 17–24, 26): income growth recomputed per year (5.56% ± 5.71%, was 16.3% ± 16.6%); SJC gold formula fixed (CAGR 14.88%, annual σ 14.13%); VN-Index dates repaired (autodate bug) and re-estimated (mean 7.99%, σ 19.30%); loan-to-value reread (a "5 billion" figure was a limit, not a ratio) giving Boom 100% / Base 80% / Downturn 70%; savings rate 6.50% ± 0.82% marked as an upper bound; MB rates 7.7 / 8.3 / 8.5 / 9.0% added; all percentages stored as fractions; new `Lai_tham_chieu` sheet. **Plan decisions** (B2–B8): same-measure price comparison for rentals, price anchor needs at least 3 units, removed `collection_date`, rental deposit excluded, 2.6% purchase costs deducted from savings, 4 promo-rate options, loan term options, rent growth, house-price path proposal. | Formulas mixed periods and units (for example a 2-year growth treated as 1 year); several figures had no source; some plan rules could never trigger or compared incomparable measures |
| 2 Oct | 2 | Maximum borrower age 75 → 70 (75 kept as sensitivity); a source column added for every financial number in the plan. | The 75 cap had no bank source; every figure needed to be traceable |
| 7 Oct | 3 | **Purchase costs sourced**: 2% maintenance fee (Article 152 of the 2023 Housing Law), 0.5% registration fee, ~0.05–0.07% notarial fee (corrected from ~0.1%). New limitation: the 2% fee may not apply to resale units. Rental deposit documented as market practice and left out of the model; furnishing premium dropped from scope. | Replace unsourced or outdated legal references (an older source cited a law no longer in force) |
| 7 Oct | 4 | **Reference rate** moved from OPEN to PROPOSED at 10.5% (market floating rate 13–15% minus MB margin 3.5%). Figures from a teammate's to-do file were checked against sources and **rejected** where wrong (swapped margin order, average lending rate mistaken for a reference rate, expired promo, rental yield mistaken for rent growth, unsourced DTI tiers). | A reference value is needed for MB's floating rate and the MB document does not state it |
| 7 Oct | 5 | **House-price path (PA2) finalized**: 20.43% decaying to 8.38% with τ = 3.24 years, calibrated so the next 10 years average the last 10 years (12.66%); 30-year growth ×17 instead of ×185 under the old fixed 19%. Loan term by age of the older borrower with age cap 70. Rent growth 6% base with a full justification. Income series set to the Red River Delta (NSO KSMS 2024). Engine fixed as HTML/JS. | The fixed 19% extended the hottest five years to 30 years and made BUY almost always win |
| 7 Oct | 6 | **Scenarios and sensitivity designed**: each scenario mirrors a real period in 2016–2026 data; Boom/Downturn LTV 80%/70%; seven-row sensitivity table; gold base lowered to 11.12% (2016–2024, excluding the 2025 spike); multi-channel investing with four rules; result-page layout; default comparison horizon. | Every number should have a source year; avoid a sensitivity design based on arbitrary ±1σ |
| 7–8 Oct | 7 | **MVP code, steps 1–5**: purchase fee and emergency fund deducted from the down payment; safety check over the whole term in today's money; 4-channel investing with proportional withdrawals; Monte Carlo (1,000 runs, fixed seed) in JavaScript; "safe / not safe" banner with risk sentences; scenarios; sensitivity; SVG chart with P10–P90 band. Rounding error fixed (long-run growth 8.39% → 8.38%). Team decided on 10.5% and age 70 without waiting for MB. | Bring the plan's decisions into running code; the Chart.js chart needed internet access |
| 9 Oct | 8 | **FINAL-PRODUCT V2**: relevance engine rewritten to match plan B2 (six deviations fixed, no more "more than 5 targets" rule, median anchors, luxury-level price measure for rentals, score then distance ordering); Plan B flow (finances first); "Your budget" card; district, beltway, ward and name filters; default horizon 10 years. | V1 left 29/235 BUY and 13/102 RENT combinations with no suggestions and deviated from the plan |
| 9 Oct | 9 | **FINAL-PRODUCT V3** (following expert feedback that assumptions leaned towards BUY): service fee, repairs, fire insurance, 1.5% selling cost deducted from BUY net worth in every year; "Reality check" rental-yield card; unit labels computed directly with the engine; five new sensitivity rows; one-factor correlation option in Monte Carlo (default off). Workbook v5 rows 36–42. | Model ignored the costs of owning and selling, which favoured BUY |
| 9 Oct | 10 | **FINAL-PRODUCT V4** (four open questions decided): rent growth 6% confirmed; "In today's money" toggle added; safety-check banner kept; service fee 10,000 VND/m², insurance 0.05%, selling cost 1.5%, repairs removed from the main result (sensitivity at 1% only). Workbook v6. | Close open questions; repairs had the weakest source |
| 9 Oct | 11 | **FINAL-PRODUCT V5** (interface and presentation only, formulas unchanged): five-step flow with a new Step 4 for spare money and the Calculate button; "Same filters as Buy"; shorter unit cards with "Show details"; grouped assumptions box with source links beside numbers; one-line conclusion bar with Comfortable / Tight / Not safe labels; rewritten "Reality check" and "What is varied". Test suite built from this build (88 calculation, 28 input-error, 7 filter cases). | Make the product easier to read and every number traceable to a source |

## 3. Corrections and reversals worth noting

These show how earlier positions were revised once evidence or feedback required it.

| Earlier position | Revised position | Reason |
|---|---|---|
| Income growth 16.3% ± 16.6% | 5.56% ± 5.71% | Old column divided across rows with unequal year gaps |
| SJC gold return −2.9% | 14.88% CAGR, then 11.12% base | Formula used one cell; later removed the 2025 spike (+81.5%) from the base |
| Loan-to-value Boom 100% | 80% (100% is a different bank's package) | All loan terms come from the MB package, maximum 80% |
| House prices fixed at 19%/year (later 19% → 8.4%, τ = 5) | 20.43% → 8.38%, τ = 3.24 | Endpoints and decay rate each need a source or a calibration target |
| "σ of 4% is too low" for house prices | 4% kept | The model draws one growth rate per path, so the right uncertainty is about 14% ÷ √30 ≈ 2.6% |
| Rent growth 8–10% proposed | 6% base, 3 / 7 / 10% sensitivity | Rent cannot outgrow income for 30 years; sources conflict |
| Age cap 75 | 70 (75 and 65 as sensitivity) | 75 had no support from MB or the cited bank |
| Purchase costs only used to block insufficient savings | Deducted from savings and increase the loan | BUY net worth was inflated by about 2.6% of the price |
| Repairs 0.5%/year in the main result | 0 in the main result, 1% sensitivity row | Weakest source |
| Reference rate "open" | 10.5% (extrapolated, 9.5–11.5% sensitivity) | A value is needed and the MB document does not state one |

Effect of the V3 cost changes on one test profile: BUY safety margin 20.9% → 17.1%, and "BUY richer after 30 years" 90% → 87%.

## 4. Items deliberately not changed

- Data-entry errors in the listing file (mismatches with source links, non-2-bedroom listings, "unit-fund" listings, outdated and duplicate rows): the team decided to freeze the data at 9 Sep 2026. They are documented as Limitation #2.
- Coordinates of three buildings (HD072–HD074) were fixed in the repository's `project_master_fixes.json`, not in the data workbook.
- `beltway_zone` mixed types and the timing of the +1.5% margin were already handled in the code and closed.
- The intentional error cell at VN-Index C65 in the assumptions workbook is kept (it is outside the calculation range and commented).

## 5. Where to find the details

| Need | Location |
|---|---|
| Item-by-item revision record | Revision log, batches 1–11 |
| Current financial logic | [`financial_logic.md`](financial_logic.md) |
| Sources for every number | [`data_and_sources.md`](data_and_sources.md) |
| Remaining limitations | [`limitations.md`](limitations.md) |
| Test evidence | [`testing.md`](testing.md) |
