# Feature Scope: FinFlow V5

## 1. Main feature

Compare one chosen BUY unit with one chosen RENT unit on near-term safety (every month of the loan) and long-term net worth, and report the result with its risk. If this were removed, the product would have no purpose.

## 2. Supporting features

| Feature | Supports the main feature by |
|---|---|
| Step 1 "Your finances" and budget card | Gives the safety check its inputs and shows what is within reach before choosing |
| Steps 2–3 project and unit selection, relevance engine, budget labels | Produces a valid, comparable BUY and RENT pair |
| Step 4 investment mix and spare-money table | Sets how spare cash grows on both sides |
| Verdict, Comfortable / Tight / Not safe, reason in numbers | Turns calculations into a readable conclusion |
| Monte Carlo risk lines | Shows how fragile the result is |
| Assumptions box with source links, "How we check" | Makes the result auditable |
| Error messages, defaults, loan eligibility rules | Prevents silent wrong answers |

## 3. Built since midterm

Monte Carlo and risk labels · scenarios Boom / Stable / Downturn · 17-row sensitivity table · age-based loan term · emergency fund · multi-channel investment · rent growth, income growth and CPI · prepayment fee · service fee, insurance and selling costs · rent-vs-price reality check · nominal / today's-money view · three districts instead of one · Plan B flow (finances first, units second).

## 4. Optional features

| Feature | Why optional | Status |
|---|---|---|
| Net-worth chart | Decision and risk render without it | Built (inline SVG, works offline) |
| Scenario buttons, sensitivity table | Add insight, not needed for the base verdict | Built |
| Reality-check card | Context only | Built |
| Smooth safety thresholds, correlation ρ | Stress tests | Built as sensitivity rows only (off by default) |

## 5. Not built or out of scope

| Item | Reason |
|---|---|
| Buy-to-let (buy and rent out) | Dropped 07/10: needs a separate yield and management model |
| Live listing or rate data | Static snapshot (9 Sep 2026) by design |
| Accounts, saved history | No backend |
| Rental deposit, in-unit repairs, furnishing, building depreciation | Weak sources or small effect; repairs run as sensitivity only |
| Other property types and districts | 2-bedroom apartments in Tay Ho, Cau Giay, Ha Dong only |
| Correlation matrix estimated from data | No data; ρ = 0.5 is a stress test only |

## 6. Core versus optional test

- Remove Step 1 or the unit selection: no product left. **Core.**
- Remove the risk lines: still a verdict, but fragility is hidden. **Supporting, high value.**
- Remove the chart: decision still works. **Optional.**
- Remove error messages: users get stuck on bad input. **Supporting, effectively required.**

## 7. User goal

Decide whether to buy the chosen unit or rent the chosen one, or try another pair. The five-step flow ([user_flow.md](user_flow.md)) follows this goal: finances, projects, units, investment mix, result.

Trying other options after a result:
- Scenario (Boom / Stable / Downturn), comparison horizon and nominal / today's-money view change with one click and recompute the result page.
- Another unit is picked again in Step 3, and another project or size in Step 2. Either change clears the result, so the user presses Calculate again.
