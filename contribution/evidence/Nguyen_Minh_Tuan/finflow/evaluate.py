"""Safety margin BUY/RENT, quyết định BUY/RENT/NEITHER, break-even — port từ MVP JS (evaluateBuy/evaluateRent/decide/
findBreakEven/buildNetWorthTimeline), nối với B3.1 (loan term theo tuổi), gói ưu đãi, phân bổ 4 kênh."""
import math
from functools import reduce

from .fin_assumptions import FIN_ASSUMPTIONS, apply_promo_package, portfolio_return_pct
from .loan_calc import amortization_schedule, js_round, simulate
from .loan_term import calc_max_loan_term, validate_loan_term


def evaluate_buy(sim, assumptions):
    """Port evaluateBuy(): quét TOÀN BỘ lịch trả nợ, lấy tháng tệ nhất theo 3 giai đoạn (promo / thả nổi trong ân hạn
    / sau ân hạn). Headline = tháng tệ nhất trên toàn kỳ."""
    b, s = sim["buy"], sim["series"]
    thr = sim["safety_margin_min_pct"]
    base = {"error": b["error"], "min_down_payment": b["min_down_payment"], "safety_margin_min_pct": thr}
    if b["error"]:
        base.update({"required_loan": None, "monthly_repayment": None, "money_remaining": None, "safety_margin": None,
                     "is_safe": None, "net_worth_series": None, "stage_promo": None, "stage_floating_grace": None,
                     "stage_post_grace": None, "post_grace_worst_month": None})
        return base
    grace = int(assumptions["grace_period_months"])
    promo_end = min(int(assumptions["promo_period_months"]), grace)
    promo_w = fg_w = post_w = None
    for m, rate, pay, mr, sm in zip(s["month"], s["annual_rate_pct"], s["monthly_repayment"],
                                   s["money_remaining_buy"], s["safety_margin_buy"]):
        ev = {"month": m, "annual_rate_pct": rate, "monthly_repayment": pay, "money_remaining": mr,
              "safety_margin": sm, "is_safe": sm >= thr}
        if m <= promo_end:
            if promo_w is None or sm < promo_w["safety_margin"]:
                promo_w = ev
        elif m <= grace:
            if fg_w is None or sm < fg_w["safety_margin"]:
                fg_w = ev
        elif post_w is None or sm < post_w["safety_margin"]:
            post_w = ev
    cands = [x for x in (promo_w, fg_w) if x is not None]
    grace_eval = reduce(lambda p, q: p if p["safety_margin"] <= q["safety_margin"] else q, cands) if cands else post_w
    post_eval = post_w or grace_eval
    grace_worse = grace_eval["safety_margin"] <= post_eval["safety_margin"]
    worst = grace_eval if grace_worse else post_eval

    def stage(ev, start, end):
        return None if ev is None else dict(ev, range_start=start, range_end=end)

    base.update({
        "required_loan": b["required_loan"],
        "monthly_repayment": worst["monthly_repayment"],
        "money_remaining": worst["money_remaining"],
        "safety_margin": min(grace_eval["safety_margin"], post_eval["safety_margin"]),
        "is_safe": bool(grace_eval["is_safe"] and post_eval["is_safe"]),
        "net_worth_series": [{"month": m, "net_worth_buy": v} for m, v in zip(s["month"], s["net_worth_buy"])],
        "stage_promo": stage(promo_w, 1, promo_end),
        "stage_floating_grace": stage(fg_w, promo_end + 1, grace),
        "stage_post_grace": stage(post_w, grace + 1, len(s["month"])),
        "post_grace_worst_month": post_eval["month"],
    })
    return base


def evaluate_rent(sim):
    """RENT: tháng 1 (như MVP) + tháng tệ nhất trên toàn kỳ. Headline = tháng tệ nhất (trùng tháng 1 khi không có
    tăng trưởng; khi bật rent/income growth thì phản ánh đúng rủi ro cuối kỳ)."""
    s, thr = sim["series"], sim["safety_margin_min_pct"]
    i = min(range(len(s["month"])), key=lambda k: (s["safety_margin_rent"][k], k))
    return {
        "monthly_rent": s["monthly_rent"][0],
        "month1_money_remaining": s["money_remaining_rent"][0],
        "month1_safety_margin": s["safety_margin_rent"][0],
        "worst_month": s["month"][i],
        "money_remaining": s["money_remaining_rent"][i],
        "safety_margin": s["safety_margin_rent"][i],
        "safety_margin_min_pct": thr,
        "is_safe": bool(s["safety_margin_rent"][i] >= thr),
        "net_worth_series": [{"month": m, "net_worth_rent": v} for m, v in zip(s["month"], s["net_worth_rent"])],
    }


def decide(buy, rent):
    """Port decide() của MVP (locked decision note #2: ưu tiên BUY khi BUY đạt ngưỡng)."""
    if buy["error"] is not None:
        if rent["is_safe"]:
            return "RENT", "BUY không khả thi do thiếu tiết kiệm — RENT đạt ngưỡng an toàn."
        return "NEITHER", "BUY không khả thi do thiếu tiết kiệm, RENT cũng không đạt ngưỡng an toàn."
    bm, rm = buy["safety_margin"], rent["safety_margin"]
    note = (" (Lưu ý: safety margin của BUY và RENT khá sát nhau — nên cân nhắc thêm yếu tố ngoài mô hình.)"
            if buy["is_safe"] and rent["is_safe"] and abs(bm - rm) < 0.05 else "")
    if buy["is_safe"]:
        return "BUY", "BUY đạt ngưỡng an toàn." + note
    if rent["is_safe"]:
        return "RENT", "RENT đạt ngưỡng an toàn (BUY không đạt)." + note
    if buy["money_remaining"] >= 0 and rent["money_remaining"] >= 0:
        if bm > rm:
            return "NEITHER", f"Cả hai chưa đạt ngưỡng, nhưng BUY có safety margin cao hơn ({bm:.1%} so với {rm:.1%})."
        if rm > bm:
            return "NEITHER", f"Cả hai chưa đạt ngưỡng, nhưng RENT có safety margin cao hơn ({rm:.1%} so với {bm:.1%})."
        return "NEITHER", f"Cả hai chưa đạt ngưỡng (cùng safety margin {bm:.1%})."
    return "NEITHER", "Cả BUY và RENT đều không đạt ngưỡng an toàn."


def find_break_even(buy_series, rent_series):
    """Port findBreakEven(): tháng đầu tiên chênh lệch Net worth BUY−RENT đổi dấu (hoặc = 0)."""
    if not buy_series or not rent_series:
        return None, None
    rent_by_month = {r["month"]: r["net_worth_rent"] for r in rent_series}
    prev = None
    for row in buy_series:
        m = row["month"]
        if m not in rent_by_month:
            continue
        diff = row["net_worth_buy"] - rent_by_month[m]
        if prev is not None and prev != 0 and diff != 0:
            if (prev < 0 < diff) or (prev > 0 > diff):
                return m, js_round(m / 12)
        elif prev is not None and diff == 0:
            return m, js_round(m / 12)
        prev = diff
    return None, None


def build_net_worth_timeline(sim):
    """Port buildNetWorthTimeline(): 1 điểm/năm, điểm cuối rơi đúng tháng cuối kỳ."""
    s = sim["series"]
    by_b = dict(zip(s["month"], s["net_worth_buy"])) if s["net_worth_buy"] else {}
    by_r = dict(zip(s["month"], s["net_worth_rent"]))
    return [{"year": i + 1, "month": m, "net_worth_buy": by_b.get(m), "net_worth_rent": by_r.get(m)}
            for i, m in enumerate(sim["timeline_months"])]


def evaluate_buy_vs_rent(inputs, loan_term_months, assumptions=None, *, ages=None, promo_months=None, allocation=None):
    """Hàm tổng hợp Step 3 → Step 4.

    ages=(age_1, age_2|None): nếu truyền → áp B3.1 (calc_max_loan_term + validate_loan_term), ném LoanTermError.
    promo_months ∈ {6,12,18,24}: áp gói ưu đãi (lỗi rõ ràng nếu gói chưa có lãi suất).
    allocation: phân bổ 4 kênh (tổng = 1) → lợi suất danh mục cho B5.
    """
    a = FIN_ASSUMPTIONS if assumptions is None else assumptions
    if promo_months is not None:
        a = apply_promo_package(a, promo_months)
    term_info = None
    if ages is not None:
        age_1, age_2 = (ages + (None,))[:2] if isinstance(ages, tuple) else (ages, None)
        term_info = calc_max_loan_term(age_1, age_2, a["bank_max_term_months"],
                                       max_age_at_maturity=a["max_borrower_age_at_maturity"],
                                       grace_period_months=a["grace_period_months"], min_age=a["min_borrower_age"])
        loan_term_months = validate_loan_term(loan_term_months, term_info["final_max_term_months"],
                                              a["grace_period_months"])
    inv_ret = portfolio_return_pct(allocation, a["investment_channels"]) if allocation is not None else None
    sim = simulate(inputs, loan_term_months, a, investment_return_pct=inv_ret, keep_series=True)
    buy, rent = evaluate_buy(sim, a), evaluate_rent(sim)
    decision, reason = decide(buy, rent)
    be_m = int(sim["break_even_month"][0]) if sim["break_even_month"] is not None and sim["break_even_month"][0] > 0 else None
    return {
        "buy": buy, "rent": rent, "decision": decision, "reason": reason,
        "loan_term_months": int(loan_term_months), "loan_term_info": term_info,
        "investment_return_pct": inv_ret if inv_ret is not None else portfolio_return_pct(
            a["investment_allocation_default"], a["investment_channels"]),
        "net_worth": {"break_even_month": be_m, "break_even_year": js_round(be_m / 12) if be_m else None,
                      "timeline": build_net_worth_timeline(sim)},
        "amortization_schedule": amortization_schedule(sim),
        "_sim": sim,
    }
