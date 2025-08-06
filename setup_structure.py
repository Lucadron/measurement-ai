import os

base_dir = "C:/Users/Administrator/Desktop/measure-ai"

folders = [
    "config",
    "core",
    "gui",
    "images",
    "models",
]

files = {
    "main.py": "",
    "requirements.txt": "",
    "config/settings.yaml": "# Mode: auto or manual\nmode: auto\nthreshold_mm: 3\n",
    "core/measure.py": "",
    "core/manual.py": "",
    "core/utils.py": "",
    "gui/interface.py": "",
}

# Klasörleri oluştur
for folder in folders:
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "__init__.py"), "w") as f:
        pass  # Python modülü için boş init

# Dosyaları oluştur
for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ measurement-ai klasör yapısı başarıyla oluşturuldu.")
