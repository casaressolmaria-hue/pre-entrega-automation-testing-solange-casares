import pytest
import sys
import os
from selenium.webdriver.common.by import By

from utils.driver import get_driver
from utils.helpers import entrar_a_la_pagina

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

URL = 'https://www.saucedemo.com/'
USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def login_saucedemo(driver):
    entrar_a_la_pagina(driver, URL, 'Swag Labs')

    # Completa los campos de login y hace clic en el botón de iniciar sesión, verificando que cada elemento exista
    assert driver.find_element(By.ID, "user-name"), "No se encontró el campo de usuario"
    driver.find_element(By.ID, "user-name").send_keys(USERNAME)

    assert driver.find_element(By.ID, "password"), "No se encontró el campo de contraseña"
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    assert driver.find_element(By.ID, "login-button"), "No se encontró el botón de login"
    driver.find_element(By.ID, "login-button").click()

    print("Se completaron correctamente los campos de login y se hizo clic en el botón.")

def test_login():
    login_saucedemo(driver)

    # Verifica que estamos en el inventario
    assert '/inventory.html' in driver.current_url, "No se redirigió a la página de inventario después del login"
    print('Login completado correctamente y se ingresó a la página de inventario.')
