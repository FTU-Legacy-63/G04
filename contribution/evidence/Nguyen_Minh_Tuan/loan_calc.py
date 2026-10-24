"""LOAN_CALC (B4) + Net worth BUY/RENT (B5) — engine vector hoá bằng numpy.

Port từ MVP JS (Week 6 'MVP sau chỉnh sửa.html': loanCalc / netWorthRentSchedule / findBreakEven) với các thay đổi
theo to-do 2026-09-25:
  (1) loan_term_months là THAM SỐ BẮT BUỘC (B3.1, edge case 3) — không đọc hằng số toàn cục.
  (2) Phí trả nợ trước hạn theo năm vay (B4): mỗi tháng có prepayment_fee_pct / prepayment_fee_vnd / payoff_amount;
      Net worth BUY cơ sở 'liquidation' = giá trị nhà − (dư nợ + phí nếu tất toán tại tháng t) + khoản đầu tư.
  (3) Các biến tốc độ nhận scalar HOẶC ma trận (n_paths × n_years) → cùng 1 engine cho tất định (n=1) và Monte Carlo.
      Nhờ vậy B5.1 Phương án 2 (tăng giá suy giảm theo năm) KHÔNG cần sửa engine: chỉ truyền đường f(year).
Với LEGACY_MVP_OVERRIDES (tắt tăng trưởng, basis='book', không phí) kết quả trùng MVP JS — xem tests/test_parity_mvp.py.
"""
import math

import numpy as np

from .fin_assumptions import FIN_ASSUMPTIONS, portfolio_return_pct

SERIES_FIELDS = (
    "month", "annual_rate_pct", "balance_start", "principal_payment", "interest_payment", "monthly_repayment",
    "balance_end", "prepayment_fee_pct", "prepayment_fee_vnd", "payoff_amount", "money_remaining_buy",
    "invested_balance_buy", "property_value", "net_worth_buy", "safety_margin_buy", "income", "living_cost",
    "monthly_rent", "money_remaining_rent", "net_worth_rent", "safety_margin_rent",
)


def get_safety_margin_min_pct(total_income):
    """Mục 4: ngưỡng safety margin theo tổng thu nhập hộ (40/35/30/25%)."""
    trieu = total_income / 1_000_000
    if trieu < 35:
        return 0.40
    if trieu < 50:
        return 0.35
    if trieu < 75:
        return 0.30
    return 0.25


def annual_rate_pct_at(month, assumptions, float_ref_pct=None):
    """Lãi suất %/năm áp dụng tháng `month` (1-indexed): promo → ref+margin năm 1 → ref+margin từ năm 2."""
    ref = assumptions["interest_rate_float_ref_pct"] if float_ref_pct is None else float_ref_pct
    promo = assumptions["promo_period_months"]
    if month <= promo:
        return assumptions["interest_rate_promo_pct"]
    if month <= promo + 12:
        return ref + assumptions["float_rate_margin_year1_pct"]
    return ref + assumptions["float_rate_margin_from_year2_pct"]


def prepayment_fee_pct_at(month, assumptions):
    """B4: % phí nếu tất toán TOÀN BỘ dư nợ ở cuối tháng `month`. Năm vay = ceil(month/12). Hết lịch = 0%."""
    schedule = assumptions.get("prepayment_fee_pct_by_loan_year") or []
    loan_year_index = (month - 1) // 12
    return float(schedule[loan_year_index]) if 0 <= loan_year_index < len(schedule) else 0.0


def _as_path_vector(x, n, name):
    arr = np.asarray(x, dtype=float)
    if arr.ndim == 0:
        return np.full(n, float(arr))
    if arr.shape == (n,):
        return arr.astype(float)
    raise ValueError(f"{name}: cần scalar hoặc shape ({n},), nhận {arr.shape}")


def _as_year_matrix(x, n, years, name):
    arr = np.asarray(x, dtype=float)
    if arr.ndim == 0:
        return np.full((n, years), float(arr))
    if arr.ndim == 1 and arr.shape[0] >= years:  # đường %/năm dùng chung mọi path (B5.1 PA2); dài hơn thì cắt
        return np.repeat(arr[None, :years].astype(float), n, axis=0)
    if arr.ndim == 2 and arr.shape == (n, years):
        return arr
    if arr.ndim == 2 and arr.shape == (1, years):
        return np.repeat(arr, n, axis=0)
    raise ValueError(f"{name}: cần scalar hoặc shape ({n}, {years}) / (1, {years}), nhận {arr.shape}")


def _year_multipliers(growth_pct):
    """Hệ số năm y = Π_{k<y}(1+g_k): năm đầu = 1, tăng bậc thang mỗi 12 tháng."""
    g = 1.0 + growth_pct / 100.0
    mult = np.ones_like(g)
    if g.shape[1] > 1:
        mult[:, 1:] = np.cumprod(g[:, :-1], axis=1)
    return mult


def js_round(x):
    """Math.round của JS cho số dương (làm tròn .5 lên) — Python round() là banker's rounding."""
    return int(math.floor(x + 0.5))


def simulate(inputs, loan_term_months, assumptions=None, *, n_paths=1, float_ref_pct=None, appreciation_pct=None,
             rent_growth_pct=None, income_growth_pct=None, living_cost_growth_pct=None,
             investment_return_pct=None, keep_series=None):
    """Chạy LOAN_CALC + Net worth BUY/RENT theo tháng cho n_paths đường song song.

    inputs: purchase_price, savings, income_1, income_2 (opt), living_cost, existing_debt (opt), monthly_rent.
    Tốc độ (%/năm): scalar hoặc ma trận (n_paths, n_years) [float_ref_pct: scalar hoặc (n_paths,)].
    Mặc định lấy từ assumptions; investment_return_pct mặc định = danh mục investment_allocation_default.
    """
    if loan_term_months is None:
        raise TypeError("loan_term_months là tham số bắt buộc (B3.1) — lấy từ calc_max_loan_term()/lựa chọn user")
    a = FIN_ASSUMPTIONS if assumptions is None else assumptions
    T, n = int(loan_term_months), int(n_paths)
    if T <= 0 or n <= 0:
        raise ValueError("loan_term_months và n_paths phải > 0")
    Y = math.ceil(T / 12)
    keep_series = (n == 1) if keep_series is None else bool(keep_series)

    P, S = float(inputs["purchase_price"]), float(inputs["savings"])
    I0 = float(inputs["income_1"]) + float(inputs.get("income_2") or 0.0)
    L0, D = float(inputs["living_cost"]), float(inputs.get("existing_debt") or 0.0)
    R0 = float(inputs["monthly_rent"])
    if not math.isfinite(I0) or I0 <= 0:
        raise ValueError("Tổng thu nhập (income_1 + income_2) phải > 0 để tính safety margin")
    for name, v in (("purchase_price", P), ("savings", S), ("living_cost", L0), ("existing_debt", D), ("monthly_rent", R0)):
        if not math.isfinite(v) or v < 0:
            raise ValueError(f"{name} không hợp lệ: {v}")

    ref = _as_path_vector(a["interest_rate_float_ref_pct"] if float_ref_pct is None else float_ref_pct, n, "float_ref_pct")
    app = _as_year_matrix(a["property_annual_appreciation_pct"] if appreciation_pct is None else appreciation_pct, n, Y, "appreciation_pct")
    rg = _as_year_matrix(a.get("rent_annual_growth_pct", 0.0) if rent_growth_pct is None else rent_growth_pct, n, Y, "rent_growth_pct")
    ig = _as_year_matrix(a.get("income_annual_growth_pct", 0.0) if income_growth_pct is None else income_growth_pct, n, Y, "income_growth_pct")
    lg = _as_year_matrix(a.get("living_cost_annual_growth_pct", 0.0) if living_cost_growth_pct is None else living_cost_growth_pct, n, Y, "living_cost_growth_pct")
    if investment_return_pct is None:
        investment_return_pct = portfolio_return_pct(a["investment_allocation_default"], a["investment_channels"])
    inv = _as_year_matrix(investment_return_pct, n, Y, "investment_return_pct")
    m_inc, m_liv, m_rent = _year_multipliers(ig), _year_multipliers(lg), _year_multipliers(rg)

    ltv, closing = float(a["max_loan_to_value_pct"]), float(a.get("buy_closing_costs_pct", 0.0))
    grace, promo = int(a["grace_period_months"]), int(a["promo_period_months"])
    r_promo = float(a["interest_rate_promo_pct"])
    m1, m2 = float(a["float_rate_margin_year1_pct"]), float(a["float_rate_margin_from_year2_pct"])
    basis = a.get("net_worth_basis", "liquidation")
    if basis not in ("liquidation", "book"):
        raise ValueError("net_worth_basis phải là 'liquidation' hoặc 'book'")

    # ---- LOAN_CALC: điều kiện vay (giữ nguyên logic MVP JS: min down gồm phí giao dịch) ----
    min_down = P * (1 - ltv / 100) + P * (closing / 100)
    buy_error = None
    if S < min_down:
        buy_error = (f"Cần thêm ít nhất {min_down - S:,.0f} VNĐ tiết kiệm để đủ điều kiện vay "
                     f"(LTV tối đa {ltv:g}%, đã gồm phí giao dịch {closing:g}%).")
    elif T - grace <= 0:
        buy_error = f"grace_period_months ({grace}) ≥ loan_term_months ({T}) — không hợp lệ."
    buy_ok = buy_error is None
    loan = max(0.0, P - S) if buy_ok else None
    excess = max(0.0, S - P) if buy_ok else None
    principal_fixed = (loan / (T - grace)) if buy_ok else 0.0
    threshold = get_safety_margin_min_pct(I0)

    timeline_months = [min(y * 12, T) for y in range(1, Y + 1)]
    year_slot = {m: i for i, m in enumerate(timeline_months)}
    V = np.full(n, P)
    inv_b = np.full(n, excess if buy_ok else 0.0)
    inv_r = np.full(n, S)
    bal = loan if buy_ok else 0.0

    def _init_agg():
        return {"min_margin": np.full(n, np.inf), "min_margin_month": np.zeros(n, dtype=int),
                "min_money_remaining": np.full(n, np.inf), "any_negative_cashflow": np.zeros(n, dtype=bool),
                "any_negative_balance": np.zeros(n, dtype=bool)}
    agg_b, agg_r = _init_agg(), _init_agg()

    def _update(agg, margin, mr, t):
        better = margin < agg["min_margin"]
        agg["min_margin"] = np.where(better, margin, agg["min_margin"])
        agg["min_margin_month"] = np.where(better, t, agg["min_margin_month"])
        agg["min_money_remaining"] = np.minimum(agg["min_money_remaining"], mr)
        agg["any_negative_cashflow"] |= mr < 0

    yearly_b = np.full((n, Y), np.nan) if buy_ok else None
    yearly_r = np.full((n, Y), np.nan)
    be_month = np.zeros(n, dtype=int)
    prev_diff = None
    series = {f: [] for f in SERIES_FIELDS} if keep_series else None
    nw_b = None

    for t in range(1, T + 1):
        y = (t - 1) // 12
        inc = I0 * m_inc[:, y]
        liv = L0 * m_liv[:, y]
        rent = R0 * m_rent[:, y]
        r_inv = inv[:, y] / 100.0 / 12.0
        # ---- RENT (công thức đóng của MVP viết dạng đệ quy; trùng khi không tăng trưởng) ----
        mrr = inc - liv - D - rent
        inv_r = inv_r * (1.0 + r_inv) + mrr
        agg_r["any_negative_balance"] |= inv_r < 0  # cạn tiết kiệm → phải vay ngoài để chi tiêu
        margin_r = mrr / inc
        _update(agg_r, margin_r, mrr, t)
        # ---- BUY ----
        if buy_ok:
            if t <= promo:
                r_ann = np.full(n, r_promo)
            elif t <= promo + 12:
                r_ann = ref + m1
            else:
                r_ann = ref + m2
            bal_start = bal
            princ = 0.0 if t <= grace else principal_fixed
            interest = bal_start * ((r_ann / 100.0) / 12.0)
            pay = princ + interest
            bal = bal_start - princ
            if t == T and abs(bal) < 1e-6 * max(1.0, loan):
                bal = 0.0
            mrb = inc - liv - D - pay
            inv_b = inv_b * (1.0 + r_inv) + mrb
            agg_b["any_negative_balance"] |= inv_b < 0
            V = V * (1.0 + app[:, y] / 100.0) ** (1.0 / 12.0)
            fee_pct = prepayment_fee_pct_at(t, a) if basis == "liquidation" else 0.0
            fee_vnd = bal * fee_pct / 100.0
            payoff = bal + fee_vnd
            nw_b = V - payoff + inv_b
            margin_b = mrb / inc
            _update(agg_b, margin_b, mrb, t)
            diff = nw_b - inv_r  # break-even theo đúng ngữ nghĩa findBreakEven() của MVP
            if prev_diff is not None:
                crossed = (prev_diff != 0) & (diff != 0) & (np.sign(prev_diff) != np.sign(diff))
                hit = (be_month == 0) & (crossed | (diff == 0))
                be_month = np.where(hit, t, be_month)
            prev_diff = diff
        if t in year_slot:
            yearly_r[:, year_slot[t]] = inv_r
            if buy_ok:
                yearly_b[:, year_slot[t]] = nw_b
        if keep_series:
            s = series
            s["month"].append(t)
            s["income"].append(float(inc[0])); s["living_cost"].append(float(liv[0]))
            s["monthly_rent"].append(float(rent[0])); s["money_remaining_rent"].append(float(mrr[0]))
            s["net_worth_rent"].append(float(inv_r[0])); s["safety_margin_rent"].append(float(margin_r[0]))
            if buy_ok:
                s["annual_rate_pct"].append(float(r_ann[0])); s["balance_start"].append(float(bal_start))
                s["principal_payment"].append(float(princ)); s["interest_payment"].append(float(interest[0]))
                s["monthly_repayment"].append(float(pay[0])); s["balance_end"].append(float(bal))
                s["prepayment_fee_pct"].append(fee_pct); s["prepayment_fee_vnd"].append(float(fee_vnd))
                s["payoff_amount"].append(float(payoff)); s["money_remaining_buy"].append(float(mrb[0]))
                s["invested_balance_buy"].append(float(inv_b[0])); s["property_value"].append(float(V[0]))
                s["net_worth_buy"].append(float(nw_b[0])); s["safety_margin_buy"].append(float(margin_b[0]))

    def _pack(agg):
        out = dict(agg)
        out["safe_all_months"] = agg["min_margin"] >= threshold
        return out

    buy = {"error": buy_error, "min_down_payment": min_down, "required_loan": loan, "excess_cash": excess}
    if buy_ok:
        buy.update(_pack(agg_b))
        buy["final_net_worth"] = nw_b
        buy["yearly_net_worth"] = yearly_b
    rent_out = _pack(agg_r)
    rent_out["final_net_worth"] = inv_r
    rent_out["yearly_net_worth"] = yearly_r
    return {
        "n_paths": n, "loan_term_months": T, "years": Y, "timeline_months": timeline_months,
        "safety_margin_min_pct": threshold, "total_income_initial": I0,
        "buy": buy, "rent": rent_out,
        "break_even_month": be_month if buy_ok else None,
        "series": series,
    }


def amortization_schedule(sim):
    """Bảng AMORTIZATION_SCHEDULE (list dict, 1 dòng/tháng) từ kết quả simulate(n=1) — cho UI/kiểm tra."""
    s = sim["series"]
    if s is None or sim["buy"]["error"]:
        return []
    keys = ("month", "annual_rate_pct", "balance_start", "principal_payment", "interest_payment",
            "monthly_repayment", "balance_end", "prepayment_fee_pct", "prepayment_fee_vnd", "payoff_amount")
    return [dict(zip(keys, row)) for row in zip(*(s[k] for k in keys))]
