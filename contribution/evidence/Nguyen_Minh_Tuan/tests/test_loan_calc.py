"""B4 (LOAN_CALC + prepayment) và B5 (Net worth) — engine loan_calc.simulate + evaluate."""
import math
import unittest

import numpy as np

from finflow.evaluate import decide, evaluate_buy_vs_rent, find_break_even
from finflow.fin_assumptions import LEGACY_MVP_OVERRIDES, get_assumptions, portfolio_return_pct, validate_allocation
from finflow.loan_calc import amortization_schedule, js_round, prepayment_fee_pct_at, simulate
from finflow.loan_term import LoanTermError

BASE = dict(purchase_price=7.2e9, savings=1.5e9, income_1=30e6, income_2=20e6, living_cost=12e6,
            existing_debt=0, monthly_rent=21.5e6)


def legacy(**kw):
    a = get_assumptions(**LEGACY_MVP_OVERRIDES)
    a["investment_channels"]["savings"]["return_pct"] = 6.0  # MVP: investment_return_pct = 6
    a.update(kw)
    return a


class TestLoanCalc(unittest.TestCase):
    def test_week4_python_reference_numbers(self):
        # Test gốc loan_calc.py Week 4: 7.2 tỷ, savings 1.5 tỷ, 360 tháng, lãi 8.3%, không phí giao dịch
        a = legacy(buy_closing_costs_pct=0.0, interest_rate_float_ref_pct=8.3)
        sim = simulate(BASE, 360, a)
        self.assertAlmostEqual(sim["buy"]["min_down_payment"], 1_440_000_000, places=3)
        self.assertAlmostEqual(sim["buy"]["required_loan"], 5_700_000_000, places=3)
        sch = amortization_schedule(sim)
        self.assertAlmostEqual(sch[0]["interest_payment"], 39_425_000, places=3)
        self.assertEqual(sch[23]["principal_payment"], 0.0)
        self.assertAlmostEqual(sch[24]["principal_payment"], 5.7e9 / 336, places=3)
        self.assertEqual(sch[-1]["balance_end"], 0.0)
        self.assertEqual([sch[m - 1]["annual_rate_pct"] for m in (12, 13, 24, 25)], [8.3, 9.8, 9.8, 11.8])

    def test_insufficient_savings_error_and_no_schedule(self):
        sim = simulate(dict(BASE, savings=1.0e9), 360, legacy())
        self.assertIsNotNone(sim["buy"]["error"])
        self.assertIsNone(sim["buy"]["required_loan"])
        self.assertEqual(amortization_schedule(sim), [])

    def test_savings_above_price_no_negative_loan(self):  # MVP locked fix #1
        sim = simulate(dict(BASE, purchase_price=3e9, savings=3.5e9), 240, legacy())
        self.assertEqual(sim["buy"]["required_loan"], 0.0)
        self.assertAlmostEqual(sim["buy"]["excess_cash"], 0.5e9)
        self.assertTrue(all(x >= 0 for x in sim["series"]["interest_payment"]))

    def test_prepayment_fee_schedule_and_liquidation_basis(self):
        a = get_assumptions()
        self.assertEqual([prepayment_fee_pct_at(m, a) for m in (1, 12, 13, 60, 61, 360)], [1, 1, 1, 1, 0, 0])
        inp = dict(BASE, savings=1.8e9)
        liq = simulate(inp, 360, a)
        book = simulate(inp, 360, get_assumptions(net_worth_basis="book"))
        s = liq["series"]
        for m in (30, 60):
            i = m - 1
            self.assertAlmostEqual(s["prepayment_fee_vnd"][i], s["balance_end"][i] * 0.01, places=3)
            self.assertAlmostEqual(book["series"]["net_worth_buy"][i] - s["net_worth_buy"][i], s["prepayment_fee_vnd"][i], places=2)
        self.assertEqual(s["prepayment_fee_vnd"][60], 0.0)
        self.assertAlmostEqual(book["series"]["net_worth_buy"][60], s["net_worth_buy"][60], places=4)

    def test_rent_recursion_matches_mvp_closed_form(self):
        sim = simulate(BASE, 360, legacy())
        r = 6.0 / 100 / 12
        mrr = 50e6 - 12e6 - 21.5e6
        for t in (1, 12, 120, 360):
            closed = 1.5e9 * (1 + r) ** t + mrr * (((1 + r) ** t - 1) / r)
            self.assertAlmostEqual(sim["series"]["net_worth_rent"][t - 1] / closed, 1.0, places=11)

    def test_yearly_step_growth(self):
        sim = simulate(BASE, 60, get_assumptions(rent_annual_growth_pct=10.0, income_annual_growth_pct=5.0))
        rent, inc = sim["series"]["monthly_rent"], sim["series"]["income"]
        self.assertEqual(rent[0], rent[11])
        self.assertAlmostEqual(rent[12], 21.5e6 * 1.10)
        self.assertAlmostEqual(inc[24], 50e6 * 1.05 ** 2)

    def test_appreciation_path_supports_plan_b(self):  # B5.1 Phương án 2 = truyền đường f(year)
        years = 30
        g = np.array([[8.4 + (19 - 8.4) * math.exp(-y / 5) for y in range(years)]])
        dec = simulate(dict(BASE, savings=1.8e9), 360, get_assumptions(), appreciation_pct=g)
        const = simulate(dict(BASE, savings=1.8e9), 360, get_assumptions())
        self.assertLess(dec["series"]["property_value"][-1], const["series"]["property_value"][-1])
        self.assertAlmostEqual(dec["series"]["property_value"][11], 7.2e9 * (1 + g[0, 0] / 100), places=0)

    def test_js_round(self):
        self.assertEqual(js_round(30 / 12), 3)
        self.assertEqual(round(30 / 12), 2)  # lý do phải dùng js_round cho break_even_year


class TestEvaluate(unittest.TestCase):
    def test_ages_wire_b31_into_evaluation(self):
        with self.assertRaises(LoanTermError) as cm:
            evaluate_buy_vs_rent(BASE, 360, ages=(50, 30))
        self.assertEqual(cm.exception.code, "TERM_ABOVE_MAX")
        r = evaluate_buy_vs_rent(dict(BASE, savings=1.8e9), 300, ages=(50, 30))
        self.assertEqual(r["loan_term_info"]["final_max_term_months"], 300)
        self.assertEqual(r["loan_term_months"], 300)

    def test_promo_package_without_rate_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_buy_vs_rent(BASE, 360, promo_months=6)
        self.assertEqual(evaluate_buy_vs_rent(dict(BASE, savings=1.8e9), 360, promo_months=12)["decision"] in ("BUY", "RENT", "NEITHER"), True)

    def test_allocation_validation(self):
        with self.assertRaises(ValueError):
            validate_allocation({"savings": 0.5, "stocks": 0.3})
        with self.assertRaises(ValueError):
            validate_allocation({"savings": 1.2, "stocks": -0.2})
        self.assertAlmostEqual(portfolio_return_pct({"savings": 0.5, "stocks": 0.5}), (6.50 + 7.99) / 2)

    def test_decide_prioritises_buy_when_safe(self):  # MVP locked fix #2
        buy = {"error": None, "is_safe": True, "safety_margin": 0.31, "money_remaining": 1}
        rent = {"is_safe": True, "safety_margin": 0.50, "money_remaining": 1}
        self.assertEqual(decide(buy, rent)[0], "BUY")
        self.assertEqual(decide(dict(buy, is_safe=False), rent)[0], "RENT")
        self.assertEqual(decide({"error": "x"}, dict(rent, is_safe=False))[0], "NEITHER")

    def test_find_break_even_port(self):
        b = [{"month": m, "net_worth_buy": v} for m, v in ((1, -5), (2, -1), (3, 2))]
        r = [{"month": m, "net_worth_rent": 0.0} for m in (1, 2, 3)]
        self.assertEqual(find_break_even(b, r), (3, 0))
        self.assertEqual(find_break_even(None, r), (None, None))


if __name__ == "__main__":
    unittest.main()
