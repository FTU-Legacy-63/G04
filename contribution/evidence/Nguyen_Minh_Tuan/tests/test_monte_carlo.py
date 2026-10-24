"""B8 — khung Monte Carlo."""
import time
import unittest
from copy import deepcopy

import numpy as np

from finflow.evaluate import evaluate_buy_vs_rent
from finflow.fin_assumptions import MC_STD, appreciation_decay_path, get_assumptions
from finflow.monte_carlo import n_warning, resolve_n, run_monte_carlo

INP = dict(purchase_price=4.0e9, savings=1.3e9, income_1=45e6, income_2=35e6, living_cost=15e6,
           existing_debt=0, monthly_rent=14e6)


def zero_std_setup():
    a = get_assumptions()
    for ch in a["investment_channels"].values():
        ch["std_dev_pct"] = 0.0
    mc_std = deepcopy(MC_STD)
    for v in mc_std.values():
        v["std"] = 0.0
    return a, mc_std


class TestN(unittest.TestCase):
    def test_presets_only(self):
        self.assertEqual(resolve_n(), 1000)
        self.assertEqual(resolve_n(final_run=True), 10000)
        for ok in (500, 1000, 2000):
            self.assertEqual(resolve_n(ok), ok)
        for bad in (1500, 50, True, "1000"):
            with self.assertRaises(ValueError):
                resolve_n(bad)
        self.assertIsNotNone(n_warning(300))
        self.assertIsNone(n_warning(500))


class TestMonteCarlo(unittest.TestCase):
    def test_zero_std_reproduces_deterministic_engine(self):
        a, mc_std = zero_std_setup()
        mc = run_monte_carlo(INP, 300, assumptions=a, n=500, seed=7, mc_std=mc_std)
        det = evaluate_buy_vs_rent(INP, 300, a)
        nwb = det["net_worth"]["timeline"][-1]["net_worth_buy"]
        nwr = det["net_worth"]["timeline"][-1]["net_worth_rent"]
        for q in ("p10", "p50", "p90"):
            self.assertAlmostEqual(mc["buy"]["final_net_worth"][q] / nwb, 1.0, places=9)
            self.assertAlmostEqual(mc["rent"]["final_net_worth"][q] / nwr, 1.0, places=9)
        self.assertEqual(mc["buy"]["pct_safe_all_months"], 1.0 if det["buy"]["is_safe"] else 0.0)

    def test_seed_reproducible_and_valid_ranges(self):
        m1 = run_monte_carlo(INP, 360, n=1000, seed=42)
        m2 = run_monte_carlo(INP, 360, n=1000, seed=42)
        self.assertEqual(m1["comparison"], m2["comparison"])
        c = m1["comparison"]
        for k in ("pct_buy_wins", "pct_rent_wins", "pct_paths_with_break_even"):
            self.assertTrue(0.0 <= c[k] <= 1.0)
        self.assertLessEqual(c["pct_buy_wins"] + c["pct_rent_wins"], 1.0)
        self.assertEqual(len(m1["buy"]["yearly_p10_p50_p90"]), 30)

    def test_per_year_sampling_is_less_dispersed_than_per_path(self):
        alloc = {"savings": 0.0, "stocks": 1.0, "bonds": 0.0, "gold": 0.0}
        a_year = get_assumptions()
        a_path = get_assumptions()
        a_path["investment_channels"]["stocks"]["sampling"] = "per_path"
        py = run_monte_carlo(INP, 360, assumptions=a_year, allocation=alloc, n=2000, seed=3)
        pp = run_monte_carlo(INP, 360, assumptions=a_path, allocation=alloc, n=2000, seed=3)
        spread = lambda m: m["rent"]["final_net_worth"]["p90"] - m["rent"]["final_net_worth"]["p10"]
        self.assertLess(spread(py), spread(pp))

    def test_buy_infeasible_is_reported(self):
        mc = run_monte_carlo(dict(INP, savings=0.2e9), 360, n=500, seed=1)
        self.assertIn("error", mc["buy"])
        self.assertIsNone(mc["comparison"])

    def test_decay_path_mean_supported_in_mc(self):  # B5.1 PA2 chạy được cả tất định lẫn Monte Carlo
        a, mc_std = zero_std_setup()
        a["property_annual_appreciation_pct"] = appreciation_decay_path(19.0, 8.4, 5.0, 35)
        mc = run_monte_carlo(INP, 300, assumptions=a, n=500, seed=1, mc_std=mc_std)
        det = evaluate_buy_vs_rent(INP, 300, a)
        self.assertAlmostEqual(mc["buy"]["final_net_worth"]["p50"] / det["net_worth"]["timeline"][-1]["net_worth_buy"], 1.0, places=9)
        self.assertLess(det["net_worth"]["timeline"][-1]["net_worth_buy"], evaluate_buy_vs_rent(INP, 300)["net_worth"]["timeline"][-1]["net_worth_buy"])

    def test_bankrupt_proxy_flags_unaffordable_buy(self):
        h1 = dict(purchase_price=7.2e9, savings=1.7e9, income_1=30e6, income_2=20e6, living_cost=12e6, existing_debt=0, monthly_rent=21.5e6)
        mc = run_monte_carlo(h1, 360, n=500, seed=5)
        self.assertGreater(mc["buy"]["pct_savings_exhausted_any_month"], 0.99)
        self.assertLess(mc["comparison"]["pct_buy_wins_and_buy_solvent"], 0.01)
        self.assertGreater(mc["comparison"]["pct_buy_wins"], 0.9)  # lý do cần chỉ số 'solvent'
        ok = run_monte_carlo(INP, 360, n=500, seed=5)
        self.assertLess(ok["buy"]["pct_savings_exhausted_any_month"], 0.05)

    def test_final_run_speed(self):
        t0 = time.time()
        mc = run_monte_carlo(INP, 360, final_run=True, seed=0)
        self.assertEqual(mc["n"], 10000)
        self.assertLess(time.time() - t0, 10.0)


if __name__ == "__main__":
    unittest.main()
