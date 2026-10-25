"""FIN_ASSUMPTIONS — schema mới theo FINAL PLAN (cập nhật 2026-09-25) §B3, §B3.1, §B4, §B8 và Spec 2026-09-25 §10.

Trạng thái mỗi giá trị:
  CHOT    (✅) đã chốt trong plan, có nguồn
  DE_XUAT (🟡) tính từ dữ liệu ngày 2026-09-29, chờ Coordinator + Finance duyệt
  TODO    (🔴) giả lập / chờ xác nhận — PHẢI xử lý trước khi nộp (checklist Giai đoạn 8)
Mọi giá trị chưa chốt có comment '# TODO(<mã>)'. Chạy list_open_todos() để rà toàn bộ.
Nguồn + cách tính: docs/sources.md, docs/assumptions.md, data/Supporting_data_v2.xlsx.
"""
from copy import deepcopy
from pathlib import Path
import re

# ===================== B3.1 — sửa ĐÚNG 1 DÒNG khi Finance xác nhận (to-do #1) =====================
BANK_MAX_TERM_MONTHS = 30 * 12  # TODO(#1): 360 = MB CN Vạn Phúc (khuyến nghị giữ). Nếu Finance chốt 35 năm → 35 * 12
MAX_BORROWER_AGE_AT_MATURITY = 75  # TODO(#1b): plan dùng 75; nguồn tổng hợp (TheBank) ghi MB = 70 → xin MB Vạn Phúc xác nhận
MIN_BORROWER_AGE = 18  # đủ 18 tuổi — điều kiện chung của các ngân hàng

# ===================== Gói lãi suất ưu đãi (Step 3: 6/12/18/24 tháng) =====================
PROMO_PACKAGES = {
    6: None,   # TODO(#promo): chưa có lãi suất gói 6 tháng trong văn bản MB CN Vạn Phúc
    12: 8.3,   # CHOT: MB CN Vạn Phúc (ảnh văn bản gốc)
    18: None,  # TODO(#promo): chưa có
    24: None,  # TODO(#promo): chưa có
}

# ===================== A3.1 — 4 kênh đầu tư (return_pct, std_dev_pct theo %/năm) =====================
# sampling: 'per_path' = rút 1 lần/đường (bất định về MỨC lãi suất dài hạn);
#           'per_year' = rút mỗi năm (biến động thị trường theo năm). Xem docs/KET_QUA_TODO.md mục B8.
INVESTMENT_CHANNELS = {
    "savings": {
        "return_pct": 6.50, "std_dev_pct": 0.82, "sampling": "per_path", "status": "DE_XUAT",  # TODO(#9): duyệt
        "method": "TB & std mẫu LSHĐ VND kỳ hạn 6-12 tháng (mức CAO NHẤT) cuối năm 2016-2025 + 25/09/2026, n=11",
        "caveat": "Dùng mức cao nhất thị trường → lệch lên so với Big4; chưa có snapshot chính thức theo NH/kỳ hạn.",
    },
    "stocks": {
        "return_pct": 7.99, "std_dev_pct": 19.30, "sampling": "per_year", "status": "DE_XUAT",  # TODO(#10): duyệt
        "method": "VN-Index đóng cửa tháng 05/2021-08/2026 (đã sửa lỗi autodate), 63 lợi suất tháng; TB×12, std×√12",
        "caveat": "Cửa sổ ~5 năm (có 2022 giảm mạnh, 2025 tăng 40,9%); chỉ số giá, chưa gồm cổ tức.",
    },
    "bonds": {
        "return_pct": 4.02, "std_dev_pct": 1.37, "sampling": "per_path", "status": "DE_XUAT",  # TODO(#11): duyệt
        "method": "Lợi suất TPCP 10 năm cuối năm 2016-2025 + 25/09/2026 (FiinPro), n=11",
        "caveat": "Giả định giữ đến đáo hạn (return ≈ lợi suất lúc mua); cá nhân khó mua trực tiếp TPCP.",
    },
    "gold": {
        "return_pct": 14.89, "std_dev_pct": 14.13, "sampling": "per_year", "status": "DE_XUAT",  # TODO(#12): duyệt
        "method": "Giá bán SJC cuối tháng 01/2016-09/2026 (FiinPro), 128 lợi suất tháng; TB×12, std×√12",
        "caveat": "Giai đoạn vàng tăng bất thường (2025: +81,5%); std Dec-to-Dec = 24,9%.",
    },
}
CHANNEL_NAMES = tuple(INVESTMENT_CHANNELS)

# ===================== B8 — độ lệch chuẩn Monte Carlo =====================
MC_STD = {
    "interest_rate_float_ref_pct": {"std": 0.75, "sampling": "per_path", "status": "CHOT"},
    "property_annual_appreciation_pct": {"std": 4.0, "sampling": "per_path", "status": "CHOT"},
    "rent_annual_growth_pct": {"std": 1.25, "sampling": "per_path", "status": "CHOT"},
    "income_annual_growth_pct": {"std": 5.68, "sampling": "per_year", "status": "DE_XUAT"},  # TODO(#8): duyệt — NSO KSMS 2019-2024
}
MC_N_DEFAULT = 1000       # chạy thường
MC_N_FINAL = 10000        # bản nộp cuối
MC_N_PRESETS = (500, 1000, 2000)  # nếu cho user chọn: CHỈ preset, không nhập tự do
MC_N_WARN_BELOW = 500

# ===================== B7 — kịch bản (placeholder theo khoảng trong plan; chốt ở Giai đoạn 5) =====================
SCENARIOS = {
    "boom": {"property_annual_appreciation_pct": 27.5, "rent_annual_growth_pct": 10.0,
             "max_loan_to_value_pct": 95, "float_ref_delta_pct": -0.75},  # TODO(B7): chốt số
    "stable": {"property_annual_appreciation_pct": None, "rent_annual_growth_pct": None,  # None = lấy FIN_ASSUMPTIONS
               "max_loan_to_value_pct": 80, "float_ref_delta_pct": 0.0},
    "downturn": {"property_annual_appreciation_pct": 2.5, "rent_annual_growth_pct": 4.0,
                 "max_loan_to_value_pct": 70, "float_ref_delta_pct": 0.75},  # TODO(B7): chốt số + income shock
}

FIN_ASSUMPTIONS = {
    # ---- Lãi vay (MB Bank – CN Vạn Phúc) ----
    "interest_rate_promo_pct": 8.3,            # CHOT (gói 12 tháng)
    "promo_period_months": 12,                 # CHOT
    "interest_rate_float_ref_pct": 8.3,        # TODO(Q4): Python cũ = 8.3, MVP JS = 10.5 → Finance chốt 1 số
    "float_rate_margin_year1_pct": 1.5,        # CHOT
    "float_rate_margin_from_year2_pct": 3.5,   # CHOT
    "rate_adjustment_frequency_months": 3,     # CHOT (engine tất định chưa dùng)
    "grace_period_months": 24,                 # CHOT
    "max_loan_to_value_pct": 80,               # CHOT (base case)
    "buy_closing_costs_pct": 2.6,              # giữ nguyên MVP JS — xem phát hiện F-3 (cách hạch toán)
    # ---- B3.1: KHÔNG còn 'Loan_term_months' hằng số — loan term là tham số truyền vào mỗi lần gọi ----
    "bank_max_term_months": BANK_MAX_TERM_MONTHS,
    "max_borrower_age_at_maturity": MAX_BORROWER_AGE_AT_MATURITY,
    "min_borrower_age": MIN_BORROWER_AGE,
    # ---- B4: phí trả nợ trước hạn theo NĂM VAY (phần tử 0 = năm 1). Hết danh sách = miễn phí ----
    "prepayment_fee_pct_by_loan_year": [1.0, 1.0, 1.0, 1.0, 1.0],  # TODO(#1c): theo to-do; nguồn công khai có gói MB bậc thang 2.5/2.5/2/1.5/1
    "net_worth_basis": "liquidation",          # 'liquidation' = Net worth BUY trừ phí nếu tất toán tại tháng t; 'book' = như MVP
    # ---- B5 ----
    "property_annual_appreciation_pct": 19.0,  # TODO(#3): plan PA1 = 18-20%; xem khuyến nghị docs/KET_QUA_TODO.md #3
    "rent_annual_growth_pct": 7.0,             # TODO(#7): mean 7% chờ nguồn (plan); bằng chứng 2023-2025: thuê tăng chậm hơn giá
    "income_annual_growth_pct": 4.87,          # TODO(#8): ĐỀ XUẤT MỚI — NSO KSMS 2019-2024 (bắt buộc đi kèm rent growth)
    "living_cost_annual_growth_pct": 3.09,     # TODO(#8b): ĐỀ XUẤT MỚI — CPI World Bank 2016-2025
    # ---- 4 kênh đầu tư (thay investment_return_pct = 6% cũ) ----
    "investment_channels": deepcopy(INVESTMENT_CHANNELS),
    "investment_allocation_default": {"savings": 1.0, "stocks": 0.0, "bonds": 0.0, "gold": 0.0},
}

# Bộ tham số tái tạo đúng hành vi MVP Week 6 (dùng cho kiểm tra đối chiếu / so sánh trước-sau)
LEGACY_MVP_OVERRIDES = {
    "interest_rate_float_ref_pct": 10.5, "property_annual_appreciation_pct": 12.0,
    "rent_annual_growth_pct": 0.0, "income_annual_growth_pct": 0.0, "living_cost_annual_growth_pct": 0.0,
    "prepayment_fee_pct_by_loan_year": [], "net_worth_basis": "book",
}


def appreciation_decay_path(g0_pct, g_inf_pct, tau_years, years=35):
    """B5.1 Phương án 2 (bản rút gọn): g(t) = g∞ + (g0 − g∞)·e^(−t/τ), t = 0, 1, … (năm). Trả list %/năm.
    Gán list này vào property_annual_appreciation_pct là engine tất định + Monte Carlo dùng được ngay."""
    import math
    if tau_years <= 0:
        raise ValueError("tau_years phải > 0")
    return [g_inf_pct + (g0_pct - g_inf_pct) * math.exp(-t / tau_years) for t in range(int(years))]


def get_assumptions(**overrides):
    """Bản sao FIN_ASSUMPTIONS có ghi đè; báo lỗi nếu field không tồn tại (tránh gõ sai tên)."""
    a = deepcopy(FIN_ASSUMPTIONS)
    for key, value in overrides.items():
        if key not in a:
            raise KeyError(f"Không có field '{key}' trong FIN_ASSUMPTIONS")
        a[key] = deepcopy(value)
    return a


def apply_promo_package(assumptions, promo_months):
    if promo_months not in PROMO_PACKAGES:
        raise ValueError(f"Kỳ hạn ưu đãi phải là một trong {sorted(PROMO_PACKAGES)} tháng, nhận {promo_months!r}")
    rate = PROMO_PACKAGES[promo_months]
    if rate is None:
        raise ValueError(f"Chưa có lãi suất cho gói ưu đãi {promo_months} tháng (TODO #promo — cần văn bản MB CN Vạn Phúc)")
    a = deepcopy(assumptions)
    a["promo_period_months"] = promo_months
    a["interest_rate_promo_pct"] = rate
    return a


def apply_scenario(assumptions, scenario):
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario phải là một trong {list(SCENARIOS)}")
    a = deepcopy(assumptions)
    s = SCENARIOS[scenario]
    for key in ("property_annual_appreciation_pct", "rent_annual_growth_pct", "max_loan_to_value_pct"):
        if s[key] is not None:
            a[key] = s[key]
    a["interest_rate_float_ref_pct"] = a["interest_rate_float_ref_pct"] + s["float_ref_delta_pct"]
    return a


def validate_allocation(allocation, channels=None):
    """Phân bổ 4 kênh: không âm, tổng = 100%, kênh có tỷ trọng > 0 phải có dữ liệu."""
    channels = INVESTMENT_CHANNELS if channels is None else channels
    unknown = set(allocation) - set(channels)
    if unknown:
        raise ValueError(f"Kênh đầu tư không hợp lệ: {sorted(unknown)}")
    w = {c: float(allocation.get(c, 0.0)) for c in channels}
    if any(x < 0 for x in w.values()):
        raise ValueError("Tỷ trọng phân bổ không được âm")
    total = sum(w.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Tổng phân bổ 4 kênh phải bằng 100%, hiện là {total * 100:.2f}%")
    for c, x in w.items():
        if x > 0 and (channels[c].get("return_pct") is None or channels[c].get("std_dev_pct") is None):
            raise ValueError(f"Kênh '{c}' chưa có dữ liệu return/std (TODO: chờ data) — không thể phân bổ > 0%")
    return w


def portfolio_return_pct(allocation, channels=None):
    """Lợi suất kỳ vọng danh mục = Σ w_i × return_i (dùng cho B5 tất định)."""
    channels = INVESTMENT_CHANNELS if channels is None else channels
    w = validate_allocation(allocation, channels)
    return sum(w[c] * channels[c]["return_pct"] for c in w if w[c] > 0)


def validate_assumptions(a=None):
    """Danh sách cảnh báo nhất quán — chạy trước khi merge/nộp."""
    a = FIN_ASSUMPTIONS if a is None else a
    warnings = []
    if "Loan_term_months" in a:
        warnings.append("Còn field 'Loan_term_months' hằng số — B3.1 yêu cầu bỏ")
    if a.get("rent_annual_growth_pct", 0) > 0 and a.get("income_annual_growth_pct", 0) == 0:
        warnings.append("rent_annual_growth_pct > 0 nhưng income_annual_growth_pct = 0 → RENT bị bất lợi giả tạo theo thời gian")
    for c, ch in a["investment_channels"].items():
        if ch.get("return_pct") is None or ch.get("std_dev_pct") is None:
            warnings.append(f"Kênh {c}: chưa có return/std")
        elif ch.get("status") != "CHOT":
            warnings.append(f"Kênh {c}: đang ở trạng thái {ch.get('status')} (chưa duyệt)")
    for months, rate in PROMO_PACKAGES.items():
        if rate is None:
            warnings.append(f"Gói ưu đãi {months} tháng: chưa có lãi suất")
    return warnings


_TODO_RE = re.compile(r"#\s*TODO\(([^)]+)\)\s*:?\s*(.*)")


def list_open_todos(root=None):
    """Quét mọi file .py trong package tìm '# TODO(<mã>)' — phục vụ checklist trước khi merge/nộp."""
    root = Path(__file__).resolve().parent if root is None else Path(root)
    found = []
    for path in sorted(root.rglob("*.py")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            m = _TODO_RE.search(line)
            if m and not m.group(1).startswith("<"):  # bỏ qua ví dụ '<mã>' trong docstring
                found.append({"file": path.name, "line": i, "code": m.group(1), "text": m.group(2).strip()})
    return found
