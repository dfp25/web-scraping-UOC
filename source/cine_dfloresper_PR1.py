#!/usr/bin/env python
# coding: utf-8

# # Configuración del entorno

# ## Importación de paquetes

# In[1]:


import numpy as np
import os
import pandas as pd
import re
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


# ## Directorio de trabajo

# In[2]:


# Directorio de trabajo actual
dir_actual = os.getcwd()

# Cambio a directorio actual
os.chdir(dir_actual)


# # Datos Premios Goya

# ## Manejar ventana de aceptar cookies

# Gestionar la aparición de cookies en el primer acceso al site.

# In[3]:


def manejar_cookies():
    """
    Esta función maneja la el aviso de cookies de la página web.
    
    Espera 3 segundos para permitir que la página cargue completamente,  busca el botón de
    "NO ACEPTO" para las cookies y hace clic en él. Si el botón no se encuentra, se imprime
    un mensaje de aviso.

    Returns:
        None: No devuelve ningún valor, solo sirve para saltar las cookies.
    """
    try:
        # Espera 3 segundos
        time.sleep(3)

        # Clic sobre el botón de no aceptar cookies
        boton = driver.find_element(By.XPATH, "//button[span[text()='NO ACEPTO']]")
        boton.click()

        # Espera 3 segundos
        time.sleep(3)
        return

    except:
        print("Botón de cookies no encontrado")
        
        return


# ## Datos 1

# Título de la película ganadora, títulos de las nominadas y número de nominaciones de las películas.

# In[4]:


def datos1():
    """
    Extrae los datos de películas nominadas y ganadoras de los premios Goya.

    Utiliza un objeto de beautifulsoup ('html1') para obtener información sobre las películas nominadas
    y la ganadora en la categoría de Mejor Película. Recopila los títulos de las películas, el número
    de nominaciones de cada una y un indicador de si la película ganó o no.

    Returns:
        tuple: Una tupla con tres listas:
            - tp (list of str): Títulos de las películas nominadas y la ganadora.
            - nomi (list of str): Número de nominaciones de cada película.
            - gdor (list of int): Indicadores de ganadora (1 para la ganadora, 0 si no ganó).
    """
    # Listas para títulos y nominaciones recibidas
    tp, nomi = [], []
    
    # Título de la película ganadora del Goya
    tp.append(html1.find(id='goya_best_picture').parent.select('span.movie-title-link')[0].text.strip())

    # Título de las películas nominadas
    for n in html1.find(id='goya_best_picture').parent.select('span.movie-title-link')[1:]:
        tp.append(n.a.text.strip())

    # Nominaciones de todas las películas finalistas incluida la ganadora
    for m in html1.find(id='goya_best_picture').parent.select('div.nom-wins'):
        if m.b == None:
            nomi.append('0')
            continue
        nomi.append(m.b.text)

    # Lista con ganador (1) o no (0)
    gdor = [1] + [0] * (len(tp) - 1)
    
    return tp, nomi, gdor


# ## Datos 2

# Puntuación media, número de votos, número de críticas y si es una coproducción o no.
# 
# Se puede mejorar la espera de carga de las páginas web con EC (espera de condiciones) de Selenium, para tampoco hay tantos datos que scrapear, pero la página carga muy rápido, no tiene elmentos raros y no son muchos datos a recolectar como para resultar en una demanda abusiva.

# In[50]:


def datos2():
    """
    Extrae datos adicionales a "datos1" de una segunda página de una película.

    Obtiene información sobre su puntuación, cantidad de votos, número de críticas,
    si es una coproducción y sus géneros principales. La función utiliza el controlador
    'driver' para obtener algunos elementos de la página y 'html2' para seleccionar
    géneros y verificar si es una coproducción.

    Returns:
        list: Una lista con los siguientes elementos:
            - puntuacion (str): Puntuación promedio de la película.
            - votos (str): Número total de votos recibidos por la película.
            - criticas (str): Número de críticas escritas sobre la película.
            - coproduccion (int): Indicador de coproducción (1 si es coproducción, 0 si no lo es).
            - genero (list of str): Lista de géneros principales asociados a la película.
    """
    # Puntuación promedio (Selenium)
    puntuacion = driver.find_element(By.CSS_SELECTOR, '#movie-rat-avg').text.replace(",", ".")

    # Número de votos (Selenium)
    votos = driver.find_element(By.CSS_SELECTOR, '#movie-count-rat > span').text.replace(".", "")

    # Número de críticas (Selenium)
    criticas = driver.find_element(By.CSS_SELECTOR, '#movie-reviews-box').text.split()[0]

    # Si es coproducción o no (Beautiful Soup)
    coproduccion = [1 if "Coproducción" in i.text else 0 for i in html2.select('dd.card-producer')]
    if 1 in coproduccion:
        coproduccion = 1
    else:
        coproduccion = 0
    
    # Lista de géneros principales (Beautiful Soup)
    genero = [i.text for i in html2.select('dd span[itemprop="genre"]')]
    
    return [puntuacion, votos, criticas, coproduccion, genero]


# ## Rutina principal

# Iteración sobre cada uno de los años en que se celebran los premios Goya para extraer los 2 bloques de datos

# In[51]:


# Listas iniciales
ttl, nmn, gnd, yr = [], [], [], []
dts2 = []

# Abrir Chrome y manejar cookies
driver = webdriver.Chrome()
driver.get("https://www.filmaffinity.com/es/award_data.php?award_id=goya")
manejar_cookies()

# Cargar páginas años
for ed in range(1987, 2025):
    driver.get("https://www.filmaffinity.com/es/awards.php?award_id=goya&year=" + str(ed))

    # Espera 2 segundos
    time.sleep(2)

    # Bloque 1 de datos
    html1 = BeautifulSoup(driver.page_source, 'html.parser')
    titulo, nominaciones, ganador = datos1()
    year = [ed] * len(titulo)
    
    # Unión de listas del bloque 1
    ttl.extend(titulo)
    nmn.extend(nominaciones)
    gnd.extend(ganador)
    yr.extend(year)

    # Bloque 2 de datos
    for ti in titulo:
        link = html1.find(id='goya_best_picture').parent.find(
            href=True, string=re.compile(ti.split("(")[0].strip())).get('href')
        driver.get("https://www.filmaffinity.com/es/film" + link[link.rfind("=")+1:] + ".html")
        time.sleep(2)  # Espera 2 segundos.
        html2 = BeautifulSoup(driver.page_source, 'html.parser')
        dts2.append(datos2())

# Unir datos
d = {'ganador': gnd, 'titulo': ttl, 'year': yr, 'nominaciones': nmn}
df1 = pd.DataFrame(d)
df2 = pd.DataFrame(dts2, columns=['puntuacion', 'votos', 'criticas', 'coproduccion', 'genero'])
df = df1.join(df2)

# Cerrar driver
driver.close()

# Guardar tabla de datos
df.to_csv('df_goyas_data.csv', index=False)


# # Datos Premios Feroz

# ## Generación de lista de etiquetas para ganadores y nominados

# Crear una lista de etiquetas para identificar ganadores y nominados para los diferentes premios que se vayan scrapeando.

# In[8]:


def ganador_nominado(titulos):
    """
    Crea una lista de etiquetas que identifica el primer título como "ganador" y los demás como "nominado".

    Parameters:
        titulos (list): Lista de títulos. El primer elemento es el ganador y el resto son nominados.

    Returns:
        list: Lista de etiquetas donde el primer elemento es "ganador" y el resto es "nominado".
    """
    return ["ganador"] + ["nominado"] * (len(titulos) - 1)


# ## Función de recolección de datos

# Los datos de los premios Feroz incluidos son los títulos de las películas finalistas en las categorías de drama y comedia, y si la película es ganador o nominado en cada categoría.

# In[9]:


def datos_feroz():
    """
    Extrae los títulos y el estado de ganador/nominado para las categorías de drama y comedia de los premios Feroz.

    Returns:
        tuple: Contiene cuatro listas en el siguiente orden:
            - tp_drama (list of str): Títulos de películas de tipo drama.
            - gdor_drama (list of str): Estado ('ganador' o 'nominado') de cada título en 'tp_drama'.
            - tp_comedia (list of str): Títulos de películas de tipo comedia.
            - gdor_comedia (list of str): Estado ('ganador' o 'nominado') de cada título en 'tp_comedia'.
    """
    # Búsqueda de ganadores y nominados por categoría drama
    tp_drama = [d.text.strip() for d in html1.find(id='feroz_mejor_pelicula_drama').parent.select('span.movie-title-link')]
    gdor_drama = ganador_nominado(tp_drama)

    # Búsqueda de ganadores y nominados por categoría comedia
    tp_comedia = [c.text.strip() for c in html1.find(id='feroz_mejor_comedia').parent.select('span.movie-title-link')]
    gdor_comedia = ganador_nominado(tp_comedia)

    return tp_drama, gdor_drama, tp_comedia, gdor_comedia


# ## Rutina principal Premios Feroz

# Iteración sobre cada uno de los años en que se han otorgado los premios Feroz.

# In[10]:


# Listas iniciales
drama_feroz, comedia_feroz, gs_drama, gs_comedia = [], [], [], []

# Abrir driver y manejar cookies
driver = webdriver.Chrome()
driver.get("https://www.filmaffinity.com/es/award_data.php?award_id=feroz")
manejar_cookies()

# Cargar páginas años
for ed in range(2014, 2025):
    driver.get("https://www.filmaffinity.com/es/awards.php?award_id=feroz&year=" + str(ed))

    # Espera 2 segundos
    time.sleep(2)

    # Datos Premios Feroz
    html1 = BeautifulSoup(driver.page_source, 'html.parser')
    dr_feroz, g_dr_feroz, co_feroz, g_co_feroz = datos_feroz()

    # Unión de listas Premios Feroz
    drama_feroz.extend(dr_feroz)
    comedia_feroz.extend(co_feroz)
    gs_drama.extend(g_dr_feroz)
    gs_comedia.extend(g_co_feroz)

# Cerrar driver
driver.close()


# ## Unión de datos Feroz y Goya

# Coordinación y unión de los datos de los premios Goya (obtenidos anteriormente) y Feroz.

# In[53]:


# Coordinación con Premios Goya
df = pd.read_csv('df_goyas_data.csv')
dra, com = [], []
fedrlow = [t.lower() for t in drama_feroz]
fecolow = [t.lower() for t in comedia_feroz]
for i in df.titulo.tolist():
    if i.lower() in fedrlow:
        dra.extend([gs_drama[drama_feroz.index(i)]])
    else:
        dra.extend(["no_clasificado"])
    if i.lower() in fecolow:
        com.extend([gs_comedia[comedia_feroz.index(i)]])
    else:
        com.extend(["no_clasificado"])

# Unión Premios Feroz a Premios Goya
df['feroz_drama'] = dra
df['feroz_comedia'] = com

# Guardar tabla de datos Goya + Feroz
df.to_csv('df_goyas_feroz_data.csv', index=False)


# # Datos Premios Forqué

# Se celebran en diciembre y premian a las películas del año que termina.

# ## Recolección datos Premios Forqué

# Datos de los ganadore y nominados de los Premios Forqué.

# In[13]:


def datos_forque():
    """
    Extrae los títulos de la película ganadora y las nominadas al premio Forqué a mejor película.

    A partir de un elemento beautiful soup ('html1') se realiza lo siguiente: obtiene títulos y crea
    una lista con el ganador y el resto de títulos como nominados.

    Returns:
        tuple: Una tupla con 2 listas:
            - tp (list): Lista de títulos de las películas ganadora y nominadas.
            - gdor (list): Lista de etiquetas ("ganador", "nominado") para cada película en 'tp'.
    """
    # Ganador y nominados
    tp = [d.text.strip() for d in html1.find(id='forque_best_picture').parent.select('span.movie-title-link')]
    gdor = ganador_nominado(tp)

    return tp, gdor


# ## Rutina principal Premios Forqué

# Iteración sobre cada año para obtener ganador y nominados.

# In[14]:


# Listas iniciales
ti_forque, ga_forque = [], []

# Abrir driver y manejar cookies
driver = webdriver.Chrome()
driver.get("https://www.filmaffinity.com/es/award_data.php?award_id=forque")
manejar_cookies()

# Cargar páginas años:
# La edición de los Premos Forqué del año X se celebra en diciembre del año X, y corresponde con
# la edición de los Premios Goya del año siguiente, celebrada en enero del año X+1.
for ed in range(1996, 2024):
    driver.get("https://www.filmaffinity.com/es/awards.php?award_id=forque&year=" + str(ed))

    # Espera 2 segundos
    time.sleep(2)

    # Datos Premios Feroz
    html1 = BeautifulSoup(driver.page_source, 'html.parser')
    tit_fq, gan_fq = datos_forque()

    # Unión de listas Premios Feroz
    ti_forque.extend(tit_fq)
    ga_forque.extend(gan_fq)

# Cerrar driver
driver.close()


# ## Unión de datos Forqué y dataset goyas_feroz

# Coordinación y unión del dataset anterior y los datos Forqué.

# In[55]:


# Coordinación con Premios Goya
df = pd.read_csv('df_goyas_feroz_data.csv')
fq = []
tfq = [t.lower() for t in ti_forque]
for i in df.titulo.tolist():
    if i.lower() in tfq:
        fq.extend([ga_forque[ti_forque.index(i)]])
    else:
        fq.extend(["no_clasificado"])

# Unión Premios Feroz a Premios Goya
df['forque'] = fq

# Guardar tabla de datos Goya + Feroz
df.to_csv('df_goyas_feroz_forque_data.csv', index=False)


# # Datos Premios CEC

# La página oficial de los premios CEC tiene los datos poco estructurados y más difíciles de extraer:
# 
# https://archivocine.com/index.php/premios/circulo-de-escritores-cinematograficos-cec
# 
# La alternativa es la página de los Premios CEC que hay en Wikipedia:
# 
# https://es.wikipedia.org/wiki/Anexo:Medalla_del_CEC_a_la_mejor_pel%C3%ADcula

# ## Datos desde Wikipedia

# La página de la Wikipedia no tiene elementos dinámicos, ni hay que logarse o manejar cookies, por tanto, uso requests y BeautifulSoup.
# 
# Dado que estos datos los cargo de una tacada con request no hago ninguna pausa con time.

# In[17]:


def tablas_wiki(link_wiki):
    """
    La función extrae datos de tablas en una página de Wikipedia con la clase 'wikitable'.

    Se carga una página web a través del enlace que se le pasa a la función como parámetro, luego 
    se analiza el HTML con BeautifulSoup para encontrar todas las tablas con la clase 'wikitable',
    y organiza los datos en un diccionario con encabezados fijados, que son:
    - Año
    - Ganadora
    - Director
    - Finalistas
    - Notas

    Si una tabla no contiene un encabezado específico, se agrega un valor NaN a la lista correspondiente 
    que acumula los valores de la columna.

    Parámetros:
    ----------
    link_wiki : str
        URL de la página de Wikipedia desde la cual se extraen los datos de las tablas.

    Retorna:
    --------
    dict: Un diccionario donde las claves son los encabezados fijos y los valores son listas
          que contienen los datos extraídos de las tablas. Cada lista contiene los datos
          correspondientes a cada encabezado de las tablas encontradas.
    """
    # Página parseada
    response = requests.get(link_wiki)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Cargo todas las tablas con clase 'wikitable'
    tablas = soup.find_all('table', {'class': 'wikitable'})

    # Diccionario con encabezados fijos y como valores una lista vacía
    dicc = {encabezado: [] for encabezado in ['Año', 'Ganadora', 'Director', 'Finalistas', 'Notas']}

    """TABLAS"""
    # Recorremos todas las tablas de la página
    for tabla in tablas:
        filas = tabla.find_all('tr')

        # Encabezados (primera fila de la tabla)
        encabezados_tabla = [th.text.strip() for th in filas[0].find_all('th')]

        """FILAS"""
        # Recorrer el resto de filas de la tabla (a partir de la fila de encabezado)
        for fila in filas[1:]:
            columnas = fila.find_all('td')

            """DATOS"""
            # Procesar cada encabezado en dicc
            for encabezado in dicc.keys():

                if encabezado in encabezados_tabla:  # El encabezado sí está en la tabla.
                    ind = encabezados_tabla.index(encabezado)  # Posición (columna) del encabezado en la tabla.

                    if encabezado == "Finalistas":  # Extraer cada elemento <i> como lista de nombres.
                        finalistas = [elem.text.strip() for elem in columnas[ind].find_all('i')]
                        dicc["Finalistas"].append(finalistas)

                    else:  # Extraer el texto normalmente para otras columnas
                        dicc[encabezado].append(columnas[ind].text.strip())

                else:  # Se pone un nan si la tabla no tiene un encabezado concreto.
                    dicc[encabezado].append(np.nan)

    return dicc


# ## Rutinas principal Premios CEC

# Se pasa el link de los premios CEC en la wikipedia y se descargan todos los datos de las tablas. Se devuelve un diccionario.

# In[18]:


# URL de Wikipedia con los premios CEC
url_cec = 'https://es.wikipedia.org/wiki/Anexo:Medalla_del_CEC_a_la_mejor_pel%C3%ADcula'

# Obtengo todas las ediciones de los Premios CEC
cec_dicc = tablas_wiki (url_cec)


# ## Unión de datos CEC y el dataset goyas_feroz_forque

# Coordinación y unión de los datos almacenados hasta ahora y los datos de los premios CEC.

# In[57]:


# Coordinación y unión con dataset anterior

# Dataset hasta ahora
df = pd.read_csv('df_goyas_feroz_forque_data.csv')

# Lista de películas CEC ganadoras
cec_win = [w.lower() for w in cec_dicc['Ganadora']]

# Lista de películas CEC nominadas. Evitando añadir 'nan' controlando si es una lista.
cec_nom = []
for nominadas in cec_dicc['Finalistas']:
    if isinstance(nominadas, list):
        cec_nom.extend([n.lower() for n in nominadas])

# Lista para la columna del dataframe
cec_col = []

for i in df.titulo.tolist():
    if i.lower() in cec_win:
        cec_col.append('ganador')
    elif i.lower() in cec_nom:
        cec_col.append('nominado')
    else:
        cec_col.append('no_clasificado')

# Unión Premios CEC a Premios Goya
df['cec'] = cec_col

# Guardar tabla de datos Goya + CEC
df.to_csv('df_goyas_feroz_forque_cec_data.csv', index=False)


# # User Agent y otros comentarios

# ## User agent en Selenium

# Referencias para el código:
# 
# https://developer.mozilla.org/es/docs/Web/HTTP/Headers/User-Agent
# 
# https://www.tutorialspoint.com/how-to-get-useragent-information-in-selenium-web-driver

# In[59]:


# Utilizo una página web cualquiera ya que el user agent no va a cambiar y no he utilizado
# diferentes user agent para este scraping.
driver = webdriver.Chrome()
driver.get("https://www.dataschool.io/")
time.sleep(5)

# Ejecuto un script en la consola de JavaScript para obtener el User-Agent
user_agent1 = driver.execute_script("return navigator.userAgent")
print("User-Agent utilizado: ", user_agent1)

driver.close()


# ## Navegación sin cabecera (headless)

# Esto se puede encontrar en la documentación de Selenium o en este vídedo:
# 
# https://www.youtube.com/watch?app=desktop&v=DK51epkLHZk

# In[60]:


# Importación de opciones para quitar navegador
from selenium.webdriver.chrome.options import Options

# Configuración para ejecutar el navegador en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Obtengo de web y espera de carga
driver.get("https://www.filmaffinity.com/es/award_data.php?award_id=goya")
time.sleep(5)

# Ejecuto un script en la consola de JavaScript para obtener el User-Agent
user_agent2 = driver.execute_script("return navigator.userAgent")
print("User-Agent utilizado: ", user_agent2)

driver.close()


# ## User agent en requests

# Información aquí:
# 
# https://realpython.com/python-requests/
# 
# https://stackoverflow.com/questions/10606133/sending-user-agent-using-requests-library-in-python

# In[61]:


# Página parseada
response = requests.get("https://es.wikipedia.org/wiki/Anexo:Medalla_del_CEC_a_la_mejor_pel%C3%ADcula")

user_agent = response.request.headers['User-Agent']
print("User-Agent utilizado: ", user_agent)

