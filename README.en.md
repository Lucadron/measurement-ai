# Measurement-AI 📏  
**Computer Vision-Based Band Alignment and Skew Detection System**

🔗 [Türkçe README Dosyasına Git](README.md)

---

## 📌 About the Project

**Measurement-AI** is a desktop application developed to measure the alignment of adhesive protection bands on production lines. It calculates the distance from the edges, determines center deviation, and estimates the skew angle of the band using image processing techniques.

Built with Python, the system leverages **PyQt5**, **OpenCV**, **Matplotlib**, and **ReportLab** to deliver a fully-featured GUI that is both powerful and user-friendly.

---

## 🎯 Goals

- Detect and measure band position using images
- Automatically detect left and right edges
- Calculate center deviation (offset) and skew angle
- Support automatic or manual measurement modes
- Display and export graphical statistics of the last 10 measurements
- Save all measurements permanently in `.csv` format
- Generate annotated **PDF reports** with visual overlays
- Provide a **scrollable GUI** with table, chart, and image
- Support **Turkish characters** in reports and GUI

---

## 🧰 Technologies Used

| Technology   | Description                                |
|--------------|--------------------------------------------|
| PyQt5        | GUI development                            |
| OpenCV       | Image processing                           |
| Matplotlib   | Chart plotting                             |
| ReportLab    | PDF report generation                      |
| pandas       | Data handling and CSV export               |
| YAML         | Configuration management (`settings.yaml`) |

---

## 📂 Project Structure

---

measurement-ai/
├── gui/ → User interface (interface.py)
├── core/ → Core logic and helpers
│ ├── measure.py
│ ├── utils.py
│ └── report_utils.py
├── config/ → Configuration files
│ └── settings.yaml
├── fonts/ → Font file for Turkish characters (DejaVuSans.ttf)
├── data/ → Saved measurement history (history.csv)
├── main.py → Main application entry
├── requirements.txt → Required Python libraries
├── .gitignore
├── README.md → Turkish README
└── README.en.md → English README


---

## ⚙️ Features

- [x] Load and process image files (JPG, PNG)
- [x] Detect left and right band edges automatically
- [x] Calculate center offset and skew angle
- [x] Save annotated report as **PDF**
- [x] Save each measurement to a **CSV file**
- [x] Plot the last 10 measurements using **Matplotlib**
- [x] Display results in a **scrollable GUI**
- [x] View result table with export & clear options
- [x] **Turkish language support** for image & report text

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Lucadron/measurement-ai.git
cd measurement-ai
pip install -r requirements.txt
python main.py
