# Assumptions — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026-09-08. Người cập nhật: [Dương Phương Anh].

## 1. Giả định tài chính (`FIN_ASSUMPTIONS`, `loan_calc.py`)

| Assumption | Giá trị demo | Vì sao cần | Rủi ro nếu sai |
|---|---|---|---|
| Lãi suất cố định trong suốt kỳ hạn theo từng giai đoạn (không mô phỏng biến động lãi suất thị trường theo thời gian thực) | 8.3% năm đầu (ưu đãi 12 tháng) → 8.3%+1.5%=9.8% năm 2 sau ưu đãi → 8.3%+3.5%=11.8% từ năm 3 trở đi | Đơn giản hoá để có thể tính dư nợ giảm dần tất định, không cần Monte Carlo | Lãi suất thật có thể biến động theo thị trường (`rate_adjustment_frequency_months=3` có nguồn thật từ MB Bank nhưng **không được dùng** trong demo này) → chi phí vay thật có thể cao/thấp hơn (ảnh đính kèm [`docs/assets/mb-bank-rate-sheet.png`](assets/mb-bank-rate-sheet.png)) |
| Không có phí trả trước / phí phạt tất toán sớm | Không tính bất kỳ phí nào ngoài gốc + lãi | Giữ công thức đơn giản cho demo | Thực tế nhiều ngân hàng có phí phạt trả trước hạn — output demo lạc quan hơn thực tế nếu user có ý định trả sớm. |
| `grace_period_months = 24`: 24 tháng đầu chỉ trả lãi, không trả gốc | 24 tháng | Phản ánh chính sách ân hạn phổ biến ở một số sản phẩm vay mua nhà. | |
| `max_loan_to_value_pct = 80%`: không dùng `MIN()` để tự động hạ khoản vay khi savings không đủ — nếu `savings < min_down_payment` thì báo lỗi thẳng, không âm thầm giảm khoản vay | 80% | Tránh sai lệch số liệu do "tự sửa" input của user mà không báo | Nếu user không hiểu lỗi, có thể tưởng sản phẩm bị hỏng thay vì hiểu là "chưa đủ vốn tự có". |
| `Loan_term_months = 360` (mặc định, user có thể sửa ở Step 3) | 360 tháng | Kỳ hạn vay phổ biến cho vay mua nhà dài hạn | |
| `investment_return_pct = 6%/năm`: tiền dư ra hàng tháng (sau khi trả nợ/thuê + chi phí sinh hoạt) được giả định đem đầu tư sinh lời 6%/năm, lãi kép hàng tháng | 6% | Cần một con số để tính Net worth theo thời gian (Step 4) | Đây là giả định **giáo dục**, không gắn với một kênh đầu tư cụ thể (gửi tiết kiệm, chứng khoán...) — không nên hiểu là khuyến nghị đầu tư thật |
| `property_annual_appreciation_pct = 12%/năm`: giá bất động sản tăng đều 12%/năm trong suốt kỳ hạn vay (vd 30 năm) | 12% (lấy điểm giữa khoảng 10–15%/năm) | Cần 1 con số để tính `Property_value(t)` trong Net worth BUY | Giả định tăng **đều** trong 30 năm là phi thực tế — thị trường BĐS có chu kỳ tăng/giảm/đi ngang. |
| `rent_annual_growth_pct = 0%`: tiền thuê được giữ **cố định** suốt kỳ so sánh, không tăng theo thời gian | 0% (không dùng field này trong công thức) | Đơn giản hoá Net worth RENT thành công thức đóng (không cần vòng lặp) | Thực tế giá thuê thường tăng theo thời gian (lạm phát, thị trường) → Net worth RENT trong demo có thể bị **đánh giá cao hơn thực tế** ở các năm xa. |
| Bedrooms cố định = 2.0 khi lọc listing (`mua_calc`/`thue_calc` mặc định `bedrooms=2.0`) | 2.0 | Giữ phạm vi demo hẹp, không cần UI chọn số phòng ngủ | Sản phẩm hiện **không phục vụ** nhu cầu tìm căn hộ khác 2 phòng ngủ |
| Không lọc theo project cụ thể, không tính trung bình, không xếp hạng theo khoảng cách (locked decision #6, `mua_thue_calc.py`) | — | Giữ logic lọc đơn giản: khớp đúng `(ward_old, size_band, bedrooms)`, trả về TOÀN BỘ kết quả khớp | User phải tự chọn 1 trong danh sách (có thể dài) thay vì được gợi ý "căn tốt nhất" |

## 2. Giả định về hành vi user

| Assumption | Ghi chú |
|---|---|
| User nhập số liệu tài chính (thu nhập, tiết kiệm, chi phí sinh hoạt) **chính xác và trung thực** | Sản phẩm không xác minh chéo với bất kỳ nguồn nào khác (vd. sao kê ngân hàng) — chỉ validate định dạng (số, không âm), không validate tính đúng đắn của số liệu |
| User hiểu đơn vị "triệu VNĐ" trên UI | Toàn bộ input tiền trên UI đều ghi rõ đơn vị triệu VNĐ; quy đổi sang VNĐ chỉ diễn ra 1 lần trong JS ngay trước khi tính (xem `docs/input-dictionary.md` mục D) |
| Thu nhập hộ gia đình gồm đúng 2 nguồn (`income1`, `income2`) | Không hỗ trợ hộ có 1 người hoặc >2 nguồn thu nhập — nhập `0` cho `income2` nếu chỉ có 1 người |

## 3. Ngưỡng "an toàn tài chính" (`get_safety_margin_min_pct`, `evaluate.py`)

Đây là 1 dạng **rule/threshold** (không chỉ là con số đơn lẻ), áp dụng theo
bậc thu nhập hộ gia đình:

| Tổng thu nhập hộ (triệu VNĐ/tháng) | `safety_margin_min_pct` | Trạng thái |
|---|---|---|
| < 35 | 40% | In use — khớp đúng đề xuất ban đầu của Khánh An |
| 35 – < 50 | 35% | In use — khớp đúng đề xuất ban đầu của Khánh An |
| 50 – < 75 | 30% | In use — khớp đúng đề xuất ban đầu của Khánh An |
| ≥ 75 | 25% | In use — **"tạm, chưa xác nhận"** |

`Safety_margin = Money_remaining / Total_income`, trong đó
`Money_remaining = Income1 + Income2 − Living_cost − Existing_debt − Monthly_repayment_or_rent`.
Nếu `Safety_margin ≥ safety_margin_min_pct` thì phương án đó được coi là "an
toàn" (`is_safe = True`).

**Rủi ro:** bậc trên cùng (25%, cho hộ thu nhập ≥ 75 triệu/tháng) chưa được
xác nhận từ nguồn nào — cần một chuyên gia tài chính cá nhân hoặc tài liệu
tham khảo để thay thế "tạm" bằng con số có căn cứ. Nguồn tham khảo: [CFPB — Ability-to-Repay/Qualified
Mortgage final rule](https://files.consumerfinance.gov/f/201301_cfpb_final-rule_ability-to-repay-preamble.pdf)
(quy định của Mỹ về debt-to-income) — có thể dùng làm tài liệu tham khảo
nguyên tắc chung, nhưng cần lưu ý đây là chuẩn Mỹ, không phải chuẩn ngân
hàng Việt Nam, nên không nên trích dẫn như một con số áp dụng trực tiếp.

## 4. Locked decisions liên quan đến assumption (không được thay đổi khi code tiếp)

1. **#6** — MUA_CALC/THUE_CALC lọc đúng `(ward_old, size_band, bedrooms)`,
   không trung bình/xếp hạng/tolerance/Haversine.
2. **#9** — Quy đổi triệu VNĐ → VNĐ chỉ thực hiện **đúng 1 lần**, ở phía JS,
   ngay trước khi gọi hàm tính toán; không sửa input contract phía logic tính
   (Python gốc hoặc bản JS port).
3. Không dùng `MIN()` để âm thầm hạ khoản vay khi thiếu vốn tự có — phải báo
   lỗi rõ ràng (`"You need at least {shortfall} more in savings..."`).

## 5. Ownership

| Việc | Người phụ trách |
|---|---|
| Thiết kế khung bảng `FIN_ASSUMPTIONS` ban đầu (các field cần chốt) | Dương Phương Anh |
| Nghiên cứu + đề xuất bộ số liệu FIN_ASSUMPTIONS (lãi suất theo kỳ hạn, safety margin tiers, nguồn tăng giá BĐS/giá thuê) | Phạm Thị Khánh An |
| Nghiên cứu bộ số liệu thay thế từ nguồn Vietcombank (VCB) + tài liệu công thức LOAN_CALC (dư nợ giảm dần) | Phạm Nam Phương |
| Bổ sung nguồn tham khảo CFPB cho ngưỡng an toàn tài chính | Dương Phương Anh |
| Xác nhận số liệu cuối cùng đưa vào `loan_calc.py::FIN_ASSUMPTIONS` (giải quyết discrepancy giữa các đề xuất) | [Dương Phương Anh] |
