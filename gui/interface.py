from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QScrollArea
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys
import cv2
import numpy as np
import os
import yaml
import pandas as pd

from core.measure import measure_band_edges as measure_band_position
from core.utils import get_warning_message
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class BandMeasurementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.recent_diffs = []
        self.setWindowTitle("Measurement-AI | Bant Kontrol Sistemi")
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet("background-color: #f0f0f0;")

        # ⚙️ Ayarları yükle
        with open("config/settings.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.mode = config.get("mode", "auto")
        self.threshold_mm = config.get("threshold_mm", 3)

        # Ana layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 🧭 Kontrol ve mesajlar
        control_layout = QHBoxLayout()
        self.label_msg = QLabel("🖼 Görsel yüklenmedi.")
        self.label_msg.setStyleSheet("font-size: 16px; padding: 10px; color: gray;")
        self.label_stats = QLabel("📊 Ortalama sapma: Henüz veri yok.")
        self.label_stats.setStyleSheet("font-size: 14px; padding: 8px; color: #444;")

        btn = QPushButton("📂 Görsel Yükle ve Ölçüm Yap")
        btn.clicked.connect(self.load_and_measure)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)
        control_layout.addWidget(btn)
        control_layout.addWidget(self.label_msg)

        # 🖼 Görsel alanı
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        self.label_image.setMinimumHeight(300)

        # 📊 Grafik alanı
        self.canvas = FigureCanvas(Figure(figsize=(5, 2)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_title("Son 10 Ölçüm | Merkez Sapması (px)")
        self.ax.set_xlabel("Ölçüm #")
        self.ax.set_ylabel("Sapma (px)")

        # 📋 Tablo üstü butonlar
        table_controls = QHBoxLayout()
        self.export_button = QPushButton("📤 Export Geçmiş (CSV)")
        self.export_button.setStyleSheet("padding: 6px; font-size: 13px;")
        self.export_button.clicked.connect(self.export_history_to_csv)

        self.clear_button = QPushButton("🗑️ Geçmişi Temizle")
        self.clear_button.setStyleSheet("padding: 6px; font-size: 13px;")
        self.clear_button.clicked.connect(self.clear_history)

        table_controls.addWidget(self.export_button)
        table_controls.addWidget(self.clear_button)

        # 📋 Tablonun kendisi
        self.table_history = QTableWidget()
        self.table_history.setColumnCount(5)
        self.table_history.setHorizontalHeaderLabels(["#", "Sol (px)", "Sağ (px)", "Sapma (px)", "Açı (°)"])
        self.table_history.setStyleSheet("font-size: 13px;")
        self.table_history.setEditTriggers(QTableWidget.NoEditTriggers)

        # 🔁 Scrollable alan
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addLayout(control_layout)
        scroll_layout.addWidget(self.canvas)
        scroll_layout.addWidget(self.label_image)
        scroll_layout.addWidget(self.label_stats)
        scroll_layout.addLayout(table_controls)   # butonlar üstte
        scroll_layout.addWidget(self.table_history)  # tablo altta

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # 📥 CSV'den geçmişi yükle
        self.load_history_from_csv()

    def load_and_measure(self):
        path, _ = QFileDialog.getOpenFileName(self, "Görsel Seç", "", "Image Files (*.jpg *.png *.jpeg)")
        if not path:
            return

        image = cv2.imread(path)
        if self.mode == "manual":
            from core.manual import manual_measure
            result, error = manual_measure(path)
        else:
            result, error = measure_band_position(image)

        if error:
            self.label_msg.setText("❌ " + error)
            self.label_msg.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
            return

        mesaj = get_warning_message(result["center_diff_mm"], threshold_mm=self.threshold_mm)
        if abs(result["angle_deg"]) > 3:
            mesaj += f" | Bant {abs(result['angle_deg']):.1f}° {'sağa' if result['angle_deg'] > 0 else 'sola'} eğik."
        color = "green" if "✅" in mesaj else "orange"

        self.recent_diffs.append(result["center_diff_mm"])
        if len(self.recent_diffs) > 10:
            self.recent_diffs.pop(0)
        avg_diff = np.mean(self.recent_diffs)

        self.label_msg.setText(f"{mesaj}  |  📊 Ortalama sapma: {avg_diff:.2f} px")
        self.label_msg.setStyleSheet(f"color: {color}; font-weight: bold; padding: 10px;")
        self.update_plot()

        self.label_stats.setText(
            "📊 Son 10 ölçüm sonucu: " + ", ".join(f"{v:.1f}" for v in self.recent_diffs) +
            f"\n📉 Ortalama merkez sapması: {avg_diff:.2f} mm"
        )

        drawn = self.draw_info_overlay(
            image.copy(),
            result["left_margin_mm"],
            result["right_margin_mm"],
            result["center_diff_mm"],
            result["left_line"],
            result["right_line"],
            result["angle_deg"]
        )
        self.display_image(drawn)

        self.append_to_table(result)
        self.save_to_csv(result)

        from core.report_utils import save_pdf_report
        save_pdf_report(drawn, result)

    def draw_info_overlay(self, image, left, right, diff, left_line, right_line, angle_deg):
        overlay = image.copy()
        cv2.line(overlay, tuple(left_line[0]), tuple(left_line[1]), (0, 255, 0), 2)
        cv2.line(overlay, tuple(right_line[0]), tuple(right_line[1]), (0, 0, 255), 2)

        center_x = image.shape[1] // 2
        arrow_color = (255, 100, 0)

        if angle_deg < -2:
            cv2.arrowedLine(overlay, (center_x, 120), (center_x - 100, 120), arrow_color, 2, tipLength=0.3)
            text = f"Bant {abs(angle_deg):.1f} derece sola egik"
        elif angle_deg > 2:
            cv2.arrowedLine(overlay, (center_x, 120), (center_x + 100, 120), arrow_color, 2, tipLength=0.3)
            text = f"Bant {abs(angle_deg):.1f} derece saga egik"
        else:
            text = f"Bant düz ({angle_deg:.1f} derece)"

        cv2.rectangle(overlay, (10, 10), (300, 110), (50, 50, 50), -1)
        cv2.addWeighted(overlay, 0.4, image, 0.6, 0, image)

        cv2.putText(image, f"Left:  {left} px", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f"Right: {right} px", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(image, f"Diff:  {diff} px", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(image, text, (center_x - 150, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 100, 0), 2)
        return image

    def display_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.label_image.setPixmap(pixmap.scaled(
            self.label_image.width(), self.label_image.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("Son 10 Ölçüm | Merkez Sapması (px)")
        self.ax.set_xlabel("Ölçüm #")
        self.ax.set_ylabel("Sapma (px)")
        self.ax.plot(self.recent_diffs, marker='o', color='blue')
        self.ax.grid(True)
        self.canvas.draw()

    def append_to_table(self, result):
        row_count = self.table_history.rowCount()
        if row_count >= 10:
            self.table_history.removeRow(0)
        self.table_history.insertRow(self.table_history.rowCount())
        row = self.table_history.rowCount() - 1
        self.table_history.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.table_history.setItem(row, 1, QTableWidgetItem(str(result["left_margin_mm"])))
        self.table_history.setItem(row, 2, QTableWidgetItem(str(result["right_margin_mm"])))
        self.table_history.setItem(row, 3, QTableWidgetItem(str(result["center_diff_mm"])))
        self.table_history.setItem(row, 4, QTableWidgetItem(f"{result['angle_deg']:.1f}"))

    def save_to_csv(self, result):
        os.makedirs("data", exist_ok=True)
        csv_path = "data/history.csv"
        df = pd.DataFrame([{
            "left": result["left_margin_mm"],
            "right": result["right_margin_mm"],
            "diff": result["center_diff_mm"],
            "angle": result["angle_deg"]
        }])
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode='a', index=False, header=False)
        else:
            df.to_csv(csv_path, index=False)

    def load_history_from_csv(self):
        csv_path = "data/history.csv"
        if not os.path.exists(csv_path):
            return
        try:
            df = pd.read_csv(csv_path)
            for i, row in df.tail(10).iterrows():
                self.recent_diffs.append(row["diff"])
                self.table_history.insertRow(self.table_history.rowCount())
                r = self.table_history.rowCount() - 1
                self.table_history.setItem(r, 0, QTableWidgetItem(str(r + 1)))
                self.table_history.setItem(r, 1, QTableWidgetItem(str(row["left"])))
                self.table_history.setItem(r, 2, QTableWidgetItem(str(row["right"])))
                self.table_history.setItem(r, 3, QTableWidgetItem(str(row["diff"])))
                self.table_history.setItem(r, 4, QTableWidgetItem(f"{row['angle']:.1f}"))
        except Exception as e:
            print("CSV yükleme hatası:", e)

    def export_history_to_csv(self):
        try:
            os.makedirs("data", exist_ok=True)
            csv_path = "data/history_export.csv"
            row_count = self.table_history.rowCount()
            if row_count == 0:
                return
            data = []
            for row in range(row_count):
                row_data = []
                for col in range(self.table_history.columnCount()):
                    item = self.table_history.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            df = pd.DataFrame(data, columns=["#", "Sol (px)", "Sağ (px)", "Sapma (px)", "Açı (°)"])
            df.to_csv(csv_path, index=False)
            print("Geçmiş export edildi:", csv_path)
        except Exception as e:
            print("Export hatası:", e)

    def clear_history(self):
        self.table_history.setRowCount(0)
        self.recent_diffs.clear()
        self.label_stats.setText("📉 Sonuç geçmişi temizlendi.")
        self.update_plot()
        csv_path = "data/history.csv"
        if os.path.exists(csv_path):
            os.remove(csv_path)


def run_gui():
    app = QApplication(sys.argv)
    window = BandMeasurementApp()
    window.show()
    sys.exit(app.exec_())
