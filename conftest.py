import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized") # Ventana grande
    options.add_argument("--guest")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5) # Espera implícita

    yield driver

    time.sleep(1)
    driver.quit()
