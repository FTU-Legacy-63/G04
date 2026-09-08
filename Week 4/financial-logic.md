# Financial Logic — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026-09-08. Người cập nhật: [Dương Phương Anh].

## 1. Project Logic Chain (mục 3 Week 4)

```
Problem                    → Người trẻ/hộ gia đình ở Hà Nội khó so sánh chi phí thật sự
                              giữa MUA và THUÊ nhà — 2 phương án dùng đơn vị thời gian và
                              cấu trúc chi phí khác nhau (trả góp dài hạn có lãi vs thuê
                              hàng tháng cố định), khó quy về cùng 1 thước đo.
                              [⚠️ chưa có problem evidence độc lập — xem docs/sources.md §2]

Target user                → Người 25–40 tuổi, có thu nhập ổn định, đang cân nhắc mua nhà
                              lần đầu tại khu vực Cầu Giấy, Hà Nội, có 1 khoản tiết kiệm
                              nhưng chưa chắc đủ hay có nên dùng hết vào việc mua nhà.

User task                  → Nhập thu nhập + tiết kiệm + chi phí sinh hoạt của mình, chọn
                              1 căn hộ MUA cụ thể và 1 căn hộ THUÊ cụ thể (cùng khu vực,
                              cùng phân khúc diện tích) để so sánh trực tiếp.

Difficulty                 → Không tự tính được lịch trả nợ giảm dần theo lãi suất thay
                              đổi qua từng giai đoạn (ưu đãi → thả nổi năm 1 → thả nổi từ
                              năm 2); không biết "còn lại bao nhiêu tiền mỗi tháng" sau khi
                              trừ nợ/thuê có thực sự an toàn hay không; không hình dung được
                              tài sản ròng (net worth) của 2 lựa chọn sẽ khác nhau ra sao
                              sau 5, 10, 30 năm.

Technology support          → Web app (Flask + JS thuần, không framework) tính toán tức thời
                              ngay khi user nhập input, không cần gửi hồ sơ cho ngân hàng.

Input                       → Xem docs/input-dictionary.md (user-entered + product info +
                              assumptions).

Financial logic              → LOAN_CALC (Method A, dư nợ giảm dần) + Safety margin theo
                              bậc thu nhập + Net worth projection (BUY: vòng lặp tích luỹ;
                              RENT: công thức đóng) + break-even detection + decision rule
                              BUY/RENT/NEITHER. Chi tiết ở mục 2–5 dưới đây.

Output                       → 2 result card (BUY/RENT: chi phí hàng tháng, tiền dư ra,
                              thanh progress-bar an toàn) + 1 banner quyết định cuối cùng +
                              1 biểu đồ Net worth theo năm (đánh dấu break-even nếu có).

User action                  → Quyết định nên MUA hay THUÊ căn hộ đã chọn, hoặc quay lại
                              Step 1–2 để thử phương án khác (đổi ward/size_band/listing).
```

### Tự kiểm tra (mục 3 Week 4)

- **Input có thực sự liên quan đến task?** Có — mọi input (thu nhập, tiết
  kiệm, chi phí sinh hoạt, giá nhà, giá thuê, kỳ hạn vay) đều được dùng trực
  tiếp trong công thức, không có input "trang trí" không dùng tới.
- **Logic có sử dụng input?** Có, xem bảng mapping ở mục 2.
- **Output có phản ánh logic?** Có — mỗi con số hiển thị (monthly cost,
  money left over, safety margin %, net worth theo năm) đều truy được ngược
  về đúng 1 phép tính trong `loan_calc.py`/`evaluate.py`.
- **User có thể hành động sau output?** Có — quyết định BUY/RENT/NEITHER +
  nút "Change" quay lại chọn listing khác.
- **Công nghệ có vai trò rõ?** Có — web app cho phép tính lại tức thời khi
  user đổi input, thay vì phải tự tính tay lịch trả nợ 360 dòng.

## 2. Input–Financial logic–Output Mapping (mục 4 Week 4)

| Input | Financial meaning | Rule/calculation/process | Output |
|---|---|---|---|
| `total_price_vnd` (BUY), `savings`, `max_loan_to_value_pct` | Khả năng đủ vốn tự có để vay | `Min_down_payment = total_price_vnd × (1 − max_ltv_pct)`; nếu `savings < Min_down_payment` → BUY không khả thi | Thông báo lỗi rõ ràng (nêu số tiền còn thiếu), KHÔNG tự hạ khoản vay |
| `total_price_vnd − savings`, lãi suất theo giai đoạn, `grace_period_months` | Chi phí vay hàng tháng, thay đổi theo thời gian (ân hạn → ưu đãi hết hạn → thả nổi) | `LOAN_CALC` Method A: dư nợ giảm dần, gốc cố định mỗi tháng sau ân hạn, lãi tính trên dư nợ đầu kỳ | `monthly_repayment` mỗi tháng (360 dòng lịch trả nợ) |
| `income1+income2`, `living_cost`, `existing_debt`, `monthly_repayment`/`monthly_rent` | Còn lại bao nhiêu tiền mỗi tháng sau khi lo nhà ở | `Money_remaining = Income1+Income2 − Living_cost − Existing_debt − (Repayment hoặc Rent)` | `money_remaining` (VNĐ/tháng) |
| `money_remaining`, `income1+income2` | Mức độ an toàn tài chính, so với 1 ngưỡng phụ thuộc bậc thu nhập | `Safety_margin = Money_remaining / Total_income`; so với `safety_margin_min_pct` theo bậc thu nhập (docs/assumptions.md §3) | `safety_margin` (%) + `is_safe` (đúng/sai) + progress bar |
| `safety_margin`/`is_safe` của cả BUY và RENT | Nên chọn phương án nào | `decide()`: ưu tiên RENT nếu RENT an toàn VÀ margin cao hơn BUY; nếu không, chọn BUY nếu BUY an toàn; nếu không bên nào an toàn → NEITHER | `decision` (`BUY`/`RENT`/`NEITHER`) + `reason` (câu giải thích tiếng Anh) |
| `money_remaining` mỗi tháng, `investment_return_pct`, `property_annual_appreciation_pct`, dư nợ còn lại | Tài sản ròng tích luỹ theo thời gian nếu MUA | `Net_worth_BUY(t) = Property_value(t) − Remaining_loan_balance(t) + Invested_balance_BUY(t)`, tích luỹ qua vòng lặp tháng | `net_worth_buy` mỗi tháng → sample theo năm cho biểu đồ |
| `savings`, `money_remaining_rent` (cố định), `investment_return_pct` | Tài sản ròng tích luỹ theo thời gian nếu THUÊ | `Net_worth_RENT(t) = Savings×(1+r)^t + Money_remaining_RENT×[((1+r)^t−1)/r]` (công thức đóng) | `net_worth_rent` mỗi tháng → sample theo năm cho biểu đồ |
| 2 series Net worth theo tháng | Năm nào (nếu có) 1 phương án vượt lên phương án còn lại | `find_break_even()`: dò tháng đầu tiên 2 series cắt nhau (lên hoặc xuống) | `break_even_month`/`break_even_year` (hoặc `None` nếu không cắt) |

## 3. Formula / Rule / Scoring / Classification (mục 5 Week 4)

### Formula (quan hệ tính toán rõ ràng)

- `Min_down_payment = Purchase_price × (1 − max_loan_to_value_pct)`
- `Required_loan = Purchase_price − Savings`
- Lãi suất áp dụng theo tháng `t` (rule dạng bậc thang, xem bên dưới), lãi
  hàng tháng `= balance_start × (annual_rate_pct/100)/12`
- `Net_worth_BUY(t) = Property_value(t) − Remaining_loan_balance(t) +
  Invested_balance_BUY(t)`, trong đó `Property_value(t) = Purchase_price ×
  (1+property_annual_appreciation_pct/100)^(t/12)`
- `Net_worth_RENT(t) = Savings×(1+r)^t + Money_remaining_RENT×[((1+r)^t−1)/r]`
  (công thức đóng, `r = investment_return_pct/100/12`)

### Rule (bậc thang / threshold)

- Lãi suất theo tháng (`get_monthly_rate_pct`): tháng ≤ 12 → 8.3%; tháng
  13–24 → 8.3%+1.5%=9.8%; tháng > 24 → 8.3%+3.5%=11.8%.
- Ngưỡng an toàn theo thu nhập (`get_safety_margin_min_pct`): xem
  `docs/assumptions.md` §3 (< 35tr → 40%; 35–50tr → 35%; 50–75tr → 30%;
  ≥75tr → 25% "tạm, chưa xác nhận").
- `is_safe = (Safety_margin ≥ safety_margin_min_pct)`.

### Classification (output là category, không phải số)

`decide()` phân loại kết quả cuối vào đúng 1 trong 3 nhóm: `BUY`, `RENT`,
`NEITHER` — không dùng threshold tuỳ tiện, logic ưu tiên được viết tường
minh trong code (xem trích dẫn `evaluate.py::decide()` bên dưới), không phải
số "cảm tính":

```python
if buy_result["error"] is not None:
    # BUY khong kha thi (thieu savings) -> chi con RENT de xet
    return "RENT" if rent_safe else "NEITHER", ...
if rent_safe and rent_margin > buy_margin:
    return "RENT", ...
elif buy_safe:
    return "BUY", ...
elif rent_safe:
    return "RENT", ...
else:
    return "NEITHER", ...
```

### Scoring

Sản phẩm **không dùng scoring nhiều-tiêu-chí có trọng số** (weighted score) —
quyết định BUY/RENT/NEITHER dựa trên so sánh trực tiếp 2 con số
(`safety_margin`) và 1 rule ưu tiên, không cộng dồn nhiều indicator. Đây là
lựa chọn có chủ đích để giữ logic **explainable** (mục 6) — nếu sau này thêm
scoring, cần ghi rõ indicator/weight/scale/interpretation/limitation như
guide yêu cầu.

## 4. Explainability (mục 6 Week 4)

Output ở Step 4 hiện trả lời được các câu hỏi sau (đối chiếu với ví dụ mẫu
trong guide):

- **Kết quả là gì?** → Banner quyết định (`🟢 RECOMMENDED: BUY` /
  `🔵 RECOMMENDED: RENT` / `🔴 NEITHER OPTION MEETS THE SAFETY THRESHOLD`)
  + 2 card chi tiết (monthly cost, money left over, safety margin, progress
  bar).
- **Vì sao kết quả xuất hiện?** → `reason` string đi kèm mỗi quyết định (vd
  `"BUY meets the safety threshold."` hoặc `"RENT meets the safety threshold
  and has a higher safety margin than BUY."`).
- **Input nào ảnh hưởng?** → Có thể suy ngược từ input dictionary (mục 2 ở
  trên) — mỗi output đều map được về đúng input đã nhập/chọn.
- **Assumption nào được dùng?** → Disclaimer cố định dưới biểu đồ Net worth:
  *"This chart assumes property prices grow at a flat 12%/year and invested
  cash returns 6%/year for the entire loan term... treat this chart as
  illustrative, not a 30-year forecast."*
- **User nên hiểu output thế nào / output không khẳng định điều gì?** →
  Disclaimer trên đã nói rõ đây là minh hoạ giáo dục (illustrative), không
  phải dự báo tài chính chắc chắn; số liệu lãi suất trong `FIN_ASSUMPTIONS`
  cũng được ghi chú "temporary demo numbers, need hotline confirmation" ở
  cấp spec (`finflow-demo-spec-v4.md` mục 4).

**Khoảng trống cần bổ sung trước giữa kỳ:** hiện chưa có 1 câu giải thích
bằng ngôn ngữ tự nhiên tương tự ví dụ mẫu của guide (*"Burden ratio cao vì
monthly debt payment chiếm 46% thu nhập..."*) hiển thị ngay trên UI cho từng
kết quả cụ thể — hiện tại `reason` là 1 câu cố định theo nhánh logic, chưa
tự động chèn số liệu cụ thể (vd "vì Safety margin của BUY là -2.85%, thấp
hơn ngưỡng 30% cho hộ thu nhập 50 triệu/tháng"). Nên cân nhắc bổ sung.

## 5. Sample Calculation & Logic Test

Đã tách riêng ra `docs/logic-test.md` (dùng chung cho cả mục 11 Week 3 và
mục 7 Week 4, vì cùng là 1 dạng evidence — bảng Input/Expected/Actual/Status
với **4 case thật đã chạy qua code** (A, A2, B, C) cùng kiểm tra
`find_break_even()` và đối chiếu Python vs JS.
