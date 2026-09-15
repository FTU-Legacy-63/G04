# Feature Scope — FinFlow

## 1. Main feature

Compare one specific BUY unit against one specific RENT unit on two things: (a) near-term financial safety — whether the monthly cost stays within a safe share of the user's income, both during and right after the loan's grace period — and (b) long-term net worth. The product returns one clear recommendation: BUY, RENT, or NEITHER.

Test: *if this were removed, the product would have no reason to exist* — everything else supports getting to, or understanding, this one output.

## 2. Supporting features

| Feature | How it supports the main feature |
|---|---|
| Ward/size dropdowns + BUY/RENT card lists (Step 1–2) | Gets the user to a valid, specific comparison pair — the main feature needs exactly one BUY listing and one RENT listing to run |
| Auto-generated loan-assumptions box (Step 3) | Shows the current rate/grace/LTV terms *before* the user commits to entering their financial details, so the eventual result isn't a black box |
| Labels, units, hints, and placeholders on every input | Reduces wrong or ambiguously-scaled input (e.g., typing "25" not knowing if it means million or full VND) |
| Two-phase safety badges (grace / post-grace) on the BUY card | Prevents a loan that "looks safe" during the grace period from being read as fully safe |
| Decision banner reason text + income-tier caption + "close margins" note | Turns a bare BUY/RENT/NEITHER label into an explained recommendation |
| "Change" buttons on each selected listing | Lets the user try a different pair without restarting the whole flow |
| Global + inline error messages | Tells the user exactly what to fix, in place, without a blank or broken page |
| Break-even marker + disclaimer on the net-worth chart | Adds context (when, if ever, one option overtakes the other) and states plainly that this is illustrative, not a forecast |

## 3. Optional features (safe to freeze post-midterm)

| Feature | Why it's optional | Current status |
|---|---|---|
| Net-worth chart itself (Chart.js) | The BUY/RENT/NEITHER decision and both result cards render fully even if the chart fails to load — the chart adds insight, it isn't required for the core recommendation | Built, with a 3-mirror CDN fallback and a Retry button |
| Data export to CSV for review (`data/sample-buy.csv` etc.) | A documentation/review convenience for the team, not something end users interact with | Built (see `../week3/data.md`) |
| `rent_annual_growth_pct` (rent rising over time) | Would make the net-worth-RENT projection more realistic, but the core recommendation doesn't depend on it | Not built — logged as a known limitation in `../week4/financial-logic.md` §4.4 |
| Prepayment fee modeling | Same — improves accuracy of a secondary chart, not the core safety decision | Not built |
| Multi-channel investment modeling (savings/gold/stocks split) | A richer version of `investment_return_pct` | Not built, correctly out of MVP scope |

Per the guide's advice, none of these optional items should be added before the core flow (Step 1 → Step 4, happy + error paths) is confirmed solid.

## 4. Core vs. optional test, applied

For every feature above, the question is: *if this feature were removed, could the user still complete the core task (get a BUY/RENT/NEITHER recommendation for a chosen pair)?*

- Remove the loan-assumptions box → still yes, but the result would feel less explained. **Supporting, not core.**
- Remove the two-phase safety badges → still yes, but the product would silently regress to the pre-midterm-fix behavior (the exact bug Week 4 fixed). **Supporting, but high-value — do not remove.**
- Remove the net-worth chart entirely → still yes, the decision banner and cards are unaffected. **Optional.**
- Remove Step 1–3 input entirely → no, there is no product left. **Core.**
- Remove error messages → the user could still technically get a result with valid input, but would be stuck silently on bad input. **Supporting, effectively required for usability.**

## 5. User goal — reused, not rewritten

The user goal was already set in Weeks 1–4 (see `../week4/financial-logic.md` §1): *decide whether to BUY or RENT the selected unit, or try a different combination.* Week 5 only checks whether the current interface actually gets the user there.

**Self-check:**

- **Does the user know where to start?** Yes — the page opens directly at Step 1, with steps numbered 1–4 and only the current step's content usable until its prerequisites are met (e.g., Step 2's cards don't populate until ward/size are picked; Calculate stays disabled until both a BUY and a RENT unit are selected).
- **Does every step serve the goal?** Yes — ward/size narrows the candidate pool, selecting BUY+RENT defines the comparison, the financial profile personalizes the safety calculation, and Calculate produces the decision. No step is decorative.
- **Is any step unnecessary?** None found — no login, no interstitial pages, no step that could be skipped without breaking the flow.
- **Does the output lead to a clear next action?** Yes — the decision banner is immediately followed by "Change" buttons on both selected listings, so trying an alternative pair is one click away rather than a restart.
