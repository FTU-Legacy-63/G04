# Assumptions — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026-09-08. Người cập nhật: [Dương Phương Anh].

Theo mục 3 Week 3: "Assumption phải được ghi rõ, không được ẩn trong code."
Tài liệu này liệt kê **mọi giả định** đang chi phối output của FinFlow, giữ
nguyên giá trị thật đang chạy trong `loan_calc.py` / `evaluate.py` /
`mua_thue_calc.py` (không tự đặt lại số mới).

## 1. Giả định tài chính (`FIN_ASSUMPTIONS`, `loan_calc.py`)

| Assumption | Giá trị demo | Vì sao cần | Rủi ro nếu sai |
|---|---|---|---|
| Lãi suất cố định trong suốt kỳ hạn theo từng giai đoạn (không mô phỏng biến động lãi suất thị trường theo thời gian thực) | 8.3% năm đầu (ưu đãi 12 tháng) → 8.3%+1.5%=9.8% năm 2 sau ưu đãi → 8.3%+3.5%=11.8% từ năm 3 trở đi | Đơn giản hoá để có thể tính dư nợ giảm dần tất định, không cần Monte Carlo | Lãi suất thật có thể biến động theo thị trường (`rate_adjustment_frequency_months=3` có nguồn thật từ MB Bank nhưng **không được dùng** trong demo này) → chi phí vay thật có thể cao/thấp hơn. ✅ **Đã xác nhận nguồn:** văn bản gốc "Biểu lãi suất cho vay mua nhà đất, chung cư" của **MB Bank – Chi nhánh Vạn Phúc** (ảnh đính kèm [`docs/assets/mb-bank-rate-sheet.png`](assets/mb-bank-rate-sheet.png)) ghi đúng thứ tự đang chạy trong code: năm đầu = Biên độ **1.5%**, thời gian còn lại = Biên độ **3.5%**. |
| Không có phí trả trước / phí phạt tất toán sớm | Không tính bất kỳ phí nào ngoài gốc + lãi | Giữ công thức đơn giản cho demo | Thực tế nhiều ngân hàng có phí phạt trả trước hạn — output demo lạc quan hơn thực tế nếu user có ý định trả sớm. ⚠️ Văn bản MB Bank thực tế có ghi rõ phí này: **năm 1–5: 1%, năm 6 trở đi: miễn phí** — đây là dữ liệu thật đã có sẵn nhưng **chưa được đưa vào công thức** `loan_calc.py`. Nếu muốn mô hình chính xác hơn (đặc biệt hữu ích khi so sánh kịch bản "trả nợ sớm"), có thể bổ sung sau. |
| `grace_period_months = 24`: 24 tháng đầu chỉ trả lãi, không trả gốc | 24 tháng | Phản ánh chính sách ân hạn phổ biến ở một số sản phẩm vay mua nhà | ✅ **Đã xác nhận nguồn:** văn bản MB Bank ghi rõ "Ân hạn nợ gốc: Tối đa 24 tháng" — khớp chính xác. Nam Phương cũng tìm được [trang Vietcombank](https://www.vietcombank.com.vn/vi-VN/KHCN/Truy-cap-nhanh/Tin-noi-bat/Articles/2023/08/31/Khach-hang-co-the-vay-von-tai-vietcombank) ghi cùng con số 24 tháng ở 1 ngân hàng khác — càng củng cố đây là 1 chính sách phổ biến, không phải số bịa. |
| `max_loan_to_value_pct = 80%`: không dùng `MIN()` để tự động hạ khoản vay khi savings không đủ — nếu `savings < min_down_payment` thì báo lỗi thẳng, không âm thầm giảm khoản vay | 80% | Tránh sai lệch số liệu do "tự sửa" input của user mà không báo | Nếu user không hiểu lỗi, có thể tưởng sản phẩm bị hỏng thay vì hiểu là "chưa đủ vốn tự có". ✅ **Đã xác nhận nguồn:** văn bản MB Bank ghi rõ "Mức cho vay tối đa: 80% giá trị mua bán" — khớp chính xác, không còn là "market norm chung" nữa. Nam Phương tìm được 1 nguồn VCB khác ghi LTV tối đa **100%** cho 1 số sản phẩm vay riêng — khác biệt này là thật giữa 2 ngân hàng, nhóm chọn theo MB Bank (nguồn văn bản gốc, đầy đủ nhất) là hợp lý. |
| `Loan_term_months = 360` (mặc định, user có thể sửa ở Step 3) | 360 tháng | Kỳ hạn vay phổ biến cho vay mua nhà dài hạn | ✅ **Đã xác nhận nguồn:** văn bản MB Bank ghi rõ "Thời gian vay: 360 tháng (30 năm)" — khớp chính xác với giá trị mặc định trong `FIN_ASSUMPTIONS`. |
| `investment_return_pct = 6%/năm`: tiền dư ra hàng tháng (sau khi trả nợ/thuê + chi phí sinh hoạt) được giả định đem đầu tư sinh lời 6%/năm, lãi kép hàng tháng | 6% | Cần một con số để tính Net worth theo thời gian (Step 4) | Đây là giả định **giáo dục**, không gắn với một kênh đầu tư cụ thể (gửi tiết kiệm, chứng khoán...) — không nên hiểu là khuyến nghị đầu tư thật |
| `property_annual_appreciation_pct = 12%/năm`: giá bất động sản tăng đều 12%/năm trong suốt kỳ hạn vay (vd 30 năm) | 12% (lấy điểm giữa khoảng 10–15%/năm) | Cần 1 con số để tính `Property_value(t)` trong Net worth BUY | Giả định tăng **đều** trong 30 năm là phi thực tế — thị trường BĐS có chu kỳ tăng/giảm/đi ngang. UI đã có disclaimer cảnh báo điều này ở Step 4. Nguồn: [Bộ Xây dựng qua VnExpress](https://vnexpress.net/bo-xay-dung-gia-nha-o-tang-binh-quan-10-15-moi-nam-4994992.html) (Khánh An tìm) — Nam Phương tìm được 1 nguồn khác (globalpropertyguide.com) cho ra **24.33%/năm**, nhóm đã không dùng con số này. |
| `rent_annual_growth_pct = 0%`: tiền thuê được giữ **cố định** suốt kỳ so sánh, không tăng theo thời gian | 0% (không dùng field này trong công thức) | Đơn giản hoá Net worth RENT thành công thức đóng (không cần vòng lặp) | Thực tế giá thuê thường tăng theo thời gian (lạm phát, thị trường) → Net worth RENT trong demo có thể bị **đánh giá cao hơn thực tế** ở các năm xa. Nhóm **đã có sẵn 2 nguồn thật** cho con số này nếu muốn bổ sung sau: Khánh An tìm [VnExpress ~5–10%/năm](https://vnexpress.net/chat-vat-vi-gia-thue-chung-cu-leo-thang-4927114.html), Nam Phương tìm [globalpropertyguide.com 3.34%/năm](https://www.globalpropertyguide.com/asia/vietnam/rental-yields) — hiện chưa nối vào `net_worth_rent_at()` (`evaluate.py`). |
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
tham khảo để thay thế "tạm" bằng con số có căn cứ. Dương Phương Anh đã ghi
chú thêm 1 nguồn tham khảo khả dĩ: [CFPB — Ability-to-Repay/Qualified
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
