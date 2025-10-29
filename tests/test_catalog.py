import pytest
from pages.login_page import LoginPage
from utils.driver import get_driver
from utils.helpers import captura_de_pantalla
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_catalogo(driver):

    login_page = LoginPage(driver)

    try:
        # Hace login
        login_page.abrir()
        login_page.login(USERNAME, PASSWORD)

        # Verifica título de sección
        titulo = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
        assert titulo == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{titulo}'"

        verifica_menu(driver)
        verifica_filtro(driver)
        verifica_carrito_vacio(driver)

        # Confirma que aparece al menos un div.inventory_item
        productos = driver.find_elements(By.CSS_SELECTOR, "div.inventory_item")
        assert len(productos) > 0, "No se encontraron productos en el catálogo"

        # Verifica que cada producto tenga nombre y precio visibles
        for producto in productos:
            verifica_producto_basico(producto)

        # Muestra en consola el nombre y precio del primer producto
        primer_producto = productos[0]
        nombre_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

        print(f"Nombre: {nombre_del_producto}, Precio: {precio_del_producto}")

    except Exception as e:
        captura_de_pantalla(driver, 'test_catalogo')
        raise e
    

def verifica_menu(driver):
    # Verifica que exista el botón de menú lateral antes de hacer clic
    menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
    assert menu_button, "No se encontró el botón con clase 'react-burger-menu-btn'"
    print("Botón de menú encontrado.")

    # Abre el menú lateral haciendo clic en el botón de menú (hamburguesa)
    print("Haciendo clic en el botón de menú lateral")
    menu_button.click()

    # Espera hasta que aparezca el contenedor del menú lateral
    print("Esperando a que aparezca el menú lateral")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "bm-item-list"))
    )
    print("El menú lateral está visible.")

    # Verifica que los enlaces requeridos estén presentes y con el texto correcto
    menu_items = [
        ("inventory_sidebar_link", "All Items"),
        ("about_sidebar_link", "About"),
        ("logout_sidebar_link", "Logout"),
        ("reset_sidebar_link", "Reset App State")
    ]

    for item_id, expected_text in menu_items:
        print(f"Verificando el enlace con id '{item_id}' y texto esperado '{expected_text}'")
        element = driver.find_element(By.ID, item_id)
        assert element, f"No se encontró el enlace con id '{item_id}'"
        assert element.text == expected_text, f"Texto inesperado para '{item_id}': se esperaba '{expected_text}' pero se obtuvo '{element.text}'"
        print(f"Enlace '{expected_text}' verificado correctamente.")


def verifica_filtro(driver):
    # Verifica que el elemento con clase active_option tenga el valor esperado
    print("Verificando que la opción activa sea 'Name (A to Z)'")
    active_option = driver.find_element(By.CLASS_NAME, "active_option")
    assert active_option, "No se encontró el elemento con clase active_option"
    assert active_option.text == "Name (A to Z)", f"Valor inesperado en active_option: se esperaba 'Name (A to Z)' pero se obtuvo '{active_option.text}'"

    # Verifica que el select de ordenamiento exista y tenga opciones
    print("Verificando la existencia del select de ordenamiento")
    sort_select = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert sort_select, "No se encontró el select con clase product_sort_container"
    options = sort_select.find_elements(By.TAG_NAME, "option")
    assert len(options) > 0, "El select no contiene opciones"

    # Verifica que las opciones estén en el orden esperado
    expected_values = [
        "Name (A to Z)",
        "Name (Z to A)",
        "Price (low to high)",
        "Price (high to low)"
    ]

    print("Verificando el orden y texto de las opciones")
    for index, expected_text in enumerate(expected_values):
        option_text = options[index].text
        assert option_text == expected_text, f"Texto inesperado en opción {index}: se esperaba {expected_text} pero se obtuvo {option_text}"


def verifica_carrito_vacio(driver):
    # Verifica que exista el carrito de compras
    print("Verificando la existencia del carrito de compras")
    carrito = driver.find_element(By.ID, "shopping_cart_container")
    assert carrito, "No se encontró el elemento con id shopping_cart_container"

    # Verifica que el carrito esté vacío (sin contador de cantidad)
    print("Verificando que el carrito esté vacío")
    contador = carrito.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(contador) == 0, "El carrito no está vacío: se encontró un contador de cantidad"


def verifica_producto_basico(producto):
        assert producto.find_element(By.CLASS_NAME, "inventory_item_name"), "Producto sin nombre"
        assert producto.find_element(By.CLASS_NAME, "inventory_item_price"), "Producto sin precio"