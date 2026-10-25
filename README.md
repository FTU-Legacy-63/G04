# FinFlow — Buy vs Rent

**FinFlow is a browser-based simulator that helps a young Hanoi household decide whether to buy or rent a 2-bedroom apartment, by checking whether each option is affordable every month and which one leaves more net worth over time.**

Course: Technology Applications in Finance and Banking (NHA408E), FTU 2026 · Group 04 (G04) · Instructor: Assoc. Prof., Dr. Phan Tran Trung Dung

**Final build:** `src/index.html` (FINAL-PRODUCT-V5) · **Live link:** [GitHub Pages](https://ftu-legacy-63.github.io/G04/src/)

---

## 1. The problem

Young couples and single people in Hanoi with some savings often compare buying and renting by the monthly payment alone. That hides two questions:

1. **Can I carry it?** After housing payments, holding costs and living costs, is there enough money left every month, including the months when the loan payment jumps?
2. **Who is richer later?** After many years, which option leaves higher net worth once purchase fees, selling costs and the return on invested savings are counted?

## 2. Target user and decision supported

- **Target user:** young couples or single people in Hanoi who are deciding whether to buy or rent a 2-bedroom apartment.
- **Decision:** buy one specific listed apartment, or rent another, given the user's own income, savings, age and debts.
- **Scope:** 2-bedroom apartments in Cau Giay, Ha Dong and Tay Ho. Data: 205 buildings, 756 sale listings and 277 rental listings from batdongsan.com.vn, frozen at **9 September 2026**.

## 3. What the product outputs

- A **safety verdict** for each side, labelled **Comfortable / Tight / Not safe**, with the tightest month and the money left in that month.
- A **net worth comparison** over time (median path and a P10–P90 band) and the break-even year.
- A **risk summary** from 1,000 simulated futures: how often BUY ends richer, and how often each side has to use its emergency fund.
- **Boom / Stable / Downturn** scenarios and a one-at-a-time **sensitivity table** showing which assumptions matter most.

The tool does not tell the user what to choose. The conclusion is a check on average assumptions, Monte Carlo is shown as risk information, and the decision is the user's.

## 4. How it works

The user goes through five steps; Steps 1–4 are on one page and Step 5 is the result screen.

1. **Your finances:** income, savings, living cost, debt, emergency fund, age(s), promotional-rate package. A "Your budget" card updates as the user types.
2. **Choose a project and size:** independently for BUY and RENT.
3. **Choose a BUY unit and a RENT unit:** each unit card shows a budget label (Within budget, Payment too tight, Not enough savings, No loan available).
4. **How you invest spare money (optional):** a split across four channels (savings deposits, government bonds, gold, stocks), then **Calculate**.
5. **Result:** conclusion, reality check on rental yield, net worth chart, 1,000 simulated futures, sensitivity, detailed BUY and RENT cards.

Full description: [`docs/user_flow.md`](docs/user_flow.md).

## 5. How to run or access the product

- **Online:** open the [live link](https://ftu-legacy-63.github.io/G04/src/).
- **Locally:** download the repository and open [`src/index.html`](src/index.html) in any modern browser. No installation, server, API key or login is needed. The listing data and the calculation engine are embedded in the file, and the user's input never leaves the browser. (Only two web fonts are fetched from Google Fonts when online; without them the browser uses default fonts.)

Technical details: [`docs/technical_readiness.md`](docs/technical_readiness.md).

## 6. Sample input and example use case

Enter this profile in Step 1:

| Field | Value |
|---|---|
| Income 1 / Income 2 | 30 / 20 million VND per month |
| Savings | 1,500 million VND |
| Minimum living cost | 15 million VND per month |
| Age 1 | 32 (Age 2 blank = applying alone, or enter a second age) |
| Emergency fund | 6 months (default) |
| Promo package | 12 months (default) |

The "Your budget" card then shows the largest purchase price and the largest rent that pass the safety check (about 2.8 billion VND for a typical 72 m² unit and about 19 million VND per month for an 80 m² rental in the Final Plan's version of this example). Pick a project and size in Step 2, one BUY unit and one RENT unit in Step 3, press **Calculate** in Step 4, and read the conclusion at the top of Step 5.

## 7. Financial logic summary

Both paths start from the same savings and run month by month for the whole loan term.

- **Loan:** modelled on MBBank (Van Phuc branch): promotional rate 7.7 / 8.3 / 8.5 / 9.0% for 6 / 12 / 18 / 24 months, then reference rate 10.5% plus margin (+1.5% for 12 months, +3.5% after); 24-month interest-only grace period; equal principal afterwards; loan-to-value up to 80%; maximum term 360 months and age 70 at payoff (older borrower's age).
- **Buying costs:** 2.6% purchase fees paid from savings, plus an emergency fund. Holding costs: service fee and fire insurance. Selling cost 1.5% is deducted from BUY net worth in every year.
- **House prices:** a path that starts at 20.43% a year and cools toward 8.38%, calibrated so the next 10 years average the last 10 (12.66%). Income grows 5.56%, living cost 3.09%, rent 6%.
- **Safety check:** every month, money left must stay above 40 / 35 / 30 / 25% of income (by income band, in today's money).
- **Net worth:** BUY = house value − selling cost − remaining loan − fees + investments; RENT = investments. The RENT side invests in four channels.
- **Monte Carlo:** 1,000 simulated futures with a fixed seed (20260909), so the same input always gives the same output.

Details and worked examples: [`docs/financial_logic.md`](docs/financial_logic.md) and [`docs/assumptions.md`](docs/assumptions.md).

## 8. Data and source summary

| Data | Where | Source |
|---|---|---|
| Listings (buildings, sale, rent) | [`data/sample_data/`](data/sample_data/) | batdongsan.com.vn, snapshot 9 Sep 2026 |
| Financial assumptions, one CSV per topic | [`data/financial_assumptions/`](data/financial_assumptions/) | FiinPro, World Bank, NSO, investing.com, CafeF, Cushman & Wakefield, press and bank sources |
| Loan terms | [`mb_bank_rate.jpg`](data/financial_assumptions/mb_bank_rate.jpg) | MBBank, Van Phuc branch rate sheet |

Every number has a source and a status in [`docs/data_and_sources.md`](docs/data_and_sources.md). The workbook-to-code check ([`Code_Cross_Check.csv`](data/financial_assumptions/Code_Cross_Check.csv)) compares 48 parameters with the code and found no mismatch.

## 9. Testing summary

- **Test workbook:** 123 written cases: 88 calculation cases, 28 input-error cases and 7 filter cases (`tests/FinFlow_Test_Cases_V5.xlsx`).
- **Developer checks during the build:** regression between versions V1 → V5, budget labels compared with the live safety check on all 756 + 277 listings, Monte Carlo with zero variance equal to the average path.
- **Results of running the workbook:** all 123 cases passed (88/88 calculation, 28/28 input errors, 7/7 filters), run by hand in Microsoft Edge and Google Chrome on a laptop on 9 Oct 2026. No critical bug was found; two cosmetic wording issues (negative savings and negative debt messages show raw variable names) remain open.
- The expected values in the workbook are a baseline for regression (what V5 returns), not an independent answer key.

Details: [`docs/testing.md`](docs/testing.md).

## 10. Known limitations

- The data is a fixed snapshot of asking prices, hand-entered and not corrected by the team; many buildings have only 1–2 listings.
- The 10.5% reference rate is extrapolated from market floating rates because the MB document does not state a value; rent growth of 6% is a reasoned judgement, not a measurement.
- Repairs inside the unit, building depreciation, the rental deposit and furnishing costs are not in the main result. These omissions lean slightly towards BUY.
- Monte Carlo uses standard deviations estimated from short series; it is risk information, not a forecast.
- The product supports a decision; it is not personal financial advice.

Full list of 26 items: [`docs/limitations.md`](docs/limitations.md).

## 11. Revisions after the midterm

The product went from the 27 September MVP to the final V5 build (9 October 2026): corrected assumptions workbook, house-price path replacing a fixed 19%, holding and selling costs added, relevance engine rebuilt, safety check over the whole term, scenarios and sensitivity, and an interface rewrite. Summary: [`docs/revision_summary.md`](docs/revision_summary.md); item-by-item record: [`docs/FinFlow - Change log (Midterm to Final).pdf`](<docs/FinFlow - Change log (Midterm to Final).pdf>).

## 12. Team and contribution evidence

| Member | Main responsibility | Individual footprint |
|---|---|---|
| Dương Phương Anh | Coordinator, repository owner, financial model and assumptions, integration | [Duong_Phuong_Anh.md](contribution/individuals/Duong_Phuong_Anh.md) |
| Nguyễn Minh Tuấn | Cau Giay data, Monte Carlo and dashboard framework | [Nguyen_Minh_Tuan.md](contribution/individuals/Nguyen_Minh_Tuan.md) |
| Nguyễn Hải Sơn | Ha Dong and Tay Ho data, relevance engine, loan term by age, loan calculation link | [Nguyen_Hai_Son.md](contribution/individuals/Nguyen_Hai_Son.md) |
| Phạm Thị Khánh An | Macro and market figures, bank sources, initial idea | [Pham_Thi_Khanh_An.md](contribution/individuals/Pham_Thi_Khanh_An.md) |
| Phạm Nam Phương | VN-Index, loan-to-value and bank loan rates, initial assumptions | [Pham_Nam_Phuong.md](contribution/individuals/Pham_Nam_Phuong.md) |

Group contribution map: [`contribution/contribution_map.md`](contribution/contribution_map.md).

## 13. Repository structure

```text
/
├── README.md
├── src/index.html                 final product (single file, runs offline)
├── data/
│   ├── financial_assumptions/     assumptions, scenarios, market series, MB rate sheet
│   └── sample_data/               BUY_RAW, RENT_RAW, PROJECT_MASTER
├── docs/                          financial logic, sources, user flow, testing,
│                                  limitations, revisions, Final Plan, change log
├── tests/                         FinFlow_Test_Cases_V5.xlsx
└── contribution/
    ├── contribution_map.md        group contribution map
    └── individuals/               one footprint file per member
```
