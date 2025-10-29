from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import captura_de_pantalla
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

def test_login(driver):

    login_page = LoginPage(driver)

    try:
        login_page.abrir()
        login_page.login(USERNAME, PASSWORD)

        inventory_page = InventoryPage(driver)

        # Verificar que el login fue exitoso comprobando que estamos en la página de productos
        WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
            )

        # Verifica que estamos en el inventario
        assert '/inventory.html' in driver.current_url, "No se redirigió a la página de inventario después del login"

        # Verifica que exista el elemento del título y que su texto sea 'Swag Labs'
        titulo = driver.find_element(By.CLASS_NAME, "app_logo")
        assert titulo, "No se encontró el elemento con clase 'app_logo'"
        assert titulo.text == "Swag Labs", f"Texto inesperado en logo: se esperaba 'Swag Labs' pero se obtuvo '{titulo.text}'"

        # Verifica título de sección
        seccion = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
        assert seccion == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion}'"

        print('Login completado correctamente y se ingresó a la página de inventario.')

    except Exception as e:
        captura_de_pantalla(driver, 'test_login')
        raise e