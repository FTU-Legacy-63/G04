"""Build ui/FinFlow_UI_prototype.html: nhúng dữ liệu DATA.xlsx (đã áp bản sửa toạ độ) + engine JS + cấu hình từ fin_assumptions.py.
Chạy: python3 ui/build_ui.py <DATA.xlsx>"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from finflow.fin_assumptions import (FIN_ASSUMPTIONS, MC_N_DEFAULT, MC_N_PRESETS, MC_N_WARN_BELOW, PROMO_PACKAGES)
from finflow.relevance_engine import haversine_km, load_data_xlsx

fixes = {k: v for k, v in json.loads((ROOT / "data/project_master_fixes.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
raw = load_data_xlsx(sys.argv[1])
d = load_data_xlsx(sys.argv[1], coordinate_fixes=fixes)
for pid, fx in fixes.items():
    name = d["projects"][pid]["project_name"]
    assert fx["expected_name_contains"].lower() in name.lower(), (pid, name)
    old = raw["projects"][pid]
    print(f"  {pid} {name}: dời {haversine_km(old['latitude'], old['longitude'], fx['latitude'], fx['longitude']):.2f} km")
    d["projects"][pid]["coord_fixed"] = True

keep_b = ("listing_id", "project_id", "project_name", "district_old", "ward_old", "beltway_zone", "area_m2", "size_band", "bedrooms", "total_price_vnd", "price_m2_vnd")
keep_r = ("listing_id", "project_id", "project_name", "district_old", "ward_old", "beltway_zone", "area_m2", "size_band", "bedrooms", "rent_monthly_vnd")
ranges = {}
for L in d["buy"] + d["rent"]:
    if L.get("area_m2"):
        lo, hi = ranges.get(L["size_band"], (1e9, 0))
        ranges[L["size_band"]] = (min(lo, L["area_m2"]), max(hi, L["area_m2"]))
labels = {"savings": "Tiết kiệm", "stocks": "Chứng khoán", "bonds": "Trái phiếu", "gold": "Vàng"}
payload = {
    "projects": {pid: {k: p.get(k) for k in ("project_name", "district_old", "ward_old", "beltway_zone", "latitude", "longitude", "coord_fixed")} for pid, p in d["projects"].items()},
    "buy": [{k: L.get(k) for k in keep_b} for L in d["buy"]],
    "rent": [{k: L.get(k) for k in keep_r} for L in d["rent"]],
    "config": {
        "loan": {"bankMaxTermMonths": FIN_ASSUMPTIONS["bank_max_term_months"], "maxAgeAtMaturity": FIN_ASSUMPTIONS["max_borrower_age_at_maturity"],
                 "minAge": FIN_ASSUMPTIONS["min_borrower_age"], "gracePeriodMonths": FIN_ASSUMPTIONS["grace_period_months"],
                 "prepaymentFeePctByLoanYear": FIN_ASSUMPTIONS["prepayment_fee_pct_by_loan_year"]},
        "promo": [{"months": m, "rate": r} for m, r in sorted(PROMO_PACKAGES.items())],
        "channels": {k: {"label": labels[k], "return_pct": v["return_pct"], "std_dev_pct": v["std_dev_pct"], "status": v["status"]} for k, v in FIN_ASSUMPTIONS["investment_channels"].items()},
        "mc": {"presets": list(MC_N_PRESETS), "default": MC_N_DEFAULT, "warn_below": MC_N_WARN_BELOW},
    },
}
for pid in payload["projects"]:
    payload["projects"][pid]["coord_fixed"] = bool(payload["projects"][pid].get("coord_fixed"))
tpl = (ROOT / "ui/prototype_template.html").read_text(encoding="utf-8")
hint_old = "Nhỏ: dưới 60 m² · Vừa: 60–80 m² · Lớn: trên 80 m² (theo size band trong DATA.xlsx)."
assert hint_old in tpl
vn = {"Small": "Nhỏ", "Medium": "Vừa", "Large": "Lớn"}
hint_new = "Diện tích thực tế trong dữ liệu: " + "; ".join(f"{vn[k]} {ranges[k][0]:g}–{ranges[k][1]:g} m²" for k in ("Small", "Medium", "Large")) + "."
engine = (ROOT / "ui/finflow_engine.js").read_text(encoding="utf-8")
out = (tpl.replace(hint_old, hint_new).replace("/*__ENGINE__*/", engine)
          .replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False, separators=(",", ":"))))
assert "/*__" not in out
(ROOT / "ui/FinFlow_UI_prototype.html").write_text(out, encoding="utf-8")
print("size band ranges:", ranges)
print(f"projects {len(payload['projects'])}, buy {len(payload['buy'])}, rent {len(payload['rent'])}; HTML {len(out.encode()) / 1024:.0f} KB")
