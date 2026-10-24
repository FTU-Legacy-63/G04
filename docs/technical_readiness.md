# Technical Readiness: FinFlow V5

## 1. Technical route

| Item | Choice |
|---|---|
| Stack | Plain HTML, CSS and JavaScript, no framework and no build step; one file, `src/index.html` (about 620 KB) |
| Data | Listing data embedded as JSON arrays in the file: 205 buildings, 756 BUY and 277 RENT listings, snapshot 2026-09-09. No database |
| User input | Kept in the browser's memory only; never sent anywhere, no cookies, no `localStorage` |
| External requests | None. The net-worth chart is drawn as inline SVG, so the page works fully offline |
| Deployment | Static file: open it directly in a browser, or host on GitHub Pages. Link: [DEPLOYMENT LINK] |
| Engine | Loan, safety check, net worth, Monte Carlo, scenarios and sensitivity all run in the browser |

## 2. Computation and performance

| Part | Detail |
|---|---|
| Monte Carlo | 1,000 runs, mulberry32 with fixed seed 20260909, so the same input always gives the same output; about 0.7 s |
| Sensitivity | 17 rows × 500 runs, computed row by row on click so the page does not freeze |
| Budget labels | The same safety function runs on all 1,033 units, about 0.3 s |
| Scenario / horizon / today's money | Recompute or re-read the same engine output; the horizon change does not rerun Monte Carlo |

## 3. Verification

| Check | Result |
|---|---|
| Excel assumptions vs code | 48 parameters compared in `Doi_chieu_index_html`: 0 mismatches |
| Listing figures | 13 numbers recomputed from the embedded data match |
| Test suite | 123 cases in [tests/](../tests/): [RESULTS TO BE ADDED]; see [testing.md](testing.md) |
| Regression check | With all four new cost fields set to 0, V3 reproduces V2 results |

## 4. Fallbacks

| Risk | Behaviour |
|---|---|
| Invalid or inconsistent input | Specific error message; no calculation runs |
| Savings below the minimum down payment, or borrower too old | BUY card shows the reason; RENT and the verdict still compute |
| Monte Carlo fails | Risk lines show "The simulation could not run (…)"; safety results still display |
| Unexpected exception | Global error message instead of a blank page |

## 5. Why this route fits the project

- No server, API key, domain or uptime risk, which suits a live demo.
- Privacy: personal financial data never leaves the browser.
- Easy for the team to read and fix: no dependencies or build tools.
- Reproducible: a reviewer can open the file and get the same numbers.

## 6. AI-assisted coding

AI assistance was used to implement and adjust logic and interface text at the team's request. Each change was checked by running the engine and comparing with hand calculations and the Excel assumptions workbook.

## 7. Limitations

- No backend: no saved history, no accounts, no live data; changing listings means editing the file.
- Data is a fixed snapshot of asking prices, not a feed.
- Dead code remains in the file: an unused Chart.js loader with CDN addresses (never called). [CLEAN UP OR KEEP]
- Automated browser tests ran in headless Chromium only. [ADD MOBILE / OTHER BROWSERS IF TESTED]
- Scope is deliberately narrow: 2-bedroom apartments in three districts. Expansion is a separate phase.
