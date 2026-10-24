"""Đối chiếu 1-1 B2 bản JS (ui/finflow_engine.js) với bản Python trên TOÀN BỘ dữ liệu thật (mọi tòa × 3 size band × 2 nhánh)."""
import json, os, shutil, subprocess, tempfile, unittest
from pathlib import Path

from finflow.relevance_engine import load_data_xlsx, run_relevance_engine

ROOT = Path(__file__).resolve().parents[1]
DATA = os.environ.get("FINFLOW_DATA_XLSX")


@unittest.skipUnless(DATA and os.path.exists(DATA) and shutil.which("node"), "Cần FINFLOW_DATA_XLSX và node")
class TestB2Parity(unittest.TestCase):
    def test_python_js_identical(self):
        d = load_data_xlsx(DATA)
        combos = [[pid, sb, mode] for pid in d["projects"] for sb in ("Small", "Medium", "Large") for mode in ("buy", "rent")]
        with tempfile.TemporaryDirectory() as tmp:
            dp, cp = Path(tmp, "data.json"), Path(tmp, "combos.json")
            dp.write_text(json.dumps(d, default=str)); cp.write_text(json.dumps(combos))
            js = json.loads(subprocess.run(["node", str(ROOT / "tests/b2_js_harness.js"), str(ROOT / "ui/finflow_engine.js"), str(dp), str(cp)],
                                           check=True, capture_output=True, text=True).stdout)
        rows_checked = 0
        for (pid, sb, mode), j in zip(combos, js):
            p = run_relevance_engine(d["buy"] if mode == "buy" else d["rent"], d["projects"], pid, sb, mode)
            m = p["meta"]
            self.assertEqual([m["n_pool"], m["reference_source"], m["price_scoring_enabled"]], [j["meta"][0], j["meta"][2], j["meta"][3]])
            if m["reference_price_m2"] is not None:
                self.assertAlmostEqual(m["reference_price_m2"], j["meta"][1], delta=1e-9 * m["reference_price_m2"])
            self.assertEqual(len(p["candidates"]), len(j["rows"]))
            for a, b in zip(p["candidates"], j["rows"]):
                self.assertEqual([a["listing_id"], a["relevance_level"], a["relevance_score"], a["candidate_rank"]], b[:4])
                self.assertAlmostEqual(a["distance_km"], b[4], delta=1e-9)
                self.assertEqual(None if a["matched"] is None else [a["matched"]["price"], a["matched"]["district"], a["matched"]["beltway"]], b[5])
                rows_checked += 1
            self.assertEqual([r["listing_id"] for r in p["display"]], j["display"])
            self.assertEqual(p["show_warning_banner"], j["banner"])
        print(f"\n[B2 parity] {len(combos)} lần chạy, {rows_checked} dòng candidate khớp 100%")


if __name__ == "__main__":
    unittest.main()
