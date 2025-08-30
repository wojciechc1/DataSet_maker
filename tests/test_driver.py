import pytest
from downloader.selenium_driver import get_driver


def test_driver_launches():
    driver = get_driver(headless=True)
    driver.get("https://www.google.com")

    assert "Google" in driver.title

    driver.quit()
