# Input Dictionary — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026-09-08. Người cập nhật: [Dương Phương Anh].

Theo mục 3 Week 3, input được chia 4 nhóm: **user-entered**, **product
information**, **scenario information**, **assumptions**. Bảng dưới liệt kê
từng input thật đang tồn tại trong code (`app.py`/`standalone/finflow.html`
Step 1–3, `loan_calc.py`, `evaluate.py`, `mua_thue_calc.py`).

## A. User-entered input (Step 1–3 trên UI)

| Input name | Meaning | Type | Unit | Example | Valid range | Missing value handling | Source/owner |
|---|---|---|---|---|---|---|---|
| `ward_old` | Phường (tên cũ) nơi user muốn tìm nhà | string (dropdown, lấy từ data) | — | `"Trung Hoa"` | Phải là 1 trong các giá trị unique lấy từ `get_unique_wards()` (9 phường trong `DATA_DEMO.xlsx`) | Bắt buộc — nếu rỗng, API trả lỗi 400 `"Missing required field: ward_old or size_band."` | user |
| `size_band` | Phân khúc diện tích | string (dropdown cố định) | — | `"Medium"` | 1 trong 3 giá trị cố định: `Small`, `Medium`, `Large` | Bắt buộc, cùng lỗi như trên | user |
| BUY listing đã chọn (`buy_listing`) | 1 căn hộ MUA cụ thể user chọn ở Step 2 (object, không phải số đơn lẻ) | object | — | `{listing_id: "BCG0156", total_price_vnd: 3780000000, ...}` | Phải có field `total_price_vnd` > 0 | Bắt buộc — thiếu thì lỗi 400 `"Missing required field: buy_listing"` | user (chọn từ danh sách do sản phẩm lọc sẵn) |
| RENT listing đã chọn (`rent_listing`) | 1 căn hộ THUÊ cụ thể user chọn ở Step 2 | object | — | `{listing_id: "RCG0037", rent_monthly_vnd: 16500000, ...}` | Phải có field `rent_monthly_vnd` > 0 | Bắt buộc, cùng cơ chế như trên | user |
| `income1` | Thu nhập tháng của người thứ nhất (chủ hộ) | number | **triệu VNĐ** (UI) → quy đổi sang VNĐ trước khi tính (×1,000,000, xem `docs/assumptions.md` mục "Locked decision #9") | `25` (triệu) → 25,000,000 VNĐ | ≥ 0 | Bắt buộc — thiếu/rỗng → lỗi 400 | user |
| `income2` | Thu nhập tháng của người thứ hai (vợ/chồng, hoặc 0 nếu độc thân) | number | triệu VNĐ | `15` | ≥ 0 | Bắt buộc (nhập `0` nếu không có) | user |
| `savings` | Tổng tiền tiết kiệm hiện có, dùng làm khoản trả trước | number | triệu VNĐ | `2000` (= 2 tỷ) | ≥ 0 | Bắt buộc | user |
| `living_cost` | Chi phí sinh hoạt tối thiểu hàng tháng (ăn uống, đi lại, không tính tiền nhà) | number | triệu VNĐ | `10` | ≥ 0 | Bắt buộc | user |
| `existing_debt` | Nghĩa vụ nợ hiện có khác (vay tiêu dùng, trả góp xe...) | number | triệu VNĐ | `0` | ≥ 0 | Không bắt buộc, mặc định `0` | user |
| `loan_term_months` | Kỳ hạn vay do user tự chỉnh (Step 3) | integer | tháng | `360` | > 0 (số nguyên) | Không bắt buộc — bỏ trống thì dùng mặc định `FIN_ASSUMPTIONS["Loan_term_months"] = 360` | user |

## B. Product information (đặc tính sản phẩm vay/tài chính, không do user nhập)

| Input name | Meaning | Type | Unit | Example | Valid range | Source/owner |
|---|---|---|---|---|---|---|
| `total_price_vnd` | Giá bán căn hộ (đã có sẵn trong data, không tính lại) | number | VNĐ | `3,780,000,000` | > 0 | `DATA_DEMO.xlsx` (sheet `BUY_RAW_CG`) |
| `price_m2_vnd` | Đơn giá/m² (chỉ để hiển thị, không dùng trong công thức tài chính) | number | VNĐ/m² | `84,000,000` | > 0 | `DATA_DEMO.xlsx` |
| `rent_monthly_vnd` | Giá thuê hàng tháng | number | VNĐ/tháng | `16,500,000` | > 0 | `DATA_DEMO.xlsx` (sheet `RENT_RAW_CG`) |
| `area_m2`, `bedrooms`, `bathrooms` | Đặc tính căn hộ hiển thị trên card | number | m², phòng | `45.0`, `2.0`, `1.0` (`bathrooms` có thể là `None` — ẩn icon 🚿 khi đó) | > 0 (riêng `bathrooms` cho phép thiếu) | `DATA_DEMO.xlsx` |
| `beltway_zone` | Vị trí căn hộ so với vành đai (VD "1-2" = giữa vành đai 1 và 2) | string | — | `"2.5-3"` | Dạng `"X-Y"` | `DATA_DEMO.xlsx` (đã vá lỗi Excel tự đổi thành ngày tháng — xem `docs/sources.md`) |
| `address_street` | Tên đường (join từ `PROJECT_MASTER` theo `project_id`) | string | — | `"Nguyen Chanh"` | — | `DATA_DEMO.xlsx` sheet `PROJECT_MASTER` |

## C. Scenario information / Assumptions (`FIN_ASSUMPTIONS`, `loan_calc.py`)

Đây là **assumptions**, không phải input user nhập — nhưng theo mục 3 Week 3
vẫn cần liệt kê rõ vì chúng ảnh hưởng trực tiếp tới output. Xem giải thích đầy
đủ (kèm nguồn) tại `docs/assumptions.md`.

| Input name | Meaning | Type | Unit | Demo value | Source/owner |
|---|---|---|---|---|---|
| `interest_rate_promo_pct` | Lãi suất ưu đãi năm đầu | number | %/năm | `8.3` | product source — xem `docs/sources.md` |
| `promo_period_months` | Số tháng áp dụng lãi ưu đãi | int | tháng | `12` | product source |
| `interest_rate_float_ref_pct` | Lãi suất tham chiếu thả nổi (cố định trong bản demo, không random hoá) | number | %/năm | `8.3` | product source |
| `float_rate_margin_year1_pct` | Biên độ cộng thêm năm đầu sau ưu đãi | number | % | `1.5` | product source |
| `float_rate_margin_from_year2_pct` | Biên độ cộng thêm từ năm thứ 2 trở đi | number | % | `3.5` | product source |
| `grace_period_months` | Số tháng ân hạn gốc (chỉ trả lãi) | int | tháng | `24` | product source — **chưa xác nhận nguồn** |
| `max_loan_to_value_pct` | Tỷ lệ vay tối đa/giá trị tài sản (LTV) | number | % | `80` | product source (market norm) |
| `investment_return_pct` | Lợi suất giả định khi đầu tư tiền dư hàng tháng | number | %/năm | `6` | assumption nội bộ |
| `property_annual_appreciation_pct` | Tốc độ tăng giá bất động sản giả định | number | %/năm | `12` | problem/assumption evidence — xem `docs/sources.md` |
| `Loan_term_months` | Kỳ hạn vay mặc định (user có thể ghi đè bằng `loan_term_months`) | int | tháng | `360` | product source |

## D. Ghi chú validation & unit

- **Toàn bộ tiền do user nhập ở UI là đơn vị "triệu VNĐ"**, và **chỉ được quy
  đổi sang VNĐ đúng 1 lần**, ngay trước khi build payload gửi vào hàm tính
  toán (locked decision #9 của spec) — không sửa gì phía logic tính toán để
  nhận thẳng đơn vị "triệu".
- Toàn bộ dữ liệu listing trong `DATA_DEMO.xlsx` đã ở đơn vị VNĐ đầy đủ
  (không phải "triệu" hay "tỷ") — không cần quy đổi thêm.
- Chi tiết validation (số âm, thiếu field, sai kiểu, chia cho 0...) xem
  `docs/data-flow.md` mục "Input Validation".
