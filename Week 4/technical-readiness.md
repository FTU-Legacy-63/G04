# Technical Readiness — FinFlow (BUY vs RENT, Cầu Giấy)

> Cập nhật lần cuối: 2026-09-08. Người cập nhật: [Dương Phương Anh].

## 1. Route hiện tại (mục 8 Week 4)

FinFlow hiện có **2 bản triển khai song song, cùng 1 logic tài chính**:

| Hạng mục | Bản Flask (backend) | Bản standalone (khuyến nghị dùng để demo/nộp bài) |
|---|---|---|
| Coding environment | Python 3 | HTML/CSS/JS thuần (không cần môi trường chạy nào) |
| Framework | Flask (`app.py`) phục vụ 3 route: `/`, `/api/wards`, `/api/listings`, `/api/evaluate` | Không có framework — 1 file `standalone/finflow.html` duy nhất |
| Data storage | Đọc `DATA_DEMO.xlsx` trực tiếp mỗi lần gọi API (qua `openpyxl`) | Toàn bộ 309 BUY + 129 RENT đã được xuất sẵn thành JSON, nhúng thẳng vào file HTML (`BUY_LISTINGS`/`RENT_LISTINGS`) |
| Deployment platform | Cần máy có Python + `pip install flask openpyxl`, chạy `python app.py`, mở `http://127.0.0.1:5000` | Không cần deploy — mở file `.html` trực tiếp bằng trình duyệt (`file://`), hoặc host tĩnh ở bất kỳ đâu (GitHub Pages, Netlify...) nếu muốn có link chia sẻ |
| AI-assisted coding tool | Claude (Cowork) | Claude (Cowork) |
| Fallback khi thiếu internet | Không có — cần Python cài đúng, đúng thư mục | Toàn bộ tính năng chính (lọc, tính toán, quyết định BUY/RENT) chạy **offline hoàn toàn**; chỉ riêng biểu đồ Chart.js cần internet 1 lần, có 3 nguồn CDN dự phòng (cdnjs → jsdelivr → unpkg) + nút "Retry" nếu cả 3 đều lỗi |

### Vì sao chuyển sang bản standalone là route chính

Trong quá trình phát triển, bản Flask đã gây ra 3 lượt lỗi setup liên tiếp
cho người dùng cuối (thiếu `DATA_DEMO.xlsx` đúng thư mục → dropdown ward
trống; mở nhầm file bằng `file://` thay vì chạy server → "Failed to fetch";
thiếu `pip install openpyxl` → `ModuleNotFoundError`). Đây là dấu hiệu cho
thấy **kiến trúc** (yêu cầu chạy server Python cục bộ) chính là nguồn gốc ma
sát, không phải lỗi code đơn lẻ — nên nhóm đã port toàn bộ logic Python sang
JS và nhúng dữ liệu trực tiếp vào 1 file HTML để loại bỏ hẳn lớp phụ thuộc
này. Bản Flask vẫn được giữ lại trong repo làm **phiên bản tham chiếu** (dễ
đọc code Python hơn JS đã minify theo logic, và là nơi test ban đầu diễn ra),
không phải bản để nộp/demo.

## 2. Ưu điểm / hạn chế / chi phí / khả năng tự sửa (mục 8 Week 4)

| | Bản Flask | Bản standalone |
|---|---|---|
| Ưu điểm | Code Python dễ đọc, dễ mở rộng logic hơn; tách rõ backend/frontend | Không phụ thuộc môi trường; mở được trên mọi máy có trình duyệt; không có lớp lỗi "setup sai" |
| Hạn chế | Phải cài đúng Python + đúng package + đúng thư mục; dễ lỗi khi người khác không rành kỹ thuật chạy thử | File JS dài (~200KB), khó đọc/sửa tay hơn Python; phải port lại logic 2 lần nếu công thức đổi (rủi ro lệch số nếu quên đồng bộ) |
| Chi phí | Miễn phí (chạy local) | Miễn phí (chạy local hoặc host tĩnh miễn phí) |
| Khả năng deploy | Cần 1 server (Render, Railway, PythonAnywhere...) nếu muốn có link online | Deploy tức thời lên bất kỳ static host nào, hoặc không cần deploy gì cả |
| Khả năng nhóm tự sửa | Dễ nếu quen Python | Cần quen đọc JS; nhóm đã kiểm chứng 2 bản cho ra **cùng 1 kết quả số** (xem `docs/logic-test.md` mục 6) nên an toàn để tiếp tục sửa song song, miễn là luôn đối chiếu lại sau mỗi lần đổi công thức |

## 3. Fallback

- **Chart.js (biểu đồ Net worth) không tải được:** thử tuần tự 3 CDN
  (cdnjs → jsdelivr → unpkg); nếu cả 3 đều lỗi, hiển thị thông báo rõ ràng +
  nút "Retry" — toàn bộ số liệu/card kết quả vẫn hiển thị đầy đủ, chỉ thiếu
  phần biểu đồ trực quan.
- **Dữ liệu nguồn (`DATA_DEMO.xlsx`) hỏng/thiếu:** chỉ ảnh hưởng bản Flask
  (trả lỗi 500 rõ ràng qua `errorhandler`); bản standalone không có rủi ro
  này vì dữ liệu đã nhúng sẵn trong file, không đọc file ngoài lúc chạy.
- **Input sai định dạng:** cả 2 bản đều validate và trả thông báo lỗi tiếng
  Anh rõ ràng (xem `docs/data-flow.md` mục 3), không crash trắng trang.

## 4. Đánh giá mức độ MVP (mục 9–10 Week 4)

- Route kỹ thuật hiện tại (1 file HTML tĩnh) **nhỏ, khả thi trong thời gian
  môn học**, không đòi hỏi hạ tầng phức tạp.
- MVP vẫn giữ đúng phạm vi hẹp ban đầu: 1 khu vực (Cầu Giấy), 1 số phòng ngủ
  cố định (2), dữ liệu demo tĩnh — chưa mở rộng thêm scope mới ngoài dự
  kiến.
