from unittest.mock import MagicMock, patch
import pandas as pd
from src.scraper import scrape_tapera_sup001


@patch("src.scraper.requests.get")
def test_scrape_tapera_sup001_success(mock_get, tmp_path, monkeypatch):
    # Ubah working directory sementara ke tmp_path agar tidak mengotori folder data/raw asli
    monkeypatch.chdir(tmp_path)

    # Simulasi response CSV palsu dari server Metabase
    fake_csv_content = (
        b"provinsi,kabupaten,nama_perumahan,jumlah_unit\n"
        b"Jawa Tengah,Kota Surakarta,Griya Harmoni,120\n"
        b"Jawa Barat,Kab. Bogor,Bukit Indah,250\n"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [fake_csv_content]
    mock_response.__enter__.return_value = mock_response
    mock_get.return_value = mock_response

    # Jalankan fungsi scraper
    output_file = scrape_tapera_sup001()

    # Assertions (pengecekan)
    assert output_file is not None
    assert (tmp_path / output_file).exists()

    df = pd.read_csv(tmp_path / output_file)
    assert len(df) == 2
    assert "provinsi" in df.columns


@patch("src.scraper.requests.get")
def test_scrape_tapera_sup001_http_error(mock_get):
    # Simulasi server error / timeout
    mock_get.side_effect = Exception("Connection timeout")

    result = scrape_tapera_sup001()
    assert result is None