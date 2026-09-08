# Data Structure & Data Flow — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026-09-08. Người cập nhật: [Dương Phương Anh].

## 1. Data structure (mục 8 Week 3)

Sản phẩm dùng **2 hình thức lưu trữ**, không dùng database:

1. **`DATA_DEMO.xlsx`** — 1 file Excel, 3 sheet, đọc bằng `openpyxl`
   (`read_only=True, data_only=True`) — đây là nguồn dữ liệu gốc, chỉ đọc,
   không ghi ngược lại.
   - `PROJECT_MASTER` (91 dòng thật): `project_id, project_name,
     district_old, ward_old, ward_2025, beltway_zone, address_street`
   - `BUY_RAW_CG` (309 dòng thật / 1000 dòng có đệm): `listing_id,
     project_id, district_old, ward_old, ward_2025, beltway_zone, area_m2,
     size_band, bedrooms, bathrooms, total_price_billion_vnd_input,
     total_price_vnd, price_m2_vnd, project_name`
   - `RENT_RAW_CG` (129 dòng thật / 1000 dòng có đệm): tương tự `BUY_RAW_CG`
     nhưng có `rent_monthly_million_vnd_input`/`rent_monthly_vnd` thay vì giá
     bán.
2. **Object trong code** (dict/JS object) — kết quả sau khi lọc + join, được
   truyền thẳng giữa các hàm/qua JSON, không lưu file trung gian:
   - `mua_calc()`/`thue_calc()` trả `list[dict]`, mỗi dict là 1 listing đã
     join `address_street`.
   - `loan_calc()` trả `dict` gồm `min_down_payment`, `required_loan`,
     `error`, `schedule` (list 360 dict, 1 dict/tháng).
   - `evaluate_buy_vs_rent()` trả `dict` tổng hợp `buy`, `rent`, `decision`,
     `reason`, `net_worth` (gồm `buy_series`, `rent_series`,
     `break_even_month`, `break_even_year`).

**Có 2 bản triển khai song song, cùng 1 cấu trúc dữ liệu:**

- Bản Flask (`app.py` + `evaluate.py`/`loan_calc.py`/`mua_thue_calc.py` bằng
  Python) — đọc `DATA_DEMO.xlsx` trực tiếp mỗi lần gọi API.
- Bản standalone (`standalone/finflow.html`) — toàn bộ 309 BUY + 129 RENT đã
  được xuất sẵn thành JSON và **nhúng thẳng vào file HTML** dưới dạng hằng số
  JS `BUY_LISTINGS`/`RENT_LISTINGS`, cùng bản port JS 1:1 của mọi công thức
  Python — không cần server, không cần đọc file `.xlsx` lúc chạy.

**Vì sao không dùng database:** dữ liệu tĩnh trong suốt vòng đời demo, không
cần ghi/cập nhật đồng thời nhiều user, không cần transaction — 1 file Excel
đọc-only (hoặc JSON nhúng sẵn) đơn giản và dễ kiểm tra hơn nhiều so với dựng
database chỉ để "trông chuyên nghiệp".

## 2. Data flow (mục 9 Week 3)

```
Source/User                     Input                          Validation                                  Process                                          Output
────────────                   ───────                        ────────────                                ─────────                                        ────────
DATA_DEMO.xlsx        →   ward_old, size_band       →   phải khớp 1 trong danh sách    →   mua_calc()/thue_calc() lọc (ward_old,        →   Danh sách card BUY/RENT
(BUY_RAW_CG/RENT_RAW_CG/       (user chọn ở Step 1)        unique lấy từ get_unique_wards()      size_band, bedrooms=2.0) + join                (Step 2)
 PROJECT_MASTER)                                                                                  address_street từ PROJECT_MASTER

Danh sách card (trên)  →   buy_listing, rent_listing →   phải có total_price_vnd > 0    →   User click chọn 1 BUY + 1 RENT             →   2 object listing đã chọn
                            (user chọn ở Step 2)           / rent_monthly_vnd > 0

User nhập tay           →   income1, income2,          →  _parse_nonneg_float(): phải     →   ×1,000,000 (locked decision #9) ngay        →   income/savings/... đơn vị VNĐ
(Step 3, đơn vị triệu)       savings, living_cost,          là số hợp lệ, không âm             trước khi build payload
                             existing_debt, loan_term_months →  loan_term_months (nếu có)
                                                                 phải là số nguyên > 0

Tất cả input trên       →   evaluate_buy_vs_rent(...)  →   income1+income2 > 0            →   loan_calc() (Method A, dư nợ giảm dần,      →   result = {buy, rent, decision,
                                                             (chặn chia cho 0 ở                mở rộng vòng lặp tính Net worth BUY)             reason, net_worth: {buy_series,
                                                             Safety_margin)                →   evaluate_buy()/evaluate_rent() tính              rent_series, break_even_month,
                                                                                                 Safety_margin, so hạn mức theo bậc                break_even_year}}
                                                                                                 thu nhập (docs/assumptions.md §3)
                                                                                             →   net_worth_rent_schedule() (công thức đóng)
                                                                                             →   find_break_even() (dò điểm cắt)
                                                                                             →   decide() (BUY / RENT / NEITHER)

result (trên)           →   build_net_worth_timeline() →   —                              →   Sample lại theo NĂM (t=12,24,36...)         →   Step 4: 2 result card
                                                                                                 khớp đúng độ dài loan_term_months               (progress bar an toàn) +
                                                                                                 user chọn                                       biểu đồ Net worth theo năm
                                                                                                                                                  (đánh dấu break-even nếu có)
```

Ví dụ cụ thể (Case C, đã kiểm chứng — xem `docs/logic-test.md`):

```
DATA_DEMO.xlsx (BUY_RAW_CG, ward_old=Trung Hoa, size_band=Small)
  → user chọn listing BCG0156 (total_price_vnd = 3,780,000,000)
  → user chọn listing RCG0037 (rent_monthly_vnd = 16,500,000)
  → user nhập income1=50tr, income2=30tr, savings=2000tr, living_cost=10tr, loan_term=360
  → validate OK (đủ savings ≥ min_down_payment 756,000,000)
  → loan_calc(): required_loan=1,780,000,000, monthly_repayment tháng 1=12,311,667
  → evaluate_buy_vs_rent(): decision="BUY", reason="BUY meets the safety threshold."
  → build_net_worth_timeline(): 30 điểm (năm 1..30), net_worth_buy tại năm 30 ≈ 167,488,630,821 VNĐ
```

## 3. Input Validation (mục 10 Week 3)

Validation được thực hiện ở **2 lớp giống hệt nhau** (do có 2 bản triển
khai): phía Python (`app.py::_parse_nonneg_float`,
`app.py::_validate_listing`) và phía JS (`standalone/finflow.html`, trong
handler của nút Calculate) — cùng thông điệp lỗi tiếng Anh để đồng nhất trải
nghiệm.

| Loại kiểm tra | Áp dụng cho | Quy tắc | Thông điệp lỗi (ví dụ thật trong code) |
|---|---|---|---|
| Required input | `ward_old`, `size_band`, `buy_listing`, `rent_listing`, `income1`, `income2`, `savings`, `living_cost` | Không được rỗng/`None` | `"Missing required field: ward_old or size_band."` / `"Missing required field: buy_listing"` |
| Number format | `income1/2`, `savings`, `living_cost`, `existing_debt` | Phải convert được sang `float` | `"Field 'income1' must be a valid number, got: 'abc'"` |
| Negative value | tất cả field tiền + `existing_debt` | `< 0` → lỗi | `"Value 'savings' cannot be negative."` |
| Impossible range | `loan_term_months` | phải là số nguyên `> 0` | `"'loan_term_months' must be a valid integer."` / `"...must be greater than 0."` |
| Missing/invalid category | `buy_listing`/`rent_listing` thiếu field giá | phải có `total_price_vnd`/`rent_monthly_vnd` và `> 0` | `"'buy_listing' is missing field 'total_price_vnd'."` / `"'buy_listing.total_price_vnd' must be greater than 0."` |
| Chia cho 0 | `income1 + income2` | phải `> 0` (mẫu số của `Safety_margin`) | `"Total income (Income1 + Income2) must be greater than 0 to calculate the safety margin."` |
| Body JSON không hợp lệ (chỉ bản Flask) | toàn bộ request `/api/evaluate` | phải parse được thành JSON object | `"Request body must be a valid JSON object."` |
| Unit mismatch (locked decision #9) | mọi input tiền từ UI | UI luôn nhập "triệu VNĐ", chuyển đổi `×1,000,000` **đúng 1 lần** ngay trước khi build payload — không được để lẫn đơn vị "triệu" và "VNĐ đầy đủ" trong cùng 1 object | Xem `docs/assumptions.md` mục 4 |
| Lỗi nghiệp vụ (không phải lỗi input format) | `savings < min_down_payment` | Không dùng `MIN()` để âm thầm hạ khoản vay — báo lỗi rõ | `"You need at least {shortfall:,.0f} more in savings to qualify for this loan (max LTV {max_ltv_pct}%)."` |

**Chưa kiểm tra (limitation cần ghi nhận):**
- Không giới hạn giá trị tối đa (vd. `income1 = 999,999,999,999` vẫn được
  chấp nhận) — chỉ chặn âm, chưa chặn "vô lý lớn".
- Không kiểm tra tính nhất quán giữa `size_band` của listing đã chọn với
  `size_band` đã chọn ở Step 1 (tin tưởng UI luôn đồng bộ 2 giá trị này).

## 4. Ownership của Data và Evidence (mục 12 Week 3)

Theo đúng 6 đầu mục guide yêu cầu — không mô tả chung chung "cả nhóm tìm dữ
liệu":

| Đầu mục | Việc cụ thể trong FinFlow | Người phụ trách |
|---|---|---|
| **Source added by** | Đưa `DATA_DEMO.xlsx` vào repo | [Dương Phương Anh] |
| **Source verified by** | Xác minh 3 sheet (`PROJECT_MASTER`/`BUY_RAW_CG`/`RENT_RAW_CG`) đủ field, đúng số dòng thật (91/309/129) như spec mô tả | [Dương Phương Anh] |
| **Data cleaned by** | Lọc bỏ dòng đệm (`listing_id` rỗng); phát hiện + vá lỗi Excel tự đổi `beltway_zone="1-2"` thành kiểu ngày tháng (`_fix_excel_autodate()`) | [Dương Phương Anh] |
| **Structure designed by** | Thiết kế schema gốc `PROJECT_MASTER`/`MUA_RAW`/`THUE_RAW` + logic `MUA_CALC`/`THUE_CALC` (tài liệu kế hoạch "FINAL PLAN — BUY vs RENT") — bản triển khai thật (`mua_thue_calc.py`) là phiên bản đơn giản hoá của thiết kế này (bỏ phần comparable-listing/relevance scoring theo locked decision #6) | Dương Phương Anh (thiết kế gốc); chọn cấu trúc lưu trữ triển khai thật (đọc trực tiếp `.xlsx` cho bản Flask, JSON nhúng sẵn cho bản standalone): [Dương Phương Anh] |
| **Validation tested by** | Viết + chạy thử 7 loại validation ở mục 3 phía trên (`app.py::_parse_nonneg_float`/`_validate_listing`, và bản JS tương ứng) | [Dương Phương Anh] |
| **Logic integration by** | Nối `mua_calc()`/`thue_calc()` (data đã lọc) vào `loan_calc()`/`evaluate.py` (công thức tài chính); port toàn bộ sang JS cho bản standalone | [Dương Phương Anh] |
