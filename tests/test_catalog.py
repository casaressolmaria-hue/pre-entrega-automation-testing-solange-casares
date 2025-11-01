from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import captura_de_pantalla
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

def test_catalogo(driver):

    login_page = LoginPage(driver)

    try:
        # Hace login
        login_page.abrir()
        login_page.login(USERNAME, PASSWORD)

        inventory_page = InventoryPage(driver)
        
        # Verifica título de sección
        seccion = inventory_page.titulo_de_seccion()
        assert seccion, "No se encontró el elemento de título de sección"
        assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

        # Verifica que exista el botón de menú lateral antes de hacer clic
        menu_button = inventory_page.menu_boton()
        assert menu_button, "No se encontró el botón del menú"
        print("Botón de menú encontrado.")

        # Abre el menú lateral
        print("Haciendo clic en el botón de menú lateral")
        inventory_page.abrir_menu()
        print("El menú lateral está visible.")

        # Verifica que los enlaces requeridos estén presentes y con el texto correcto
        menu_items_esperados = ["All Items", "About", "Logout", "Reset App State"]
        menu_items = inventory_page.menu_items()

        assert len(menu_items) == len(menu_items_esperados), (
            f"Cantidad de ítems inesperada: se esperaban {len(menu_items_esperados)}, "
            f"pero se encontraron {len(menu_items)}."
        )

        for index, esperado in enumerate(menu_items_esperados):
            obtenido = menu_items[index]
            print(f"Verificando menú ítem: esperado '{esperado}', obtenido '{obtenido}'")
            assert esperado == obtenido, (
                f"Texto inesperado: se esperaba '{esperado}' pero se obtuvo '{obtenido}'"
            )

        print("Todos los ítems del menú fueron verificados correctamente.")

        # Verifica que el elemento activo del ordenamiento tenga el valor esperado
        print("Verificando que la opción del ordenamiento activo sea 'Name (A to Z)'")
        active_option = inventory_page.filtro_activo()
        assert active_option, "No se encontró el elemento con el ordenamiento activo."
        assert active_option.text == "Name (A to Z)", f"El ordenamiento activo no es el esperado: se esperaba 'Name (A to Z)', pero se encontró '{active_option.text}'."
        
        # Verifica que el select de ordenamiento exista y tenga opciones
        print("Verificando la existencia del select de ordenamiento")
        sort_select = inventory_page.select_de_ordenamiento()
        assert sort_select, "No se encontró el select de ordenamiento"
        opciones = inventory_page.opciones_de_ordenamiento()
        assert len(opciones) > 0, "El select no contiene opciones"

        # Verifica que las opciones estén en el orden esperado
        opciones_esperadas = [
            "Name (A to Z)",
            "Name (Z to A)",
            "Price (low to high)",
            "Price (high to low)"
        ]

        print("Verificando el orden y texto de las opciones")
        for index, texto_esperado in enumerate(opciones_esperadas):
            option_text = opciones[index].text
            assert option_text == texto_esperado, f"Texto inesperado en opción {index}: se esperaba {texto_esperado} pero se obtuvo {option_text}"

        verifica_carrito_vacio(driver)

        # Confirma que aparece al menos un producto
        cantidad_de_productos = inventory_page.obtener_cantidad_productos()
        assert cantidad_de_productos > 0, "No se encontraron productos en el catálogo"

        productos = inventory_page.obtener_productos()

        # Verifica que cada producto tenga nombre y precio visibles
        for producto in productos:
            assert inventory_page.nombre_del_producto(producto), "Producto sin nombre"
            assert inventory_page.precio_del_producto(producto), "Producto sin precio"

        # Muestra en consola el nombre y precio del primer producto
        primer_producto = productos[0]
        nombre_del_producto = inventory_page.nombre_del_producto(primer_producto)
        precio_del_producto = inventory_page.precio_del_producto(primer_producto)

        print(f"Primer producto: Nombre: {nombre_del_producto}, Precio: {precio_del_producto}")

    except Exception as e:
        captura_de_pantalla(driver, 'test_catalogo')
        raise e
    

def verifica_carrito_vacio(driver):
    # Verifica que exista el carrito de compras
    print("Verificando la existencia del carrito de compras")
    carrito = driver.find_element(By.ID, "shopping_cart_container")
    assert carrito, "No se encontró el elemento con id shopping_cart_container"

    # Verifica que el carrito esté vacío (sin contador de cantidad)
    print("Verificando que el carrito esté vacío")
    contador = carrito.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(contador) == 0, "El carrito no está vacío: se encontró un contador de cantidad"
