# FinFlow engine — Python (bản chuẩn) + JS (UI)

Công cụ so sánh MUA vs THUÊ căn 2 phòng ngủ ở Hà Nội (Cầu Giấy, Hà Đông, Tây Hồ). Repo này là kết quả thực hiện to-do ngày 25/09/2026 — báo cáo đầy đủ ở `docs/KET_QUA_TODO.md`.

## Cấu trúc
```
finflow/fin_assumptions.py   FIN_ASSUMPTIONS schema mới + helper (promo, scenario, phân bổ 4 kênh, list_open_todos)
finflow/loan_term.py         B3.1 calc_max_loan_term + validate_loan_term (3 edge case)
finflow/loan_calc.py         B4 + B5 engine vector hoá (tất định = Monte Carlo với n=1)
finflow/evaluate.py          safety margin, quyết định BUY/RENT/NEITHER, break-even (port MVP JS)
finflow/relevance_engine.py  B2 MUA_CALC / THUE_CALC
finflow/monte_carlo.py       B8
finflow/disclaimers.py       UI Step 4
ui/finflow_engine.js         B2 + B3.1 + disclaimer bản JS (đối chiếu 1-1 với Python)
ui/FinFlow_UI_prototype.html Prototype Step 1–6 (dữ liệu thật 3 quận; dashboard dữ liệu giả)
data/Supporting_data_v2.xlsx Dữ liệu hỗ trợ đã sửa, mean/std bằng công thức, bảng nguồn
data/project_master_fixes.json Sửa toạ độ 3 dự án Hà Đông (#13)
docs/                        sources.md, assumptions.md, KET_QUA_TODO.md
tests/                       60 test (unittest) + 2 bài đối chiếu với MVP JS và với bản JS
```

## Chạy kiểm thử
```bash
pip install numpy openpyxl          # Python ≥ 3.10; node ≥ 18 cho 2 bài đối chiếu
export FINFLOW_DATA_XLSX=/đường/dẫn/DATA.xlsx
export FINFLOW_MVP_HTML="/đường/dẫn/Week 6/MVP sau chỉnh sửa.html"
python3 -m unittest discover -s tests -t .
```
Không đặt 2 biến môi trường thì các test cần dữ liệu thật/MVP tự bỏ qua (skip), phần còn lại vẫn chạy.

## Build lại
```bash
python3 ui/build_ui.py /đường/dẫn/DATA.xlsx     # → ui/FinFlow_UI_prototype.html
python3 data/build_supporting_v2.py             # → data/Supporting_data_v2.xlsx (đường dẫn nguồn sửa ở đầu file)
```

## Quy ước
- Python là bản chuẩn: sửa logic ở Python trước → port sang `ui/finflow_engine.js` → chạy lại `tests/test_parity_b2_js.py`.
- Giá trị chưa chốt luôn có `# TODO(<mã>)`. Trước khi merge/nộp: `python3 -c "from finflow.fin_assumptions import list_open_todos; print(list_open_todos())"` phải rỗng hoặc chỉ còn mục đã được duyệt.
- Không sửa giá trị trong code mà không cập nhật `docs/assumptions.md` + `docs/sources.md`.
