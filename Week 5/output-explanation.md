# Input & Output Presentation, and Interface Explainability — FinFlow

Input meaning/type/unit/validation and output formulas/interpretation were already defined in Weeks 3–4 (`../week3/input-dictionary.md`, `../week4/financial-logic.md`). This file only covers how they're **presented** on screen.

## 1. Input presentation (Step 1–3)

| Checklist item | Current state |
|---|---|
| Clear label | ✅ — e.g. "Existing monthly debt payment", not "Debt" |
| Unit shown | ✅ — every money field is labeled "(million VND / month)" or similar next to the label |
| Example | ⚠️ Partial — `existing_debt` has a placeholder (`e.g. 5`); income/savings/living-cost fields do not have example placeholders |
| Required/optional marked | ⚠️ Implicit only — required fields aren't marked with an asterisk or "(required)" tag; the user only discovers a field is required after submitting and seeing the error banner |
| Valid range stated up front | ⚠️ Partial — the UI doesn't state "must be ≥ 0" before submission; it only appears as an error after an invalid entry |
| Error message | ✅ — specific, plain-English, named to the exact field |
| Reasonable default | ✅ — `existing_debt` defaults to 0, `loan_term_months` defaults to 360, `size_band` defaults to "Medium" |

**Gap to consider before Week 6:** required fields and valid ranges are currently only communicated reactively (after an error), not proactively (before the user types). Adding "(required)" tags and example placeholders to income/savings/living-cost would close this gap cheaply.

## 2. Output presentation (Step 4)

| Checklist item | Current state |
|---|---|
| Main result stands out | ✅ — the decision banner (🟢/🔵/🔴, large, colored) sits above the two result cards |
| Unit is clear | ✅ — every VND figure uses a formatted short form (e.g., "13.8M VND") consistently |
| Interpretation given | ✅ — Safe/Not-safe badges, not just a bare percentage |
| Comparison/context | ✅ — BUY and RENT cards sit side by side; the chart compares both over time |
| Explanation | ✅ — the `reason` string under the banner |
| Limitation stated | ✅ — the net-worth chart disclaimer, the income-tier caption, the "close margins" note |
| Next action | ✅ — "Change" buttons right next to each selected listing |

## 3. Interface explainability

Week 4 established *why* the logic produces a given result (see `../week4/financial-logic.md` §4). Week 5's question is narrower: does the **screen itself** make that reasoning visible, without requiring the user to read code?

**Already in place:**

- The auto-generated assumptions box (shown *before* Calculate) — a form of "assumption box."
- Two labeled "Monthly cost" lines (grace / post-grace) instead of one blended number — a form of "breakdown."
- The `reason` sentence under the decision banner — a "reason statement."
- The income-tier caption — a short, always-visible "why this threshold" note.
- The net-worth chart disclaimer — a "warning" / limitation note.

**Not yet in place (carried over from `../week4/financial-logic.md` §4.3):** the `reason` sentence is a fixed string — it doesn't insert the user's actual numbers (e.g., *"BUY's safety margin is −17.7%, below the 30% threshold for a 65M/month household"*). A user currently has to manually compare the two badge rows to reconstruct that story. This remains open going into Week 6; closing it would move FinFlow from "shows numbers with labels" to "explains its own numbers in one sentence."

**Not tested yet:** whether a first-time user (someone who has not seen this documentation) can look at Step 4 cold and correctly explain, in their own words, why the recommendation came out the way it did. This is a "does the user understand," not "is the logic correct," question — worth a quick 2–3 person test before Week 6.
