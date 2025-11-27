import pytest
from pages.login_page import LoginPage
from utils.helpers import captura_de_pantalla

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.mark.smoke
def test_catalogo(driver):
    """
    Prueba integral del catálogo en la página de inventario.

    Pasos:
    - Inicia sesión con credenciales válidas.
    - Verifica el título de sección 'Products'.
    - Confirma la existencia y funcionamiento del menú lateral.
    - Valida la presencia y el texto de los ítems del menú.
    - Comprueba el ordenamiento activo y las opciones disponibles.
    - Revisa la existencia del carrito y que esté vacío.
    - Valida que haya productos visibles en el catálogo.
    - Confirma que cada producto tenga nombre y precio visibles.
    - Imprime en consola el nombre y precio del primer producto.

    Si ocurre un error durante la prueba:
    - Captura una captura de pantalla.
    - Relanza la excepción para que el test falle correctamente.
    """
    
    login_page = LoginPage(driver)

    try:
        # Hace login
        login_page.abrir()
        inventory_page = login_page.login(USERNAME, PASSWORD)

        # Verifica título de sección
        seccion = inventory_page.titulo_de_seccion()
        assert seccion, "No se encontró el elemento de título de sección"
        assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

        # Verifica que exista el botón de menú lateral antes de hacer clic
        assert inventory_page.menu_boton(), "No se encontró el botón del menú"
        print("Botón de menú encontrado.")

        # Abre el menú lateral
        print("Haciendo clic en el botón de menú lateral")
        inventory_page.abrir_menu()
        print("El menú lateral está abierto.")

        # Verifica que los enlaces requeridos estén presentes y con el texto correcto
        menu_items_esperados = ["All Items", "About", "Logout", "Reset App State"]
        menu_items = inventory_page.menu_items()

        assert len(menu_items) == len(menu_items_esperados), (
            f"Cantidad de ítems inesperada: se esperaban {len(menu_items_esperados)}, "
            f"pero se encontraron {len(menu_items)}."
        )

        for index, esperado in enumerate(menu_items_esperados):
            obtenido = menu_items[index]
            print(f"Verificando menú ítem: esperado '{esperado}', obtenido '{obtenido.text}'")
            assert esperado == obtenido.text, (
                f"Texto inesperado: se esperaba '{esperado}' pero se obtuvo '{obtenido.text}'"
            )

        print("Todos los ítems del menú fueron verificados correctamente.")

        # Verifica que el elemento activo del ordenamiento tenga el valor esperado
        print("Verificando que la opción del ordenamiento activo sea 'Name (A to Z)'")
        active_option = inventory_page.filtro_activo()
        assert active_option, "No se encontró el elemento con el ordenamiento activo."
        assert active_option.text == "Name (A to Z)", f"El ordenamiento activo no es el esperado: se esperaba 'Name (A to Z)', pero se encontró '{active_option.text}'."
        
        # Verifica que el select de ordenamiento exista y tenga opciones
        print("Verificando la existencia del select de ordenamiento")
        assert inventory_page.select_de_ordenamiento(), "No se encontró el select de ordenamiento"
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

        # Verifica que exista el carrito de compras
        print("Verificando la existencia del carrito de compras")
        assert inventory_page.carrito(), "No se encontró el elemento con id shopping_cart_container"

        # Verifica que el carrito esté vacío (sin contador de cantidad)
        print("Verificando que el carrito esté vacío")
        contador = inventory_page.carrito_contador()
        assert contador == 0, f"El carrito no está vacío: se encontró un contador de cantidad: {contador}"

        # Confirma que aparece al menos un producto
        assert inventory_page.obtener_cantidad_productos() > 0, "No se encontraron productos en el catálogo"

        productos = inventory_page.obtener_productos()

        # Verifica que cada producto tenga nombre y precio visibles
        for producto in productos:
            nombre_del_producto = inventory_page.nombre_del_producto(producto)
            assert nombre_del_producto, "Producto sin nombre"
            assert inventory_page.obtener_precio_del_producto(nombre_del_producto), "Producto sin precio"

        # Muestra en consola el nombre y precio del primer producto
        primer_producto = productos[0]
        nombre_del_producto = inventory_page.nombre_del_producto(primer_producto)
        precio_del_producto = inventory_page.obtener_precio_del_producto(nombre_del_producto)

        print(f"Primer producto: Nombre: {nombre_del_producto}, Precio: {precio_del_producto}")

    except Exception as e:
        captura_de_pantalla(driver, 'test_catalogo')
        raise e

