import cv2

clicked_points = []

def click_event(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"📍 Nokta eklendi: {x}, {y}")

def manual_measure(image_path):
    global clicked_points
    clicked_points = []

    image = cv2.imread(image_path)
    clone = image.copy()
    cv2.imshow("Görsel üzerinde tıklayınız", image)
    cv2.setMouseCallback("Görsel üzerinde tıklayınız", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(clicked_points) < 2:
        return None, "En az 2 nokta seçmelisiniz."

    left_x = clicked_points[0][0]
    right_x = clicked_points[1][0]
    width = image.shape[1]
    left_margin = left_x
    right_margin = width - right_x
    center_diff = abs(left_margin - right_margin)

    return {
        "left_margin_mm": left_margin,
        "right_margin_mm": right_margin,
        "center_diff_mm": center_diff
    }, None
