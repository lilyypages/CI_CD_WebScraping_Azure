import os
import pandas as pd
import requests

DOWNLOAD_URL = "https://meta.tapera.go.id/public/question/1d0f4f48-2e13-43c0-8af7-6ed71b1a364d.csv"


def test_tapera_endpoint_reachable():
    """Memastikan endpoint Metabase Tapera merespons 200 OK dan bertipe CSV."""
    headers = {"User-Agent": "Mozilla/5.0"}
    with requests.get(
        DOWNLOAD_URL, headers=headers, stream=True, timeout=30
    ) as r:
        assert r.status_code == 200
        # Pastikan tidak mengembalikan halaman HTML error
        content_type = r.headers.get("Content-Type", "").lower()
        assert "text/html" not in content_type

        # Baca 1 KB pertama saja untuk verifikasi header CSV
        first_chunk = next(r.iter_content(chunk_size=1024))
        assert len(first_chunk) > 0


def test_scraped_csv_schema_if_exists():
    """Validasi file CSV hasil scraping jika sudah ada di data/raw/."""
    raw_dir = "data/raw"
    if not os.path.exists(raw_dir):
        return

    csv_files = [
        f
        for f in os.listdir(raw_dir)
        if f.startswith("tapera_sup001_") and f.endswith(".csv")
    ]
    if not csv_files:
        return

    latest_file = os.path.join(raw_dir, sorted(csv_files)[-1])
    df = pd.read_csv(latest_file, nrows=10)

    assert not df.empty, "File CSV hasil scraping kosong!"
    assert (
        len(df.columns) >= 10
    ), f"Jumlah kolom tidak wajar: {len(df.columns)}"