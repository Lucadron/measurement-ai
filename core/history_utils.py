# core/history_utils.py

import csv
import os

CSV_PATH = "data/history.csv"

def save_measurement(result):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            result["left_margin_mm"],
            result["right_margin_mm"],
            result["center_diff_mm"],
            f"{result['angle_deg']:.1f}"
        ])

def load_measurements():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)[-10:]  # Son 10 ölçüm
