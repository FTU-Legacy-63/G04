# User Flow — FinFlow

## Happy path

| Step | User action | System response | Evidence |
|---|---|---|---|
| 1 | Opens the page | Step 1 loads with the ward dropdown populated from the embedded data; size defaults to "Medium" | `loadWards()`, `<select id="size_band">` default |
| 2 | Picks a ward (and optionally changes size) | Step 2's BUY/RENT card lists populate, filtered to that ward + size + 2 bedrooms | `loadListings()` → `muaCalc()`/`thueCalc()` |
| 3 | Clicks one BUY card and one RENT card | Each column collapses to a "selected" summary with a "Change" button; the Calculate button (Step 3) becomes enabled once both are picked | `updateCalculateButton()` |
| 4 | Enters income1, income2, savings, living cost (required); optionally existing debt and loan term | The auto-generated assumptions box is already visible above the button, showing the current rate/grace/LTV terms | `renderLoanAssumptionsBox()` |
| 5 | Clicks "Calculate" | Input is validated, converted from million VND to VND once, and run through the calculation; Step 4 appears and the page scrolls to it | Calculate-button click handler, `evaluateBuyVsRent()` |
| 6 | Reads the decision banner and the two result cards | Sees a 🟢/🔵/🔴 recommendation with a plain-language reason, two "Monthly cost" lines on the BUY card (grace / post-grace) each with a Safe/Not-safe badge, and a net-worth chart with a break-even note | `buildDecisionBannerHTML()`, `buildResultCardHTML()` |
| 7 | Clicks "Change" on either listing, or edits a Step 3 number and clicks Calculate again | The flow returns to Step 2 (or simply recalculates) without losing ward/size context | `resetSelections()` on listing "Change"; direct recalculation on edited numbers |

## Alternative paths

| Scenario | What happens |
|---|---|
| User changes ward or size after already selecting listings | Both selections and any existing result are cleared (`resetSelections()`), Step 4 is hidden, and Step 2 repopulates with the new candidate list — the user is not left with a stale, mismatched selection |
| User leaves "Existing monthly debt payment" blank | Treated as `0`, not an error — it's the only fully optional financial field |
| User leaves "Loan term" blank | Falls back to the default 360 months from `FIN_ASSUMPTIONS`, not an error |
| User picks a BUY/RENT pair, then picks a *different* BUY or RENT card before calculating | The new selection simply replaces the old one in that column; no confirmation dialog, no restart needed |
| User recalculates after already seeing a result | Step 4 re-renders in place with the new numbers; no page reload |

## Error paths

| Trigger | System response | Evidence |
|---|---|---|
| Income 1, Income 2, Savings, or Living cost left blank | Global error banner: "Please fill in Income 1, Income 2, Savings, and Minimum living cost." | `showError()` |
| A financial field is not a valid number | "`"<field>"` is not a valid number." | Number-format check |
| A financial field is negative | "`"<field>"` cannot be negative." | Negative-value check |
| Income 1 + Income 2 = 0 | "Income 1 + Income 2 must be greater than 0 to calculate the safety margin." | Divide-by-zero guard |
| Loan term entered but ≤ 0 or invalid | "Loan term (months) must be a valid number greater than 0." | Loan-term check |
| Savings below the required minimum down payment (LTV + closing costs) | **Not a global error** — the BUY card itself shows: "You need at least X more in savings to qualify for this loan (max LTV 80%)."; the RENT card and the final decision still compute normally | `loanCalc()` error branch, `buildResultCardHTML()` |
| An unexpected exception during calculation | Global error: "Something went wrong during the calculation (...). Please check your inputs and try again." | `try/catch` around `evaluateBuyVsRent()` |
| All 3 Chart.js CDN mirrors fail to load | The chart area shows a message plus a "Retry" button; every card and the decision banner are unaffected | Chart-loading fallback |
| Ward/size list fails to populate (shouldn't happen — data is hard-coded, but guarded anyway) | Error message suggesting a page reload | `catch` around `loadWards()` |

Note the distinction between the insufficient-savings case (a real, expected business outcome — the flow completes, the user gets a full answer) and the other error cases (a blocking problem with the input itself, which must be fixed before anything can be calculated). Both start and end clearly: every path either ends at a full Step 4 result or at a specific, fixable error message — there is no dead end.

## Unnecessary-step check

- No re-entry of data the app already has (ward/size persist across listing changes; a "Change" only affects the one column clicked).
- No purely decorative page or step.
- No button that doesn't trigger a real action.
- No duplicated output.
- No login or account step.
- No technical step exposed to the user without value (e.g., no manual "convert to VND" step — the million-VND → VND conversion is invisible to the user, handled once in code).
