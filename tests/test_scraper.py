import pytest
from downloader.selenium_driver import get_driver
from downloader.scraper import accept_cookies, scroll_to_load_thumbnails
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = get_driver(headless=True)
    yield driver
    driver.quit()

def test_accept_cookies(driver):
    driver.get("https://images.google.com")
    accept_cookies(driver)  # powinno przejść bez wyjątku

def test_scroll_to_load_thumbnails(driver):
    driver.get("https://images.google.com")

    # wyszukiwanie "cats"
    box = driver.find_element(By.NAME, "q")
    box.send_keys("cats")
    box.send_keys(Keys.ENTER)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img")))

    thumbnails = scroll_to_load_thumbnails(driver, wait, min_count=5, scroll_pause=0.5)

    assert isinstance(thumbnails, list)
    assert len(thumbnails) >= 1
