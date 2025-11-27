import csv
import pathlib
import json

def leer_csv_login(ruta_archivo):
    """
    Lee un archivo CSV y devuelve una lista de tuplas
    para usar en parametrización de pytest
    """
    datos = []
    ruta = pathlib.Path(ruta_archivo)
    
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Convertir string 'True'/'False' a booleano
            debe_funcionar = fila['debe_funcionar'].lower() == 'true'
            datos.append((fila['usuario'], fila['clave'], debe_funcionar))
    
    return datos


def leer_json_productos(ruta_archivo):
    """
    Lee un archivo JSON con información de productos
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        productos = json.load(archivo)
    
    return productos
    # Extraer solo los nombres para parametrización
    # nombres = [producto['nombre'] for producto in productos]
    # return nombres