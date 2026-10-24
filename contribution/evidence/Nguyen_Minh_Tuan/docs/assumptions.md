# docs/assumptions.md — FIN_ASSUMPTIONS (schema mới, 29/09/2026)

Trạng thái: ✅ chốt · 🟡 đề xuất, chờ Coordinator + Finance duyệt · 🔴 giả lập/chờ xác nhận (phải xử lý trước khi nộp).
Code: `finflow/fin_assumptions.py` (mỗi dòng chưa chốt có `# TODO(<mã>)`; chạy `list_open_todos()` để rà). ID nguồn: `docs/sources.md`.

## 1. Vay (MB Bank – CN Vạn Phúc)

| Field | Giá trị | Trạng thái | Nguồn | Ghi chú |
|---|---|---|---|---|
| interest_rate_promo_pct | 8,3 | ✅ | S-LOAN-00 | Gói 12 tháng |
| promo_period_months | 12 | ✅ | S-LOAN-00 | UI cho chọn 6/12/18/24; chỉ gói 12 có lãi suất (`PROMO_PACKAGES`) |
| interest_rate_float_ref_pct | 8,3 | 🔴 Q4 | S-LOAN-00 | MVP JS đang dùng 10,5 → chốt 1 số |
| float_rate_margin_year1_pct / from_year2 | 1,5 / 3,5 | ✅ | S-LOAN-00 | |
| grace_period_months | 24 | ✅ | S-LOAN-00 | |
| max_loan_to_value_pct | 80 | ✅ | S-LOAN-00 | Downturn 70% (S-LOAN-10, 12) |
| buy_closing_costs_pct | 2,6 | 🟡 | kế thừa MVP | Chưa thấy nguồn; cách hạch toán cần sửa (F-3) |
| bank_max_term_months | 360 | 🔴 #1 | S-LOAN-00…05 | Khuyến nghị giữ 360 |
| max_borrower_age_at_maturity | 75 | 🔴 #1b | S-LOAN-06…08 | MB có thể là 70 |
| min_borrower_age | 18 | ✅ | S-LOAN-07 | Điều kiện chung |
| prepayment_fee_pct_by_loan_year | [1, 1, 1, 1, 1] | 🔴 #1c | to-do / S-LOAN-09 | Nguồn công khai có bậc thang 2,5→1% |
| net_worth_basis | "liquidation" | 🟡 | B4 | Net worth BUY trừ phí nếu tất toán ở tháng t |

## 2. Tăng trưởng (B5)

| Field | Giá trị | Trạng thái | Nguồn | Ghi chú |
|---|---|---|---|---|
| property_annual_appreciation_pct | 19,0 | 🔴 #3 | S-PROP-01…03 | Nhận số hoặc đường theo năm (`appreciation_decay_path`) |
| rent_annual_growth_pct | 7,0 | 🔴 #7 | S-RENT-01…02 | Bằng chứng: thuê gần đi ngang 2022–2025 |
| income_annual_growth_pct | 4,87 | 🟡 MỚI | S-MKT-07 | Bắt buộc có khi bật rent growth |
| living_cost_annual_growth_pct | 3,09 | 🟡 MỚI | S-MKT-08 | CPI TB 2016–2025 |

## 3. Bốn kênh đầu tư (thay `investment_return_pct = 6`)

| Kênh | return_pct | std_dev_pct | Sampling | Cửa sổ, n | Nguồn | Lưu ý |
|---|---|---|---|---|---|---|
| savings | 6,50 | 0,82 | per_path | cuối năm 2016–2026, n=11 | S-MKT-06 | Mức cao nhất → lệch lên |
| stocks | 7,99 | 19,30 | per_year | tháng 05/2021–08/2026, n=63 | S-MKT-01…03 | Chỉ số giá, cửa sổ ngắn |
| bonds | 4,02 | 1,37 | per_path | cuối năm 2016–2026, n=11 | S-MKT-05 | Giữ đến đáo hạn |
| gold | 14,89 | 14,13 | per_year | tháng 01/2016–09/2026, n=128 | S-MKT-04 | Std Dec-to-Dec = 24,9% |

Phân bổ mặc định: 100% savings. Tổng 4 kênh phải = 100% (`validate_allocation`).

## 4. Monte Carlo (B8)

| Biến | Std | Sampling | Trạng thái |
|---|---|---|---|
| interest_rate_float_ref_pct | 0,75 điểm % | per_path | ✅ (S-RATE-05 ủng hộ) |
| property_annual_appreciation_pct | 4,0 | per_path | ✅ |
| rent_annual_growth_pct | 1,25 | per_path | ✅ (mean chờ #7) |
| income_annual_growth_pct | 5,68 | per_year | 🟡 (S-MKT-07; n=5) |
| 4 kênh đầu tư | xem mục 3 | theo kênh | 🟡 |

N: mặc định 1.000; bản nộp cuối 10.000 (`final_run=True`, ~0,5 giây); nếu cho user chọn thì chỉ 500/1.000/2.000; cảnh báo khi N < 500.

## 5. Kịch bản B7 (placeholder theo khoảng trong plan — chốt ở Giai đoạn 5)

| Kịch bản | Tăng giá nhà | Tăng giá thuê | LTV | Lãi tham chiếu |
|---|---|---|---|---|
| boom | 27,5 | 10,0 | 95 | −0,75 |
| stable | theo FIN_ASSUMPTIONS | theo FIN_ASSUMPTIONS | 80 | 0 |
| downturn | 2,5 | 4,0 | 70 | +0,75 |

## 6. Khác biệt so với MVP Week 6 (`LEGACY_MVP_OVERRIDES` tái tạo đúng MVP)

| Nội dung | MVP Week 6 | Engine mới |
|---|---|---|
| Lãi tham chiếu | 10,5 | 8,3 (chờ Q4) |
| Tăng giá nhà | 12 | 19 (chờ #3) |
| Tăng giá thuê / thu nhập / sinh hoạt | 0 / 0 / 0 (chưa nối) | 7 / 4,87 / 3,09 |
| Thời hạn vay | hằng số 360 | tham số, tối đa theo tuổi (B3.1) |
| Phí trả trước hạn | không có | có, Net worth cơ sở thanh lý |
| Đầu tư | 1 số 6% | 4 kênh, phân bổ |
| Đánh giá RENT | tháng 1 | tháng tệ nhất toàn kỳ (trùng tháng 1 khi không tăng trưởng) |
