# **PROJECT PROPOSAL**

## **1. Problem Direction**

Young households and first-time homebuyers in Hanoi need to decide whether to buy a home or continue leasing. However, the traditional way this decision gets approached often follows the same narrow comparison:

**Look at House Price → Compare with Monthly Rent → Feel Overwhelmed by the Numbers → Postpone the Decision**

Repeatedly relying on this narrow, single-number comparison may leave users afraid of the scale of the numbers involved and unable to see whether their monthly cash flow will actually remain safe over time.

At the same time, simply comparing house price to rent may not provide enough decision value. Users also need clear feedback about which option keeps their monthly cash flow stable, how much safety margin they would have left, and which alternative — buy, rent, or buy-to-let — actually fits their financial capacity.

The project therefore focuses on developing a buy-vs-lease decision-support tool that turns this overwhelming, single-number comparison into a clear, cash-flow-based recommendation the user can act on.

## **2. Target User**

### **Primary Users**

Young, financially independent individuals or couples (25–35 years old) in Hanoi who are considering whether to buy or rent a home in one of five inner districts (Thanh Xuân, Đống Đa, Cầu Giấy, Nam Từ Liêm, Hà Đông).

These users:

* have initial savings of 500 triệu – 1.5 tỷ VNĐ, often from personal savings and/or family support;
* have a mid-to-high household income (30–60 triệu VNĐ/month);
* are comfortable with technology and prefer to research before deciding;
* value work-life balance rather than living solely to repay debt;
* need to evaluate multiple financial variables (income, price, rent, loan terms) simultaneously;
* may feel overwhelmed by the scale of numbers involved in a home-purchase decision.

The product is therefore designed primarily as a **decision-support and cash-flow planning tool**, rather than a general real estate browsing platform.

## **3. User Task**

The core user task is to input their target property and financial profile, and receive a clear decision on whether to buy, rent, or buy-to-let — one that keeps their monthly cash flow stable and safe.

Typical flow:

1. Select target area (district), property type, and size.
2. Choose a specific budget within the suggested price range.
3. Enter income, savings, and monthly living costs.
4. Run the simulation engine.
5. Receive a recommendation (Rent / Buy / Buy + Rent out) with a concrete safety margin.
6. Adjust budget or area to see how the recommendation changes.
7. Use the safety margin figure to plan their actual finances.

The main decision the user should be able to make after each session is:

**"Which option — buy, rent, or buy-to-let — keeps my monthly cash flow safe while still letting me enjoy my life?"**

## **4. Desired User Outcome**

Users should be able to:

* understand whether they can financially afford to buy the property they are considering;
* compare buy vs rent on the same underlying property, not two unrelated options;
* see a concrete monthly safety margin instead of an abstract total cost;
* identify which option keeps them from living in a state of constant debt stress;
* decide with confidence rather than postponing the decision out of fear of the numbers.

The project therefore targets two major outcomes:

**Decision Outcome:**
Users receive a clear, specific recommendation — not just raw numbers — on which housing path fits their finances.

**Confidence Outcome:**
Users feel less overwhelmed by the scale of the numbers and gain a concrete sense of control over their monthly cash flow.

## **5. Product Statement**

**FinFlow** is a buy-vs-lease decision-support web tool for young households and first-time homebuyers in Hanoi, where users input their target property and financial profile and receive a cash-flow-based recommendation — rent, buy, or buy-to-let — along with a concrete monthly safety margin, backed by a simulation engine.

The simulation and market-scenario layer is intended to support the recommendation rather than replace it — it feeds the decision, but the decision itself, not the raw output, is what the user needs.

## **6. Main Output**

The main output is a recommendation that tells users which housing path is financially safe for them, along with the concrete monthly number behind that recommendation.

The result may include:

* suggested price range for the target property;
* equivalent monthly rent for the same property;
* monthly installment (PMT) if bought;
* **Recommendation**: Rent / Buy / Buy + Rent out;
* concrete **Safety Margin** (VNĐ/month) after the chosen option;
* (Phase 2) comparison across 3 market scenarios;
* (Phase 2) % Buy wins / % Rent wins / % bankrupt from Monte Carlo.

The primary output of the product remains **a clear financial decision**, while market-scenario and Monte Carlo analytics act only as supporting evidence behind that decision.

## **7. Product Pattern**

**Select Area/Property → Choose Budget → Enter Financial Profile → Run Simulation → Apply Recommendation Rule → Show Decision + Safety Margin → (Phase 2) Compare Market Scenarios**

## **8. Finance and Banking Relevance**

The project directly involves core personal-finance concepts:

* Time value of money (cash flows occurring at different points in time);
* Mortgage financing (PMT, interest rate, loan term);
* Opportunity cost of capital used for the down payment;
* Investment returns on capital not spent when renting;
* Housing appreciation and rent growth;
* Inflation;
* Long-term wealth accumulation / net worth comparison.

## **9. Feasibility**

The MVP can focus on the Base Case engine, a static reference price table for the 5 target districts, and a rule-based recommendation engine — without needing Market Scenarios, Monte Carlo, or a full dashboard. These advanced layers can be added once the core recommendation loop works end-to-end.

## **10. Revision Notes**

After reviewing the initial concept, the group clarified that:

* the project should center on a clear **recommendation**, not just a raw comparison table;
* the core problem is the fear of losing control of monthly cash flow, not simply "which number is bigger";
* market scenarios and Monte Carlo should act as a **supporting evidence layer** behind the core recommendation engine, not the main user experience;
* "enjoying life" (living-cost margin) needs to be an explicit constraint inside the recommendation logic, not an afterthought;
* the target user has been narrowed from "young households" (Week 1) to a specific demographic/income/location profile (Week 2);
* both the **decision outcome** and the **confidence/control outcome** should eventually be validated with real users.
