import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from requests.exceptions import RequestException, Timeout

import logging


logging.basicConfig(
    level=logging.INFO,  # lub DEBUG
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


def download_image(url, folder, count, timeout=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # podniesie wyjątek przy błędzie HTTP


        with open(os.path.join(folder, f'image_{count}.jpg'), 'wb') as f:
                f.write(response.content)

        logging.info(f'Downloaded image {count} ({url})')
        return True

    except (RequestException, Timeout) as e:
        logging.info(f"Cannot download image {count} ({url}): {e}")
        return False


def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 5)

        accept_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[contains(@class, 'QS5gu') and contains(text(), 'Zaakceptuj wszystko')]"
        )))
        accept_button.click()
        logging.info(f"Accepted cookies")

    except (TimeoutException, NoSuchElementException):
        logging.info(f"Can't accept cookies")
        pass


def scroll_to_load_thumbnails(driver, wait, min_count=150, scroll_pause=1):
    last_height = driver.execute_script("return document.body.scrollHeight")
    thumbnails = []

    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        # download all thubnails
        new_thumbnails = driver.find_elements(By.CSS_SELECTOR, ".cC9Rib")

        if len(new_thumbnails) > len(thumbnails):
            thumbnails = new_thumbnails
        else:
            break  # nie załadowały się nowe

        if len(thumbnails) >= min_count:
            break

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    logging.info(f"Found {len(thumbnails)} thumbnails.")
    return thumbnails


def downloader(query, directory, num_images=5):
    folder = directory
    os.makedirs(folder, exist_ok=True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://images.google.com")

    accept_cookies(driver)

    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(0.1)  # Poczekaj na załadowanie wyników


    # .cC9Rib img.sFlh5c
    thumbnails = scroll_to_load_thumbnails(driver, wait)


    # clicking thubnails
    i = 0
    count = 0
    while count < num_images and i < len(thumbnails):
        try:
            driver.execute_script("arguments[0].click();", thumbnails[i])
            logging.info(f"Clicked thumbnail nr. {i+1}")

            # big image
            large_image = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
            )

            src = large_image.get_attribute("src")


            if src:
                succes = download_image(src, folder, count)
                count +=1 if succes else 0

            time.sleep(0.1)
            if count >= num_images:
                break

        except Exception as e:
            logging.info(f"Error during clicking or downloading image. {e}")

        i += 1

    driver.quit()
