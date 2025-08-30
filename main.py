import os
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from downloader.selenium_driver import get_driver
from downloader.scraper import accept_cookies, scroll_to_load_thumbnails
from downloader.downloader import download_image


def run_downloader(query, directory="downloads", num_images=5):
    folder = directory
    os.makedirs(folder, exist_ok=True)

    driver = get_driver(headless=False)
    driver.get("https://images.google.com")

    accept_cookies(driver)

    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(0.5)

    thumbnails = scroll_to_load_thumbnails(driver, wait)

    i, count = 0, 0
    while count < num_images and i < len(thumbnails):
        try:
            driver.execute_script("arguments[0].click();", thumbnails[i])
            logging.info(f"Clicked thumbnail nr. {i+1}")

            large_image = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
            )

            src = large_image.get_attribute("src")
            if src:
                success = download_image(src, folder, count)
                if success:
                    count += 1

            time.sleep(0.2)

        except Exception as e:
            logging.error(f"Error during clicking/downloading image: {e}")

        i += 1

    logging.info(f"Finished. Downloaded {count} images")
    driver.quit()


if __name__ == "__main__":
    run_downloader("cats", "downloads", num_images=5)
