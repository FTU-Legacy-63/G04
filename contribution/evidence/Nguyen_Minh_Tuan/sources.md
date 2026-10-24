# docs/sources.md — Nguồn dữ liệu FinFlow

Cập nhật: 29/09/2026. Quy tắc: mỗi con số trong `finflow/fin_assumptions.py` phải trỏ được về ít nhất 1 ID ở đây (cột "Dùng cho"). Số liệu tự tính ghi rõ file › sheet › ô công thức.

## 1. Khung trích nguồn (template)

| Cột | Bắt buộc | Hướng dẫn |
|---|---|---|
| ID | ✔ | `S-<nhóm>-<số>`, VD `S-LOAN-01` |
| Nguồn | ✔ | Tổ chức + tên văn bản/bài viết |
| Phát hành | ✔ | Ngày đăng/ban hành; ghi "không rõ" nếu trang không ghi |
| Tra cứu | ✔ | Ngày mở nguồn (dd/mm/yyyy) |
| Loại | ✔ | Sơ cấp (văn bản/trang chính thức) · Dữ liệu (FiinPro, NSO, World Bank) · Báo chí · Tổng hợp (wiki, blog, trang so sánh) |
| Dùng cho | ✔ | Field trong FIN_ASSUMPTIONS hoặc mục to-do |
| Nội dung | ✔ | Tóm tắt bằng lời mình, có con số; không chép nguyên văn dài |
| Tin cậy | ✔ | Cao / Trung bình / Thấp + lý do |
| Link | ✔ | Link trực tiếp; PDF dễ bị gỡ → lưu thêm bản Wayback hoặc bản tải về |

### Checklist trước khi dùng một nguồn
- [ ] Có ngày phát hành (hoặc ghi "không rõ") và ngày tra cứu
- [ ] Link mở được; PDF đã lưu bản sao
- [ ] Đã ghi loại nguồn; ưu tiên Sơ cấp > Dữ liệu > Báo chí > Tổng hợp
- [ ] Báo chí/Tổng hợp: có nguồn thứ hai xác nhận, hoặc gắn nhãn "chưa xác nhận"
- [ ] Định nghĩa con số khớp với field dùng nó (VD: lãi cho vay MỚI bình quân mọi kỳ hạn ≠ lãi vay mua nhà thả nổi)
- [ ] Nguồn mâu thuẫn: liệt kê hết, ghi lựa chọn và lý do
- [ ] Số tự tính: ghi file › sheet › ô (VD `data/Supporting_data_v2.xlsx › VNIndex_fixed › H8`)

## 2. Nguồn đã điền (tra cứu 28–29/09/2026)

### 2.1 Điều kiện vay — to-do #1, #1b, #1c, #2

| ID | Nguồn | Phát hành | Loại | Dùng cho | Nội dung | Tin cậy | Link |
|---|---|---|---|---|---|---|---|
| S-LOAN-00 | MB Bank CN Vạn Phúc — văn bản gốc (ảnh team lưu) | 2026 | Sơ cấp | promo 8,3%/12 tháng; biên 1,5/3,5; ân hạn 24; LTV 80%; 360 tháng; phí trả trước | Nguồn của phần lớn tham số vay | Cao — **cần đưa bản chụp vào repo** | (team bổ sung) |
| S-LOAN-01 | MB — trang sản phẩm vay mua nhà cho người trẻ (MB Dream Home) | không rõ | Sơ cấp | #1 | Vay tới 80%, thời hạn tới 35 năm | Cao, nhưng là gói KHÁC gói Vạn Phúc | https://www.mbbank.com.vn/26/37/113/Chi-tiet/mua-nha-dat-tho-cu-chung-cu-du-an-cho-nguoi-tre-2024-6-5-17-58-30 |
| S-LOAN-02 | Báo Chính phủ | 28/03/2025 | Báo chí | #1 | MB Dream Home dành cho khách 23–40 tuổi | TB | https://baochinhphu.vn/mb-tien-phong-ho-tro-nguoi-tre-mua-nha-voi-goi-tin-dung-dream-home-102250328181355734.htm |
| S-LOAN-03 | Thanh Niên | 08/2024 | Báo chí | #1 | Hạn mức tối đa 5 tỷ; không trả gốc tới 5 năm đầu | TB | https://thanhnien.vn/gioi-tre-hien-thuc-hoa-giac-mo-an-cu-voi-goi-vay-uu-dai-tu-mb-18524080416314239.htm |
| S-LOAN-04 | Hiệp hội Ngân hàng (VNBA) | 03/2024 | Báo chí | #1 | Gói ra mắt với thời hạn 30 năm (sau nâng lên 35) | TB | https://vnba.org.vn/vi/mb-ra-mat-goi-vay-mua-nha-uu-dai-dac-biet-danh-rieng-cho-khach-tre-13583.htm |
| S-LOAN-05 | wiki.batdongsan — các gói vay MB | không rõ | Tổng hợp | #1 | Có gói MB cho vay tới 420 tháng | Thấp | https://wiki.batdongsan.com.vn/wiki/cac-goi-vay-ngan-hang-mb-bank-809784 |
| S-LOAN-06 | TheBank — vay mua căn hộ dự án MB | không rõ | Tổng hợp | #1b | Tuổi khi kết thúc khoản vay ≤ 70 | Thấp–TB; mâu thuẫn mốc 75 của plan | https://thebank.vn/vay-the-chap/cho-vay-mua-can-ho-nha-dat-du-an-ngan-hang-mbbank-40.html |
| S-LOAN-07 | PVcomBank — vay mua nhà trả góp | không rõ | Sơ cấp (NH khác) | #1b đối chiếu | Từ đủ 18 và không quá 75 tuổi khi kết thúc thời hạn cấp tín dụng | Cao cho PVcomBank | https://www.pvcombank.com.vn/tin-tuc/cam-nang-tai-chinh/vay-mua-nha-tra-gop |
| S-LOAN-08 | Techcombank — điều kiện vay thế chấp | không rõ | Sơ cấp (NH khác) | #1b đối chiếu | Không quá 65 tuổi khi tất toán | Cao cho Techcombank | https://techcombank.com/thong-tin/blog/dieu-kien-vay-the-chap |
| S-LOAN-09 | wiki.batdongsan — lãi suất MB | không rõ | Tổng hợp | #1c | Một gói MB: phí trả trước năm 1–2: 2,5%; năm 3: 2%; năm 4: 1,5%; năm 5: 1%; từ năm 6 miễn | Thấp; khác mức phẳng 1% của to-do | https://wiki.batdongsan.com.vn/wiki/lai-suat-ngan-hang-mbbank-evr-803484 |
| S-LOAN-10 | CafeF | 20/05/2025 | Báo chí | #2 | VCB Nhà Mới Thành Đạt: khách 20–35 tuổi, vay tối đa 70% giá trị nhà (50% nếu thuê mua), tới 40 năm, miễn trả gốc 5 năm, tối đa 5 tỷ, thả nổi = LS huy động 24 tháng + 3% | TB–Cao | https://cafef.vn/lai-suat-cho-vay-mua-nha-tai-vietcombank-vietinbank-agribank-bidv-thap-nhat-bao-nhieu-188250520101155192.chn |
| S-LOAN-11 | Vietcombank — trang sản phẩm Nhà Mới Thành Đạt | không rõ | Sơ cấp | #2 | Trang chính thức của gói ở S-LOAN-10 (nội dung tải bằng JavaScript — cần mở bằng trình duyệt) | Cao khi đọc được | https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Vay/Nha-moi-thanh-dat |
| S-LOAN-12 | banchungcusaigon — vay mua BĐS Vietcombank | cũ | Tổng hợp | #2 | Vay nhà dự án: tối đa 70% nếu thế chấp chính căn nhà; tới 100% nếu thế chấp tài sản khác; tối đa 20 năm | Thấp (cũ) | https://banchungcusaigon.com.vn/vay-mua-bat-dong-san-tu-vietcombank.html |
| S-LOAN-13 | Sức khỏe & Đời sống (Pháp luật) | 2025 | Báo chí | #2 | Gói 20.000 tỷ của VCB: thời hạn tới 35 năm, tỷ lệ cho vay có thể tới 100% tuỳ hồ sơ | TB | https://phapluat.suckhoedoisong.vn/vietcombank-mo-goi-tin-dung-20000-ty-dong-thi-truong-ha-lai-suat-vay-mua-nha-toi-1nam-284865.html |
| S-LOAN-14 | Vietcombank — PDF plan đang trích | 29/07/2026 | Sơ cấp | #2 | Theo tên file là thông báo lãi suất; không mở được trong phiên này | Chưa kiểm | https://www.vietcombank.com.vn/-/media/Project/VCB-Sites/VCB/Tin-tuc/2026/Vietcombank/Vietcombank_202607/Vietcombank_20260721/20260729_Thong-bao-lai-suat-2026-thang-6.pdf |
| S-LOAN-15 | Vietcombank — thông báo LS cơ sở cho vay trung dài hạn | 16/03/2026 | Sơ cấp | tham khảo | Ví dụ loại văn bản "thông báo lãi suất" của VCB (không nêu LTV) | Cao | https://www.vietcombank.com.vn/vi-VN/Trang-thong-tin-dien-tu/Articles/2026/03/16/Thong-bao-LSCS-cho-vay-trung-dai-han |

**Sửa dòng cũ:** "VCB — LTV=100%" → "VCB: 70% (Nhà Mới Thành Đạt; vay nhà dự án thế chấp chính căn nhà). Tới 100% chỉ khi thế chấp tài sản khác hoặc gói 20.000 tỷ tuỳ hồ sơ (S-LOAN-10, 12, 13)". LTV Downturn 70% vẫn có cơ sở.

### 2.2 Lãi suất cho vay theo thời gian — #4, #6

| ID | Nguồn | Phát hành | Loại | Nội dung | Tin cậy | Link |
|---|---|---|---|---|---|---|
| S-RATE-01 | Mekong ASEAN (trích NHNN) | 12/2025 | Báo chí | LS cho vay MỚI bình quân 6,96%/năm cuối 2024, giữ quanh 6,96% đến cuối 11/2025 | TB–Cao | https://mekongasean.vn/lai-suat-cho-vay-binh-quan-giu-on-dinh-quanh-muc-696nam-50364.html |
| S-RATE-02 | DNSE | 04/2025 | Báo chí | ~6,34% giữa 04/2025 (−0,6 điểm % so với cuối 2024); FiinPro: thấp nhất 2020–2022 theo quý là 7,9% (quý I/2022) | TB | https://www.dnse.com.vn/senses/tin-tuc/lai-suat-cho-vay-ang-re-ky-luc-35086402 |
| S-RATE-03 | CafeF (trích NHNN) | 21/07/2026 | Báo chí | LS cho vay bình quân (cũ + mới còn dư nợ) 8,1–10,5%/năm | TB–Cao | https://cafef.vn/so-lieu-lai-suat-cho-vay-lai-suat-huy-dong-moi-nhat-cua-he-thong-ngan-hang-188260721204319885.chn |
| S-RATE-04 | VietnamFinance | chưa xác minh | Báo chí | 8,4–10,7%/năm, +0,2 điểm % so với tháng trước | Thấp đến khi rõ ngày | https://vietnamfinance.vn/lai-suat-cho-vay-trung-binh-len-107-nam-thuc-te-khach-vay-cham-dinh-18-d150849.html |
| S-RATE-05 | Tự tính — sheet 'Lãi huy động' của team | — | Dữ liệu | Std LSHĐ >12 tháng (mức cao nhất) 2016–2026 = 0,63 điểm % | Cao (định nghĩa: mức cao nhất) | `Supporting_data_v2.xlsx › Savings_hist › F8` |

### 2.3 Giá thuê — #7

| ID | Nguồn | Phát hành | Loại | Nội dung | Tin cậy | Link |
|---|---|---|---|---|---|---|
| S-RENT-01 | Vietnambiz | 04/2025 | Báo chí | Giá thuê chung cư ~13 triệu/căn, gần như đi ngang 3 năm; lợi suất cho thuê giảm từ >4% (Q1/2023) xuống ~3% (Q1/2025); năm 2024 giá thuê tăng chỉ ~một nửa tốc độ giá nhà | TB–Cao | https://vietnambiz.vn/loi-suat-cho-thue-chung-cu-dang-giam-dan-202541323742923.htm |
| S-RENT-02 | wiki.batdongsan | Q1/2025 | Tổng hợp | Giá thuê chung cư Hà Nội tăng nhẹ trong quý I/2025 | TB | https://wiki.batdongsan.com.vn/tin-tuc/gia-thue-chung-cu-Ha-Noi-tang-nhe-trong-quy-1-2025-cd-hn-832002 |
| S-RENT-03 | VARS | không rõ | Hiệp hội | Bài về giá thuê căn hộ tăng cao — chưa trích được con số | Chưa dùng | https://vars.com.vn/tin-tuc/gia-thue-can-ho-tang-cao-n1897 |

Không tìm được chuỗi giá thuê **căn hộ thường** của Savills/CBRE (chỉ có căn hộ dịch vụ).

### 2.4 Giá căn hộ — #3

| ID | Nguồn | Phát hành | Loại | Nội dung | Tin cậy | Link |
|---|---|---|---|---|---|---|
| S-PROP-01 | Sheet 'Lạm phát giá mua bds' của team (CafeF + Cushman & Wakefield) | — | Dữ liệu | Giá sơ cấp USD/m² 2016–2025: CAGR 12,66%; 2016–20: 3,64%; 2020–25: 20,43% | TB (sơ cấp, USD) | `Supporting_data_v2.xlsx › Property_CAGR` |
| S-PROP-02 | Savills Việt Nam | Q1/2025 | Báo cáo | Giá sơ cấp Hà Nội +32% YoY; giá thứ cấp giảm nhẹ lần đầu sau 5 năm | Cao | https://vn.savills.com.vn/research_articles/164027/223536-0 |
| S-PROP-03 | Vietnambiz (dữ liệu Batdongsan) | 10/2025 | Báo chí | Giá chung cư Hà Nội +14% năm 2023, +39% năm 2024; 2025 tăng chậm lại | TB | https://vietnambiz.vn/nhung-khu-vuc-tang-gia-chung-cu-manh-tai-ha-noi-202510985919392.htm |

### 2.5 Kênh đầu tư và vĩ mô — #8 đến #12

| ID | Nguồn | Loại | Nội dung | Link / vị trí |
|---|---|---|---|---|
| S-MKT-01 | Sheet 'VNIndex return - npp' (đã sửa ngày) | Dữ liệu | 64 giá đóng cửa tháng 05/2021–08/2026 | `VNIndex_fixed` |
| S-MKT-02 | Thanh Niên, 31/12/2025 | Báo chí | Đối chiếu: 1.266,78 (cuối 2024), 1.784,49 (cuối 2025) — khớp dữ liệu | https://thanhnien.vn/vn-index-ket-thuc-nam-2025-voi-muc-tang-khung-gan-41-185251231154434459.htm |
| S-MKT-03 | VnEconomy, 31/12/2025 | Báo chí | VN-Index 2025 +40,87% — khớp dữ liệu | https://vneconomy.vn/vn-index-chot-2025-o-dinh-cao-lich-su-tang-ky-luc-9-nam.htm |
| S-MKT-04 | Sheet 'Giá vàng SJC' (FiinPro) | Dữ liệu | 129 giá cuối tháng 01/2016–09/2026 | `Gold_SJC` |
| S-MKT-05 | Sheet 'Return Bond' (FiinPro) | Dữ liệu | Lợi suất TPCP 5 & 10 năm cuối năm 2016–2026. To-do gợi ý kết quả đấu thầu KBNN — **chưa thu thập** | `Bond_10Y` |
| S-MKT-06 | Sheet 'Lãi huy động' | Dữ liệu | LSHĐ cao nhất kỳ hạn 6–12 tháng & >12 tháng, 2016–2026 | `Savings_hist` |
| S-MKT-07 | NSO — Kết quả KSMS dân cư 2024 | Dữ liệu (sơ cấp) | Thu nhập bình quân đầu người/tháng 2019–2024 | https://www.nso.gov.vn/wp-content/uploads/2026/03/Sach-Khao-sat-muc-song-dan-cu-2024.pdf |
| S-MKT-08 | World Bank (sheet 'Inflation') | Dữ liệu | CPI 2016–2025 | `CPI_WB` |

### 2.6 Lãi suất tiết kiệm hiện tại — #9 (báo chí mâu thuẫn → cần nguồn chính thức)

| ID | Nguồn | Phát hành | Nội dung | Link |
|---|---|---|---|---|
| S-SAV-01 | CafeF | 22/02/2026 | VCB: 12–18 tháng 5,2%; 24 tháng 5,3% | https://cafef.vn/nam-moi-gui-tiet-kiem-tai-agribank-vietcombank-bidv-vietinbank-cao-nhat-bao-nhieu-188260222210249665.chn |
| S-SAV-02 | Znews | 03/2026 | Big4 tăng lãi suất: 12–18 tháng từ 5,2% lên 5,9% | https://znews.vn/vietcombank-vietinbank-bidv-agribank-cung-tang-lai-suat-tiet-kiem-post1638131.html |
| S-SAV-03 | Gia đình & Xã hội | chưa rõ | Big4 cùng niêm yết 6,8% kỳ hạn 12 tháng — mâu thuẫn S-SAV-01/02 | https://giadinh.suckhoedoisong.vn/lai-suat-agribank-vietinbank-vietcombank-bidv-moi-nhat-gui-tiet-kiem-400-trieu-dong-vao-agribank-nhan-bao-nhieu-tien |

→ Điền bảng mẫu `Supporting_data_v2.xlsx › Tiet_kiem_snapshot` từ biểu lãi suất chính thức của 5 ngân hàng.

### 2.7 Toạ độ — #13

| ID | Nguồn | Tra cứu | Nội dung |
|---|---|---|---|
| S-GEO-01 | Google Maps/Places | 29/09/2026 | V8 The Vesta (20.9451528, 105.7558822); Toà Văn Phú Victoria (20.9579161, 105.7691591; tòa V1: 20.9601278, 105.7678317); Chung cư Vinaconex 21, 804 Quang Trung (20.9567772, 105.7563336). Chi tiết: `data/project_master_fixes.json` |
