import pytest
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.driver import get_driver
from utils.helpers import entrar_a_la_pagina

URL = 'https://www.saucedemo.com/'
USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login(driver):
    login_saucedemo(driver)

    # Verificar que el login fue exitoso comprobando que estamos en la página de productos
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
        )

    # Verifica que estamos en el inventario
    assert '/inventory.html' in driver.current_url, "No se redirigió a la página de inventario después del login"

    # Verifica título de sección
    titulo = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
    assert titulo == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{titulo}'"

    print('Login completado correctamente y se ingresó a la página de inventario.')

def login_saucedemo(driver):
    entrar_a_la_pagina(driver, URL, 'Swag Labs')

    # Espera a que se cargue el formulario de login
    WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user-name"))
            )

    # Verifica que los elementos esenciales del formulario de login estén presentes antes de interactuar con ellos
    assert driver.find_element(By.ID, "user-name"), "No se encontró el campo de usuario"
    assert driver.find_element(By.ID, "password"), "No se encontró el campo de contraseña"
    assert driver.find_element(By.ID, "login-button"), "No se encontró el botón de login"

    # Completa los campos de login y hace clic en el botón de iniciar sesión, verificando que cada elemento exista
    driver.find_element(By.ID, "user-name").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    print("Se completaron correctamente los campos de login y se hizo clic en el botón.")
