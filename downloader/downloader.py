import os
import requests
from requests.exceptions import RequestException, Timeout
from utils.logger import setup_logger


logger = setup_logger(__name__)


def download_image(url, folder, count, timeout=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        filename = os.path.join(folder, f"image_{count}{ext}")
        with open(filename, 'wb') as f:
            f.write(response.content)

        logger.info(f'Downloaded image {count} ({url})')
        return True
    except Exception as e:
        logger.error(f"Cannot download image {count} ({url})", exc_info=True)
        return False
