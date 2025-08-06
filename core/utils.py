def is_centered(center_diff_mm, threshold_mm=3):
    return center_diff_mm <= threshold_mm

def get_warning_message(center_diff_mm, threshold_mm):
    if is_centered(center_diff_mm, threshold_mm):
        return f"✅ Bant ortalanmış. Hata: {center_diff_mm:.2f} mm"
    else:
        return f"⚠️ Bant ortalanmamış! Hata: {center_diff_mm:.2f} mm (Eşik: {threshold_mm} mm)"
