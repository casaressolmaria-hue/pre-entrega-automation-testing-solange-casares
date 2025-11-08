import os
from datetime import datetime


def captura_de_pantalla(driver, caso):
    # Guarda una captura de pantalla con tiempo y nombre de test.
    os.makedirs("reports", exist_ok=True)
    tiempo = datetime.now().strftime("%d-%m-%Y %S-%M-%H")
    archivo = f"reports/{caso}_{tiempo}.png"
    driver.save_screenshot(archivo)
    print(f"Screenshot guardado en: {archivo}")