# Ownership of Data and Evidence — FinFlow

Most contributor names below come from the team's own project records. A few cells are still `[Fill in name]` — these are genuinely unknown from the material available (mainly reviewer/verifier names, and who specified two of the technical rules). Fill those in before submission.

## Ownership table by evidence item

| Evidence / task | Description | Responsible member | 
|---|---|---|
| Listing data source — original schema | Designed the project-master schema, the listing-filtering logic, and the `FIN_ASSUMPTIONS` table skeleton | Duong Phuong Anh |
| Listing data source — Cau Giay scraping | Found and scraped the Cau Giay listing data actually used in the current MVP | Nguyen Minh Tuan |
| Listing data source — Ha Dong & Tay Ho scraping | Found and scraped listing data for the other 2 districts in the team's full-scope plan; **out of scope for the current Cau-Giay-only MVP**, but real evidence of individual contribution | Nguyen Hai Son |
| Normalizing data into `BUY_LISTINGS`/`RENT_LISTINGS` | Cleaned the raw scraped data into the final listing dataset embedded in `finflow.html` | Duong Phuong Anh |
| Data export to `data/sample-buy.csv` / `data/sample-rent.csv` / `data/project-master.csv` for review | Exported a human-readable sample of the listing data for review outside the code | Duong Phuong Anh |
| Input dictionary (`input-dictionary.md`) | Listing and describing every input | Duong Phuong Anh |
| Source register — MB Bank rate sheet, VnExpress/Ministry of Construction sources | Found and saved the MB Bank – Van Phuc Branch document (confirms 6 of 7 `FIN_ASSUMPTIONS` loan values); found the VnExpress/Ministry of Construction source for the property-appreciation assumption, and the VnExpress source for rent growth | Pham Thi Khanh An |
| Source register — CFPB reference for the safety-margin concept | Added the CFPB Ability-to-Repay reference as qualitative support for the safety-margin idea (not a direct numeric source — see the caveat in `assumptions.md`) | Duong Phuong Anh |
| Source register — SBV deposit-rate report | Found the State Bank of Vietnam average-deposit-rate report supporting `investment_return_pct` = 6% | Pham Thi Khanh An |
| Source register — alternative Vietcombank (VCB) dataset research | Investigated VCB's published rates as an alternative/cross-check source; not adopted in the final MVP numbers | Pham Nam Phuong |
| Source register — floating-rate research and closing-cost legal citations | Found the Dan Tri/SSI and Thanh Nien/Ministry of Construction+VARS-IRE sources behind `interest_rate_float_ref_pct` = 10.5%, and the 3 legal citations (registration tax, maintenance fund, notary fee) behind `buy_closing_costs_pct` = 2.6% | Duong Phuong Anh, Pham Thi Khanh An |
| Verifying the 4 problem-evidence sources (CBRE, VnExpress ×2, VnEconomy/Happiness Saigon survey) | Personally reading each source in full and confirming the exact figures/links before citing them officially | Duong Phuong Anh, Pham Thi Khanh An |
| Assumptions — initial `FIN_ASSUMPTIONS` values (safety-margin tiers) | Proposed the first working set of `FIN_ASSUMPTIONS`, including the income-based safety-margin tiers | Pham Thi Khanh An, Pham Nam Phuong |
| Assumptions — table skeleton | Designed the original `FIN_ASSUMPTIONS` structure | Duong Phuong Anh |
| Data flow (`data-flow.md`) | Drawing and describing the Source→Input→Validation→Process→Output flow | Duong Phuong Anh, Pham Thi Khanh An, Nguyen Hai Son |
| Input validation (in the Calculate-button handler of `finflow.html`) | Implementing the input-checking rules | Duong Phuong Anh |
| Early logic test (`validation-and-early-logic-test.md`) | Designing test cases, calculating by hand, cross-checking against the code | Duong Phuong Anh |
| Core financial logic — declining-balance repayment formula | Documented and/or implemented the declining-balance repayment method | Duong Phuong Anh, Pham Nam Phuong, Pham Thi Khanh An |
| Two-point safety-margin rule (grace period / right after grace period, headline = the worse of the two) | Designed the rule and specified it for implementation | Duong Phuong Anh, Nguyen Minh Tuan |
| Closing-cost addition to the minimum-savings check (`buy_closing_costs_pct`) | Designed the rule (add closing costs to `min_down_payment`, keep `required_loan` cash-financed only) and specified it for implementation | Duong Phuong Anh, Nguyen Minh Tuan |
| Implementing the above rules, UI text/label updates, and the auto-generated assumptions box in `finflow.html` | Coded the changes (AI-assisted, see note below), at the request of the member(s) above | Done with AI assistance (Claude), at the request of Duong Phuong Anh, Nguyen Minh Tuan |
| Step 1–4 UI (HTML/CSS portion of `finflow.html`) | Designing and coding the interface | Duong Phuong Anh, Pham Nam Phuong, Nguyen Minh Tuan |
| Overall repo owner / coordinator | Maintains the repo, coordinates the team's contributions | Duong Phuong Anh |

