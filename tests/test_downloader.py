import os
import pytest
from unittest.mock import patch, Mock
from downloader.downloader import download_image


@pytest.fixture
def tmp_folder(tmp_path):
    folder = tmp_path / "images"
    folder.mkdir()
    return folder


def test_download_image_success(tmp_folder):
    url = "https://example.com/image.jpg"
    # mockujemy requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"fake_image_data"
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response):
        success = download_image(url, tmp_folder, 0)

    assert success is True
    # sprawdzamy, że plik został zapisany
    file_path = tmp_folder / "image_0.jpg"
    assert file_path.exists()
    assert file_path.read_bytes() == b"fake_image_data"


def test_download_image_failure(tmp_folder):
    url = "https://example.com/image.jpg"
    # mockujemy wyjątek requests
    with patch("requests.get", side_effect=Exception("Network error")):
        success = download_image(url, tmp_folder, 0)

    assert success is False
