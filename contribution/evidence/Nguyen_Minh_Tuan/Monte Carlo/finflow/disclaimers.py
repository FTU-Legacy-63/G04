"""UI Step 4 — Disclaimer 2 lớp (Spec 2026-09-25 §5, §6). Thuần logic hiển thị, không giả lập."""

STATIC_DISCLAIMER = ("Nếu bạn muốn so sánh Mua vs Thuê cho cùng 1 kích cỡ căn hộ, hãy chọn cùng size band "
                     "ở cả 2 phương án tại Step 2.")
DYNAMIC_TEMPLATE = ("Bạn đang so sánh Mua [{buy}] với Thuê [{rent}] — kết quả có thể phản ánh chênh lệch giá "
                    "giữa 2 loại căn khác nhau, không chỉ chênh lệch giữa việc mua và thuê.")


def size_band_disclaimers(size_band_buy, size_band_rent, avg_price_m2_buy=None, avg_rent_m2_rent=None):
    """Trả {'static': str (luôn hiện), 'dynamic': str|None (chỉ khi 2 size band khác nhau), 'extra': str|None}."""
    if not size_band_buy or not size_band_rent:
        raise ValueError("Cần chọn size band cho cả BUY và RENT ở Step 2")
    dynamic = None
    if size_band_buy != size_band_rent:
        dynamic = DYNAMIC_TEMPLATE.format(buy=size_band_buy, rent=size_band_rent)
    extra = None  # tuỳ chọn mở rộng (Spec §5): giá/m² TB của 2 lựa chọn
    if avg_price_m2_buy is not None and avg_rent_m2_rent is not None:
        extra = (f"Giá mua TB: {avg_price_m2_buy / 1e6:.1f} triệu/m² ({size_band_buy}) · "
                 f"Giá thuê TB: {avg_rent_m2_rent / 1e3:.0f} nghìn/m²/tháng ({size_band_rent})")
    return {"static": STATIC_DISCLAIMER, "dynamic": dynamic, "extra": extra}
