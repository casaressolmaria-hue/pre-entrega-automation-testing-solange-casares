
import pytest
from pages.login_page import LoginPage
from utils.datos import leer_json_productos
from utils.helpers import captura_de_pantalla

_PRODUCTOS = leer_json_productos('datos/productos.json')

@pytest.fixture
def usuario_logueado(driver):
    """
    Fixture que realiza login antes de cada test de carrito
    """
    login_page = LoginPage(driver)
    login_page.abrir()
    return login_page.login("standard_user", "secret_sauce")


@pytest.mark.parametrize("producto", _PRODUCTOS)
def test_carrito(driver, usuario_logueado, producto):
    """
    Test end-to-end del flujo de agregar un producto al carrito.

    Este test valida:

    1. Que el usuario logueado accede correctamente a la página de inventario.
    2. Que la sección de productos muestra el título esperado ("Products").
    3. Que el catálogo contiene al menos un producto.
    4. Que el precio del producto obtenido coincide con el precio definido en los datos.
    5. Que el producto puede agregarse al carrito.
    6. Que el contador del carrito incrementa tras agregar el producto.
    7. Que el carrito contiene exactamente un producto.
    8. Que el nombre y precio del producto en el carrito coinciden con los esperados.

    Si ocurre cualquier excepción, se captura una captura de pantalla antes de relanzar el error.

    Parámetros:
        driver (WebDriver): Instancia del navegador para la prueba.
        usuario_logueado (InventoryPage): Página ya autenticada para comenzar el test.
        producto (dict): Datos del producto (nombre y precio) proporcionados por la parametrización.
    """
        
    try:
        inventory_page = usuario_logueado

        # Verifica título de sección
        seccion = inventory_page.titulo_de_seccion()
        assert seccion, "No se encontró el elemento de título de sección"
        assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

        # Confirma que aparece al menos un producto
        assert inventory_page.obtener_cantidad_productos() > 0, "No se encontraron productos en el catálogo"

        precio_del_producto = inventory_page.obtener_precio_del_producto(producto["nombre"])
        assert precio_del_producto, "Producto sin precio"
        print(precio_del_producto)
        assert precio_del_producto == producto["precio"], f"El precio mostrado ({precio_del_producto}) no coincide con el esperado ({producto['precio']}) para el producto {producto['nombre']}"

        print(f"Producto: Nombre: {producto["nombre"]}, Precio: {precio_del_producto}")

        # Haz clic en "Add to cart" del primer producto
        print("Agregando primer producto haciendo clic en el botón 'Add to cart'")
        inventory_page.agregar_producto_por_nombre(producto["nombre"])

        # Verifica que el contador del carrito muestre 1
        print("Verificando que el contador del carrito muestre 1")
        assert inventory_page.carrito_contador() > 0, "No se encontró el contador del carrito después de agregar el producto"

        # Ingresa al carrito
        print("Ingresando al carrito")
        cart_page = inventory_page.ir_al_carrito()

        # Verifica que exista la lista de productos del carrito
        print("Verificando que exista la lista de productos en el carrito")
        assert cart_page.lista_de_los_productos(), "No se encontró la lista de productos en el carrito"

        productos_del_carrito = cart_page.productos_del_carrito()
        assert len(productos_del_carrito) == 1, f"Se esperaba 1 producto en el carrito, pero se encontraron {len(productos_del_carrito)}"
        
        # Verificar que el producto añadido esté en la lista
        print("Verificando que el producto añadido sea el correcto")
        primer_producto_del_carrito = productos_del_carrito[0]

        nombre_en_carrito = cart_page.nombre_del_producto_agregado(primer_producto_del_carrito)
        assert nombre_en_carrito, "No se encontró el nombre del producto en el carrito"
        assert nombre_en_carrito.text == producto["nombre"], (
            f"Nombre inesperado en el carrito: se esperaba {producto["nombre"]} pero se obtuvo {nombre_en_carrito.text}"
        )

        precio_en_carrito = cart_page.precio_del_producto_agregado(primer_producto_del_carrito)
        assert precio_en_carrito, "No se encontró el precio del producto en el carrito"
        assert precio_en_carrito == precio_del_producto, (
            f"Precio inesperado en el carrito: se esperaba {precio_del_producto} pero se obtuvo {precio_en_carrito.text}"
        )

        print("El producto en el carrito coincide con el producto añadido.")

    except Exception as e:
        captura_de_pantalla(driver, 'test_carrito')
        raise e
