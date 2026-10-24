// node tests/b2_js_harness.js <engine.js> <data.json> <combos.json>  → in kết quả JSON (không gồm text lý do)
const fs = require("fs");
const E = require(require("path").resolve(process.argv[2]));
const data = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const combos = JSON.parse(fs.readFileSync(process.argv[4], "utf8"));
const out = combos.map(([pid, sb, mode]) => {
  const r = E.runRelevanceEngine(mode === "buy" ? data.buy : data.rent, data.projects, pid, sb, mode);
  return { meta: [r.meta.n_pool, r.meta.reference_price_m2, r.meta.reference_source, r.meta.price_scoring_enabled],
           rows: r.candidates.map((x) => [x.listing_id, x.relevance_level, x.relevance_score, x.candidate_rank, x.distance_km,
                   x.matched ? [x.matched.price, x.matched.district, x.matched.beltway] : null]),
           display: r.display.map((x) => x.listing_id), banner: r.show_warning_banner };
});
process.stdout.write(JSON.stringify(out));
