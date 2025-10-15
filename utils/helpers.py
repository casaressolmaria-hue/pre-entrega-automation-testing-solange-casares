from selenium.webdriver.common.by import By

def entrar_a_la_pagina(driver, url, titulo):
    # Entra a la página
    driver.get(url)
    
    # Verifica título de la página
    assert driver.title == titulo

    print('Se ingresó correctamente a la página {} con el título esperado: {}', url, titulo)