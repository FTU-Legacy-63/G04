# Early Logic Test — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026\-09\-08. Người cập nhật: \[Dương Phương Anh\].
> Toàn bộ số liệu dưới đây là **output thật** lấy từ `python3 evaluate.py`
> (self\-test có sẵn trong repo), không phải số minh hoạ.

## 1\. Case A — nhánh hợp lệ (Savings đủ)

| Input | Expected process | Expected output | Actual (từ code) | Status |
| --- | --- | --- | --- | --- |
| BUY: project CG086, `total_price_vnd=7,200,000,000`. RENT cùng project, `rent_monthly_vnd=21,500,000`. `income1=30tr, income2=20tr, savings=1,500tr, living_cost=12tr, existing_debt=0` | `min_down_payment = 7.2B×(1−0.8) = 1.44B` (đủ, vì savings 1.5B ≥ 1.44B) → `required_loan = 7.2B − 1.5B = 5.7B` → tháng 1 đang trong ân hạn (24 tháng đầu) nên `interest = 5.7B×8.3%/12 = 39,425,000`, `principal=0` | `Monthly_repayment = 39,425,000`; `Money_remaining_BUY = 50,000,000−12,000,000−0−39,425,000 = −1,425,000`; `Safety_margin_BUY = −2.85%` (\< ngưỡng 30% cho tier 50–75tr) → BUY không an toàn | `Required_loan=5,700,000,000`; `Monthly_repayment=39,425,000`; `Money_remaining=-1,425,000`; `Safety_margin=-2.85%`; `is_safe=False` | ✅ Khớp 100% |
| RENT cùng input tài chính | `Money_remaining_RENT = 50,000,000−12,000,000−0−21,500,000 = 16,500,000`; `Safety_margin = 16,500,000/50,000,000 = 33%` (≥ ngưỡng 30%) → an toàn | `Money_remaining=16,500,000`, `Safety_margin=33%`, an toàn | Đúng như cột trước | ✅ Khớp 100% |
| Quyết định cuối | RENT an toàn \+ margin (33%) \> BUY margin (−2.85%) → chọn RENT | `decision="RENT"` | `decision="RENT"`, `reason="RENT meets the safety threshold and has a higher safety margin than BUY."` | ✅ Khớp |

## 2\. Case A2 — nhánh báo lỗi (Savings không đủ)

| Input | Expected process | Expected output | Actual | Status |
| --- | --- | --- | --- | --- |
| Giống Case A nhưng `savings=1,000,000,000` (giảm) | `min_down_payment=1.44B > savings 1.0B` → thiếu `1.44B−1.0B=440,000,000` → BUY phải báo lỗi ngay, KHÔNG tính tiếp Money\_remaining/Safety\_margin | `error="You need at least 440,000,000 more in savings to qualify for this loan (max LTV 80%)."` | Đúng nguyên văn | ✅ Khớp |
| Quyết định cuối | BUY không khả thi → chỉ xét RENT (vẫn an toàn 33%) → chọn RENT | `decision="RENT"` | `decision="RENT"`, `reason="BUY not viable due to insufficient savings — RENT meets the safety threshold."` | ✅ Khớp |

## 3\. Case B — cả BUY và RENT đều không an toàn (nhánh NEITHER)

| Input | Expected process | Expected output | Actual | Status |
| --- | --- | --- | --- | --- |
| BUY: `total_price_vnd=3,990,000,000`, RENT: `rent_monthly_vnd=13,500,000`. `income1=20tr, income2=10tr, savings=600tr, living_cost=8tr` | `min_down_payment=3.99B×20%=798,000,000 > savings 600,000,000` → thiếu 198,000,000 → BUY lỗi | `error` với shortfall `198,000,000` | `"You need at least 198,000,000 more in savings..."` | ✅ Khớp |
| RENT | `total_income=30tr` → tier `<35tr` → ngưỡng 40%. `Money_remaining=30M−8M−13.5M=8.5M`, `Safety_margin=28.33%` (\< 40%) → KHÔNG an toàn | `is_safe=False` | `Safety_margin=28.33%`, `is_safe=False` | ✅ Khớp |
| Quyết định cuối | Cả 2 đều không an toàn → NEITHER | `decision="NEITHER"` | `decision="NEITHER"`, `reason="BUY not viable due to insufficient savings, and RENT also does not meet the safety threshold."` | ✅ Khớp |

## 4\. Kiểm tra format/đọc file nguồn

| Kiểm tra | Kỳ vọng | Actual | Status |
| --- | --- | --- | --- |
| `DATA_DEMO.xlsx` đọc được bằng `openpyxl` (không lỗi format) | Đọc thành công 3 sheet | Đọc thành công, tổng 91 project / 309 BUY / 129 RENT dòng thật | ✅ |
| Dòng đệm (`listing_id` rỗng) bị bỏ qua đúng | 1000 dòng/sheet nhưng chỉ giữ lại dòng có `listing_id` | 309/1000 (BUY), 129/1000 (RENT) | ✅ |
| `beltway_zone="1-2"` (project CG087, RENT) không bị Excel tự đổi thành ngày tháng | Trả về string `"1-2"` | Trả về đúng `"1-2"` sau khi vá `_fix_excel_autodate()` | ✅ (trước khi vá: trả về `datetime.datetime(2026,1,2)`, đã ghi trong `docs/sources.md`) |
| `address_street` join đúng theo `project_id` | Cùng `project_id` → cùng `address_street` | Đã assert trong `mua_thue_calc.py::__main__` (`BCG0054`/`RCG0032`, cùng CG086) | ✅ |

## 5\. Ownership

| Việc | Người phụ trách |
| --- | --- |
| Viết test case A/A2/B (Python) | \[Dương Phương Anh\] |
| Kiểm tra format DATA\_DEMO.xlsx | \[Dương Phương Anh\] |
