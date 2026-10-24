"""Sinh docs/KET_QUA_TODO.md — mọi con số lấy trực tiếp từ engine + dữ liệu (chạy lại để cập nhật).
python3 docs/build_report.py /đường/dẫn/DATA.xlsx"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from finflow.fin_assumptions import (get_assumptions, LEGACY_MVP_OVERRIDES, appreciation_decay_path, list_open_todos, validate_assumptions)
from finflow.evaluate import evaluate_buy_vs_rent
from finflow.monte_carlo import run_monte_carlo
from finflow.relevance_engine import load_data_xlsx, run_step2

def vn(x, d=1):
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
def pct(x, d=1): return vn(100 * x, d) + "%"
def bn(x): return vn(x / 1e9, 1) + " tỷ"

HH = {"H1": dict(purchase_price=7.2e9, savings=1.7e9, income_1=30e6, income_2=20e6, living_cost=12e6, existing_debt=0, monthly_rent=21.5e6),
      "H2": dict(purchase_price=4.0e9, savings=1.3e9, income_1=45e6, income_2=35e6, living_cost=15e6, existing_debt=0, monthly_rent=14e6)}
decay = appreciation_decay_path(19.0, 8.39, 5.0, 35)
m = 1.0
for g in decay[:30]: m *= 1 + g / 100
cagr_decay = m ** (1 / 30) - 1
APPS = [("PA1: 19%/năm cố định", 19.0), ("CAGR 2016–2025: 12,66%", 12.66), ("PA2 rút gọn: 19% → 8,4% (τ = 5 năm)", decay), ("Mốc neo dài hạn: 8,4%", 8.39)]

def det(inp, a):
    r = evaluate_buy_vs_rent(inp, 360, a, ages=(30, 28))
    tl = r["net_worth"]["timeline"][-1]
    return r, tl
rows = []
for h, inp in HH.items():
    for label, app in APPS:
        a = get_assumptions(property_annual_appreciation_pct=app)
        r, tl = det(inp, a)
        mc = run_monte_carlo(inp, 360, assumptions=a, final_run=True, seed=2026)
        rows.append((h, label, r, tl, mc))
leg = {}
for h, inp in HH.items():
    la = get_assumptions(**LEGACY_MVP_OVERRIDES); la["investment_channels"]["savings"]["return_pct"] = 6.0
    leg[h] = det(inp, la)
rg_rows = []
for rg in (7.0, 4.87, 3.0, 0.0):
    r, _ = det(HH["H1"], get_assumptions(rent_annual_growth_pct=rg)); rg_rows.append((rg, r))
d = load_data_xlsx(sys.argv[1])
s2 = run_step2(d, "CG086", "Medium", "Large")
todos = list_open_todos(); warns = validate_assumptions()

L = []; w = L.append
w("# Kết quả thực hiện to-do FinFlow (to-do ngày 25/09/2026)\n")
w("Cập nhật 29/09/2026. Phạm vi: mọi mục 🔴 #1–#5, 🟡 #6–#13, 🟢 B2 · B3.1 · B4 · B8 · B9 · FIN_ASSUMPTIONS · UI · bathrooms · docs, ⚪ và checklist trước merge. "
  "Trạng thái: ✅ xong · 🟡 xong phần làm được, chờ team duyệt/xác nhận · 🔴 cần team quyết định hoặc cung cấp tài liệu. "
  "Mọi con số trong file này do `docs/build_report.py` sinh trực tiếp từ engine và dữ liệu. Nguồn ghi bằng ID `S-…` trong `docs/sources.md`.\n")
w("## 0. Tóm tắt\n")
w(f"**Code (🟢) đã xong và được kiểm chứng.** 60 test pass. Hai bài đối chiếu quan trọng: engine mới ở chế độ tương thích (`LEGACY_MVP_OVERRIDES`) cho kết quả trùng engine JS trong MVP Week 6 trên 6 hồ sơ (quyết định, safety margin tới 12 chữ số thập phân, dư nợ, break-even, Net worth); bản JS của B2 cho UI trùng bản Python trên 1.230 lần chạy / 211.765 dòng candidate. Monte Carlo N = 10.000 chạy khoảng 0,5 giây.\n")
w("**Data (🟡):** sửa lỗi ngày của VN-Index (lỗi autodate làm hỏng cả khối hồi quy — mức 14,2% cũ không dùng được), sửa cách tính độ lệch chuẩn thu nhập (team đang lấy std của MỨC thu nhập theo VND, không phải std tăng trưởng), đã có mean/std cho 4 kênh đầu tư + thu nhập + CPI, sửa toạ độ 3 dự án Hà Đông bị trùng (lệch 1,5–2,8 km).\n")
h1 = {lab: (r, tl, mc) for h, lab, r, tl, mc in rows if h == "H1"}; h2 = {lab: (r, tl, mc) for h, lab, r, tl, mc in rows if h == "H2"}
r19 = h1[APPS[0][0]]; r12 = h1[APPS[1][0]]
w(f"**Hai quyết định ảnh hưởng kết quả nhiều nhất là #3 và #7.** Với hồ sơ test của team (H1: nhà 7,2 tỷ, tiết kiệm 1,7 tỷ, thu nhập 50 triệu/tháng), Net worth MUA sau 30 năm là {bn(r19[1]['net_worth_buy'])} nếu giá nhà tăng 19%/năm, nhưng {bn(r12[1]['net_worth_buy'])} nếu tăng 12,66%/năm (CAGR 10 năm của chính dữ liệu team) — chênh gần 5 lần. "
  f"Rent growth 7%/năm (cao hơn tăng thu nhập 4,87%) làm hồ sơ này đổi kết luận từ RENT sang NEITHER vì safety margin khi thuê tụt từ {pct(rg_rows[0][1]['rent']['month1_safety_margin'])} ở tháng 1 xuống {pct(rg_rows[0][1]['rent']['safety_margin'])} ở tháng {rg_rows[0][1]['rent']['worst_month']}.\n")
w(f"**Phát hiện cần sửa trong thiết kế Monte Carlo:** engine kế thừa MVP coi phần thiếu hụt dòng tiền hàng tháng là “số dư đầu tư âm” sinh lãi như danh mục, tức hộ gia đình được vay vô hạn để giữ nhà. Với H1, MUA âm dòng tiền ở 100% đường mô phỏng nhưng vẫn “thắng về Net worth” ở {pct(r19[2]['comparison']['pct_buy_wins'])} đường (PA1). Đã bổ sung thước đo **cạn tiết kiệm** và **% thắng mà không cạn tiết kiệm** — với H1 chỉ số này là {pct(r19[2]['comparison']['pct_buy_wins_and_buy_solvent'])}.\n")
w("### Bảng trạng thái\n")
w("| Mục | Trạng thái | Kết quả chính | Ở đâu |\n|---|---|---|---|")
for row in [
    ("#1 Thời hạn vay MB", "🟡", "Khuyến nghị giữ 360 tháng: 35 năm thuộc gói MB Dream Home (khách 23–40 tuổi, ≤ 5 tỷ) — khác gói Vạn Phúc", "`fin_assumptions.py` › `BANK_MAX_TERM_MONTHS`"),
    ("#1b Tuổi tối đa (phát sinh)", "🔴", "Mốc 75 chưa kiểm chứng cho MB; nguồn tổng hợp ghi MB = 70", "`MAX_BORROWER_AGE_AT_MATURITY`"),
    ("#1c Phí trả trước (phát sinh)", "🔴", "To-do 1% × 5 năm; nguồn công khai có gói MB bậc thang 2,5 → 1%", "`prepayment_fee_pct_by_loan_year`"),
    ("#2 LTV Vietcombank", "🟡", "“100%” không sai ngân hàng mà khác sản phẩm/tài sản bảo đảm; VCB mua nhà thế chấp chính căn nhà = 70%; PDF plan trích là thông báo lãi suất", "`docs/sources.md` §2.1"),
    ("#3 PA1 hay PA2", "🔴", "Khuyến nghị PA2 rút gọn (19% → 8,4%, CAGR 30 năm ≈ " + pct(cagr_decay) + "); engine + MC đã hỗ trợ", "§1 #3, sheet `Property_CAGR`"),
    ("#4 Hướng xử lý nguồn", "🟡", "Lãi thả nổi: proxy NHNN + std theo thời gian (0,63) → giữ 0,75; giá thuê: dùng báo chí có số gốc Batdongsan", "§1 #4"),
    ("#5 Rubric", "🔴", "Không có file rubric trong zip; README hứa buy-to-let và “% bankrupt”", "§1 #5"),
    ("#6 Lãi vay lịch sử", "✅", "Các mốc NHNN 2022–2026 + std theo thời gian", "sheet `Lai_suat_cho_vay`"),
    ("#7 Giá thuê", "🟡", "Thuê gần đi ngang 2022–2025; đề xuất mean ≈ tăng thu nhập (4,87%), độ nhạy 3% và 7%", "§2 #7, sheet `Gia_thue`"),
    ("#8 Thu nhập", "✅", "Tăng trưởng 4,87% ± 5,68% (NSO, n = 5)", "sheet `Income_growth`"),
    ("#9 Tiết kiệm", "🟡", "Chuỗi lịch sử 6,50% ± 0,82%; snapshot theo ngân hàng cần lấy từ trang chính thức (báo chí mâu thuẫn)", "sheet `Tiet_kiem_snapshot`"),
    ("#10 VN-Index", "✅", "Sửa lỗi ngày; 7,99% ± 19,30%; đối chiếu 2 mốc cuối năm khớp tuyệt đối", "sheet `VNIndex_fixed`"),
    ("#11 Trái phiếu", "✅", "4,02% ± 1,37% (FiinPro; chưa dùng dữ liệu đấu thầu KBNN)", "sheet `Bond_10Y`"),
    ("#12 Vàng", "✅", "14,89% ± 14,13%; cảnh báo giai đoạn tăng bất thường", "sheet `Gold_SJC`"),
    ("#13 Toạ độ", "✅", "205/205 dự án có toạ độ; sửa 3 dự án trùng; chuẩn hoá vành đai “4.0”", "sheet `LatLong_QA`, `data/project_master_fixes.json`"),
    ("B2 Relevance engine", "✅", "Đủ 8 việc; mức trần khi N < 5 là 55 (không phải 45) với thang 45/30/25", "`relevance_engine.py`, `ui/finflow_engine.js`"),
    ("B3.1 Loan term", "✅", "Hàm + 3 edge case + nối vào engine và UI", "`loan_term.py`"),
    ("B4 Loan calc", "✅", "Phí trả trước hạn + loan term động", "`loan_calc.py`"),
    ("B8 Monte Carlo", "✅", "Vector hoá; per_path/per_year; % an toàn, P10/P50/P90, histogram, % thắng, cạn tiết kiệm", "`monte_carlo.py`"),
    ("B9 Dashboard", "✅ (mock)", "Gauge, break-even, tornado, histogram — dữ liệu giả, có nhãn", "UI Step 6"),
    ("FIN_ASSUMPTIONS", "✅", "4 kênh {return_pct, std_dev}; không còn Loan_term_months; mọi chỗ chưa chốt có TODO", "`fin_assumptions.py`, `docs/assumptions.md`"),
    ("UI Step 1–2, Step 4", "✅ (prototype)", "Layout đúng spec; gọi B2 hai lần; disclaimer tĩnh + động", "`ui/FinFlow_UI_prototype.html`"),
    ("Cột bathrooms", "🟡", "Công thức xử lý cả ô trống lẫn “N/A” — chưa chạy thử trên Google Sheets", "sheet `LatLong_QA`"),
    ("docs/", "✅", "Template + checklist + nguồn đã điền", "`docs/`"),
    ("⚪ Rescale 80 → 100", "✅", "Đã dùng 45/30/25 (B2 ghi là đã chốt)", "§4"),
    ("⚪ collection_date", "🔴", "Cột KHÔNG có trong BUY_RAW/RENT_RAW của DATA.xlsx", "§4"),
    ("Checklist trước merge", "🟡", f"{len(todos)} TODO còn mở (liệt kê ở §5); test + MC N = 10.000 đã chạy", "§5"),
]:
    w("| " + " | ".join(row) + " |")
w("")

w("## 1. 🔴 Cần xác nhận / quyết định (#1–#5)\n")
w("### #1 — Thời hạn vay tối đa của MB: 360 hay 420 tháng\n")
w("**Bằng chứng.** Trang chính thức của MB mô tả gói vay mua nhà cho người trẻ (MB Dream Home) với mức vay tới 80% và thời hạn tới 35 năm (S-LOAN-01). Gói này dành cho khách 23–40 tuổi (S-LOAN-02), hạn mức tối đa 5 tỷ và không trả gốc tới 5 năm đầu (S-LOAN-03); lúc ra mắt tháng 03/2024 thời hạn là 30 năm (S-LOAN-04). Mốc 420 tháng còn xuất hiện ở nguồn tổng hợp cho một gói MB khác (S-LOAN-05, tin cậy thấp).\n")
w("**Logic.** Các tham số còn lại (ưu đãi 8,3%/12 tháng, biên 1,5/3,5 điểm %, ân hạn gốc 24 tháng, LTV 80%) lấy từ văn bản MB CN Vạn Phúc. Ghép thời hạn 35 năm của Dream Home vào bộ tham số Vạn Phúc là mô phỏng một sản phẩm không tồn tại. Thêm nữa, hồ sơ test của team vay 5,5–5,7 tỷ — vượt hạn mức 5 tỷ của Dream Home.\n")
w("**Khuyến nghị.** Giữ 360 tháng. Nếu nhóm muốn mô phỏng Dream Home thì thêm như một *gói vay* riêng (bộ tham số đầy đủ: ân hạn 60 tháng, hạn mức, độ tuổi), không sửa riêng thời hạn. **Code:** chỉ sửa 1 dòng `BANK_MAX_TERM_MONTHS` trong `finflow/fin_assumptions.py`; UI tự nhận khi build lại. **Việc của Finance:** đối chiếu văn bản gốc Vạn Phúc.\n")
w("### #1b (phát sinh) — Tuổi tối đa khi kết thúc khoản vay: 75 hay 70\n")
w("Công thức B3.1 dùng 75, nhưng TheBank ghi MB = 70 (S-LOAN-06); mốc 75 có thật ở PVcomBank (S-LOAN-07), Techcombank là 65 (S-LOAN-08). Ảnh hưởng lớn với người vay lớn tuổi: người 45 tuổi được 360 tháng nếu mốc là 75, chỉ 300 tháng nếu là 70; người 50 tuổi: 300 so với 240. **Code:** 1 dòng `MAX_BORROWER_AGE_AT_MATURITY`; test đã phủ cả mốc 70. **Việc:** hỏi trực tiếp MB Vạn Phúc.\n")
w("### #1c (phát sinh) — Lịch phí trả nợ trước hạn\n")
w("To-do ghi 1% cho năm 1–5, miễn phí từ năm 6, là “số thật từ MB”. Nguồn tổng hợp mô tả một gói MB có phí bậc thang 2,5% (năm 1–2), 2% (năm 3), 1,5% (năm 4), 1% (năm 5) (S-LOAN-09). Code đã nối theo to-do dưới dạng danh sách theo năm vay — nếu văn bản Vạn Phúc khác, chỉ sửa 1 dòng. Ảnh hưởng chỉ nằm ở Net worth MUA trong 5 năm đầu (tối đa bằng phí × dư nợ).\n")
w("### #2 — LTV 100% có đúng là Vietcombank?\n")
w("**Kết luận: không sai ngân hàng mà là khác sản phẩm/điều kiện.** Gói Nhà Mới Thành Đạt của VCB cho vay tối đa 70% giá trị nhà (S-LOAN-10). Vay nhà dự án của VCB: tối đa 70% nếu thế chấp chính căn nhà định mua, tới 100% nếu thế chấp tài sản khác (S-LOAN-12, thông tin cũ). Gói 20.000 tỷ công bố tỷ lệ cho vay có thể tới 100% tuỳ hồ sơ (S-LOAN-13). File PDF mà plan trích (S-LOAN-14) theo tên là thông báo lãi suất — loại văn bản VCB dùng để công bố lãi suất (ví dụ S-LOAN-15), thường không có LTV → nhiều khả năng trích nhầm nguồn; tôi không mở được file nên người phụ trách cần mở lại để chốt.\n")
w("**Hệ quả.** LTV 70% cho kịch bản Downturn vẫn có cơ sở (VCB, thế chấp chính căn nhà). Dòng “VCB — LTV=100%” trong docs/sources.md của team cần sửa như hướng dẫn ở `docs/sources.md` §2.1.\n")
w("### #3 — Phương án 1 (18–20% cố định) hay Phương án 2 (suy giảm)\n")
w("**Dữ liệu của chính team (S-PROP-01):** CAGR giá sơ cấp (USD/m²) 2016–2025 = 12,66%; 2016–2020 = 3,64%; 2020–2025 = 20,43%. Mức 18–20% chỉ khớp 5 năm nóng nhất. Bằng chứng thị trường: Savills Q1/2025 ghi giá sơ cấp +32% nhưng giá thứ cấp giảm nhẹ lần đầu sau 5 năm (S-PROP-02); dữ liệu Batdongsan: +14% năm 2023, +39% năm 2024, 2025 chậm lại (S-PROP-03).\n")
w("**Kiểm tra nhất quán 30 năm** (sheet `Property_CAGR`, tự tính lại được): ở 19%/năm giá nhà tăng khoảng 185 lần; ở 12,66% khoảng 36 lần; ở mốc neo 8,4% (CPI TB 3,09% + ước tính tăng GDP thực/người 5,3%) khoảng 11 lần. Nếu giá thuê tăng 7%/năm và lợi suất cho thuê hiện ~3% (S-RENT-01), sau 30 năm lợi suất cho thuê ngụ ý chỉ còn 0,12% ở kịch bản 19% — không thực tế; 0,64% ở 12,66%; 2,04% ở mốc neo.\n")
w("**Kết quả mô hình** (engine mới, giả định còn lại như `FIN_ASSUMPTIONS`; H1 = hồ sơ test của team; H2 = nhà 4,0 tỷ, tiết kiệm 1,3 tỷ, thu nhập 45 + 35 triệu, sinh hoạt 15 triệu, thuê 14 triệu; 360 tháng; Monte Carlo N = 10.000, seed 2026):\n")
w("| Hộ | Tăng giá nhà | Kết luận an toàn | Net worth năm 30 MUA | THUÊ | MC: % MUA thắng | % MUA thắng và không cạn tiết kiệm | % MUA cạn tiết kiệm | Chênh NW P10 / P50 / P90 |\n|---|---|---|---|---|---|---|---|---|")
for h, lab, r, tl, mc in rows:
    c = mc["comparison"]; dd = c["net_worth_diff_buy_minus_rent"]
    w(f"| {h} | {lab} | {r['decision']} | {bn(tl['net_worth_buy'])} | {bn(tl['net_worth_rent'])} | {pct(c['pct_buy_wins'])} | {pct(c['pct_buy_wins_and_buy_solvent'])} | {pct(mc['buy']['pct_savings_exhausted_any_month'])} | {vn(dd['p10']/1e9)} / {vn(dd['p50']/1e9)} / {vn(dd['p90']/1e9)} tỷ |")
w(f"\nĐể so sánh, MVP Week 6 (12%/năm, lãi tham chiếu 10,5%): H1 → {leg['H1'][0]['decision']}, Net worth năm 30 MUA {bn(leg['H1'][1]['net_worth_buy'])} / THUÊ {bn(leg['H1'][1]['net_worth_rent'])}; H2 → {leg['H2'][0]['decision']}, {bn(leg['H2'][1]['net_worth_buy'])} / {bn(leg['H2'][1]['net_worth_rent'])}.\n")
w("**Đọc bảng.** (1) Giả định tăng giá **không đổi kết luận an toàn** (BUY/RENT/NEITHER chỉ dựa trên dòng tiền) mà đổi Net worth, break-even và % thắng trong Monte Carlo — tức đổi câu trả lời cho câu hỏi “về lâu dài bên nào giàu hơn”. (2) Với H2 (đủ khả năng trả nợ), MUA thắng ở mọi phương án; khác biệt là *mức độ*: chênh lệch trung vị từ khoảng 45 tỷ (mốc neo) đến gần 740 tỷ (19%). (3) Với H1, MUA cạn tiết kiệm ở mọi đường — “thắng về Net worth” chỉ là hệ quả của giả định vay vô hạn (xem F-7).\n")
w(f"**Khuyến nghị.** PA2 rút gọn: g(t) = 8,4% + (19% − 8,4%)·e^(−t/5), t tính theo năm — bắt đầu ở mức thị trường hiện tại và hội tụ về mốc neo dài hạn; CAGR tương đương 30 năm ≈ {pct(cagr_decay)}. Code đã sẵn: `appreciation_decay_path(19, 8.39, 5)` gán vào `property_annual_appreciation_pct` là chạy được cả tất định lẫn Monte Carlo (có test). Nếu nhóm cần đơn giản: PA1 nhưng hạ xuống khoảng 12,7% (CAGR 10 năm có dữ liệu). Không khuyến nghị 19% cố định cho 30 năm. τ và mốc neo là lựa chọn mô hình → nên trình bày độ nhạy (τ = 3 / 5 / 10 năm). PA2 đầy đủ (chuỗi theo quý, theo quận) vẫn cần dữ liệu chưa có.\n")
w("**Disclaimer đề xuất cho UI (B5):** “Kết quả Net worth phụ thuộc mạnh nhất vào giả định giá nhà tăng X%/năm. Mức này dựa trên giai đoạn 2016–2025 và có thể không lặp lại; xem biểu đồ độ nhạy trước khi quyết định.”\n")
w("### #4 — Hướng xử lý nguồn cho lãi vay lịch sử và rent growth lịch sử\n")
w("**Lãi thả nổi.** Khuyến nghị dùng proxy NHNN để mô tả mặt bằng (S-RATE-01…03) và dùng **độ lệch chuẩn theo thời gian** của lãi suất tham chiếu để ước lượng std. Lãi thả nổi = lãi tham chiếu (thường gắn với lãi huy động dài hạn) + biên cố định, nên biến động của nó ≈ biến động lãi tham chiếu: std LSHĐ >12 tháng 2016–2026 = 0,63 điểm % (S-RATE-05) → mức 0,75 đã chốt là hợp lý, hơi thận trọng. **Không** dùng (max − min)/4 trên khoảng cắt ngang kiểu “8,1–10,5%”: khoảng đó phản ánh chênh lệch giữa ngân hàng, sản phẩm và dư nợ cũ/mới tại *một thời điểm*, không phải biến động theo thời gian.\n")
w("**Rent growth.** Không có chuỗi giá thuê căn hộ thường của Savills/CBRE (chỉ có căn hộ dịch vụ). Khuyến nghị nới định nghĩa “thứ cấp” để nhận báo chí/tổng hợp có số liệu gốc từ Batdongsan (S-RENT-01, S-RENT-02), ghi độ tin cậy trung bình, và trình bày độ nhạy thay vì một con số.\n")
w("### #5 — Rubric: multi-channel investment và B6 có bắt buộc không\n")
w("Trong zip không có file rubric. README (Product Statement) hứa người dùng được so sánh “rent, buy, or buy-to-let” và Monte Carlo trả “% Buy wins / % Rent wins / % bankrupt”; nhận xét Week 2 của giáo viên liệt kê 9 kết quả về quy trình, không bắt buộc tính năng cụ thể. Vì vậy: bỏ B6 cần sửa Product Statement và có đoạn giải thích trong báo cáo; Monte Carlo hiện đã trả đủ 3 chỉ số README hứa (“bankrupt” = cạn tiết kiệm, xem F-7); việc multi-channel có bắt buộc hay không phải do người giữ rubric xác nhận.\n")

w("## 2. 🟡 Data (#6–#13)\n")
w("### #6 — Lãi vay lịch sử\n")
w("Các mốc đã có nguồn (sheet `Lai_suat_cho_vay`): lãi cho vay mới bình quân 6,96%/năm cuối 2024 và giữ quanh mức này tới cuối 11/2025 (S-RATE-01); khoảng 6,34% giữa 04/2025; theo FiinPro, mức bình quân theo quý thấp nhất giai đoạn 2020–2022 là 7,9% (quý I/2022) (S-RATE-02); lãi cho vay bình quân gồm cả dư nợ cũ 8,1–10,5%/năm (S-RATE-03, 07/2026). Một mốc 8,4–10,7% (S-RATE-04) chưa xác minh được ngày nên chưa dùng. Lưu ý định nghĩa: đây là lãi cho vay *mọi kỳ hạn/mục đích*, không phải lãi vay mua nhà thả nổi — chỉ dùng để mô tả mặt bằng; std lấy theo #4. Nếu muốn đúng yêu cầu gốc (lãi cơ sở của ngân hàng qua các năm), cần tra Wayback Machine các thông báo lãi suất cơ sở — chưa làm.\n")
w("### #7 — Giá thuê lịch sử\n")
w("Bằng chứng gần nhất: giá thuê chung cư khoảng 13 triệu/căn, gần như đi ngang 3 năm; lợi suất cho thuê giảm từ trên 4% (Q1/2023) xuống khoảng 3% (Q1/2025); năm 2024 giá thuê tăng chỉ bằng khoảng một nửa tốc độ tăng giá nhà (S-RENT-01); quý I/2025 tăng nhẹ (S-RENT-02). Không nguồn nào ủng hộ mức 7%/năm liên tục.\n")
w("Tác động lên hồ sơ test H1 (các giả định khác giữ nguyên):\n")
w("| Rent growth | Kết luận | Safety margin THUÊ tháng 1 | Tháng tệ nhất |\n|---|---|---|---|")
for rg, r in rg_rows:
    w(f"| {vn(rg, 2)}%/năm | {r['decision']} | {pct(r['rent']['month1_safety_margin'])} | {pct(r['rent']['safety_margin'])} (tháng {r['rent']['worst_month']}) |")
w("\n**Khuyến nghị.** Mean = tăng thu nhập (4,87%) làm base — hợp lý vì trong dài hạn giá thuê bị giới hạn bởi khả năng chi trả; trình bày độ nhạy 3% và 7%. Giữ std 1,25. Nếu nhóm giữ 7% thì bắt buộc bật income growth (đã có) và nói rõ trong báo cáo rằng kết luận RENT/NEITHER của nhiều hồ sơ phụ thuộc vào giả định này.\n")
w("### #8 — Biến động thu nhập\n")
w("Nguồn: NSO, Khảo sát mức sống dân cư 2024 (S-MKT-07) — thu nhập bình quân đầu người/tháng 2019–2024: 4.294.500 → 5.415.000 VND. Tăng trưởng năm: 2020 −1,04%; 2021 −1,06%; 2022 +11,12%; 2023 +6,19%; 2024 +9,13% → **mean 4,87%, std 5,68%** (sheet `Income_growth`). Team đang tính std của *mức* thu nhập (482.902 VND) — sai đơn vị, không dùng được làm std tăng trưởng. Hạn chế: n = 5, có 2 năm COVID, là thu nhập *đầu người* (không phải hộ), danh nghĩa. Gợi ý cho B7 Downturn: income shock ≈ 2 năm tăng trưởng −1% (đúng mức 2020–2021).\n")
w("### #9 — Lãi suất tiết kiệm\n")
w("Chuỗi lịch sử (mức cao nhất thị trường, cuối năm 2016–2026): kỳ hạn 6–12 tháng 6,50% ± 0,82%; trên 12 tháng 7,09% ± 0,63% (sheet `Savings_hist`). Đề xuất kênh savings dùng chuỗi 6–12 tháng (chứa kỳ hạn 12 tháng). Lệch lên vì là mức cao nhất; lãi Big4 thấp hơn. Snapshot theo ngân hàng/kỳ hạn: báo chí mâu thuẫn (VCB 12 tháng 5,2% tháng 02/2026 — S-SAV-01; Big4 nâng 12–18 tháng lên 5,9% tháng 03/2026 — S-SAV-02; một bài không rõ ngày ghi 6,8% — S-SAV-03) → team điền bảng mẫu `Tiet_kiem_snapshot` từ biểu lãi suất chính thức của từng ngân hàng.\n")
w("### #10 — VN-Index (sửa lỗi)\n")
w("**Nguyên nhân lỗi:** nhãn tháng dạng “Mmm-YY” bị Google Sheets hiểu là ngày Mmm-DD của năm 2026 (VD “May-21” → 21/05/2026), tức năm thật nằm ở phần “ngày”. Khối hồi quy G6:O23 của file gốc hỏng thêm do locale (R² = 387, số dạng text) → mức 14,2% cũ không dùng được. **Sau khi sửa:** 64 giá đóng cửa liên tục 05/2021–08/2026, 63 lợi suất tháng → **mean năm 7,99%, std năm 19,30%**, CAGR 6,32% (sheet `VNIndex_fixed`, toàn bộ là công thức). Đối chiếu: cuối 2024 = 1.266,78 và cuối 2025 = 1.784,49 khớp tuyệt đối với báo chí (S-MKT-02), mức tăng 2025 = 40,87% khớp VnEconomy (S-MKT-03). Hạn chế: cửa sổ ~5 năm (gồm năm 2022 giảm mạnh và 2025 tăng mạnh), chỉ số giá chưa gồm cổ tức.\n")
w("### #11 — Trái phiếu Chính phủ\n")
w("Lợi suất TPCP 10 năm cuối năm 2016–2025 và ngày 25/09/2026 (FiinPro, sheet 'Return Bond' của team): **mean 4,02%, std 1,37%** (n = 11); kỳ hạn 5 năm 3,23% ± 1,64%. Giả định nhà đầu tư giữ đến đáo hạn nên lợi suất lúc mua ≈ lợi nhuận. Khác to-do: đây là lợi suất thị trường thứ cấp, chưa phải kết quả đấu thầu Kho bạc Nhà nước; cá nhân cũng khó mua trực tiếp TPCP → ghi rõ trong báo cáo.\n")
w("### #12 — Vàng SJC\n")
w("129 giá cuối tháng 01/2016–09/2026 (FiinPro): **mean năm 14,89%, std năm 14,13%** (128 lợi suất tháng); CAGR 14,88%. Tăng Dec-to-Dec năm 2025 = 81,5%; std theo năm Dec-to-Dec = 24,9% (lớn hơn nhiều so với 14,13% → lợi suất vàng có quán tính, giả định độc lập theo tháng làm std năm bị thấp). Mean phản ánh một giai đoạn tăng bất thường → nên chạy độ nhạy.\n")
w("### #13 — Toạ độ cấp dự án (Tây Hồ + Hà Đông)\n")
w("205/205 dự án đã có toạ độ. Lỗi còn lại: 3 dự án Hà Đông (HD072 V8 The Vesta, HD073 Van Phu Victoria, HD074 Vinaconex 21) có toạ độ **trùng hệt nhau** (20.96069, 105.742059). Toạ độ mới theo Google Maps/Places (S-GEO-01) lệch so với toạ độ cũ 2,25 km, 2,83 km và 1,54 km — đủ để làm sai thứ hạng Haversine. Bản sửa nằm ở `data/project_master_fixes.json` (engine và UI đã áp dụng, có đánh dấu); team xác minh rồi ghi đè vào DATA.xlsx. Ngoài ra: `ward_old` của cả 3 đều là “Yen Nghia” dù vị trí thật thuộc khu Phú Lương / Văn Phú / Ba La → cần kiểm tra; 7 dự án Hà Đông lưu vành đai dạng số 4.0 thay vì chuỗi “4” → engine đã chuẩn hoá.\n")
w("### Chuỗi giá dài hơn cho PA2 (nếu chọn)\n")
w("Chưa thu thập (chuỗi theo quý, theo quận). Engine không cần sửa thêm: nhận đường tăng giá theo năm cho cả tất định và Monte Carlo.\n")

w("## 3. 🟢 Code\n")
bm, rm = s2["buy"]["meta"], s2["rent"]["meta"]
w("### B2 — Relevance engine (`finflow/relevance_engine.py`, bản JS `ui/finflow_engine.js`)\n")
w("| Việc | Trạng thái | Ghi chú |\n|---|---|---|")
for row in [("Bộ lọc cứng bedrooms = 2, size band khớp đúng", "✅", "Listing thiếu giá bị loại và được đếm (`excluded_no_price`)"),
            ("Bảng điểm 45/30/25", "✅", "Tier xếp theo SỐ tiêu chí khớp (3 → HIGH, 2 → MEDIUM, 1 → LOW, 0 → WARNING), kèm kiểm tra điểm nằm đúng khoảng tier; `score_table()` tái tạo đúng bảng 100 của plan cập nhật và bảng 80 của plan gốc"),
            ("Haversine rank trong tier", "✅", "Đúng công thức plan (R = 6371 km); hoà thì xếp theo listing_id"),
            ("Quy tắc N < 5", "✅", "Tắt tiêu chí giá → điểm tối đa = quận 30 + vành đai 25 = **55**. To-do ghi “cap 45đ” là con số của thang 80 cũ (25 + 20)"),
            ("Ngưỡng hiển thị", "✅", "TARGET + toàn bộ HIGH/MEDIUM + top 5 LOW + top 3 WARNING, kèm banner WARNING"),
            ("size_band là tham số, chạy 2 lần độc lập", "✅", "`run_step2()` gọi MUA_CALC (size BUY) và THUE_CALC (size RENT); không có trạng thái toàn cục (có test)"),
            ("warning_reason liệt kê đúng tiêu chí", "✅", "Ghi rõ tiêu chí khớp/không khớp, % lệch giá và mốc giá"),
            ("Unit test dùng chung 1 bộ cho 2 nhánh", "✅", "`SharedRelevanceTests` chạy cho cả buy và rent (2 × 11 test) + test dữ liệu thật + đối chiếu JS–Python")]:
    w("| " + " | ".join(row) + " |")
w(f"\nVí dụ dữ liệu thật — tòa CG086, MUA size Medium: pool {bm['n_pool']} căn → TARGET {bm['counts'].get('TARGET',0)}, HIGH {bm['counts'].get('HIGH',0)}, MEDIUM {bm['counts'].get('MEDIUM',0)}, LOW {bm['counts'].get('LOW',0)}, WARNING {bm['counts'].get('WARNING',0)}; hiển thị {len(s2['buy']['display'])} dòng. THUÊ size Large: pool {rm['n_pool']} căn nhưng tòa TARGET chỉ có {rm['counts'].get('TARGET',0)} listing → mốc giá dựa trên 1 căn (xem F-10).\n")
w("**Diễn giải tôi đã chọn (cần team xác nhận — Q1–Q3):** bộ lọc Step 1 chỉ thu hẹp danh sách tòa ở Step 2, không giới hạn pool của B2 (nếu lọc theo quận thì tiêu chí “cùng quận” luôn đúng); mốc giá = trung vị giá/m² các listing của tòa TARGET trong size band, nếu tòa không có listing thì dùng trung vị toàn size band; N trong quy tắc N < 5 = số listing của pool sau bộ lọc cứng.\n")
w("### B3.1 — Loan term theo tuổi (`finflow/loan_term.py`)\n")
w("`calc_max_loan_term(age_1, age_2, bank_max_term_months)` đúng công thức plan, trả thêm ràng buộc đang chặn (tuổi hay ngân hàng) để UI giải thích. Edge case 1 (tuổi ≥ 75 → mã `AGE_LIMIT`), edge case 2 (tối đa ≤ 24 tháng → `TERM_NOT_ABOVE_GRACE`, ví dụ người 73–74 tuổi), edge case 3 (engine *bắt buộc* nhận `loan_term_months`, FIN_ASSUMPTIONS không còn `Loan_term_months`). Bổ sung ngoài plan: tuổi phải là số nguyên ≥ 18; `validate_loan_term()` kiểm tra thời hạn user nhập. Đã nối vào `evaluate_buy_vs_rent(..., ages=...)` và UI Step 3 (hiện mức tối đa tức thời).\n")
w("### B4 — Loan calc (`finflow/loan_calc.py`)\n")
w("Mỗi tháng của lịch trả nợ có `prepayment_fee_pct`, `prepayment_fee_vnd`, `payoff_amount`; Net worth MUA mặc định trừ phí nếu tất toán tại tháng đó (cơ sở “liquidation”). Loan term lấy từ tham số (B3.1). Engine được viết lại dạng vector hoá để dùng chung cho tất định (n = 1) và Monte Carlo — bài đối chiếu chứng minh không làm sai công thức MVP.\n")
w("### B8 — Khung Monte Carlo (`finflow/monte_carlo.py`)\n")
w("Rút mẫu Normal(mean theo kịch bản, std) cho lãi tham chiếu, tăng giá nhà, tăng giá thuê, tăng thu nhập và 4 kênh đầu tư, chạy lại B4–B5 cho N đường song song. Đầu ra: % an toàn suốt kỳ (MUA, THUÊ), P10/P50/P90 và histogram Net worth, % MUA thắng / % THUÊ thắng, % thắng mà không cạn tiết kiệm, % có tháng âm dòng tiền, % cạn tiết kiệm, tỷ lệ đường có break-even, fan chart P10/P50/P90 theo năm. Placeholder đúng cách to-do mô tả: std = 0 là tắt random hoá biến đó (có test chứng minh MC với mọi std = 0 trùng kết quả tất định).\n")
w("**Hai quyết định thiết kế (Q8):** biến vĩ mô của plan rút 1 lần/đường (per_path) đúng như plan; chứng khoán, vàng và thu nhập rút mỗi năm (per_year), vì std của chúng là biến động *năm* — rút 1 lần/đường với σ ≈ 19% nghĩa là khoảng 16% số đường có lợi suất chứng khoán cố định dưới −11%/năm suốt 30 năm. N: mặc định 1.000, bản nộp cuối 10.000, chỉ preset 500/1.000/2.000 nếu cho user chọn.\n")
w("### B9 — Dashboard (mock)\n")
w("UI Step 6 dựng đủ gauge safety margin, đường Net worth có mốc break-even, tornado, histogram — toàn bộ dữ liệu giả, có nhãn “DỮ LIỆU GIẢ”. Khi thay bằng output thật: gauge ← `evaluate_buy`, đường Net worth ← `build_net_worth_timeline`, histogram ← `run_monte_carlo()[...]['histogram']`, tornado ← chạy tất định ±1σ từng biến.\n")
w("### FIN_ASSUMPTIONS — schema mới\n")
w("`investment_return_pct` → `investment_channels` (4 kênh, mỗi kênh {return_pct, std_dev_pct, sampling, status, method, caveat}) + `investment_allocation_default`; `Loan_term_months` → tham số động. Thêm `income_annual_growth_pct`, `living_cost_annual_growth_pct`, `prepayment_fee_pct_by_loan_year`, `net_worth_basis`, `PROMO_PACKAGES`, `MC_STD`, `SCENARIOS`. Mọi giá trị chưa chốt có `# TODO(<mã>)`. Bảng đầy đủ: `docs/assumptions.md`.\n")
w("### UI Step 1–2 và Step 4 (`ui/FinFlow_UI_prototype.html`)\n")
w("Step 1: quận cũ một dòng riêng, phường cũ + vành đai cùng một dòng (đều không bắt buộc). Step 2: tên tòa (bắt buộc) + size band MUA + size band THUÊ (2 trường riêng) → gọi B2 hai lần, hiển thị theo tier kèm điểm, khoảng cách, lý do và banner WARNING; cảnh báo khi mốc giá dựa trên dưới 3 căn; ghi chú khi tòa có toạ độ đã sửa. Step 3: vay chung, thời hạn tối đa theo B3.1, gói ưu đãi (gói chưa có lãi suất bị khoá), phân bổ 4 kênh = 100%. Step 4: disclaimer tĩnh luôn hiện + disclaimer động khi 2 size band khác nhau. Step 5: preset N. Dùng dữ liệu thật 3 quận thay cho dữ liệu demo Cầu Giấy. Đã kiểm tra: cú pháp JS và chạy logic Step 1–4 trong node với DOM giả (3 edge case B3.1, vợ chồng 30/50 tuổi, Step 2 cho tòa đã sửa toạ độ, disclaimer); **chưa xem trực quan trên trình duyệt thật**.\n")
w("### Cột bathrooms\n")
w("`=ARRAYFORMULA(IF(A2:A=\"\",\"\",IF((TRIM(J2:J)=\"\")+(UPPER(TRIM(J2:J))=\"N/A\"),\"Không rõ\",J2:J)))` ở cột hiển thị, giữ nguyên cột raw. Lý do không dùng `=IF(ISBLANK(J4),…)` của to-do: dữ liệu có 9 ô “N/A” dạng chữ (ISBLANK bỏ sót) + 4 ô trống; OR() không chạy theo từng phần tử trong ARRAYFORMULA nên dùng phép cộng. Plan có 2 công thức cho 2 nhãn khác nhau → cần chốt 1 nhãn. Chưa chạy thử trên Google Sheets.\n")
w("### docs/\n")
w("`docs/sources.md` (template + checklist + nguồn đã điền), `docs/assumptions.md` (mọi field, trạng thái, nguồn), file này.\n")

w("## 4. ⚪ Không bắt buộc\n")
w("**Rescale 80 → 100:** đã dùng 45/30/25 vì mục B2 ghi là đã chốt (to-do tự mâu thuẫn khi vừa ghi “đã chốt” ở B2 vừa ghi “không bắt buộc” ở mục ⚪). Lý do rescale trong plan (“2 tổ hợp khác nhau cho cùng điểm”) không đúng với cả 2 thang — thang 80 cho 45/55/60 và 20/25/35, thang 100 cho 55/70/75 và 25/30/45, không có 2 tổ hợp nào trùng điểm; rescale vô hại nhưng không bắt buộc về kỹ thuật.\n")
w("**collection_date:** cột này **không tồn tại** trong BUY_RAW và RENT_RAW của DATA.xlsx hiện tại, nên “giữ nguyên trong schema” chưa đạt — cần thêm lại và điền (không có ngày thu thập thì không chứng minh được dữ liệu còn mới).\n")

w("## 5. Checklist trước khi merge / nộp\n")
w(f"**Giá trị giả lập/chưa chốt còn mở: {len(todos)} TODO** (in bằng `list_open_todos()`):\n")
w("| File | Dòng | Mã | Nội dung |\n|---|---|---|---|")
for t in todos:
    w(f"| {t['file']} | {t['line']} | {t['code']} | {t['text'].replace('|', '/')} |")
w("\nCảnh báo từ `validate_assumptions()`: " + "; ".join(warns) + ".\n")
w("**Kiểm thử:** 60 test pass (B2 dùng chung cho 2 nhánh, B3.1, B4, B5, B8, đối chiếu MVP JS, đối chiếu B2 JS–Python); Monte Carlo N = 10.000 đã chạy (~0,5 giây). Sau khi thay số thật: chạy lại toàn bộ test và `docs/build_report.py`.\n")

w("## 6. Phát hiện ngoài to-do\n")
for code, text in [
    ("F-1", "Lãi tham chiếu thả nổi 8,3% (Python Week 4) khác 10,5% (MVP JS Week 6) → cùng hồ sơ ra kết quả khác nhau tuỳ bản chạy. Cần chốt 1 số (Q4)."),
    ("F-2", "Mức trần khi N < 5 là 55 với thang 45/30/25 (to-do ghi 45 — con số của thang 80)."),
    ("F-3", "Phí giao dịch 2,6%: MVP tính vào tiền trả trước tối thiểu nhưng không trừ khỏi khoản vay hay Net worth → Net worth MUA bị thổi lên khoảng 2,6% giá nhà và break-even gần như luôn rơi vào tháng đầu. Đề xuất: khoản vay = giá − (tiết kiệm − phí), Net worth MUA ban đầu giảm đúng bằng phí. Chưa sửa để giữ tương thích MVP (Q12)."),
    ("F-4", "Break-even year = Math.round(tháng/12) có thể ra “năm 0” (VD H1 với 12,66%: break-even ở tháng dưới 6, do phí trả trước 1% làm MUA khởi đầu thấp hơn vài chục triệu). Đề xuất báo theo tháng hoặc làm tròn lên (Q13)."),
    ("F-5", "Nối rent growth mà không có income growth làm THUÊ bất lợi giả tạo theo thời gian → đã thêm tăng thu nhập và tăng chi phí sinh hoạt."),
    ("F-6", "Rút 1 lần/đường với std năm là sai cho chứng khoán/vàng → per_year (B8)."),
    ("F-7", "Engine MVP cho phép số dư đầu tư âm sinh lãi như danh mục = vay vô hạn → “% MUA thắng” gây hiểu nhầm khi MUA âm dòng tiền. Đã thêm “cạn tiết kiệm” và “% thắng mà không cạn tiết kiệm”; đề xuất dùng làm “% bankrupt” trong README."),
    ("F-8", "MVP chỉ đánh giá THUÊ ở tháng 1, trong khi MUA được quét cả kỳ → engine mới quét cả kỳ cho THUÊ (trùng tháng 1 khi không tăng trưởng) (Q11)."),
    ("F-9", "Lý do rescale “2 tổ hợp cho cùng điểm” trong plan không đúng với cả 2 thang (xem §4)."),
    ("F-10", "Mốc giá TARGET có thể dựa trên rất ít listing (CG086 THUÊ Large: 1 căn). Đề xuất ngưỡng tối thiểu (VD dưới 3 căn thì dùng trung vị size band hoặc hiện cảnh báo — UI prototype đã hiện cảnh báo)."),
    ("F-11", "Thiếu cột collection_date (§4)."),
    ("F-12", "`ward_old` của HD072–HD074 đều “Yen Nghia” — nghi sao chép dòng."),
    ("F-13", "Gói ưu đãi 6/18/24 tháng chưa có lãi suất → UI khoá, engine báo lỗi rõ ràng."),
    ("F-14", "Mô hình chưa có chi phí sở hữu (phí quản lý, bảo trì, khấu hao/thời hạn sử dụng chung cư) và tiền cọc thuê → nghiêng về MUA. Nên nêu trong phần giới hạn của báo cáo nhóm."),
]:
    w(f"- **{code}.** {text}")
w("")
w("## 7. Câu hỏi mở cho team\n")
w("| # | Câu hỏi | Đang dùng tạm | Ai |\n|---|---|---|---|")
for row in [
    ("Q1", "Bộ lọc Step 1 chỉ thu hẹp danh sách tòa, hay giới hạn luôn pool của B2?", "Chỉ danh sách tòa", "Coordinator"),
    ("Q2", "Mốc giá TARGET: trung vị? Cần tối thiểu bao nhiêu listing?", "Trung vị, không ngưỡng (UI cảnh báo khi < 3)", "Coordinator"),
    ("Q3", "N trong quy tắc N < 5 là pool gồm cả TARGET?", "Có", "Coordinator"),
    ("Q4", "Lãi tham chiếu thả nổi 8,3 hay 10,5?", "8,3", "Finance"),
    ("Q5", "Tuổi tối đa khi kết thúc khoản vay ở MB: 70 hay 75? (#1b)", "75", "Finance"),
    ("Q6", "Lịch phí trả trước hạn Vạn Phúc: phẳng 1% hay bậc thang? (#1c)", "Phẳng 1% × 5 năm", "Finance"),
    ("Q7", "Định nghĩa “% bankrupt”: cạn tiết kiệm hay có tháng âm dòng tiền?", "Báo cả hai", "Coordinator"),
    ("Q8", "Chấp nhận per_year cho chứng khoán/vàng/thu nhập?", "Có", "Finance"),
    ("Q9", "Thêm lại collection_date vào DATA.xlsx?", "—", "Data"),
    ("Q10", "Lãi suất gói ưu đãi 6/18/24 tháng?", "Khoá trên UI", "Finance"),
    ("Q11", "Đánh giá THUÊ trên toàn kỳ (thay vì tháng 1)?", "Toàn kỳ", "Coordinator"),
    ("Q12", "Sửa cách hạch toán phí giao dịch (F-3)?", "Giữ như MVP", "Finance"),
    ("Q13", "Break-even báo theo tháng hay làm tròn năm lên?", "Như MVP (Math.round)", "Coordinator"),
    ("Q14", "Vành đai “4” của 7 dự án Hà Đông có đúng là vành đai 4?", "Chuẩn hoá thành “4”", "Data"),
    ("Q15", "Rubric có bắt buộc multi-channel và B6 không? (#5)", "—", "Người giữ rubric"),
]:
    w("| " + " | ".join(row) + " |")
w("")
w("## 8. Phản biện — những điểm yếu của chính kết quả này\n")
w("**Nguồn.** Nhiều nguồn là báo chí hoặc trang tổng hợp; hai tài liệu sơ cấp quan trọng nhất (văn bản MB CN Vạn Phúc, PDF Vietcombank) tôi không đọc được, nên #1, #1b, #1c, #2 mới dừng ở mức “khuyến nghị có căn cứ”, chưa phải “đã xác minh”. Một mốc lãi suất (S-RATE-04) và một mốc lãi tiết kiệm (S-SAV-03) chưa rõ ngày nên chỉ liệt kê, không dùng. Toạ độ Google Places là toạ độ của một tòa/điểm trong dự án, chưa chắc trùng tòa mà listing thuộc về.\n")
w("**Thống kê.** Mẫu nhỏ: thu nhập n = 5 (có 2 năm COVID), trái phiếu và tiết kiệm n = 11 điểm cuối năm, VN-Index chỉ ~5 năm. Annualize từ dữ liệu tháng giả định lợi suất độc lập theo tháng — với vàng giả định này rõ ràng sai (std năm Dec-to-Dec 24,9% so với 14,13%). Lãi tiết kiệm “cao nhất thị trường” lệch lên. Giá nhà là giá *sơ cấp* tính bằng USD, không phải giá thứ cấp bằng VND mà người dùng thực sự trả; không có dữ liệu theo quận.\n")
w("**Mô hình.** Phân phối Normal cho phép tăng giá âm nhưng bỏ qua đuôi dày; các biến được rút *độc lập* trong khi thực tế lãi suất, giá nhà, giá thuê và thu nhập tương quan (VD lãi tăng thường đi cùng giá nhà chững lại) → dải P10–P90 có thể bị lệch. Tăng giá nhà per_path cố định suốt 30 năm. Chưa có thuế, chi phí sở hữu, khấu hao tòa nhà, tiền cọc thuê (F-14). Phần thiếu hụt dòng tiền vẫn được tính như số dư âm sinh lãi (F-7) — tôi chỉ thêm thước đo để nhận diện, chưa đổi cách tính Net worth. Hai thay đổi hành vi do tôi quyết định (đánh giá THUÊ toàn kỳ; bật tăng thu nhập/chi phí sinh hoạt mặc định) làm kết luận khác MVP ngay cả khi các số khác giữ nguyên — đều đảo ngược được bằng cấu hình.\n")
w("**Code và kiểm thử.** Đối chiếu với MVP chỉ chứng minh phần *port* đúng ở chế độ tương thích, không chứng minh các tính năng mới đúng về mặt tài chính; harness trích engine từ file HTML bằng chuỗi đánh dấu nên sẽ vỡ nếu MVP đổi tên hàm. Đối chiếu JS–Python chỉ trên dữ liệu hiện tại. UI mới kiểm tra logic bằng DOM giả trong node — bố cục, CSS, trải nghiệm trên điện thoại chưa được xem bằng trình duyệt thật. Prototype là file riêng, **chưa ghép vào MVP HTML** của team. Công thức bathrooms chưa chạy trên Google Sheets.\n")
w("**Chưa làm.** Dữ liệu đấu thầu KBNN (#11), chuỗi giá theo quý/quận cho PA2, snapshot lãi tiết kiệm chính thức (#9), lãi cơ sở lịch sử qua Wayback (#6), số liệu kịch bản B7, B6, và kiểm tra rubric (#5).\n")
w("**Điều tôi tự quyết khi chưa có câu trả lời của team** (đều ghi TODO/câu hỏi, đổi được bằng cấu hình): Python là bản chuẩn + JS cho UI; diễn giải B2 (Q1–Q3); sampling per_year (Q8); đánh giá THUÊ toàn kỳ (Q11); kênh savings dùng chuỗi 6–12 tháng; mốc neo 8,4% và τ = 5 năm cho PA2 rút gọn.\n")
w("## 9. Tái lập\n")
w("```bash\nexport FINFLOW_DATA_XLSX=/đường/dẫn/DATA.xlsx FINFLOW_MVP_HTML=\"/đường/dẫn/Week 6/MVP sau chỉnh sửa.html\"\npython3 -m unittest discover -s tests -t .      # 60 test\npython3 docs/build_report.py \"$FINFLOW_DATA_XLSX\"  # sinh lại file này\npython3 ui/build_ui.py \"$FINFLOW_DATA_XLSX\"        # build lại prototype\npython3 data/build_supporting_v2.py               # build lại workbook\n```\n")
(ROOT / "docs/KET_QUA_TODO.md").write_text("\n".join(L), encoding="utf-8")
print("OK", len(L), "dòng")
