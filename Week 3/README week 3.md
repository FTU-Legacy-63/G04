# FinFlow — BUY vs RENT (Cầu Giấy, Hà Nội)

> Repo readiness cho Checkpoint 3 (Week 3) và giữa kỳ (Week 4).
> Cập nhật lần cuối: 2026\-09\-08. Owner tổng: \[Dương Phương Anh\].

## 1\. Problem & target user

Người 25–40 tuổi có thu nhập ổn định, đang cân nhắc mua căn hộ đầu tiên tại
khu vực Cầu Giấy, khó tự so sánh chi phí thật giữa **MUA** (trả góp dài hạn,
lãi suất thay đổi theo giai đoạn) và **THUÊ** (chi phí cố định hàng tháng) vì
2 phương án có cấu trúc chi phí khác hẳn nhau. ✅ *Đã có 4 nguồn problem
evidence thật (CBRE, VnExpress, VnEconomy/khảo sát Happiness Saigon) chứng
minh giá nhà Hà Nội vượt xa thu nhập và người trẻ đang phải tự mò mẫm chiến
lược mua/thuê — xem [`docs/sources.md`](docs/sources.md) mục 2. Cần 1 thành
viên đọc lại toàn văn trước khi trích dẫn chính thức.*

## 2\. Product direction & MVP

Web app 1 trang, 4 bước: chọn khu vực \+ phân khúc diện tích → chọn 1 căn MUA
và 1 căn THUÊ cụ thể để so sánh → nhập thông tin tài chính cá nhân → xem kết
quả (an toàn tài chính \+ khuyến nghị BUY/RENT/NEITHER \+ biểu đồ tài sản ròng
theo thời gian). Phạm vi MVP cố ý hẹp: chỉ Cầu Giấy, chỉ căn hộ 2 phòng ngủ,
dữ liệu demo tĩnh — xem [`docs/technical-readiness.md`](docs/technical-readiness.md)
mục 4.

**Bản để mở/demo:** [`standalone/finflow.html`](standalone/finflow.html) —
mở trực tiếp bằng trình duyệt, không cần cài gì. Bản Flask
([`app.py`](app.py)) vẫn giữ trong repo làm bản tham chiếu.

## 3\. Input & sources

- [`docs/input-dictionary.md`](docs/input-dictionary.md) — toàn bộ input
  (user\-entered, product info, assumptions), kèm type/unit/range.
- [`docs/sources.md`](docs/sources.md) — source register (`DATA_DEMO.xlsx`,
  các nguồn lãi suất/thị trường dùng để neo assumption), phân biệt rõ
  operational data vs problem evidence.
- `data/sample-data-buy.csv`, `data/sample-data-rent.csv`,
  `data/sample-project-master.csv` — trích mẫu thật từ `DATA_DEMO.xlsx`
  (lọc theo `ward_old="Trung Hoa"`, phường được dùng trong mọi test case).

## 4\. Financial logic

- [`docs/financial-logic.md`](docs/financial-logic.md) — project logic
  chain đầy đủ, bảng input–logic–output mapping, formula/rule/classification,
  và phần explainability.
- [`docs/assumptions.md`](docs/assumptions.md) — mọi giả định (lãi suất theo
  giai đoạn, ngưỡng an toàn theo bậc thu nhập, tăng giá BĐS/lợi suất đầu tư
  giả định...), kèm rủi ro nếu giả định sai.
- [`docs/data-flow.md`](docs/data-flow.md) — cấu trúc dữ liệu, sơ đồ
  Source → Input → Validation → Process → Output, và bảng input validation
  đầy đủ.

## 5\. Sample calculation & progress evidence

- [`docs/logic-test.md`](docs/logic-test.md) — 4 case đã kiểm tra tay và
  đối chiếu với output thật của code (Case A/A2/B/C), kiểm tra
  `find_break_even()` đủ 4 nhánh, và đối chiếu số liệu giữa bản Python và
  bản JS (standalone) để xác nhận không lệch số.
- Tự chạy lại được bằng: `python3 mua_thue_calc.py`, `python3 loan_calc.py`,
  `python3 evaluate.py` (mỗi file có `__main__` self\-test in kết quả \+ assert).

## 6\. Technical route

[`docs/technical-readiness.md`](docs/technical-readiness.md) — so sánh 2 bản
triển khai (Flask vs standalone), vì sao chuyển hướng sang standalone (bài
học từ 3 lượt lỗi setup thật của người dùng), và fallback khi CDN Chart.js
không tải được.

## 7\. Limitations (tổng hợp, chi tiết ở từng file)

- Dữ liệu `DATA_DEMO.xlsx` là **dữ liệu mô phỏng**, không phải listing thật
  cào từ thị trường — xem `docs/sources.md`.
- ✅ Đã giải quyết: `grace_period_months=24`, `max_loan_to_value_pct=80%`,
  `Loan_term_months=360`, và thứ tự biên độ lãi suất năm 1/năm 2\+ đều đã có
  nguồn thật xác nhận (văn bản MB Bank – Chi nhánh Vạn Phúc, ảnh đính kèm
  `docs/assets/mb-bank-rate-sheet.png`) — xem `docs/assumptions.md`. Ngưỡng
  an toàn 25% cho hộ thu nhập cao **vẫn chưa có nguồn**.
- Văn bản MB Bank có phí trả nợ trước hạn thật (năm 1–5: 1%, năm 6: miễn
  phí) nhưng **chưa được đưa vào công thức** `loan_calc.py` — cân nhắc bổ
  sung nếu có thời gian.
- ✅ Đã có problem evidence (4 nguồn, xem mục 1 ở trên) nhưng chưa có nguồn
  nào nói riêng về Cầu Giấy hay hành vi "so sánh bằng công cụ tính toán" — đây
  vẫn là 1 bước suy luận, có thể củng cố thêm bằng 1 khảo sát/phỏng vấn nhanh
  nếu có thời gian (`docs/sources.md` mục 3).
- Biểu đồ Net worth giả định BĐS tăng đều 12%/năm suốt 30 năm — phi thực tế,
  đã có disclaimer trên UI nhưng cần nêu rõ trong báo cáo giữa kỳ.
- Validate mới chặn số âm/sai định dạng, **chưa chặn giá trị vô lý lớn** (vd
  thu nhập nhập nhầm thêm số 0).

## 8\. Contribution / ownership

- **Dương Phương Anh** — tác giả tài liệu kế hoạch gốc (schema
  `PROJECT_MASTER`, logic `MUA_CALC`/`THUE_CALC`, user
  flow, khung bảng `FIN_ASSUMPTIONS`); clean data `MUA_RAW_CG`/`THUE_RAW_CG`;
  bổ sung nguồn CFPB cho ngưỡng an toàn.
- **Phạm Thị Khánh An** — tìm và lưu văn bản gốc **MB Bank – Chi nhánh Vạn Phúc**
  (nguồn thật xác nhận 7/9 giá trị trong `FIN_ASSUMPTIONS` — xem
  `docs/assets/mb-bank-rate-sheet.png`), đề xuất bộ số liệu `FIN_ASSUMPTIONS`
  ban đầu (safety margin tiers), tìm nguồn VnExpress/Bộ Xây dựng cho
  `property_annual_appreciation_pct` và `rent_annual_growth_pct`.
- **Phạm Nam Phương** — nghiên cứu bộ số liệu thay thế từ Vietcombank (VCB),
  tài liệu hoá công thức LOAN\_CALC (Method A, dư nợ giảm dần).
- **Nguyễn Minh Tuấn** — tìm và cào data `MUA_RAW_CG`/`THUE_RAW_CG`.
- **Nguyễn Hải Sơn** — tìm và cào data `MUA_RAW_HD`/`THUE_RAW_HD` \+
  `MUA_RAW_TH`/`THUE_RAW_TH` (out of scope for MVP).

   bảng "Owner" ở `docs/`.
4. Tự kiểm tra repo theo `../assessment/midterm-checklist.md` (file của môn
   học, chưa có trong repo này) trước khi trình bày giữa kỳ.
