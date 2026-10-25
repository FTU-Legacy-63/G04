// node tests/mvp_harness.js <MVP html> <cases.json> — chạy NGUYÊN engine JS của MVP Week 6 (trích từ file HTML của team)
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const start = html.indexOf("const FIN_ASSUMPTIONS"), end = html.indexOf("function buildNetWorthTimeline");
if (start < 0 || end < 0) throw new Error("Không tìm thấy engine trong file MVP");
const stubs = "function formatMillionShort(x){return String(x);} function formatPct(x){return String(x);}\n";
const eng = new Function(stubs + html.slice(start, end) + "\nreturn {FIN_ASSUMPTIONS, evaluateBuyVsRent};")();
const cases = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const out = cases.map((c) => {
  const r = eng.evaluateBuyVsRent({ total_price_vnd: c.purchase_price }, { rent_monthly_vnd: c.monthly_rent }, c.income_1, c.income_2,
    c.savings, c.living_cost, c.existing_debt, c.term, 1, eng.FIN_ASSUMPTIONS);
  const nw = (m) => [r.net_worth.buy_series ? r.net_worth.buy_series[m - 1].net_worth_buy : null, r.net_worth.rent_series[m - 1].net_worth_rent];
  return { decision: r.decision, buy_error: r.buy.error !== null, min_down: r.buy.min_down_payment, required_loan: r.buy.required_loan,
           buy_sm: r.buy.safety_margin, buy_safe: r.buy.is_safe, buy_mr: r.buy.money_remaining, pgw: r.buy.post_grace_worst_month,
           rent_sm: r.rent.safety_margin, rent_safe: r.rent.is_safe, be: r.net_worth.break_even_month,
           nw: [1, 12, 25, 60, 61, 120, c.term].map(nw) };
});
process.stdout.write(JSON.stringify(out));
