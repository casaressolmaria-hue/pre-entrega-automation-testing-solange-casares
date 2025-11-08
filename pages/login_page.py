from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.inventory_page import InventoryPage

class LoginPage:

    URL = 'https://www.saucedemo.com/'

    _USER_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _SUBMIT_BUTTON = (By.ID, "login-button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.URL)
        return self

    def completar_usuario(self, usuario: str):
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def completar_clave(self, clave: str):
        campo = self.driver.find_element(*self._PASSWORD_INPUT)
        campo.clear()
        campo.send_keys(clave)
        return self

    def hacer_click_login(self):
        self.driver.find_element(*self._SUBMIT_BUTTON).click()
        return self

    def login(self, usuario, clave):
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_click_login()
        return InventoryPage(self.driver)