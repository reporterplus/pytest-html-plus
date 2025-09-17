# tests/test_example_selenium.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def make_driver(request):
    chrome_options = Options()
    # headless mode
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,1024")
    svc = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=svc, options=chrome_options)
    request.node.page_for_screenshot = drv

    # using webdriver-manager to install the chromedriver binary
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def test_example_dot_com_screenshot(request):
    driver = make_driver(request)
    try:
        url = "https://example.com"
        driver.get(url)
        time.sleep(10)
        assert "Example Domainn" in driver.page_source
    finally:
        driver.quit()
