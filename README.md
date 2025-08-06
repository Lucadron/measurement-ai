# Measurement-AI 📏
**Görüntü İşleme Tabanlı Bant Hizalama ve Eğim Kontrol Sistemi**

---

## 📌 Proje Hakkında

**Measurement-AI**, üretim bantlarında akan yapışkanlı koruma bantlarının konumunu ölçmek, merkezden sapmalarını belirlemek ve eğiklik durumunu tespit etmek için geliştirilen bir masaüstü uygulamasıdır. Uygulama Python diliyle yazılmış olup PyQt5, OpenCV ve Matplotlib gibi kütüphaneler ile desteklenmiştir.

---

## 🎯 Amaçlar

- Görseller üzerinden bant konum ölçümü
- Sol/sağ kenar mesafeleri ölçme
- Merkez sapmasını ve eğiklik açısını hesaplama
- Otomatik görsel işleme (veya opsiyonel manuel ölçüm)
- PDF rapor oluşturma
- Son 10 ölçümün grafiğini ve geçmişini tablo şeklinde sunma
- Tüm verileri `.csv` formatında kalıcı olarak saklama

---

## 🖥️ Ekran Görüntüsü

![Ekran Görüntüsü](docs/screenshot.png)

---

## 🧰 Kullanılan Teknolojiler

| Teknoloji      | Açıklama                            |
|----------------|-------------------------------------|
| PyQt5          | Masaüstü GUI geliştirme             |
| OpenCV         | Görüntü işleme                      |
| Matplotlib     | Grafik çizimi                       |
| ReportLab      | PDF rapor oluşturma                 |
| pandas         | CSV kayıt ve veri işleme            |
| YAML           | Ayar dosyası yönetimi (`settings.yaml`) |

---

## 📂 Proje Yapısı

---

measurement-ai/
├── gui/ → Arayüz dosyaları (interface.py)
├── core/ → Ölçüm ve yardımcı fonksiyonlar
│ ├── measure.py
│ ├── utils.py
│ └── report_utils.py
├── config/ → Ayar dosyaları (settings.yaml)
├── fonts/ → Türkçe destekli yazı tipi (DejaVuSans.ttf)
├── data/ → CSV ölçüm geçmişi (history.csv)
├── main.py → Uygulama giriş dosyası
├── requirements.txt → Gerekli Python paketleri
├── .gitignore
└── README.md


---

## ⚙️ Özellikler

- [x] **Görsel yükleme** ve işleme (jpg/png)
- [x] **Sol ve sağ kenar** tespiti
- [x] **Eğim açısı** ve **merkez sapması** ölçümü
- [x] **PDF raporu** otomatik oluşturma
- [x] **CSV’ye kayıt** ve geçmişi kaydetme
- [x] **Son 10 ölçüm için grafik**
- [x] **Ölçüm geçmişi tablosu** ve tablo üzerinden CSV export veya temizleme
- [x] **Scroll destekli kullanıcı arayüzü**
- [x] **Türkçe karakter desteği** (hem görsel hem PDF için)

---

## 🚀 Kurulum

### 1. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
python main.py
