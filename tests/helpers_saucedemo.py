from utils.helpers import entrar_a_la_pagina
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


URL = 'https://www.saucedemo.com/'
USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'


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
