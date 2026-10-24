/* FinFlow UI engine (JS) — B2 relevance engine, B3.1 loan term, Step 4 disclaimers, B4 prepayment helper.
   BẢN CHUẨN là Python (finflow/*.py). File này được kiểm tra đối chiếu 1-1 bằng tests/test_parity_b2_js.py
   (205 tòa × 3 size band × 2 nhánh). Sửa logic ở Python trước, rồi port sang đây và chạy lại test. */
(function (root) {
  "use strict";
  const EARTH_RADIUS_KM = 6371.0;
  const DEG = Math.PI / 180;
  const DEFAULT_WEIGHTS = { price: 45, district: 30, beltway: 25 };
  const PRICE_TOLERANCE = { Small: 0.05, Medium: 0.08, Large: 0.10 };
  const N_MIN_FOR_PRICE = 5;
  const DISPLAY_CAPS = { TARGET: null, HIGH: null, MEDIUM: null, LOW: 5, WARNING: 3 };
  const LEVEL_ORDER = ["TARGET", "HIGH", "MEDIUM", "LOW", "WARNING"];
  const LEVEL_BY_MATCHES = { 3: "HIGH", 2: "MEDIUM", 1: "LOW", 0: "WARNING" };
  const EPS = 1e-9;
  const WARNING_BANNER = "Các căn mức WARNING chỉ mang tính tham khảo lỏng — không khớp tiêu chí nào ngoài size band.";
  const LOAN = { bankMaxTermMonths: 360, maxAgeAtMaturity: 75, minAge: 18, gracePeriodMonths: 24,
                 prepaymentFeePctByLoanYear: [1, 1, 1, 1, 1] }; // TODO(#1/#1b/#1c): đồng bộ với fin_assumptions.py

  function normalizeBeltway(v) {
    if (v === null || v === undefined) return null;
    if (typeof v === "number") return Number.isNaN(v) ? null : String(v);
    const s = String(v).trim();
    if (s === "") return "";
    const f = Number(s);
    if (Number.isNaN(f)) return s;
    return Number.isInteger(f) ? String(f) : s;
  }

  function haversineKm(lat1, lon1, lat2, lon2) {
    if ([lat1, lon1, lat2, lon2].some((x) => x === null || x === undefined)) return null;
    const p1 = lat1 * DEG, p2 = lat2 * DEG, dphi = (lat2 - lat1) * DEG, dl = (lon2 - lon1) * DEG;
    const h = Math.sin(dphi / 2) ** 2 + Math.cos(p1) * Math.cos(p2) * Math.sin(dl / 2) ** 2;
    return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(Math.min(1, h)));
  }

  function median(values) {
    const s = values.slice().sort((a, b) => a - b), n = s.length;
    if (!n) return null;
    const m = Math.floor(n / 2);
    return n % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
  }

  function scoreTable(weights) {
    const w = weights || DEFAULT_WEIGHTS, p = w.price, d = w.district, b = w.beltway;
    const pairs = [d + b, b + p, d + p], singles = [b, d, p];
    if (Math.max(...singles) >= Math.min(...pairs) || Math.max(...pairs) >= p + d + b) throw new Error("Trọng số làm chồng lấn tier");
    return { HIGH: p + d + b, MEDIUM_range: [Math.min(...pairs), p + d + b - 1], LOW_range: [Math.min(...singles), Math.min(...pairs) - 1], cap_when_n_lt_min: d + b };
  }

  function listingPriceM2(L, mode) {
    const area = L.area_m2;
    let v = null;
    if (mode === "buy") {
      v = L.price_m2_vnd === null || L.price_m2_vnd === undefined ? null : L.price_m2_vnd;
      if (v === null && L.total_price_vnd && area) v = L.total_price_vnd / area;
    } else {
      v = L.rent_monthly_vnd && area ? L.rent_monthly_vnd / area : null;
    }
    return v !== null && v > 0 ? Number(v) : null;
  }

  function fmtRef(v, mode) { return mode === "buy" ? (v / 1e6).toFixed(1) + " triệu/m²" : Math.round(v / 1e3) + " nghìn/m²/tháng"; }
  function fmtPct(x) { const s = (x * 100).toFixed(1); return (x >= 0 ? "+" : "") + s; }

  function runRelevanceEngine(listings, projects, targetProjectId, sizeBand, mode, opts) {
    opts = opts || {};
    if (mode !== "buy" && mode !== "rent") throw new Error("mode phải là 'buy' hoặc 'rent'");
    const tolMap = opts.tolerances || PRICE_TOLERANCE;
    if (!(sizeBand in tolMap)) throw new Error("size_band không hợp lệ: " + sizeBand);
    if (!(targetProjectId in projects)) throw new Error("TARGET project_id không có trong PROJECT_MASTER: " + targetProjectId);
    const w = opts.weights || DEFAULT_WEIGHTS, caps = opts.displayCaps || DISPLAY_CAPS;
    const nMin = opts.nMin === undefined ? N_MIN_FOR_PRICE : opts.nMin, bedrooms = opts.bedrooms === undefined ? 2 : opts.bedrooms;
    const table = scoreTable(w), tgt = projects[targetProjectId];
    const tgtD = tgt.district_old, tgtB = normalizeBeltway(tgt.beltway_zone);
    const pool = [];
    let excludedNoPrice = 0;
    for (const L of listings) {
      if (L.size_band !== sizeBand) continue;
      const bd = Number(L.bedrooms);
      if (L.bedrooms === null || L.bedrooms === undefined || Number.isNaN(bd) || bd !== Number(bedrooms)) continue;
      const pm2 = listingPriceM2(L, mode);
      if (pm2 === null) { excludedNoPrice++; continue; }
      pool.push([L, pm2]);
    }
    const nPool = pool.length, priceEnabled = nPool >= nMin;
    const targetRows = pool.filter(([L]) => L.project_id === targetProjectId);
    const candRows = pool.filter(([L]) => L.project_id !== targetProjectId);
    let ref = null, refSource = null;
    if (targetRows.length) { ref = median(targetRows.map((x) => x[1])); refSource = "TARGET"; }
    else if (candRows.length) { ref = median(candRows.map((x) => x[1])); refSource = "MEDIAN_SIZE_BAND"; }
    const tol = tolMap[sizeBand], refLabel = refSource === "TARGET" ? "mốc TARGET" : "mốc trung vị size band";
    const base = (L, p) => ({ listing_id: L.listing_id, project_id: L.project_id, project_name: L.project_name,
      district_old: L.district_old, ward_old: L.ward_old, beltway_zone: normalizeBeltway(L.beltway_zone), area_m2: L.area_m2,
      size_band: L.size_band, price_m2: p, price_total: mode === "buy" ? L.total_price_vnd : L.rent_monthly_vnd });
    const rows = [];
    for (const [L, p] of targetRows) {
      rows.push(Object.assign(base(L, p), { relevance_level: "TARGET", relevance_score: null, n_matched: null, matched: null,
        price_diff_pct: ref ? p / ref - 1 : null, distance_km: 0.0,
        warning_reason: "TARGET — đúng tòa bạn chọn (" + (tgt.project_name || targetProjectId) + ")." }));
    }
    for (const [L, p] of candRows) {
      const proj = projects[L.project_id] || {};
      const cD = L.district_old || proj.district_old;
      const cB = normalizeBeltway(L.beltway_zone !== null && L.beltway_zone !== undefined ? L.beltway_zone : proj.beltway_zone);
      const diff = ref ? p / ref - 1 : null;
      const mPrice = !!(priceEnabled && diff !== null && Math.abs(diff) <= tol + EPS);
      const mDist = cD !== null && cD !== undefined && cD === tgtD;
      const mBelt = cB !== null && cB === tgtB;
      const nMatch = (mPrice ? 1 : 0) + (mDist ? 1 : 0) + (mBelt ? 1 : 0);
      const score = w.price * (mPrice ? 1 : 0) + w.district * (mDist ? 1 : 0) + w.beltway * (mBelt ? 1 : 0);
      const ok = [], ko = [];
      if (!priceEnabled) ko.push("không đủ dữ liệu để so sánh giá (N=" + nPool + " < " + nMin + ")");
      else (mPrice ? ok : ko).push("giá/m² lệch " + fmtPct(diff) + "% so với " + refLabel + " " + fmtRef(ref, mode) + (mPrice ? " (trong ±" : " (ngoài ±") + (tol * 100) + "%)");
      (mDist ? ok : ko).push(mDist ? "cùng quận (" + cD + ")" : "khác quận (" + cD + " ≠ " + tgtD + ")");
      (mBelt ? ok : ko).push(mBelt ? "cùng vành đai (" + cB + ")" : "khác vành đai (" + cB + " ≠ " + tgtB + ")");
      rows.push(Object.assign(base(L, p), { relevance_level: LEVEL_BY_MATCHES[nMatch], relevance_score: score, n_matched: nMatch,
        matched: { price: mPrice, district: mDist, beltway: mBelt }, price_diff_pct: diff,
        distance_km: haversineKm(tgt.latitude, tgt.longitude, proj.latitude, proj.longitude),
        warning_reason: "Khớp: " + (ok.length ? ok.join("; ") : "không tiêu chí nào") + ". Không khớp: " + (ko.length ? ko.join("; ") : "—") + "." }));
    }
    for (const r of rows) { // kiểm tra điểm nằm đúng khoảng tier
      const lv = r.relevance_level, sc = r.relevance_score;
      const bad = (lv === "HIGH" && sc !== table.HIGH) || (lv === "MEDIUM" && (sc < table.MEDIUM_range[0] || sc > table.MEDIUM_range[1])) ||
        (lv === "LOW" && (sc < table.LOW_range[0] || sc > table.LOW_range[1])) || (lv === "WARNING" && sc !== 0) ||
        (!priceEnabled && sc !== null && sc > table.cap_when_n_lt_min);
      if (bad) throw new Error("Điểm không khớp tier: " + JSON.stringify(r));
    }
    const order = {}; LEVEL_ORDER.forEach((lv, i) => { order[lv] = i; });
    rows.sort((a, b) => {
      if (order[a.relevance_level] !== order[b.relevance_level]) return order[a.relevance_level] - order[b.relevance_level];
      const na = a.distance_km === null, nb = b.distance_km === null;
      if (na !== nb) return na ? 1 : -1;
      const da = na ? 0 : a.distance_km, db = nb ? 0 : b.distance_km;
      if (da !== db) return da - db;
      return a.listing_id < b.listing_id ? -1 : a.listing_id > b.listing_id ? 1 : 0;
    });
    const counts = {};
    for (const r of rows) { counts[r.relevance_level] = (counts[r.relevance_level] || 0) + 1; r.candidate_rank = counts[r.relevance_level]; }
    const display = rows.filter((r) => caps[r.relevance_level] === null || caps[r.relevance_level] === undefined || r.candidate_rank <= caps[r.relevance_level]);
    return { meta: { mode, size_band: sizeBand, target_project_id: targetProjectId, target_district: tgtD, target_beltway: tgtB,
             reference_price_m2: ref, reference_source: refSource, tolerance: tol, n_pool: nPool, n_min: nMin,
             price_scoring_enabled: priceEnabled, excluded_no_price: excludedNoPrice, weights: Object.assign({}, w), counts },
             candidates: rows, display, show_warning_banner: display.some((r) => r.relevance_level === "WARNING"), warning_banner: WARNING_BANNER };
  }

  function filterBuildings(projects, districtOld, wardOld, beltwayZone) {
    if (!districtOld) throw new Error("Step 1: quận cũ là trường bắt buộc");
    const bz = beltwayZone ? normalizeBeltway(beltwayZone) : null;
    return Object.keys(projects).filter((pid) => { const p = projects[pid];
      return p.district_old === districtOld && (!wardOld || p.ward_old === wardOld) && (bz === null || normalizeBeltway(p.beltway_zone) === bz);
    }).sort((a, b) => String(projects[a].project_name || a).localeCompare(String(projects[b].project_name || b)));
  }

  class LoanTermError extends Error { constructor(code, message) { super(message); this.code = code; } }

  function cleanAge(age, label, minAge) {
    if (typeof age !== "number" || !Number.isFinite(age) || !Number.isInteger(age)) throw new LoanTermError("AGE_INVALID", label + " phải là số nguyên (tuổi tròn năm)");
    if (age < minAge) throw new LoanTermError("AGE_BELOW_MIN", label + " = " + age + ": người vay phải từ đủ " + minAge + " tuổi");
    return age;
  }

  function calcMaxLoanTerm(age1, age2, bankMaxTermMonths, opts) {
    opts = opts || {};
    const bankMax = bankMaxTermMonths == null ? LOAN.bankMaxTermMonths : bankMaxTermMonths;
    const maxAge = opts.maxAgeAtMaturity == null ? LOAN.maxAgeAtMaturity : opts.maxAgeAtMaturity;
    const grace = opts.gracePeriodMonths == null ? LOAN.gracePeriodMonths : opts.gracePeriodMonths;
    const minAge = opts.minAge == null ? LOAN.minAge : opts.minAge;
    const a1 = cleanAge(age1, "age_1", minAge), a2 = age2 == null ? null : cleanAge(age2, "age_2", minAge);
    const older = a2 === null ? a1 : Math.max(a1, a2);
    if (older >= maxAge) throw new LoanTermError("AGE_LIMIT", "Không đủ tuổi để vay: người vay lớn tuổi nhất " + older + " tuổi, tuổi tối đa khi đáo hạn là " + maxAge + ".");
    const byAge = (maxAge - older) * 12, final = Math.min(byAge, bankMax);
    if (final <= grace) throw new LoanTermError("TERM_NOT_ABOVE_GRACE", "Thời hạn vay tối đa tính được (" + final + " tháng) không lớn hơn thời gian ân hạn gốc (" + grace + " tháng).");
    return { older_borrower_age: older, max_term_by_age_months: byAge, max_term_by_bank_months: bankMax,
             final_max_term_months: final, binding_constraint: byAge < bankMax ? "age" : "bank", grace_period_months: grace };
  }

  function prepaymentFeePctAt(month, schedule) {
    const s = schedule || LOAN.prepaymentFeePctByLoanYear, i = Math.floor((month - 1) / 12);
    return i >= 0 && i < s.length ? Number(s[i]) : 0;
  }

  const STATIC_DISCLAIMER = "Nếu bạn muốn so sánh Mua vs Thuê cho cùng 1 kích cỡ căn hộ, hãy chọn cùng size band ở cả 2 phương án tại Step 2.";
  function sizeBandDisclaimers(sizeBandBuy, sizeBandRent) {
    if (!sizeBandBuy || !sizeBandRent) throw new Error("Cần chọn size band cho cả BUY và RENT ở Step 2");
    return { static: STATIC_DISCLAIMER, dynamic: sizeBandBuy !== sizeBandRent ? "Bạn đang so sánh Mua [" + sizeBandBuy + "] với Thuê [" + sizeBandRent +
      "] — kết quả có thể phản ánh chênh lệch giá giữa 2 loại căn khác nhau, không chỉ chênh lệch giữa việc mua và thuê." : null };
  }

  const api = { normalizeBeltway, haversineKm, median, scoreTable, listingPriceM2, runRelevanceEngine, filterBuildings,
    calcMaxLoanTerm, LoanTermError, prepaymentFeePctAt, sizeBandDisclaimers, LEVEL_ORDER, DISPLAY_CAPS, PRICE_TOLERANCE, LOAN };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.FinFlowEngine = api;
})(typeof window !== "undefined" ? window : globalThis);
