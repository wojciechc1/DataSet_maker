import os
import logging
import requests
from requests.exceptions import RequestException, Timeout


def download_image(url, folder, count, timeout=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        with open(os.path.join(folder, f'image_{count}.jpg'), 'wb') as f:
            f.write(response.content)

        logging.info(f'Downloaded image {count} ({url})')
        return True
    except (RequestException, Timeout) as e:
        logging.error(f"Cannot download image {count} ({url}): {e}")
        return False
