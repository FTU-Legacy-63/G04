"""B2 — MỘT bộ test dùng chung cho cả MUA_CALC (buy) và THUE_CALC (rent) (yêu cầu to-do)."""
import os
import unittest

from finflow.relevance_engine import (filter_buildings, haversine_km, load_data_xlsx, normalize_beltway,
                                      run_relevance_engine, run_step2, score_table)


def make_projects():
    P = {}

    def add(pid, d, b, lat, lon):
        P[pid] = {"project_id": pid, "project_name": pid, "district_old": d, "beltway_zone": b, "latitude": lat, "longitude": lon}
    add("T", "A", "2-2.5", 21.000, 105.800)
    add("PH", "A", "2-2.5", 21.001, 105.800)
    add("PDB", "A", "2-2.5", 21.002, 105.800)
    add("PBP", "B", "2-2.5", 21.003, 105.800)
    add("PDP", "A", "3-3.5", 21.004, 105.800)
    add("PB", "B", "2-2.5", 21.005, 105.800)
    add("PD", "A", "3-3.5", 21.006, 105.800)
    add("PP", "B", "3-3.5", 21.007, 105.800)
    add("PW", "B", "3-3.5", 21.008, 105.800)
    for i in range(8):  # để test ngưỡng hiển thị
        add(f"LD{i}", "A", "9", 21.01 + i * 0.001, 105.8)
        add(f"W{i}", "C", "9", 21.02 + i * 0.001, 105.8)
    add("T4", "A", "4", 21.0, 105.9)
    add("Q4", "B", 4.0, 21.0, 105.91)
    return P


class SharedRelevanceTests:
    mode = None
    unit = None

    def L(self, lid, pid, factor, size="Medium", area=70.0, bedrooms=2, projects=None):
        p = (projects or self.P)[pid]
        d = {"listing_id": lid, "project_id": pid, "project_name": pid, "district_old": p["district_old"],
             "beltway_zone": p["beltway_zone"], "area_m2": area, "size_band": size, "bedrooms": bedrooms}
        price_m2 = factor * self.unit
        if self.mode == "buy":
            d.update(price_m2_vnd=price_m2, total_price_vnd=price_m2 * area)
        else:
            d.update(rent_monthly_vnd=price_m2 * area)
        return d

    def setUp(self):
        self.P = make_projects()
        self.base = [self.L("T1", "T", 100), self.L("T2", "T", 100), self.L("T3", "T", 100),
                     self.L("H1", "PH", 104), self.L("M55", "PDB", 120), self.L("M70", "PBP", 95),
                     self.L("M75", "PDP", 101), self.L("L25", "PB", 130), self.L("L30", "PD", 70),
                     self.L("L45", "PP", 99), self.L("W0", "PW", 150)]

    def run_(self, listings, target="T", size="Medium", **kw):
        return run_relevance_engine(listings, self.P, target, size, self.mode, **kw)

    def by_id(self, res):
        return {r["listing_id"]: r for r in res["candidates"]}

    def test_levels_and_scores_match_plan_table(self):
        res = self.run_(self.base)
        r = self.by_id(res)
        expect = {"H1": ("HIGH", 100), "M55": ("MEDIUM", 55), "M70": ("MEDIUM", 70), "M75": ("MEDIUM", 75),
                  "L25": ("LOW", 25), "L30": ("LOW", 30), "L45": ("LOW", 45), "W0": ("WARNING", 0)}
        for lid, (lvl, sc) in expect.items():
            self.assertEqual((r[lid]["relevance_level"], r[lid]["relevance_score"]), (lvl, sc), lid)
        for t in ("T1", "T2", "T3"):
            self.assertEqual(r[t]["relevance_level"], "TARGET")
            self.assertIsNone(r[t]["relevance_score"])
        self.assertEqual(res["meta"]["reference_source"], "TARGET")
        self.assertAlmostEqual(res["meta"]["reference_price_m2"], 100 * self.unit)

    def test_tolerance_boundary_inclusive(self):
        res = self.run_(self.base + [self.L("B108", "PH", 108), self.L("B92", "PH", 92), self.L("B10801", "PH", 108.01)])
        r = self.by_id(res)
        self.assertTrue(r["B108"]["matched"]["price"])
        self.assertTrue(r["B92"]["matched"]["price"])
        self.assertFalse(r["B10801"]["matched"]["price"])
        small = [self.L("S0", "T", 100, "Small")] + [self.L(f"S{i}", "PH", f, "Small") for i, f in enumerate((105, 105.01, 95, 103), 1)]
        r2 = self.by_id(self.run_(small, size="Small"))
        self.assertTrue(r2["S1"]["matched"]["price"])
        self.assertFalse(r2["S2"]["matched"]["price"])

    def test_n_below_5_disables_price_and_caps_at_55(self):
        res = self.run_([self.L("T1", "T", 100), self.L("H1", "PH", 100), self.L("M70", "PBP", 100), self.L("W0", "PW", 100)])
        self.assertFalse(res["meta"]["price_scoring_enabled"])
        r = self.by_id(res)
        self.assertEqual((r["H1"]["relevance_level"], r["H1"]["relevance_score"]), ("MEDIUM", 55))
        self.assertEqual((r["M70"]["relevance_level"], r["M70"]["relevance_score"]), ("LOW", 25))
        self.assertIn("không đủ dữ liệu để so sánh giá", r["H1"]["warning_reason"])
        self.assertTrue(all(x["relevance_score"] is None or x["relevance_score"] <= 55 for x in res["candidates"]))

    def test_fallback_median_when_target_has_no_listing(self):
        res = self.run_([self.L(f"C{i}", "PH", f) for i, f in enumerate((90, 95, 100, 105, 110))])
        self.assertEqual(res["meta"]["reference_source"], "MEDIAN_SIZE_BAND")
        self.assertAlmostEqual(res["meta"]["reference_price_m2"], 100 * self.unit)
        self.assertFalse(any(r["relevance_level"] == "TARGET" for r in res["candidates"]))

    def test_rank_within_tier_by_haversine_then_id(self):
        ls = self.base + [self.L("LA", "LD3", 60), self.L("LB", "LD1", 60), self.L("LC", "LD1", 60)]
        low = [r for r in self.run_(ls)["candidates"] if r["relevance_level"] == "LOW"]
        dists = [r["distance_km"] for r in low]
        self.assertEqual(dists, sorted(dists))
        ids = [r["listing_id"] for r in low]
        self.assertLess(ids.index("LB"), ids.index("LC"))
        self.assertEqual([r["candidate_rank"] for r in low], list(range(1, len(low) + 1)))

    def test_display_caps_and_warning_banner(self):
        ls = self.base + [self.L(f"LX{i}", f"LD{i}", 60) for i in range(7)] + [self.L(f"WX{i}", f"W{i}", 60) for i in range(4)]
        res = self.run_(ls)
        shown = {}
        for r in res["display"]:
            shown[r["relevance_level"]] = shown.get(r["relevance_level"], 0) + 1
        self.assertEqual(shown["LOW"], 5)
        self.assertEqual(shown["WARNING"], 3)
        self.assertEqual(shown["TARGET"], 3)
        self.assertEqual(shown["MEDIUM"], res["meta"]["counts"]["MEDIUM"])
        self.assertTrue(res["show_warning_banner"])

    def test_warning_reason_lists_exact_criteria(self):
        reason = self.by_id(self.run_(self.base))["M55"]["warning_reason"]
        self.assertIn("cùng quận (A)", reason)
        self.assertIn("cùng vành đai (2-2.5)", reason)
        self.assertIn("ngoài ±8%", reason)
        reason70 = self.by_id(self.run_(self.base))["M70"]["warning_reason"]
        self.assertIn("khác quận (B ≠ A)", reason70)
        self.assertIn("trong ±8%", reason70)

    def test_size_band_is_a_parameter_two_independent_calls(self):
        ls = self.base + [self.L("TS", "T", 100, "Small"), self.L("PS", "PH", 101, "Small")]
        med = self.run_(ls, size="Medium")
        sml = self.run_(ls, size="Small")
        self.assertEqual(med["meta"]["n_pool"], 11)
        self.assertEqual(sml["meta"]["n_pool"], 2)
        self.assertEqual(med["meta"]["target_project_id"], sml["meta"]["target_project_id"])
        self.assertEqual(self.run_(ls, size="Medium")["meta"], med["meta"])  # không có trạng thái toàn cục

    def test_hard_filter_bedrooms(self):
        res = self.run_(self.base + [self.L("B3", "PH", 100, bedrooms=3)])
        self.assertNotIn("B3", self.by_id(res))

    def test_beltway_float_vs_text_normalised(self):
        res = self.run_([self.L("TT", "T4", 100), self.L("QQ", "Q4", 300)], target="T4")
        self.assertTrue(self.by_id(res)["QQ"]["matched"]["beltway"])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            run_relevance_engine(self.base, self.P, "T", "Huge", self.mode)
        with self.assertRaises(ValueError):
            run_relevance_engine(self.base, self.P, "NOPE", "Medium", self.mode)
        with self.assertRaises(ValueError):
            run_relevance_engine(self.base, self.P, "T", "Medium", "lease")


class TestRelevanceBuy(SharedRelevanceTests, unittest.TestCase):
    mode, unit = "buy", 1e6


class TestRelevanceRent(SharedRelevanceTests, unittest.TestCase):
    mode, unit = "rent", 3e3


class TestHelpers(unittest.TestCase):
    def test_score_tables_match_both_plans(self):
        t = score_table({"price": 45, "district": 30, "beltway": 25})
        self.assertEqual((t["HIGH"], t["district+beltway"], t["beltway+price"], t["district+price"]), (100, 55, 70, 75))
        self.assertEqual((t["beltway_only"], t["district_only"], t["price_only"]), (25, 30, 45))
        self.assertEqual((t["MEDIUM_range"], t["LOW_range"], t["cap_when_n_lt_min"]), ((55, 99), (25, 54), 55))
        old = score_table({"price": 35, "district": 25, "beltway": 20})
        self.assertEqual((old["HIGH"], old["MEDIUM_range"], old["LOW_range"], old["cap_when_n_lt_min"]), (80, (45, 79), (20, 44), 45))
        with self.assertRaises(ValueError):
            score_table({"price": 60, "district": 20, "beltway": 20})

    def test_haversine(self):
        self.assertAlmostEqual(haversine_km(0, 0, 1, 0), 6371 * 3.141592653589793 / 180, places=9)
        self.assertEqual(haversine_km(21, 105.8, 21, 105.8), 0.0)
        self.assertAlmostEqual(haversine_km(21, 105.8, 21.01, 105.82), haversine_km(21.01, 105.82, 21, 105.8), places=12)
        self.assertIsNone(haversine_km(None, 1, 2, 3))

    def test_normalize_beltway(self):
        self.assertEqual([normalize_beltway(x) for x in (4.0, "4.0", "4", 1, "2.5-3", " 1-2 ", None)],
                         ["4", "4", "4", "1", "2.5-3", "1-2", None])

    def test_step1_filters_buildings_not_the_b2_pool(self):
        P = make_projects()
        self.assertEqual(filter_buildings(P, "B", beltway_zone="2-2.5"), ["PB", "PBP"])
        with self.assertRaises(ValueError):
            filter_buildings(P, "")


DATA = os.environ.get("FINFLOW_DATA_XLSX")


@unittest.skipUnless(DATA and os.path.exists(DATA), "Đặt FINFLOW_DATA_XLSX=đường dẫn DATA.xlsx để chạy smoke test dữ liệu thật")
class TestRealData(unittest.TestCase):
    def test_step2_runs_for_every_target_and_band(self):
        d = load_data_xlsx(DATA)
        levels = {"TARGET", "HIGH", "MEDIUM", "LOW", "WARNING"}
        for pid in list(d["projects"])[::10]:
            for sb in ("Small", "Medium", "Large"):
                out = run_step2(d, pid, sb, sb)
                for k in ("buy", "rent"):
                    self.assertTrue({r["relevance_level"] for r in out[k]["candidates"]} <= levels)


if __name__ == "__main__":
    unittest.main()
