from unittest.mock import MagicMock, patch
import pandas as pd
from src.scraper import scrape_tapera_sup001


@patch("src.scraper.requests.get")
def test_scrape_tapera_sup001_success(mock_get, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    fake_csv_content = (
        b"provinsi,kabupaten,nama_perumahan,jumlah_unit\n"
        b"Jawa Tengah,Kota Surakarta,Griya Harmoni,120\n"
        b"Jawa Barat,Kab. Bogor,Bukit Indah,250\n"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/csv"}
    mock_response.iter_content.return_value = [fake_csv_content]
    mock_response.__enter__.return_value = mock_response
    mock_get.return_value = mock_response

    output_file = scrape_tapera_sup001()

    assert output_file is not None
    assert (tmp_path / output_file).exists()

    df = pd.read_csv(tmp_path / output_file)
    assert len(df) == 2
    assert "provinsi" in df.columns


@patch("src.scraper.requests.get")
def test_scrape_tapera_sup001_http_error(mock_get, monkeypatch):
    # Matikan flag CI sementara agar menguji perilaku murni saat HTTP error
    monkeypatch.delenv("CI", raising=False)
    mock_get.side_effect = Exception("Connection timeout")

    result = scrape_tapera_sup001()
    assert result is None