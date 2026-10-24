# Technical Readiness — FinFlow

## 1. Current technical route

| Item | Choice | Note |
|---|---|---|
| Coding environment | Plain (vanilla) HTML + CSS + JavaScript, no framework | Everything lives in a single `finflow.html` file |
| Data storage | No database — listing data is hard-coded as JSON in the code (`BUY_LISTINGS`, `RENT_LISTINGS`) | See `../week3/data.md` |
| Handling user input | Exists only in the browser's memory (a JS `state` object), never sent anywhere, not retained after the tab closes | Appropriate, since the input is personal financial data that shouldn't be sent to a server without a clear reason |
| Deployment platform | A static HTML file — runnable by **opening it directly in a browser** (double-click), or hosted on any static hosting service (GitHub Pages, Netlify, static Vercel, etc.) | No backend and no build step required |
| Only external dependency | Chart.js, loaded via CDN (tries 3 different mirrors in sequence) — used only to draw the net worth chart | This is the **only** feature on the page that needs internet; every other calculation and result works fully offline |
| AI-assisted coding | Used to implement and adjust the financial logic (`evaluateBuy`, `decide`), add `buy_closing_costs_pct`, and update UI text/labels/disclaimers, always at the team's explicit request | Every change was specifically requested and re-verified by actually running the code (see `sample-calculation-and-logic-test.md`), rather than blindly accepting AI output |

## 2. Technical background

`finflow.html` is a self-contained client-side implementation: all calculation logic (loan amortization, safety-margin checks, net-worth projection, the BUY/RENT/NEITHER decision) runs directly in the browser in JavaScript, against the embedded listing data — there is no server, no API call, and no build step involved in producing a result. This keeps submission and demoing simple: no backend deployment, no CORS or API-key concerns, and no risk of a server being down during a live demo.

## 3. Fallbacks already in place

| Risk | Fallback implemented |
|---|---|
| All 3 Chart.js CDN mirrors fail (no internet, or blocked) | Shows a "Chart.js could not be loaded..." message with a **Retry** button; every number, result card, and recommendation **still displays fully and correctly** — only the chart is missing |
| An unexpected error while drawing the chart (e.g., abnormal net worth data) | A dedicated `catch` around the chart-rendering step shows "The chart could not be rendered (...)" instead of crashing the whole page |
| An unexpected error during calculation (e.g., invalid input somehow slips past validation) | `try/catch` around the calculation call shows "Something went wrong during the calculation (...)" instead of crashing |
| Failing to load the ward list (data is empty — shouldn't happen since data is hard-coded, but a safeguard exists anyway) | A `catch` around ward loading shows an error and suggests reloading the page |
| Input in the wrong format | Validated with clear English error messages (see `../week3/validation-and-early-logic-test.md` §1) — never a blank/crashed page |

## 4. Why this route is feasible for the scope of this course

- No hosting/server cost, no domain, no uptime concerns to manage — just one file, well suited to a midterm deadline.
- No dependency on an external API for operational data (the only external dependency is for **presentation** — the chart — not for the calculation logic itself), so the technical risk during an in-class live demo is very low.
- The team can maintain it easily (easy to read, no build tool or dependency manager needed) — matching the guide's "team's ability to fix it themselves" criterion.

## 5. Limitations to state when presenting

- Since there is no backend/database, the product **cannot** save a user's calculation history between visits, cannot support multiple users sharing one session, and cannot update listing data without editing the code directly.
- If real-time property price data is needed later, a real data source/API and an update mechanism would need to be added — currently outside the MVP scope.

## 6. MVP scope assessment

- The current technical route (one static HTML file) is **small and feasible within the course timeline** — it doesn't require complex infrastructure to build, run, or demo.
- The MVP has deliberately stayed within its original narrow scope: one area (Cau Giay), a fixed bedroom count (2), and static demo data — no new scope has been added beyond what was originally planned. Any future expansion (more districts, variable bedroom count, live data) should be treated as a distinct next phase, not a silent scope-creep into the current MVP.

## 7. Midterm repo readiness

### 7.1 Grading weight (recap from the guide)

- Group Footprint: 60%
- Objective Individual Contribution: 25%
- Individual Footprint: 15%

The midterm does **not** require a finished product — it requires demonstrating a clear direction, feasible input, explainable financial logic, a realistic MVP, evidence of progress, and clear individual contribution.

### 7.2 What the repo already lets a reader find

| What a reader needs to find | Where it is in the repo |
|---|---|
| Problem and user | `financial-logic.md` §1 (Problem, Target user, User task, Difficulty) |
| Product direction / MVP | `financial-logic.md` §1 (Technology support, User action) + `finflow.html` runs directly |
| Input and sources | `../week3/input-dictionary.md`, `../week3/source-register.md` |
| Financial logic | `financial-logic.md` §2–3 |
| Sample calculation | `sample-calculation-and-logic-test.md` (cross-referenced with `../week3/validation-and-early-logic-test.md`) |
| Current progress | The checklist at the end of each `week3/` and `week4/` `README.md` |
| Technical route | §1–6 above |
| Limitations | `../week3/assumptions.md`, `financial-logic.md` §4.4, §5 above |
| Contribution evidence | `../week3/ownership.md` |
| Next steps | See §7.4 below |

### 7.3 Self-check questions — answered based on the repo's actual state

- **Can the product run with the current data?** Yes — `finflow.html` runs standalone, no setup required, and has been verified with real cases in `sample-calculation-and-logic-test.md`.
- **Is any field still missing?** No required field is missing; two assumptions (`interest_rate_float_ref_pct`, `buy_closing_costs_pct`) recently got real sources logged in `../week3/source-register.md` — worth a final check that every reference is complete before presenting.
- **Can real data be swapped for sample data?** Not applicable in the way the guide phrases it — the current data is already **real** (scraped listings), not a placeholder to be swapped later; it's a static snapshot rather than a live feed (see `../week3/data.md` §3).
- **Are units and formats consistent?** Yes — the UI always takes input in million VND, the engine always calculates in VND, and the conversion happens at exactly one point (see `../week3/data-flow.md`).
- **Which assumption could most distort the output?** `property_annual_appreciation_pct` (a flat 12%/year) has the largest impact on the long-term chart if the real market goes flat or declines — a disclaimer already warns about this directly in the UI.
- **Is any input actually unnecessary?** No unnecessary input has been found; however, `bedrooms` is currently fixed at 2 rather than being a real input — it should be decided whether this is an intentional MVP limitation or something to expand later.
