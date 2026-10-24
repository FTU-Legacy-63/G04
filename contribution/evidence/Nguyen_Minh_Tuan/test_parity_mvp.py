"""Đối chiếu engine Python mới (chế độ LEGACY_MVP_OVERRIDES) với engine JS gốc trong 'MVP sau chỉnh sửa.html' (Week 6).
Chứng minh: phần port KHÔNG làm sai công thức cũ; mọi khác biệt kết quả về sau chỉ đến từ thay đổi có chủ đích."""
import json, os, shutil, subprocess, tempfile, unittest
from pathlib import Path

from finflow.evaluate import evaluate_buy_vs_rent
from finflow.fin_assumptions import LEGACY_MVP_OVERRIDES, get_assumptions

ROOT = Path(__file__).resolve().parents[1]
MVP = os.environ.get("FINFLOW_MVP_HTML")
CASES = [
    dict(purchase_price=7.2e9, savings=1.7e9, income_1=30e6, income_2=20e6, living_cost=12e6, existing_debt=0, monthly_rent=21.5e6, term=360),
    dict(purchase_price=3.99e9, savings=1.2e9, income_1=40e6, income_2=30e6, living_cost=10e6, existing_debt=2e6, monthly_rent=13.5e6, term=300),
    dict(purchase_price=3.0e9, savings=3.5e9, income_1=30e6, income_2=0, living_cost=10e6, existing_debt=0, monthly_rent=12e6, term=240),
    dict(purchase_price=5.0e9, savings=0.5e9, income_1=25e6, income_2=0, living_cost=9e6, existing_debt=0, monthly_rent=11e6, term=360),
    dict(purchase_price=6.0e9, savings=2.0e9, income_1=80e6, income_2=60e6, living_cost=20e6, existing_debt=0, monthly_rent=18e6, term=360),
    dict(purchase_price=4.5e9, savings=1.1e9, income_1=35e6, income_2=25e6, living_cost=14e6, existing_debt=1e6, monthly_rent=15e6, term=180),
]


@unittest.skipUnless(MVP and os.path.exists(MVP) and shutil.which("node"), "Cần FINFLOW_MVP_HTML và node")
class TestMvpParity(unittest.TestCase):
    def test_legacy_mode_matches_mvp_js(self):
        with tempfile.TemporaryDirectory() as tmp:
            cp = Path(tmp, "cases.json"); cp.write_text(json.dumps(CASES))
            js = json.loads(subprocess.run(["node", str(ROOT / "tests/mvp_harness.js"), MVP, str(cp)], check=True,
                                           capture_output=True, text=True).stdout)
        a = get_assumptions(**LEGACY_MVP_OVERRIDES)
        a["investment_channels"]["savings"]["return_pct"] = 6.0
        for c, j in zip(CASES, js):
            inp = {k: v for k, v in c.items() if k != "term"}
            r = evaluate_buy_vs_rent(inp, c["term"], a)
            b, rn = r["buy"], r["rent"]
            self.assertEqual(r["decision"], j["decision"], c)
            self.assertEqual(b["error"] is not None, j["buy_error"])
            self.assertAlmostEqual(b["min_down_payment"], j["min_down"], delta=1e-3)
            self.assertAlmostEqual(rn["safety_margin"], j["rent_sm"], places=12)
            self.assertEqual(rn["is_safe"], j["rent_safe"])
            self.assertEqual(r["net_worth"]["break_even_month"], j["be"])
            if b["error"] is None:
                self.assertAlmostEqual(b["required_loan"], j["required_loan"], delta=1e-3)
                self.assertAlmostEqual(b["safety_margin"], j["buy_sm"], places=12)
                self.assertEqual(b["is_safe"], j["buy_safe"])
                self.assertAlmostEqual(b["money_remaining"], j["buy_mr"], delta=1e-3)
                self.assertEqual(b["post_grace_worst_month"], j["pgw"])
            for m, (jb, jr) in zip([1, 12, 25, 60, 61, 120, c["term"]], j["nw"]):
                pr = rn["net_worth_series"][m - 1]["net_worth_rent"]
                self.assertAlmostEqual(pr / jr, 1.0, places=9)
                if jb is not None:
                    self.assertAlmostEqual(b["net_worth_series"][m - 1]["net_worth_buy"] / jb, 1.0, places=9)
        print(f"\n[MVP parity] {len(CASES)} hồ sơ: quyết định, safety margin, dư nợ, break-even, Net worth khớp MVP JS")


if __name__ == "__main__":
    unittest.main()
