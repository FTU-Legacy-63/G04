# Week 3 — Input, Information and Evidence Readiness

**Product:** FinFlow — Buy vs Rent (a demo comparing buying vs. renting an apartment in Cau Giay, Hanoi)
**Product file:** `finflow.html` (single-file, runs entirely client-side, no server required)

This folder answers Week 3's central question: *What information does the product need to operate, where does that information come from, and is it feasible to use?*

## File list

| File | Content |
|---|---|
| [`input-dictionary.md`] | Every input (user-entered, product information, scenario/assumption) that actually exists in the code |
| [`source-register.md`] | Operational data sources plus problem-evidence sources, with purpose/limitation/owner |
| [`data.md`] | Data structure; sample data exported to `data/*.csv` |
| [`assumptions.md`] | Every assumption currently baked into `FIN_ASSUMPTIONS` and into the logic — nothing left hidden in the code |
| [`data-flow.md`] | Source/User → Input → Validation → Process → Output |
| [`validation-and-early-logic-test.md`] | Validation already implemented, plus early logic tests actually run against the code |
| [`ownership.md`] | Owner of each key piece of evidence |

## Important note

- Every figure and formula in these files is taken directly from the current code in `finflow.html` (nothing is guessed), and part of it has been independently re-verified by running the JS engine in a standalone Node.js environment (see `validation-and-early-logic-test.md`).
- The underlying listing data (`DATA_DEMO.xlsx`, the source of `data/buy-listings.csv` / `data/rent-listings.csv`) is **real data scraped from the market**, not a synthetic/simulated dataset — see the correction note in `data.md` section 5. The one caveat is that it is a **static snapshot, not real-time**.
- Several assumptions now have a real, named source that previously had none: the MB Bank – Van Phuc Branch rate sheet (confirms 7 of 9 `FIN_ASSUMPTIONS` values), a CFPB reference for the safety-margin concept (qualitative only — see the caveat in `assumptions.md`), and a Vietcombank rate notice that was considered but not adopted. See `source-register.md` for the full detail and remaining source-verification to-dos.
- Cells shown as `[Fill in ...]` are placeholders that still need completing (mainly exact source access dates, and a couple of reviewer names in `ownership.md`) — most contributor names have now been filled in from the team's own project records.

## End-of-Week Checklist (mapped against FinFlow)

- [x] Operational data clearly separated from problem evidence — see `source-register.md`.
- [x] Input dictionary complete to the necessary level — see `input-dictionary.md`.
- [x] Source register includes purpose and limitation — see `source-register.md`.
- [x] Real listing data in place (scraped from the market, a static snapshot — not real-time, not simulated) — `data.md`.
- [x] Assumptions documented — see `assumptions.md`.
- [x] Data structure simple and workable — static embedded JSON arrays, no database.
- [x] Data flow clear — see `data-flow.md`.
- [x] Basic validation defined — see `validation-and-early-logic-test.md`.
- [x] At least one early logic test — see `validation-and-early-logic-test.md`.
- [ ] Every key piece of evidence has an owner — mostly filled in `ownership.md`; a few reviewer names and the owner of the `evaluateBuy()` dual-point fix still need confirming with the team.
- [ ] Repo updated with feedback and revisions — to be updated by the team after checkpoint feedback.
