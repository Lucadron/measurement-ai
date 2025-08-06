# core/report_utils.py

import os
import datetime
import cv2

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# 📌 Türkçe karakter destekli fontu kaydet
pdfmetrics.registerFont(TTFont("DejaVu", "fonts/DejaVuSans.ttf"))

def save_pdf_report(image_array, result, save_dir="reports"):
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = os.path.join(save_dir, f"report_{timestamp}.pdf")

    # PDF belge ayarları
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Turkish", fontName="DejaVu", fontSize=12))
    style = styles["Turkish"]

    story = []

    # 🧾 Başlık
    story.append(Paragraph("📄 Measurement-AI | Bant Kontrol Ölçüm Raporu", style))
    story.append(Spacer(1, 12))

    # 📅 Tarih/Saat
    story.append(Paragraph(f"<b>Tarih:</b> {timestamp}", style))
    story.append(Spacer(1, 12))

    # 🔢 Ölçüm Sonuçları
    story.append(Paragraph(f"<b>Sol Kenar:</b> {result['left_margin_mm']} px", style))
    story.append(Paragraph(f"<b>Sağ Kenar:</b> {result['right_margin_mm']} px", style))
    story.append(Paragraph(f"<b>Merkez Sapması:</b> {result['center_diff_mm']} px", style))
    story.append(Paragraph(f"<b>Açı:</b> {result['angle_deg']:.1f}°", style))
    story.append(Spacer(1, 12))

    # 📷 Görsel (görüntü kaydedip PDF'e ekle)
    image_filename = os.path.join(save_dir, f"image_{timestamp}.jpg")
    cv2.imwrite(image_filename, image_array)

    story.append(Image(image_filename, width=400, height=300))
    story.append(Spacer(1, 12))

    # 💬 Yorum (eğiklik yorumu)
    if abs(result["angle_deg"]) > 3:
        comment = f"Bant {abs(result['angle_deg']):.1f}° {'sağa' if result['angle_deg'] > 0 else 'sola'} eğik."
    else:
        comment = f"Bant düz ({result['angle_deg']:.1f}°)"

    story.append(Paragraph(f"<b>Yorum:</b> {comment}", style))

    # PDF oluştur
    doc.build(story)
    return pdf_path
