import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv_login
from utils.helpers import captura_de_pantalla

_CASOS_LOGIN = leer_csv_login('datos/login.csv')

@pytest.mark.parametrize("usuario, clave, debe_funcionar", _CASOS_LOGIN)
def test_login_desde_csv(driver, usuario, clave, debe_funcionar):
    """
    Test de login parametrizado usando datos provenientes de un archivo CSV.

    Este test realiza las siguientes validaciones:

    1. Abre la página de login correctamente.
    2. Intenta iniciar sesión con el usuario y clave proporcionados.
    3. Si el caso indica que el login debe funcionar:
        - Verifica que el resultado del login no sea None.
        - Confirma que la URL actual contiene 'inventory.html' (indicando éxito).
    4. Si el caso indica que el login NO debe funcionar:
        - Verifica que el resultado sea None.
        - Comprueba que se muestre un mensaje de error en la página.

    En caso de cualquier excepción durante la ejecución,
    se captura una captura de pantalla antes de relanzar el error.

    Parámetros:
        driver (WebDriver): Instancia del navegador usada en la prueba.
        usuario (str): Nombre de usuario leído desde el CSV.
        clave (str): Contraseña asociada al usuario.
        debe_funcionar (bool): Indica si el caso de prueba debe resultar en un login exitoso.
    """
    
    login_page = LoginPage(driver)

    try:
        login_page.abrir()
        resultado = login_page.login(usuario, clave)

        if debe_funcionar:
            assert resultado is not None, "El login debía funcionar pero falló."
            assert "inventory.html" in driver.current_url
        else:
            assert resultado is None, "El login no debía funcionar, pero sí funcionó."
            assert login_page.hay_error(), "Se esperaba un mensaje de error y no apareció."

    except Exception as e:
        captura_de_pantalla(driver, 'test_login_desde_csv')
        raise e