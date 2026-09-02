# **SOLUTION STRUCTURE**

## **1. Product Direction**

The product is a buy-vs-lease decision-support web tool for young households and first-time homebuyers in Hanoi, designed to turn an overwhelming multi-variable financial comparison into one clear, cash-flow-based recommendation.

The core purpose is to help users:

* estimate a realistic price range for their target property;
* compare buying vs renting on the same underlying property;
* understand their monthly cash flow under each option;
* receive a clear recommendation with a concrete safety margin;
* (Phase 2) see how that recommendation holds up across different market conditions.

Market-scenario simulation and dashboard analytics are used as a supporting evidence layer rather than the main purpose of the product.

**Scope note:** the product covers **2-bedroom apartments (2PN)** only, across **3 target districts** chosen to represent three distinct price tiers of the Hanoi apartment market:

| District | Price tier |
|---|---|
| Tây Hồ | Premium |
| Cầu Giấy | Average |
| Hà Đông | Low |

## **2. Core User Flow**

**User → Select District/Vành đai Zone/Size → Choose Budget → Enter Financial Profile → Run Simulation Engine → Apply Recommendation Rule → Show Decision + Safety Margin → (Phase 2) Compare Market Scenarios → Continue/Adjust**

The recommendation loop remains the core process, while market-scenario and Monte Carlo layers are added around it to increase confidence in the decision.

## **3. Initial Required Information**

### **Property/Area Information**

* District (3 target districts: Tây Hồ, Cầu Giấy, Hà Đông — representing premium/average/low price tiers)
* **Vành đai zone** (ring-road zone, e.g. within Beltway 2, between Beltway 2–3, between Beltway 3–3.5) — a second location filter alongside district, since price also varies meaningfully by distance from the center within the same district
* Property type: fixed to 2-bedroom apartment (2PN) — no other property type in scope
* Size (m²) — 3 size bands: small (45–59m²), medium (60–79m²), large (80–100m²)
* Reference price/m² by **district × Beltway zone × size band**
* Equivalent rent for the same property profile (same district, Beltway zone, and size band)

### **User Financial Information**

* Monthly household income
* Current savings (→ down payment)
* Fixed monthly living costs

### **Engine/Recommendation Information**

* PMT (monthly installment)
* Recommendation category (Rent / Buy / Buy + Rent out / Not affordable)
* Concrete safety margin (VNĐ/month)

Not every market-scenario or dashboard element needs to appear in the MVP.

## **4. Core Process Type**

The product uses a single-pass input-to-recommendation cycle (Phase 2 adds a repeated simulation cycle for Monte Carlo).

**Property + Financial Input → Base Case Engine → Recommendation Rule → Result (Decision + Safety Margin) → (Phase 2) Market Scenario Engine → Monte Carlo → Dashboard**

## **5. MVP Flow**

The first implementation can demonstrate one complete decision cycle:

1. **Area & Property Selection:** user selects district (Tây Hồ / Cầu Giấy / Hà Đông), Beltway zone, and size band (45–59m² / 60–79m² / 80–100m²). Property type is fixed to 2-room apartment.
2. **Budget Selection:** user picks a specific budget within the suggested Price Range; system looks up equivalent rent for the same district/Beltway zone/size band.
3. **Financial Profile:** user enters income, savings, living costs.
4. **Base Case Simulation:** system calculates PMT, rent cash flow, and invested difference.
5. **Recommendation:** system applies the Income vs Rent/PMT/Living rule and shows Rent / Buy / Buy + Rent out with a safety margin.
6. **Adjust:** user can change budget, district, vành đai zone, or size band to see how the recommendation changes.

## **6. Target Product Direction**

The full product can gradually expand to include:

* Market Scenarios (Boom/Bubble, Stable, Downturn) with locked figures for home-price growth, rent growth, and floating loan rate;
* Monte Carlo simulation (% Buy wins / % Rent wins / % bankrupt);
* Full dashboard (scenario comparison, DTI, break-even year, sensitivity/tornado chart);
* Expansion beyond the 3 initial districts and beyond 2PN apartments (e.g. 1PN, 3PN, landed houses).

Each market scenario can feed into the same recommendation engine to increase user confidence in the result.

## **7. Product Interface**

The current concept can be organized into three main areas:

* **Input**
  District + vành đai zone + size band selection, budget slider, financial profile form.
* **Decision**
  Recommendation card (Rent / Buy / Buy + Rent out) with concrete safety margin.
* **Analytics (Phase 2)**
  Market scenario comparison, Monte Carlo results, DTI, break-even chart, sensitivity/tornado chart.

## **8. MVP Scope**

Recommended first working scope:

* 3 target districts (Tây Hồ – premium, Cầu Giấy – average, Hà Đông – low), each with a static reference price table segmented by vành đai zone and by the 3 size bands;
* Price Range calculation (size band × reference price/m² for the selected district/Beltway zone × market margin);
* Equivalent rent lookup for the same district/Beltway zone/size band;
* Base case engine (PMT, rent cash flow, invested difference);
* Rule-based recommendation engine (4 branches: not affordable / rent / buy / buy + rent out);
* Result screen: recommendation + concrete safety margin.

The purpose is to prove the complete chain:

**Property + Financial Input → Base Case Engine → Recommendation → Concrete Safety Margin**

## **9. Target Scope**

After the MVP works, expansion may include:

* 3 market scenarios with locked historical figures;
* Monte Carlo simulation and win/bankrupt percentages;
* full dashboard with DTI, break-even, sensitivity/tornado chart;
* chart rendering via Chart.js;
* expansion of price data beyond the 3 initial districts, additional vành đai zones, and property types beyond 2PN.

## **10. Fallback Scope**

If implementation becomes too complex:

* drop the Beltway filter and use a single averaged reference price per district (accept a wider error margin);
* fewer than 3 districts, or a single averaged reference price per district (accept a wider error margin);
* Base case only, no market scenarios or Monte Carlo;
* no database — static JSON reference table, no backend;
* localStorage instead of a user-account system;
* one simple result screen (recommendation + safety margin only, no charts).

## **11. Out of Scope for MVP**

* real-time data feeds from banks or real estate platforms;
* user login/account system;
* formal credit/mortgage advisory;
* Market Scenarios and Monte Carlo simulation;
* full dashboard and sensitivity/tornado analysis;
* automated data crawling (manual/static update only);
* property types other than 2PN apartments;
* districts other than Tây Hồ, Cầu Giấy, Hà Đông.

## **12. Initial Rule Hypothesis**

The product is currently based on two hypotheses:

### **Cash-Flow Safety Hypothesis**

Users may struggle to judge whether buying is financially safe because they compare house price and rent directly, without seeing the actual monthly cash-flow impact and remaining living-cost margin.

The recommendation engine should therefore explicitly compare Income against Rent, PMT, and Living cost — not just compare house price to rent.

### **Decision-Clarity Hypothesis**

A single concrete recommendation (Rent / Buy / Buy + Rent out) with a stated safety margin may provide more decision value than raw comparison numbers alone.

The system should therefore use user input to generate:

* a clear recommendation category;
* a concrete safety margin figure (VNĐ/month);
* (Phase 2) supporting evidence from market scenarios and Monte Carlo.

These hypotheses still need to be validated through user observation and testing in Week 3.

## **13. Responsibility by Output**

### **Dương Phương Anh — Coordinator + Idea Web**

**Output:** Product flow, locked scenario numbers, locked recommendation thresholds

* write the detailed 5-step user flow (District/Beltway/Size → Budget → Financial Profile → Run Simulation → Result);
* lock the numbers for the 3 market scenarios (Boom/Stable/Downturn — each with 3 figures: % home-price growth/year, % rent growth/year, % loan interest rate) — this happens after Data delivers raw historical figures, not in parallel;
* lock the recommendation thresholds as a clear if/else table with worked examples, so Finance/Backend can code it directly without guessing intent;
* manage overall progress and timeline.

### **Phạm Thị Khánh An — Data**

**Output:** Price, rent, and macro reference data

* collect buy/rent prices for the 3 target districts (Tây Hồ, Cầu Giấy, Hà Đông), segmented by Beltway zone and by size band (45–59m² / 60–79m² / 80–100m²), for 2-bedroom apartments only;
* collect historical bank loan interest rates, historical rent inflation by year, and reference yields for investment channels (savings/gold/stocks) — mandatory input for Coordinator's scenario numbers and Finance's dual-investment calculation;
* deliver raw figures first, even in rough form, before Coordinator locks scenario numbers — the critical dependency for this week.

### **Nguyễn Hải Sơn — Finance**

**Output:** Full formula set (PMT, DTI, cash flow, dual-investment, net worth)

* PMT / monthly installment;
* debt-to-income ratio;
* remaining cash flow after housing cost (Buy vs Rent);
* dual-investment value if Renting (investing the price difference);
* net worth at end of period for both options;
* apply Coordinator's recommendation thresholds into the actual formulas.

### **Phạm Nam Phương — Frontend**

**Output:** User Interface + Chart Rendering

* design (mockup) and build the UI (HTML/CSS): district/vành đai/size filter controls, budget slider, results display area;
* own chart rendering (Chart.js) — Backend only needs to return correctly formatted data arrays, Frontend calls Chart.js to render them;
* flag explicitly to Backend if unable to code HTML/CSS, so responsibility is covered and not assumed.

### **Nguyễn Minh Tuấn — Backend**

**Output:** Working Engine + Integrated Web App

* implement Finance's formulas as working JavaScript functions;
* build Monte Carlo (randomize interest rate/home price around Coordinator's 3 scenarios, run several hundred iterations, compute % Buy wins / % Rent wins / % bankrupt);
* integrate Frontend + Finance formulas + Monte Carlo into one working web app, test end-to-end.
