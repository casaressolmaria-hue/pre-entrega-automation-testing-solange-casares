# Proyecto de Automatización de Pruebas con Selenium (SauceDemo)

**Autor**: Solange Casares

## Propósito del proyecto
Este proyecto automatiza pruebas funcionales en la página [SauceDemo](https://www.saucedemo.com/)

El objetivo es garantizar que las funciones críticas del sitio web se comporten como se espera mediante pruebas automatizadas.

## Tecnologías utilizadas
- **Python 3**
- **Selenium WebDriver**
- **pytest**
- **pytest-html** (para generar reportes en HTML)

## Estructura del proyecto

**utils/**  
├── `driver.py` — Configuración del WebDriver (Chrome)  
└── `helpers.py` — Funciones auxiliares y genéricas para todos los tests

**tests/**  
├── `helpers_saucedemo.py` — Funciones comunes para tests de SauceDemo  
└── `test_saucedemo.py` — Casos de prueba

**reports/** - Reportes HTML y capturas

**README.md** - Documentación del proyecto

## Instalación

1. Asegúrate de tener Python 3.7 o superior instalado
2. Descarga el WebDriver correspondiente a tu navegador: [selenium.dev](https://www.selenium.dev/)
3. Clona este repositorio:
   ```bash
   git clone https://github.com/casaressolmaria-hue/pre-entrega-automation-testing-solange-casares.git
4. Instala las dependencias:
   ```bash
    pip install selenium pytest pytest-html

## Casos de prueba incluidos
 - **test_login**: Verifica acceso correcto a la página de inventario.
 - **test_catalogo**: Comprueba la presencia de productos, filtros y menú.
 - **test_carrito**: Valida que agregar un producto al carrito funcione correctamente.

## Ejecución de pruebas

 - Ejecuta las pruebas con:
    ```bash
    pytest -v tests/test_saucedemo.py
 - Para generar un reporte HTML:
    ```bash
    pytest tests/test_saucedemo.py -v --html=./reports/reporte.html