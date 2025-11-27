import pytest
from pages.login_page import LoginPage
from utils.helpers import captura_de_pantalla

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.mark.smoke
def test_login(driver):
    """
    Prueba el proceso de inicio de sesión en la aplicación.

    Pasos:
    - Abre la página de login.
    - Ingresa credenciales válidas.
    - Verifica que se acceda correctamente al inventario.
    - Valida que los títulos esperados estén presentes.

    Si ocurre un error, captura una captura de pantalla y relanza la excepción.
    """
    
    login_page = LoginPage(driver)

    try:
        login_page.abrir()
        inventory_page = login_page.login(USERNAME, PASSWORD)

        # Verifica que exista el elemento del título y que su texto sea 'Swag Labs'
        titulo = inventory_page.titulo()
        assert titulo, "No se encontró el titulo"
        assert titulo.text == "Swag Labs", f"Texto inesperado en logo: se esperaba 'Swag Labs' pero se obtuvo '{titulo.text}'"

        # Verifica título de sección
        seccion = inventory_page.titulo_de_seccion()
        assert seccion, "No se encontró el elemento de título de sección"
        assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

        print('Login completado correctamente y se ingresó a la página de inventario.')

    except Exception as e:
        captura_de_pantalla(driver, 'test_login')
        raise e