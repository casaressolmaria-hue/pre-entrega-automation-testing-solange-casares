import os
from datetime import datetime


def entrar_a_la_pagina(driver, url, titulo):
    # Entra a la página
    driver.get(url)
    
    # Verifica título de la página
    assert driver.title == titulo

    print('Se ingresó correctamente a la página {} con el título esperado: {}', url, titulo)


def captura_de_pantalla(driver, caso):
    # Guarda una captura de pantalla con tiempo y nombre de test.
    os.makedirs("reports", exist_ok=True)
    tiempo = datetime.now().strftime("%d-%m-%Y %S-%M-%H")
    archivo = f"reports/{caso}_{tiempo}.png"
    driver.save_screenshot(archivo)
    print(f"Screenshot guardado en: {archivo}")