# Individual Footprint — Nguyễn Minh Tuấn

## Personal information

| Item | Details |
| :--- | :--- |
| **Full name** | **Nguyễn Minh Tuấn** |
| **Student ID** | [add student ID] |
| **Main role** | **Cau Giay Data / Monte Carlo, Dashboard, Scenario and Sensitivity Developer** |
| **Project** | **FinFlow — Buy vs Rent** |
| **Course** | Information Technology Applications in Finance and Banking (NHA408E) |
| **Group** | Group 04 (G04) |
| **Instructor** | Assoc. Prof., Dr. Phan Tran Trung Dung |

> **Where this file sits:** `docs/individual/tuan.md`. Links to the repository are relative to this folder.

---

## 1. Role in the project

My work covers three layers of FinFlow:

1. **Data (Weeks 1–5):** compared the initial problem candidates, then found, scraped and cleaned the Cau Giay listings used in the MVP.
2. **Risk and results framework (Weeks 6–7):** built the **Monte Carlo framework** that measures risk and the **dashboard framework** that shows safety, break-even year and risk.
3. **Scenarios and sensitivity (Weeks 6–7):** built the **Boom / Stable / Downturn scenarios** and the **sensitivity table** that show how the result changes when the market or a single assumption changes.

---

## 2. Personal footprint in the product

1. **A simulation that measures risk, not just the average.**
   Each of the 1,000 runs draws every uncertain variable around its mean and recalculates the loan and the net worth:

   $$x_i \sim \mathcal{N}(\mu_i, \sigma_i)$$

   The runs are summarized as the share of safe runs, the P10 / P50 / P90 outcomes and a histogram. A fixed seed (20260909) with the `mulberry32` generator makes the same input always give the same numbers. The three agreed σ values are reference rate ≈ 0.75, house-price growth ≈ 4 and rent growth ≈ 1.25 percentage points.

2. **A result-page framework built before the numbers existed.**
   I built the dashboard (safety gauge, break-even year, tornado chart, Monte Carlo histogram) on mock data first, so the layout was settled early; it was then wired to the real results. This framework is the base of the final result page.

3. **Scenarios and sensitivity that answer "what if?".**
   Three scenarios, each number tied to a year in the 2016–2026 data, and a 17-row sensitivity table that changes one variable at a time (500 runs per row, run only when the user opens it).

---

## 3. What I actually did

### 3.1. Problem comparison and Cau Giay data (Weeks 1–5)
- Compared the initial problem candidates on feasibility, financial relevance and potential user value (week 1, recorded in the credit table).
- Found and scraped the Cau Giay listings used in the MVP, and cleaned them into `BUY_LISTINGS` / `RENT_LISTINGS`.
- The listing data sits in [data/sample_data/](../../data/sample_data/) (`BUY_RAW.csv`, `RENT_RAW.csv`, `PROJECT_MASTER.csv`); my Cau Giay listings are the rows whose district is Cau Giay.
- Designed the **two-point safety-margin rule** and the rule adding closing costs to the minimum-savings check, with Dương Phương Anh; implemented with her (AI-assisted).
- Cau Giay is one of the three districts of the final dataset (205 buildings, 756 sale and 277 rent listings in total) ([contribution.md](../../archive/Week%205/contribution.md), [MIDTERM verification](../../MIDTERM%20-%20Project%20Readiness%20%26%20Contribution%20Verification.md)).

### 3.2. Monte Carlo framework (Weeks 6–7)
- A sampling loop drawing Normal(mean, σ) for each variable, rerunning the loan and net-worth calculation N times.
- Aggregation: % safe runs, P10 / P50 / P90, histogram.
- Built first on test numbers. Two groups of variables had no σ yet and were switched off with σ = 0, then switched back on when the data arrived: income and the four investment channels.
- Final σ values: income 5.71; savings 0.82; bonds 1.37; gold 14.13; stocks 19.30 (percentage points). Basis recorded in the plan: reference rate ±2σ around 10.5% gives 9.0–12.0%, covering the extrapolated range 9.5–11.5%; house price 4 points is about 14% a year divided by √30 ≈ 2.6, rounded up; rent growth is (10% − 5%) / 4.
- Functions: `MC_SETTINGS` (1,000 runs, seed 20260909), `runMonteCarlo`, `mulberry32` in [src/index.html](../../src/index.html).
- Standalone Monte Carlo file: [Monte Carlo](https://github.com/FTU-Legacy-63/G04/tree/main/contribution/evidence/Nguyen_Minh_Tuan).

### 3.3. Dashboard framework (Weeks 6–7)
- Components: safety-margin gauge, break-even year, tornado chart, Monte Carlo histogram.
- Built first on mock data (net worth by year, list of similar units), then replaced by the real results once the calculation was done.
- Functions in [src/index.html](../../src/index.html): `findBreakEven`, `buildConclusionHTML`, `drawNwSvg`. The gauge and the tornado chart were later replaced in the final interface (see below and [Sơn's file](son.md)).
- Standalone dashboard file: **[FILE NEEDED: `dashboard_prototype.* (your actual file)` → put in `src/prototypes/`]**.

### 3.4. Scenarios and sensitivity (Weeks 6–7)
- **Scenarios** Boom / Stable / Downturn, each number with a source year in the 2016–2026 data:

| Variable | Boom | Stable | Downturn |
| :--- | :---: | :---: | :---: |
| Income growth | 9.29% | 5.56% | 3.09% |
| Rent growth | 10% | 6% | 3% |
| LTV | 80% | 80% | 70% |
| Savings rate | 5.85% | 6.50% | 7.60% |
| Government bonds | 2.40% | 4.02% | 5.04% |
| House-price growth in year 10 | 11.40% | 9.13% | 8.09% |

- **Sensitivity table:** 17 rows × 500 runs, one variable changed per row, run only when the user opens "What drives the result?".
- Functions: `SCENARIOS`, `applyScenario`, `SENSITIVITY_ROWS`, `runSensitivity` in [src/index.html](../../src/index.html); [Scenarios_Sensitivity.csv](../../data/financial_assumptions/Scenarios_Sensitivity.csv).

---

## 4. Summary of files, logic and contributions

| Item | What I contributed | Evidence file | How to check |
| :--- | :--- | :--- | :--- |
| **Cau Giay data** | Scraped and cleaned listings | `data/sample_data/BUY_RAW.csv`, `RENT_RAW.csv`, `PROJECT_MASTER.csv` (Cau Giay rows) | In Step 2, filter by district Cau Giay: projects and units appear |
| **Monte Carlo** | Sampling loop, aggregation, fixed seed, σ values | `MC_SETTINGS`, `runMonteCarlo`, `mulberry32` in [src/index.html](../../src/index.html) | Press Calculate twice with the same input: P10 / P50 / P90 are identical |
| **σ values** | Reference rate 0.75, house price 4, rent 1.25; later income, channels | `MC_SETTINGS`; [financial_logic.md](../financial_logic.md) | "What is varied" lists the same values |
| **Dashboard framework** | Gauge, break-even year, tornado chart, histogram (first version) | `findBreakEven`, `buildConclusionHTML`, `drawNwSvg` | Result screen shows the break-even year and the net-worth chart |
| **Scenarios** | Boom / Stable / Downturn with source years | `SCENARIOS`, `applyScenario` | Click each button: the whole result page is recalculated |
| **Sensitivity** | 17 rows × 500 runs | `SENSITIVITY_ROWS`, `runSensitivity` | Open "What drives the result?": 17 rows are computed one by one |

---

## 5. Evidence by project phase

| Phase | Recorded in the team's progress | Confirmed output | What it shows about my contribution |
| :---: | :--- | :--- | :--- |
| **Weeks 1–5** | Problem comparison; Cau Giay data and samples; safety-margin and closing-cost rules | [contribution.md](../../archive/Week%205/contribution.md); `data/sample_data/` (Cau Giay rows) | Data for one of the three districts and the early rules |
| **Weeks 6–7** | Monte Carlo framework; dashboard framework | [src/index.html](../../src/index.html) | The risk engine and the base of the result page |
| **Final** | Scenarios and sensitivity | [src/index.html](../../src/index.html); [financial_logic.md](../financial_logic.md) | The "what if?" part of the result page |

---

## 6. Remaining limitations

- **Independence:** by default variables are drawn independently (ρ = 0) and no correlation matrix is estimated from data, so tail risk (rates up while house prices and income fall) may be underestimated. The same-direction shock runs only at correlation 0.5 ([limitations.md](../limitations.md), #7).
- **Short series:** the σ values come from short series, so the uncertainty in the simulation is approximate (#25); the risk-label thresholds of 10% and 25% are a group convention (#20).
- **Scenarios:** built only from 2016–2026; inflation, stocks, gold and holding costs are the same in all three scenarios, so a deeper crisis is not covered (#18).
- **Dashboard:** the framework was built on mock data, so the first layout had to be adjusted when the real numbers were connected; the gauge and the tornado chart no longer appear in their original form in the final product.

> **Note on AI assistance:** the code for the safety-margin and closing-cost rules was produced with AI assistance at the request of the group members named above, under their direction.
