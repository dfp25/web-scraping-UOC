# web-scraping-UOC
Proyecto para la materia Tipología y ciclo de vida de los datos

## Daniel Flores Pérez

## Archivos que componen el repositorio
- dataset:
     - peliculas_finalistas_premios_goya.csv
- source:
     - cine_dflores_PR1.ipynb
     - cine_dflores_PR1.py
- LICENSE
- README.md
- requirements.txt

## DOI Zenodo
[DOI](https://doi.org/10.5281/zenodo.14029149) "DOI Zenodo")


# Extracción de Datos de Premios de Cine (Goya, Feroz, Forqué, CEC)

Este proyecto utiliza Python y varias bibliotecas (Selenium, BeautifulSoup, Requests, Pandas, etc.) para realizar el scraping de datos sobre películas nominadas y ganadoras en cuatro premios de cine en España: los premios Goya, Feroz, Forqué y CEC. Los datos se organizan y guardan en archivos CSV.

## Contenido del Proyecto

1. **Configuración del Entorno**
2. **Datos de Premios Goya**
3. **Datos de Premios Feroz**
4. **Datos de Premios Forqué**
5. **Datos de Premios CEC**
6. **Unión de Datos**
7. **User-Agent en Selenium**

### 1. Configuración del Entorno

Se configuran las bibliotecas y el entorno de trabajo. El directorio de trabajo se configura para guardar los archivos en el mismo directorio donde se abre el archivo.

### 2. Datos de Premios Goya

Esta sección extrae datos de películas ganadoras y nominadas en los premios Goya, incluyendo:

- Título de la ganadora.
- Lista de películas nominadas.
- Número de nominaciones de cada película.
- Puntuación.
- Votos.
- Críticas.
- Géneros.

Para ello, se utiliza Selenium para manejar la aceptación de cookies y navegar a través de las páginas.

### 3. Datos de Premios Feroz

Similar al proceso anterior, se realiza la extracción de datos de películas ganadoras y nominadas en los premios Feroz, en las categorías de drama y comedia.

### 4. Datos de Premios Forqué

Se extraen los títulos de películas ganadoras y nominadas en la categoría de mejor película.

### 5. Datos de Premios CEC

La información de los premios CEC se obtiene desde Wikipedia, debido a que los datos en la página oficial están menos estructurados. La función recibe como parámetro el link a la página web de Wikepedia donde se encuentran las tablas.

Ejemplo:

*tablas_wiki (http:\\www.prueba.com)*

Se obtienen todas las tablas que haya en la página 'prueba.com' perteneciente a la Wikipedia.

### 6. Unión de Datos

A medida que se van extrayendo los datos de los 4 premios, se van uniendo en un solo archivo CSV.

### 7. User-Agent en Selenium

Aquí se indica el User-Agent utilizado.
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36

## Requisitos

Se ha utilizado:
- **Python 3.12.7**
- **Paquetes**: numpy, pandas, selenium, requests, beautifulsoup4
- **Selenium WebDriver**: Requiere 'chromedriver' para automatizar el navegador Chrome. Ver 7. User-Agent.

## Ejecución y uso

1. Asegúrate de tener los paquetes necesarios.
2. Ejecuta el script de extracción de datos.
3. Los archivos CSV se guardarán en el directorio de trabajo, conteniendo los datos de los cuatro premios.
