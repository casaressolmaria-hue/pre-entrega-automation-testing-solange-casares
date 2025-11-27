import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv_login
from utils.helpers import captura_de_pantalla

_CASOS_LOGIN = leer_csv_login('datos/login.csv')

@pytest.mark.parametrize("usuario, clave, debe_funcionar", _CASOS_LOGIN)
def test_login_desde_csv(driver, usuario, clave, debe_funcionar):
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