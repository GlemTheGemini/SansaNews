#Importar los modulos a usar y ponemos el contexto.
from instaloader import instaloader, Profile
import os
import json

def actualizar(pagina):
    L = instaloader.Instaloader(post_metadata_txt_pattern="",compress_json=False,dirname_pattern=(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\static\\"+ "{}\\").format(pagina))
    #Descargamos los archivos necesarios de los usuarios que se encuentran en el archivo señalado
    perfil = Profile.from_username(L.context, pagina)
    publicaciones = perfil.get_posts()
    L.posts_download_loop(publicaciones,pagina,fast_update=True, max_count=21)
    return()

def actualizar_2():
    lista_paginas = ["ergon_usm","gbu_usm", "fablab_utfsm", "ceeinf_sj", "geekusm", "movimiento.0", "primos_usmsj", "rocketscience_usm",
                    "usm.cubesat.team", "xumbra_utfsm", "yotecuidousm"]
    for pagina in lista_paginas:
        actualizar(pagina)
    return 0


def leer_archivo_json(ruta_archivo):

    #Lee un archivo JSON y retorna el texto en el campo "edge_media_to_caption" de la primera publicación.
    #Si el campo no existe o está vacío, retorna una cadena vacía.

    with open(ruta_archivo) as archivo_json:
        data = json.load(archivo_json)
        if "edge_media_to_caption" in data['node'] and len(data['node']["edge_media_to_caption"]["edges"]) > 0:
            return data['node']["edge_media_to_caption"]["edges"][0]['node']['text']
        else:
            return ""

def contenido(pagina):

    #Retorna una lista de hasta 20 publicaciones (como máximo) de la página especificada.
    #Cada publicación es una lista de imágenes (hasta 10 imágenes) y una descripción (opcional).
    #Solo se incluyen las 2 publicaciones más recientes.

    lista = []
    # Obtiene la ruta absoluta del directorio "static/pagina"
    directorio = os.path.abspath(os.path.join(__file__, "..", "..", "static", pagina))
    contenido_in_carpeta = sorted(os.listdir(directorio))
    publicacion_actual = None
    lista_multi_imagenes = []
    lista_descripción = []

    # Recorre los archivos del directorio
    for file in contenido_in_carpeta:
        # Si el archivo pertenece a una nueva publicación, agrega la anterior a la lista
        if publicacion_actual is None or not file.startswith(publicacion_actual):
            if lista_multi_imagenes:
                lista_publicación = [lista_multi_imagenes, lista_descripción]
                lista.append(lista_publicación)
                lista_descripción = []
                lista_multi_imagenes = []

            publicacion_actual = file[:24]

        # Si el archivo es una imagen, agrega su ruta a la lista de imágenes
        if file.endswith(".jpg"):
            lista_multi_imagenes.append(f"{pagina}/{file}")
        # Si el archivo es un JSON, lee su descripción y la agrega a la lista de descripciones
        elif file.endswith(".json"):
            descripcion = leer_archivo_json(os.path.join(directorio, file))
            lista_descripción.append(descripcion)

    # Agrega la última publicación a la lista (si existe)
    if lista_multi_imagenes:
        lista_publicación = [lista_multi_imagenes, lista_descripción]
        lista.append(lista_publicación)

    # Obtiene las 15 publicaciones más recientes, y las convierte a la lista de formato deseado
    lista_4 = []
    for publicacion in lista[::-1][:14]:
        imagenes = [imagen for imagen in publicacion[0] if imagen.endswith(".jpg")]
        descripcion = publicacion[1][0] if publicacion[1] else ""
        lista_4.append(imagenes + [descripcion])

    # Retorna la lista de publicaciones
    return lista_4


def recientes():
    # Lista de nombres de páginas web
    lista_paginas = ["sansanews", "ergon_usm", "gbu_usm", "fablab_utfsm", "ceeinf_sj", "geekusm", "movimiento.0",
                    "primos_usmsj", "rocketscience_usm", "usm.cubesat.team", "xumbra_utfsm", "yotecuidousm"]

    # Diccionario para almacenar la información de las publicaciones
    diccionario = {}
    for pagina in lista_paginas:
        # Agregar información de primera y última publicación al diccionario
        diccionario[pagina] = [contenido(pagina)[0][0], contenido(pagina)[0][-1]]
    # Lista de fechas y descripciones de publicaciones
    lista_fechas = []
    for llave in diccionario:
        # Agregar fecha y descripción de cada publicación a la lista
        fecha_desc = [diccionario[llave][0].split("/")[-1], diccionario[llave][-1][:150] + "..."]
        lista_fechas.append([fecha_desc, llave])

    # Ordenar la lista por fecha, de más reciente a menos reciente
    lista_fechas.sort(reverse=True)

    # Seleccionar las últimas 4 publicaciones de la lista
    lista_fechas = lista_fechas[:4]

    # Variables para generar el ID de cada publicación
    directorio = "\\{}\\{}"
    id = "wows1_{}"

    # Lista para almacenar la información de las nuevas publicaciones
    lista_nuevas_publicaciones = []
    for i, (fecha_desc, pagina) in enumerate(lista_fechas):
        # Agregar la información de la publicación a la lista, incluyendo el ID generado
        nueva_publicacion = {
            "pagina": pagina,
            "imagen": directorio.format(pagina, fecha_desc[0]),
            "descripcion": fecha_desc[-1],
            "id": id.format(i)
        }
        lista_nuevas_publicaciones.append(nueva_publicacion)

    # Devolver la lista de nuevas publicaciones
    return lista_nuevas_publicaciones
