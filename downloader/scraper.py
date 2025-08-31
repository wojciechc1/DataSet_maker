import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import setup_logger


logger = setup_logger(__name__)


def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 5)
        accept_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[contains(@class, 'QS5gu') and contains(text(), 'Zaakceptuj wszystko')]"
        )))
        accept_button.click()
        logger.info("Accepted cookies")
    except (TimeoutException, NoSuchElementException):
        logger.warning("Can't accept cookies")
        pass


def scroll_to_load_thumbnails(driver, wait, min_count=150, scroll_pause=1):
    last_height = driver.execute_script("return document.body.scrollHeight")
    thumbnails = []

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        new_thumbnails = driver.find_elements(By.CSS_SELECTOR, ".cC9Rib")
        if len(new_thumbnails) > len(thumbnails):
            thumbnails = new_thumbnails
        else:
            break

        if len(thumbnails) >= min_count:
            break

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    logger.info(f"Found {len(thumbnails)} thumbnails.")
    return thumbnails
