import cv2
import numpy as np

def measure_band_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, "Bant tespit edilemedi."

    c = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)  # center, (w,h), angle
    box = cv2.boxPoints(rect)
    box = box.astype(int)

    center_x = int(rect[0][0])
    w = image.shape[1]

    left_margin = center_x
    right_margin = w - center_x
    center_diff = abs(left_margin - right_margin)

    angle = rect[2]
    if rect[1][0] < rect[1][1]:
        angle = angle  # kısa kenar yatay
    else:
        angle = angle + 90  # uzun kenar yatay

    # Kenar çizgileri (dikdörtgenin sol ve sağ kenarını bul)
    box = sorted(box, key=lambda p: p[0])  # x'e göre sırala
    left_line = [box[0], box[1]]
    right_line = [box[2], box[3]]

    return {
        "left_margin_mm": left_margin,
        "right_margin_mm": right_margin,
        "center_diff_mm": center_diff,
        "angle_deg": angle,
        "left_line": left_line,
        "right_line": right_line
    }, None
