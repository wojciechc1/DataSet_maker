import os
import requests
from requests.exceptions import RequestException, Timeout, SSLError
from utils.logger import setup_logger


logger = setup_logger(__name__)


def download_image(url, folder, count, timeout=10, max_retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
            filename = os.path.join(folder, f"image_{count}{ext}")
            with open(filename, 'wb') as f:
                f.write(response.content)

            logger.info(f'Downloaded image {count} ({url})')
            return True
        except SSLError:
            logger.warning(f"Skipping image {count} due to SSL error: {url}")
            return False
        except (RequestException, Timeout) as e:
            logger.warning(f"Attempt {attempt} failed for image {count} ({url}): {e}")
            if attempt == max_retries:
                logger.error(f"Cannot download image {count} after {max_retries} attempts: {url}")
                return False
        except Exception as e:
            logger.error(f"Unexpected error for image {count} ({url}): {e}", exc_info=True)
            return False
