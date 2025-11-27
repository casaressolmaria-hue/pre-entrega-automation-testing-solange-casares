from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CartPage:

    _LISTA_DE_LOS_PRODUCTOS = (By.CLASS_NAME, "cart_list")
    _PRODUCTO_DEL_CARRITO = (By.CLASS_NAME, "cart_item")
    _NOMBRE_DEL_PRODUCTO = (By.CLASS_NAME, 'inventory_item_name')
    _PRECIO_DEL_PRODUCTO = (By.CLASS_NAME, 'inventory_item_price')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.wait.until(EC.url_contains("/cart.html"))

    def lista_de_los_productos(self):
        return self.driver.find_element(*self._LISTA_DE_LOS_PRODUCTOS)
    
    def productos_del_carrito(self):
        lista_de_los_productos = self.lista_de_los_productos()
        return lista_de_los_productos.find_elements(*self._PRODUCTO_DEL_CARRITO)
    
    def nombre_del_producto_agregado(self, producto):
        return producto.find_element(*self._NOMBRE_DEL_PRODUCTO)
    
    def precio_del_producto_agregado(self, producto):
        precio = producto.find_element(*self._PRECIO_DEL_PRODUCTO).text
        return float(precio.replace("$", ""))