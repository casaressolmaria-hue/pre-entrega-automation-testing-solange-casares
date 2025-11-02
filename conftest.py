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
    options.add_argument('--start-maximized') # Ventana grande
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True
    })
    options.add_argument("--disable-features=PasswordManagerOnboarding,PasswordCheck")
   
    service = Service()
    driver = webdriver.Chrome(service=service,options=options)
    driver.implicitly_wait(5) # Espera implícita
    
    yield driver

    time.sleep(1)
    driver.quit()