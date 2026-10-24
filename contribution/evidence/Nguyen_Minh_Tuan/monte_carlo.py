"""B8 — Monte Carlo (FINAL PLAN §B8 + cập nhật 2026-09-25; Spec §7).

Mỗi lần lặp: rút ngẫu nhiên Normal(mean theo scenario, std) cho từng biến → chạy lại B4-B5 (cùng engine vector hoá
loan_calc.simulate — tất cả N đường chạy song song) → tổng hợp % an toàn suốt kỳ, P10/P50/P90, histogram.

Cách rút mẫu (cần team xác nhận — Q8):
  - Biến vĩ mô trong plan (lãi thả nổi σ0.75, tăng giá BĐS σ4, tăng giá thuê σ1.25): 'per_path' đúng như plan
    (1 giá trị/đường, giữ cố định suốt kỳ).
  - Kênh đầu tư có std là BIẾN ĐỘNG NĂM (chứng khoán σ≈19%, vàng σ≈14%): 'per_year'. Nếu rút 1 lần/đường với σ năm
    thì ~16% số đường có lợi suất chứng khoán cố định < −11%/năm suốt 30 năm → phân phối vô lý.
  - Thu nhập: tăng trưởng theo năm 'per_year' (σ = std tăng trưởng thu nhập NSO), mean = income_annual_growth_pct.
  - std = 0 ⇒ tắt random hoá biến đó (đúng cách giả lập ghi trong to-do).
"% bankrupt" (README hứa) — 2 thước đo: (a) có ≥1 tháng money_remaining < 0; (b) CẠN TIẾT KIỆM: số dư đầu tư < 0 ở
bất kỳ tháng nào (engine kế thừa MVP coi phần thiếu hụt là "số dư âm" sinh lãi như danh mục = vay vô hạn) → (b) là
thước đo chính; "% thắng" nên đọc kèm "% thắng VÀ không cạn tiết kiệm".
"""
import math

import numpy as np

from .fin_assumptions import (FIN_ASSUMPTIONS, MC_N_DEFAULT, MC_N_FINAL, MC_N_PRESETS, MC_N_WARN_BELOW, MC_STD,
                              apply_scenario, validate_allocation)
from .loan_calc import js_round, simulate


def resolve_n(n=None, *, final_run=False):
    """N là tham số hệ thống: mặc định 1000; bản nộp cuối 10.000; nếu cho user chọn thì CHỈ preset 500/1000/2000."""
    if final_run:
        return MC_N_FINAL
    if n is None:
        return MC_N_DEFAULT
    if isinstance(n, bool) or n not in MC_N_PRESETS:
        raise ValueError(f"N phải chọn từ preset {MC_N_PRESETS} (không cho nhập tự do); "
                         f"bản nộp cuối dùng final_run=True → N={MC_N_FINAL}")
    return int(n)


def n_warning(n):
    if n < MC_N_WARN_BELOW:
        return f"N={n} < {MC_N_WARN_BELOW}: phân phối kém mượt, P10/P50/P90 kém tin cậy."
    return None


def _draw(rng, mean, std, sampling, n, years):
    if mean is None or std is None:
        raise ValueError("Thiếu mean/std (TODO: chờ data) — không thể random hoá biến này")
    m = np.asarray(mean, dtype=float)
    if m.ndim == 1:  # mean là đường theo năm (VD B5.1 PA2: tăng giá giảm dần)
        if m.shape[0] < years:
            raise ValueError("Đường mean theo năm ngắn hơn số năm mô phỏng")
        m = m[None, :years]
    elif m.ndim != 0:
        raise ValueError("mean phải là scalar hoặc đường theo năm (1 chiều)")
    if sampling == "per_path":  # cú sốc rút 1 lần/đường, cộng vào mọi năm
        return np.broadcast_to(m + rng.normal(0.0, std, size=(n, 1)), (n, years)).copy()
    if sampling == "per_year":
        return m + rng.normal(0.0, std, size=(n, years))
    raise ValueError("sampling phải là 'per_path' hoặc 'per_year'")


def sample_paths(assumptions, n, years, rng, allocation, mc_std=None):
    """Rút mẫu toàn bộ biến ngẫu nhiên cho n đường (thứ tự rút cố định → tái lập được với cùng seed)."""
    s = MC_STD if mc_std is None else mc_std
    a = assumptions
    ref = rng.normal(a["interest_rate_float_ref_pct"], s["interest_rate_float_ref_pct"]["std"], size=n)
    app = _draw(rng, a["property_annual_appreciation_pct"], s["property_annual_appreciation_pct"]["std"],
                s["property_annual_appreciation_pct"]["sampling"], n, years)
    rg = _draw(rng, a["rent_annual_growth_pct"], s["rent_annual_growth_pct"]["std"],
               s["rent_annual_growth_pct"]["sampling"], n, years)
    ig = _draw(rng, a["income_annual_growth_pct"], s["income_annual_growth_pct"]["std"],
               s["income_annual_growth_pct"]["sampling"], n, years)
    w = validate_allocation(allocation, a["investment_channels"])
    inv = np.zeros((n, years))
    for c, wc in w.items():
        if wc > 0:
            ch = a["investment_channels"][c]
            inv += wc * _draw(rng, ch["return_pct"], ch["std_dev_pct"], ch.get("sampling", "per_year"), n, years)
    return {"float_ref_pct": ref, "appreciation_pct": app, "rent_growth_pct": rg,
            "income_growth_pct": ig, "investment_return_pct": inv}


def _dist(x, bins):
    x = np.asarray(x, dtype=float)
    counts, edges = np.histogram(x, bins=bins)
    return {"p10": float(np.percentile(x, 10)), "p50": float(np.percentile(x, 50)), "p90": float(np.percentile(x, 90)),
            "mean": float(x.mean()), "histogram": {"counts": counts.tolist(), "edges": edges.tolist()}}


def run_monte_carlo(inputs, loan_term_months, *, assumptions=None, scenario="stable", allocation=None, n=None,
                    final_run=False, seed=None, hist_bins=30, mc_std=None):
    """Chạy B8. Trả dict tổng hợp (không trả toàn bộ chuỗi tháng để tiết kiệm bộ nhớ)."""
    a = apply_scenario(FIN_ASSUMPTIONS if assumptions is None else assumptions, scenario)
    N = resolve_n(n, final_run=final_run)
    alloc = a["investment_allocation_default"] if allocation is None else allocation
    years = math.ceil(int(loan_term_months) / 12)
    rng = np.random.default_rng(seed)
    paths = sample_paths(a, N, years, rng, alloc, mc_std)
    sim = simulate(inputs, loan_term_months, a, n_paths=N, keep_series=False, **paths)
    b, r = sim["buy"], sim["rent"]
    out = {"n": N, "scenario": scenario, "seed": seed, "n_warning": n_warning(N),
           "loan_term_months": int(loan_term_months), "safety_margin_min_pct": sim["safety_margin_min_pct"],
           "timeline_months": sim["timeline_months"],
           "rent": {"pct_safe_all_months": float(r["safe_all_months"].mean()),
                    "pct_negative_cashflow_any_month": float(r["any_negative_cashflow"].mean()),
                    "pct_savings_exhausted_any_month": float(r["any_negative_balance"].mean()),
                    "final_net_worth": _dist(r["final_net_worth"], hist_bins),
                    "min_money_remaining": _dist(r["min_money_remaining"], hist_bins),
                    "yearly_p10_p50_p90": np.percentile(r["yearly_net_worth"], [10, 50, 90], axis=0).T.tolist()}}
    if b["error"]:
        out["buy"] = {"error": b["error"], "min_down_payment": b["min_down_payment"]}
        out["comparison"] = None
        return out
    out["buy"] = {"pct_safe_all_months": float(b["safe_all_months"].mean()),
                  "pct_negative_cashflow_any_month": float(b["any_negative_cashflow"].mean()),
                  "pct_savings_exhausted_any_month": float(b["any_negative_balance"].mean()),
                  "final_net_worth": _dist(b["final_net_worth"], hist_bins),
                  "min_money_remaining": _dist(b["min_money_remaining"], hist_bins),
                  "yearly_p10_p50_p90": np.percentile(b["yearly_net_worth"], [10, 50, 90], axis=0).T.tolist()}
    diff = b["final_net_worth"] - r["final_net_worth"]
    be = sim["break_even_month"]
    has_be = be > 0
    out["comparison"] = {
        "pct_buy_wins": float((diff > 0).mean()), "pct_rent_wins": float((diff < 0).mean()),
        "pct_buy_wins_and_buy_solvent": float(((diff > 0) & ~b["any_negative_balance"]).mean()),
        "pct_rent_wins_and_rent_solvent": float(((diff < 0) & ~r["any_negative_balance"]).mean()),
        "net_worth_diff_buy_minus_rent": _dist(diff, hist_bins),
        "pct_paths_with_break_even": float(has_be.mean()),
        "median_break_even_year": js_round(float(np.median(be[has_be])) / 12) if has_be.any() else None,
    }
    return out
