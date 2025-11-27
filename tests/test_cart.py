import pytest
from pages.login_page import LoginPage
from utils.helpers import captura_de_pantalla

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'
    
@pytest.mark.smoke
def test_carrito(driver):
    """
    Prueba del flujo completo de agregar un producto al carrito.

    Pasos:
    - Inicia sesión correctamente.
    - Verifica que el catálogo muestre la sección 'Products'.
    - Confirma que exista al menos un producto.
    - Obtiene el primer producto y valida que tenga nombre y precio visibles.
    - Verifica que tenga un botón 'Add to cart' y lo presiona.
    - Comprueba que el contador del carrito aumente.
    - Ingresa al carrito.
    - Valida que exista la lista de productos del carrito.
    - Verifica que haya exactamente un producto añadido.
    - Confirma que el nombre y precio del producto del carrito coincidan con el producto seleccionado.

    En caso de error:
    - Se captura una captura de pantalla.
    - Se relanza la excepción para marcar el test como fallido.
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

        # Confirma que aparece al menos un producto
        assert inventory_page.obtener_cantidad_productos() > 0, "No se encontraron productos en el catálogo"

        productos = inventory_page.obtener_productos()
        primer_producto = productos[0]

        # Verifica que existan el nombre y el precio del primer producto
        print("Verificando que el primer producto tenga nombre y precio...")
        nombre_del_producto = inventory_page.nombre_del_producto(primer_producto)
        assert nombre_del_producto, "Producto sin nombre"
        precio_del_producto = inventory_page.obtener_precio_del_producto(nombre_del_producto)
        assert precio_del_producto, "Producto sin precio"

        print(f"Primer producto: Nombre: {nombre_del_producto}, Precio: {precio_del_producto}")

        # Verifica que exista el botón "Add to cart" en el primer producto
        print("Verificando que exista el botón 'Add to cart' en el primer producto")
        assert inventory_page.boton_agregar(primer_producto), "No se encontró el botón 'Add to cart' en el primer producto"

        # Haz clic en "Add to cart" del primer producto
        print("Agregando primer producto haciendo clic en el botón 'Add to cart'")
        inventory_page.agregar_producto(primer_producto)

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
        assert nombre_en_carrito.text == nombre_del_producto, (
            f"Nombre inesperado en el carrito: se esperaba {nombre_del_producto} pero se obtuvo {nombre_en_carrito.text}"
        )

        precio_en_carrito = cart_page.precio_del_producto_agregado(primer_producto_del_carrito)
        assert precio_en_carrito, "No se encontró el precio del producto en el carrito"
        assert precio_en_carrito == precio_del_producto, (
            f"Precio inesperado en el carrito: se esperaba {precio_del_producto} pero se obtuvo {precio_en_carrito}"
        )

        print("El producto en el carrito coincide con el producto añadido.")

    except Exception as e:
        captura_de_pantalla(driver, 'test_carrito')
        raise e
