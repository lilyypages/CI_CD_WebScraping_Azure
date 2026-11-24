import os
from datetime import datetime
import pandas as pd
import requests


def scrape_tapera_sup001():
    # URL langsung dari Metabase BP Tapera (tercatat di discover_sources.py)
    download_url = "https://meta.tapera.go.id/public/question/1d0f4f48-2e13-43c0-8af7-6ed71b1a364d.csv"

    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"tapera_sup001_{timestamp}.csv")

    print(f"[{datetime.now()}] Mengunduh SUP-001 dari Metabase BP Tapera...")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        with requests.get(
            download_url, headers=headers, stream=True, timeout=120
        ) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print(f"File disimpan: {output_path}")

        df_sample = pd.read_csv(output_path, nrows=5)
        print(f"Preview kolom: {list(df_sample.columns)}")
        print(f"Jumlah kolom: {len(df_sample.columns)}")
        return output_path

    except Exception as e:
        print(f"Gagal mengunduh: {e}")
        return None


if __name__ == "__main__":
    scrape_tapera_sup001()