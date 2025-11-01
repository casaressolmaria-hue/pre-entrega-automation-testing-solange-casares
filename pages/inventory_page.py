from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class InventoryPage:

    _TITULO = (By.CLASS_NAME, 'app_logo')
    _TITULO_DE_SECCION = (By.CSS_SELECTOR, 'div.header_secondary_container .title')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.wait.until(EC.url_contains("inventory.html"))

    def titulo(self):
        return self.driver.find_element(*self._TITULO)
    
    def titulo_de_seccion(self):
        return self.driver.find_element(*self._TITULO_DE_SECCION)
    
    # obtener_cantidad_productos

    # agregar_producto_por_indice

    # ir_al_carrito

    # realizar_logout