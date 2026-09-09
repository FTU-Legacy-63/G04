# Sample Calculation & Logic Test — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026\-09\-08. Người cập nhật: \[Dương Phương Anh\].
> Toàn bộ số liệu dưới đây là **output thật** lấy từ `python3 evaluate.py`
> (self\-test có sẵn trong repo), không phải số minh hoạ.

## 1\. Case C — Net worth BUY vs RENT theo thời gian (mục 6 spec, tính năng mới nhất)

Input: BUY `BCG0156` (CG014, `total_price_vnd=3,780,000,000`, area 45m²),
RENT `rent_monthly_vnd=18,000,000`, `income1/2, savings, living_cost` theo
test case gốc trong `evaluate.py`, `loan_term_months=360`.

| Năm | Tháng | Net worth BUY (VNĐ) | Net worth RENT (VNĐ) | Chênh lệch (BUY−RENT) |
| --- | --- | --- | --- | --- |
| 1 | 12 | 2,696,466,664 | 2,296,053,497 | \+400,413,167 |
| 5 | 60 | 6,035,326,691 | 3,674,480,732 | \+2,360,845,959 |
| 10 | 120 | 12,642,019,630 | 5,933,104,323 | \+6,708,915,307 |
| 30 | 360 | 129,317,059,207 | 26,108,361,019 | \+103,208,698,189 |

**Kiểm tra tay tháng 1 của Net worth RENT** (công thức đóng, không cần vòng
lặp — xem `docs/assumptions.md`):
`Net_worth_RENT(1) = Savings×(1+r) + Money_remaining_RENT`, kết quả code in
ra khớp đúng số tính tay: **2,024,000,000.00 VNĐ** cả hai bên.

**Kết luận đọc được từ bảng:** với bộ giả định demo hiện tại (đầu tư 6%/năm,
BĐS tăng 12%/năm), BUY luôn dẫn trước RENT về Net worth trong toàn bộ 30 năm
với case này → `find_break_even()` trả về `(None, None)` (không có điểm cắt)
— đã được assert đúng trong `evaluate.py` TEST 5.

## 2\. `find_break_even()` — kiểm tra đầy đủ 4 nhánh (dữ liệu tổng hợp)

| Kịch bản | Kỳ vọng | Actual | Status |
| --- | --- | --- | --- |
| Cắt từ dưới lên (BUY vượt RENT giữa kỳ) | `month=24, year=2` | `month=24, year=2` | ✅ |
| Cắt từ trên xuống (RENT vượt lại BUY) | `month=27, year=2` | `month=27, year=2` | ✅ |
| Không cắt nhau suốt kỳ | `(None, None)` | `(None, None)` | ✅ |
| BUY lỗi (không có series để so sánh) | `(None, None)` | `(None, None)` | ✅ |
| Case A trên dữ liệu thật (savings 1.5 tỷ) | Không có break\-even (BUY dẫn trước suốt kỳ) | `(None, None)` | ✅ |

## 3\. Kiểm tra khớp giữa bản Python (Flask) và bản JS (standalone)

Vì FinFlow có 2 bản triển khai cùng công thức (Python trong `app.py` \+
`evaluate.py`/`loan_calc.py`, và bản JS nhúng trong
`standalone/finflow.html`), nhóm đã chạy **cùng 1 input** qua cả 2 bản để
xác nhận không lệch số (kiểm bằng Playwright cho bản JS, so với chạy trực
tiếp `evaluate_buy_vs_rent()` cho bản Python):

| Input | BUY listing | RENT listing | `monthly_repayment` | `safety_margin` (BUY) | `safety_margin` (RENT) | `decision` |
| --- | --- | --- | --- | --- | --- | --- |
| `income1=50tr, income2=30tr, savings=2000tr, living_cost=10tr, loan_term=360` | BCG0156 (3.78B) | RCG0037 (16.5tr/tháng) | **12,311,667** (cả 2 bản) | **72\.11%** (cả 2 bản) | **66\.88%** (cả 2 bản) | **BUY** (cả 2 bản, `reason="BUY meets the safety threshold."`) |

→ Xác nhận bản JS port **không lệch 1 đồng** so với bản Python gốc.

## 4\. Ownership

| Việc | Người phụ trách |
| --- | --- |
| Viết test case C — Net worth (Python) | \[Dương Phương Anh\] |
| Đối chiếu Python vs JS (standalone) | \[Dương Phương Anh\] |
