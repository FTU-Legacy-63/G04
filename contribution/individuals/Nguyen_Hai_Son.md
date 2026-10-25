# Individual Footprint — Nguyễn Hải Sơn

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Nguyễn Hải Sơn** |
| **Student ID** | **2413380043** |
| **Main role** | **Relevance Engine & Loan Logic Developer / Final UI, Slides and Report Designer** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `contribution/individuals/Nguyen_Hai_Son.md`. Links to the repository are relative to this folder. The two final deliverables I designed (group report and slide deck) are attached in ([evidence/](https://github.com/FTU-Legacy-63/G04/tree/main/contribution/evidence/Nguyen_Hai_Son)).

---

## 1. Role in the project

My work covers three layers of FinFlow, from the data that goes in to what the audience finally sees:

1. **Data and problem framing (Weeks 1–5):** identified the key financial factors and pain points of the buy-versus-rent decision, collected the Ha Dong and Tay Ho listing data, and co-authored the data-flow diagram.
2. **Product logic (Weeks 6–7):** built the **relevance engine** that suggests comparable units on both the BUY and RENT sides, the **budget card and budget labels**, the **loan term by borrower age**, and the **prepayment-fee rule** that the loan calculation uses.
3. **Presentation layer (final build and submission):** designed the final user interface (charts, conclusion block, reality check, assumption box), co-designed with Phạm Thị Khánh An the *deep gradient* version, tested the final web page, and designed the group's **slide deck** and **written report**.

---

## 2. Personal footprint in the product

The three contributions that best show my individual mark on FinFlow:

1. **One relevance engine, run twice — for BUY and for RENT.**
   Most buildings in our data have only one or two listings, so a user who picks a single unit has nothing to compare it with. I built an engine that scores every 2-bedroom unit in the same size band against the user's target:

   $$\text{Score} = 45 \cdot \mathbb{1}[\text{price within tolerance}] + 30 \cdot \mathbb{1}[\text{same old district}] + 25 \cdot \mathbb{1}[\text{same beltway zone}]$$

   Units are grouped into tiers (HIGH 100, MEDIUM 55–75, LOW 25–45, WARNING 0) and, among units with the same score, ranked by Haversine distance to the target. The size band is a parameter, so the same code runs independently for the BUY unit and the RENT unit. The 45 / 30 / 25 scoring table was fixed in my first build and is still unchanged in the final product.

2. **A loan term that follows the borrower's age.**
   The original model used a fixed 360-month term for everybody. I replaced it with a rule that depends on the older borrower:

   $$\text{Term}_{\max} = \min\big((70 - \text{age}_{\text{older}}) \times 12,\; 360\big) \text{ months}$$

   A borrower aged 70 or more, or a term that is not longer than the 24-month grace period, gets **"No loan available"**. I also wrote the rule for the **1% prepayment fee in years 1–5** and connected it to the loan calculation, so BUY net worth is reduced by the fee that would be paid if the loan were settled early. (The down payment, purchase fees and net-worth formulas in the same function are Dương Phương Anh's; the value 70 and its sources are also hers.)

3. **Turning the model into something people can read and present.**
   I designed the result screen (SVG net-worth chart with the P10–P90 band, conclusion block with *Comfortable / Tight / Not safe*, reality check, assumption box with source links), then carried the same story into a 10-slide walkthrough deck and a 22-page report. The slides and the report use **the same demo household and the same numbers** as the web page (Hanoi Paragon 62 m², 4.15 billion VND vs 17T9 75 m², 14.5 million VND/month), so the audience can check every figure on screen.

---

## 3. What I actually did

### 3.1. Problem framing and data (Weeks 1–5)
- Week 1: identified the key financial factors and potential pain points of buy-versus-rent ([Week 1 README](../../archive/Week%201/README.md), section 2).
- Week 2: assigned the **Finance** role in the solution structure (formula set: monthly payment, debt-to-income, cash flow after housing cost, net worth) ([SOLUTION STRUCTURE.md](../../archive/Week%202/SOLUTION%20STRUCTURE.md)).
- Weeks 3–5: found and scraped listing data for **Ha Dong and Tay Ho**. The MVP then covered Cau Giay only (Cau Giay data: Nguyễn Minh Tuấn), so this data was outside the MVP scope, but it was later part of the final three-district dataset (205 buildings, 756 sale and 277 rent listings) ([contribution.md](../../archive/Week%205/contribution.md), [MIDTERM verification](../../MIDTERM%20-%20Project%20Readiness%20%26%20Contribution%20Verification.md), section B).
- Co-authored the **data-flow diagram** Source → Input → Validation → Process → Output, with Dương Phương Anh and Phạm Thị Khánh An ([data-flow.md](../../archive/Week%203/data-flow.md)).

### 3.2. Relevance engine — first build (Week 6)
- **Hard filter:** exactly 2 bedrooms and the same size band (Small 45–59 m², Medium 60–79 m², Large 80–100 m²).
- **Scoring:** price within tolerance 45 points (±5% Small, ±8% Medium, ±10% Large), same old district 30, same beltway zone 25.
- **Ranking:** by score, then by Haversine distance among units with the same score.
- **Small-pool rule:** if fewer than 5 units are available, the price criterion is dropped (maximum score 55).
- **Reason lines:** each card lists exactly which criteria matched or failed.
- **Size band as a parameter:** the engine runs twice, independently, for BUY and for RENT.
- Functions: `muaCalc`, `thueCalc`, `runRelevanceEngine` in [src/index.html](../../src/index.html).

### 3.3. Relevance engine revision, budget card and budget labels (Week 7)
- Removed the rule "if the target has more than 5 units, show no suggestions".
- Price anchor = **median** price per m²: the target's units if there are at least 3, otherwise the whole size band; pool under 5 units → price criterion dropped.
- RENT side compares the **luxury level of the building** (derived from sale prices, levels L1/L2); buildings without enough sale listings fall back to rent per m² (L3) — `segmentFor`.
- Display: all HIGH + up to 8 MEDIUM, topped up with LOW when fewer than 5 units are shown; **"Load more"** adds 10 units, on both sides — `selectDisplayed`.
- **"Your budget"** card (maximum price to buy and maximum rent) and four labels per unit: *Within budget / Payment too tight / Not enough savings / No loan available* — `computeBudget`, `budgetLabelFor`, `buildBudgetCardHTML`. (In V5 Dương Phương Anh shortened the wording of the card; the logic is unchanged.)
- Example: a household earning 30 + 20 million VND/month with 1.5 billion VND savings sees **22 sale units** labelled *Within budget*.

### 3.4. Loan term by age and prepayment fee (Week 7)
- `calcLoanTerm`: takes both borrowers' ages and the bank maximum; the term became a parameter passed into the loan instead of a constant.
- Results for the older borrower: 30 → 360 months; 45 → 300; 50 → 240; 60 → 120; 68 → blocked (24 months equals the grace period); 70 or more → not eligible [[financial_logic.md, B3]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/financial_logic.md).
- `getPrepaymentFeePct`: the 1% fee in years 1–5 (free from year 6). The loan calculation (`loanCalc`, Dương Phương Anh) takes the age-based term as a parameter, and the fee on the remaining balance is deducted from BUY net worth.

### 3.5. Final user interface (final build)
- **SVG net-worth chart** (no internet needed) with the P50 line and the P10–P90 band — `drawNwSvg` (it replaced the earlier Chart.js chart of the first dashboard by Nguyễn Minh Tuấn).
- Buttons for the comparison point (10 / 20 years / end of loan) and **Nominal / In today's money** — `moneyFactor`.
- **Conclusion block** with *Comfortable / Tight / Not safe* for each side — `buildConclusionHTML` (built on Tuấn's first dashboard; the right-column summary box and the scroll after Calculate were added by Dương Phương Anh in V5).
- **Reality check** card comparing the pair's rental yield with 2.3% (our data) and 3.74% (Global Property Guide) — `buildYieldCheckHTML`.
- **Assumption box** with source links — `renderLoanAssumptionsBox` (first build; Dương Phương Anh regrouped it into five groups with the shared list of source links in V5).
- The district, beltway, ward and building-name filters and the "Same filters as Buy" option are Phạm Nam Phương's.

### 3.6. Deep gradient interface (with Phạm Thị Khánh An) and final testing
- New colour scheme (deep teal with gradients) and font pair Fraunces (headings) / DM Sans (body), tabular figures for numbers.
- Four **sliders** for the investment mix; the Stocks slider is locked to 100 − (the other three), with a stacked bar showing the shares — `.mix-slider`, `.mix-bar`.
- Result screen split into **3 tabs**: Overview (reality check, net-worth chart), Risk simulation (Monte Carlo, sensitivity), Cost details (BUY and RENT cards) — `tabify`.
- Progress bars for Monte Carlo and the sensitivity table; large Boom / Stable / Downturn buttons — `.mc-load`, `.scenario-btn`.
- Khánh An's specific layout components: **[CONFIRM with Khánh An: list them, so this section and her file match]**.
- Tested the final page: fixed a text that had the same colour as its background; after the fix, no JavaScript errors and no horizontal overflow at 390 px (phone) and 768 px (tablet) widths.

### 3.7. Group slide deck
- Designed a **10-slide walkthrough** that follows the 5 steps of the web page, so the audience sees the product used live on one demo household.
- Built on the group's Canva template (green / beige, Poppins), with screenshots captured from the deep gradient web page; wrote a script for every slide and a Vietnamese explanation so each member knows what their slide does.
- Demo household: ages 32/30, income 35 + 25 million VND, savings 2.5 billion VND; result: both options pass, BUY is *Tight* in month 25 (23.0 million VND left vs a safe level of 20.1 million), and BUY ends richer in 97% of 1,000 simulated futures.
- File: [[Slide FinFlow G04 EN deep gradient 24-10-26 12h50.pptx]](https://github.com/FTU-Legacy-63/G04/blob/main/contribution/evidence/Nguyen_Hai_Son/Slide%20FinFlow%20G04%20EN%2023-10-26%2023h15.pptx.pdf).

### 3.8. Group report
- Designed and wrote the **English essay report** consistent with the final web page: Abstract; 1 Introduction (background, pain points, target users, objectives); 2 Data; 3 Product design and user flow; 4 Methodology (4.1–4.9); 5 Worked example; 6 Limitations; 7 Conclusion; References; Appendix A (base-case assumptions).
- Cover page in the university format (logo, class NHA408E, Group 04, instructor, member list), table of contents, Times New Roman 14, line spacing 1.5, page numbers at the top.
- 22 pages, 9 tables, 7 numbered equations; the worked example uses the same household as the slides.
- File: [[FinFlow Report 24-10-26 17h05.docx]](https://github.com/FTU-Legacy-63/G04/blob/main/contribution/evidence/Nguyen_Hai_Son/Group_report.docx).

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **Listing data** | Ha Dong and Tay Ho listings (2 of the 3 districts) | [contribution.md](../../archive/Week%205/contribution.md), [MIDTERM verification](../../MIDTERM%20-%20Project%20Readiness%20%26%20Contribution%20Verification.md) | In Step 2, filter by district Ha Dong or Tay Ho: the projects and units appear |
| **Data flow** | Source → Input → Validation → Process → Output (with Phương Anh, An) | [[data-flow.md]](https://github.com/FTU-Legacy-63/G04/blob/main/archive/Week%203/data-flow.md) | Read the diagram and its description |
| **Relevance engine** | Hard filter, 45 / 30 / 25 scoring, tiers, Haversine ranking, small-pool rule, median anchor, L1/L2/L3 for RENT, display rule, "Load more" | [src/index.html](../../src/index.html): `muaCalc`, `thueCalc`, `runRelevanceEngine`, `selectDisplayed`, `segmentFor`; [[user_flow.md, Step 3]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/user_flow.md) | Pick a target in Step 2: scores never rise down the list, each card shows the matched criteria |
| **Budget card and labels** | Max price / max rent; 4 labels per unit | `computeBudget`, `budgetLabelFor`, `buildBudgetCardHTML` | Profile 30 + 20 million, savings 1.5 billion → 22 sale units *Within budget* |
| **Loan term by age** | $\min((70-\text{age})\times 12, 360)$, blocks at age ≥ 70 or term ≤ 24 months | `calcLoanTerm`; [[financial_logic.md, B3]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/financial_logic.md) | Older borrower 45 → 300 months; 68 → "No loan available" |
| **Prepayment fee** | 1% in years 1–5, free from year 6, deducted from BUY net worth | `getPrepaymentFeePct` (used inside `loanCalc`) | Cost details tab: e.g. 16.5 million VND at month 60 for the demo loan |
| **Final UI** | SVG chart, N buttons, today's money, conclusion block, reality check, assumption box (first build) | `drawNwSvg`, `moneyFactor`, `buildConclusionHTML`, `buildYieldCheckHTML`, `renderLoanAssumptionsBox` | Press Calculate and read the result screen |
| **Deep gradient UI** | Colours, fonts, sliders, 3 tabs, progress bars, scenario buttons (with Khánh An) | `tabify`, `.mix-slider`, `.mc-load`, `.scenario-btn` in [src/index.html](../../src/index.html) | Open the page on desktop, 768 px and 390 px widths |
| **Slide deck** | 10-slide walkthrough of the 5 steps, script per slide | [[Slide FinFlow G04 EN deep gradient 24-10-26 12h50.pptx]](https://github.com/FTU-Legacy-63/G04/blob/main/contribution/evidence/Nguyen_Hai_Son/Slide%20FinFlow%20G04%20EN%2023-10-26%2023h15.pptx.pdf) | Numbers on slides match the web page for the demo household |
| **Report** | Full report design, cover, table of contents, formatting | [[FinFlow Report 24-10-26 17h05.docx]](https://github.com/FTU-Legacy-63/G04/blob/main/contribution/evidence/Nguyen_Hai_Son/Group_report.docx) | Section 5 reproduces the slide demo household |

---

## 5. Evidence by project week

| Week | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **W1** | Son identified key financial factors and pain points of buy vs rent. | [Week 1 README](../../archive/Week%201/README.md), section 2 | Helped define the real problem the product solves. |
| **W2** | Son assigned the Finance role (formula set) in the solution structure. | [SOLUTION STRUCTURE.md](../../archive/Week%202/SOLUTION%20STRUCTURE.md) | Responsibility for the financial formulas from the planning stage. |
| **W3** | Son co-authored the data-flow diagram. | [data-flow.md](../../archive/Week%203/data-flow.md) | Shared the design of how data moves through the tool. |
| **W4** | No separate individual entry in the Week 4 files. | — | — |
| **W5** | Son found and scraped Ha Dong and Tay Ho listings; recorded at the midterm verification. | [contribution.md](../../archive/Week%205/contribution.md), [MIDTERM verification](../../MIDTERM%20-%20Project%20Readiness%20%26%20Contribution%20Verification.md) | Data for 2 of the 3 districts of the final product, collected before they were in scope. |
| **W6** | Son built the first relevance engine and its scoring table. | [src/index.html](../../src/index.html): `runRelevanceEngine` | The suggestion step of the product; 45 / 30 / 25 kept to the end. |
| **W7** | Son revised the engine, built the budget card and labels, the age-based loan term and the prepayment-fee rule; designed the final UI. | [src/index.html](../../src/index.html); [[financial_logic.md]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/financial_logic.md); [[user_flow.md]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/user_flow.md) | Core logic of Steps 3 and 5 and the result screen the user reads. |
| **Final** | Son co-designed the deep gradient version with Khánh An, tested the final page, designed the slide deck and the report. | [src/index.html](../../src/index.html); ([evidence/](https://github.com/FTU-Legacy-63/G04/tree/main/contribution/evidence/Nguyen_Hai_Son)) | The version the group presents and submits. |

---

## 6. Remaining limitations and lessons learned

### 6.1. Limitations of my parts
- **Thin data per building:** many buildings have only 1–2 listings (99/235 building × size-band combinations on the BUY side and 47/102 on the RENT side have a single listing), so the price anchor often falls back to the whole size band or the price criterion is dropped ([[limitations.md]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/limitations.md), #3).
- **Rental comparability:** furnishing status is not distinguished, and about 25% of rent listings must be compared by rent per m² instead of building luxury level ([[limitations.md]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/limitations.md), #4).
- **Age cap:** 70 comes from the common range at other banks, and "use the older borrower's age" for joint loans is a team assumption ([[limitations.md]](https://github.com/FTU-Legacy-63/G04/blob/main/docs/limitations.md), #16).
- **Budget labels** are computed under the Stable scenario and for a typical unit (72 m² to buy, 80 m² to rent); pressing Boom / Downturn on the result screen does not update the labels in Step 3.
- **Interface:** the Monte Carlo progress bar is a timed animation, not real progress; fonts load from Google Fonts and fall back without internet; a few faint grey hints still have low contrast; the code still contains an unused Chart.js loader; there is no deployment link yet.
- **Evidence gaps:** the raw Ha Dong / Tay Ho scraping files and the relevance-engine unit tests are not stored in this repository; the data now lives inside [src/index.html](../../src/index.html).

### 6.2. Personal lessons
- **One number, one source of truth:** the slide deck once showed a different unit and price from the script (30 Pham Van Dong vs Hanoi Paragon, 4.2 vs 4.15 billion). Rebuilding the slides from screenshots of the actual web page, and using the same household in the report, removed this class of error.
- **Design for thin data:** a scoring engine looks simple, but most of the work was in the fallback rules (median anchor, small-pool rule, L1/L2/L3) that keep the ranking sensible when a building has only one listing.
- **Presentation is part of the product:** the same model can look unsafe or convincing depending on how the result is shown; labels such as *Tight* and the P10–P90 band help the audience read uncertainty instead of a single verdict.
