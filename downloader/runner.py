import os
import time
from utils.logger import setup_logger
from utils.file_utils import ensure_dir, save_metadata, load_metadata
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from downloader.selenium_driver import get_driver
from downloader.scraper import accept_cookies, scroll_to_load_thumbnails
from downloader.downloader import download_image

logger = setup_logger(__file__)


def run_downloader(queries, base_directory="downloads", folder_name=None, num_images=5, headless=False, reset_folder=False):
    folder_name = folder_name or f"dataset_{int(time.time())}"
    folder = ensure_dir(os.path.join(base_directory, folder_name))
    metadata_path = os.path.join(folder, "metadata.json")

    if reset_folder:
        # usuń wszystkie pliki w folderze i wyzeruj metadata
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
        metadata = {"downloaded": [], "queries": []}
        save_metadata(metadata_path, metadata)
    else:
        metadata = load_metadata(metadata_path)

    driver = get_driver(headless)
    driver.get("https://images.google.com")
    accept_cookies(driver)
    wait = WebDriverWait(driver, 10)

    for query in queries:
        logger.info(f"Starting download for query: {query}")
        metadata.setdefault("queries", [])
        if query not in metadata["queries"]:
            metadata["queries"].append(query)
            save_metadata(metadata_path, metadata)

        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()
        time.sleep(0.5)

        thumbnails = scroll_to_load_thumbnails(driver, wait)
        i, count = 0, 0

        while count < num_images and i < len(thumbnails):
            try:
                driver.execute_script("arguments[0].click();", thumbnails[i])
                logger.info(f"Clicked thumbnail nr. {i}")

                large_image = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
                )
                src = large_image.get_attribute("src")

                metadata.setdefault("downloaded", [])
                if src and src not in metadata["downloaded"]:
                    success = download_image(src, folder, len(metadata["downloaded"]))
                    if success:
                        metadata["downloaded"].append(src)
                        save_metadata(metadata_path, metadata)
                        count += 1

                time.sleep(0.2)

            except Exception as e:
                logger.error(f"Error during clicking/downloading image: {e}")

            i += 1

        logger.info(f"Finished query '{query}': Downloaded {count} new images")

    driver.quit()
    logger.info(f"All queries finished. Images saved in folder: {folder_name}")
