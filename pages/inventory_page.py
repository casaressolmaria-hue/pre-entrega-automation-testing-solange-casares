from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.cart_page import CartPage

class InventoryPage:

    _TITULO = (By.CLASS_NAME, 'app_logo')
    _TITULO_DE_SECCION = (By.CSS_SELECTOR, 'div.header_secondary_container .title')
    _MENU_BOTON = (By.ID, "react-burger-menu-btn")
    _MENU_CERRAR = (By.ID, "react-burger-cross-btn")
    _MENU_LIST = (By.CLASS_NAME, "bm-item-list")
    _FILTRO_ACTIVO = (By.CLASS_NAME, "active_option")
    _SELECT_DE_ORDENAMIENTO = (By.CLASS_NAME, "product_sort_container")
    _ORDENAMIENTO_OPCION = (By.TAG_NAME, "option")
    _INVENTORY_ITEM = (By.CSS_SELECTOR, "div.inventory_item")
    _NOMBRE_DEL_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
    _PRECIO_DEL_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
    _CARRITO = (By.ID, "shopping_cart_container")
    _CARRITO_CONTADOR = (By.CLASS_NAME, "shopping_cart_badge")
    _AGREGAR_PRODUCTO = (By.XPATH, ".//button[text()='Add to cart']")
    _PRODUCTO_POR_NOMBRE = (By.XPATH, "//div[@data-test='inventory-item-name' and text()='{}']/ancestor::div[@data-test='inventory-item']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.wait.until(EC.url_contains("inventory.html"))

    def titulo(self):
        return self.driver.find_element(*self._TITULO)
    
    def titulo_de_seccion(self):
        return self.driver.find_element(*self._TITULO_DE_SECCION)
    
    def menu_boton(self):
        return self.wait.until(EC.element_to_be_clickable(self._MENU_BOTON))
    
    def abrir_menu(self):
        self._cerrar_menu()
        boton = self.menu_boton()
        boton.click()
        return self.wait.until(EC.element_to_be_clickable(self._MENU_LIST))
    
    def _cerrar_menu(self):
        cerrar = self.driver.find_element(*self._MENU_CERRAR)
        if cerrar.is_displayed():
            cerrar.click()
        return self

    def menu_items(self):
        menu = self.abrir_menu()
        return menu.find_elements(By.TAG_NAME, "a")
    
    def filtro_activo(self):
        return self.driver.find_element(*self._FILTRO_ACTIVO)

    def select_de_ordenamiento(self):
        return self.driver.find_element(*self._SELECT_DE_ORDENAMIENTO)

    def opciones_de_ordenamiento(self):
        select_de_ordenamiento = self.select_de_ordenamiento()
        return select_de_ordenamiento.find_elements(*self._ORDENAMIENTO_OPCION)

    def obtener_cantidad_productos(self):
        productos = self.driver.find_elements(*self._INVENTORY_ITEM)
        return len(productos)

    def obtener_productos(self):
        return self.driver.find_elements(*self._INVENTORY_ITEM)
    
    def obtener_precio_del_producto(self, nombre_producto):
        producto = self._obtener_producto_por_nombre(nombre_producto)
        precio = producto.find_element(*self._PRECIO_DEL_PRODUCTO).text
        return float(precio.replace("$", ""))
    
    def _obtener_producto_por_nombre(self, nombre_producto):
        by, xpath_template = self._PRODUCTO_POR_NOMBRE
        xpath = xpath_template.format(nombre_producto)
        return self.driver.find_element(by, xpath)
    
    def carrito(self):
        return self.driver.find_element(*self._CARRITO)

    def carrito_contador(self):
        carrito = self.carrito()
        return len(carrito.find_elements(*self._CARRITO_CONTADOR))

    def nombre_del_producto(self, producto):
        return producto.find_element(*self._NOMBRE_DEL_PRODUCTO).text

    def boton_agregar(self, producto):
        return producto.find_element(*self._AGREGAR_PRODUCTO)

    def agregar_producto(self, producto):
        boton = self.boton_agregar(producto)
        boton.click()
        return self
    
    def agregar_producto_por_nombre(self, nombre_producto):
        producto = self._obtener_producto_por_nombre(nombre_producto)
        return self.agregar_producto(producto)

    def ir_al_carrito(self):
        carrito = self.carrito()
        carrito.click()
        return CartPage(self.driver)
