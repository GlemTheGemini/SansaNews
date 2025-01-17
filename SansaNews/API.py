from instaloader import Instaloader, Profile
from .iniciativas import INICIATIVAS
import os
import json

MAX_PUBLICACIONES = 20


"""
Resumen Función:
    La funcion descarga las ultimas 20 publicaciones más recientes de una pagina de instagram.
    Si ya existen archivos descargados de esta página entonces se descargan las publicaciones más nuevas
    y se agregan a las ya existentes.

Input: 
    Recibe como parametro un string con el usuario de instagram

Returns:
    No retorna valores
"""
def actualizar_publicaciones(iniciativa):
    LOADER = Instaloader(post_metadata_txt_pattern="", compress_json=False, dirname_pattern=(os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/{iniciativa}"))

    #Descargamos los archivos necesarios de los usuarios que se encuentran en el archivo señalado
    perfil = Profile.from_username(LOADER.context, iniciativa)
    publicaciones = perfil.get_posts()
    LOADER.posts_download_loop(publicaciones, iniciativa, fast_update=True, max_count=(MAX_PUBLICACIONES + 1))


"""
Resumen Función:
    La funcion actualiza la foto de perfil de la pagina que se le entregue dentro de los archivos de iconos, y su biografia. 

Input: 
    Recibe como parametro un string con el usuario de instagram

Returns:
    retorna la biografia de una pagina de instagram

"""
def actualizar_perfil(iniciativa):
    LOADER = Instaloader(post_metadata_txt_pattern="", compress_json=False, dirname_pattern=(os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/icons"))
    perfil = Profile.from_username(LOADER.context, iniciativa)

    # Descargar foto de perfil de iniciativa
    LOADER.context.get_and_write_raw(perfil.profile_pic_url, f"static/iniciativas/icons/{iniciativa}.jpg")

    # Actualizar biografía
    return perfil.biography


"""
Resumen Función:
    La funcion revisa dentro del archivo json que contiene la informacion de un post de instagram
    del que se desea extraer la descripcion. 

Input: 
    Recibe como parametro la ruta del archivo json.

Returns:
    retorna un string que contiene la descripcion del post si es que existe, sino retorna un string vacio 

"""
def leer_archivo_json(ruta_archivo):
    #Lee un archivo JSON y retorna el texto en el campo "edge_media_to_caption" de la primera publicación.

    with open(ruta_archivo) as archivo_json:
        data = json.load(archivo_json)
        if "edge_media_to_caption" in data['node'] and len(data['node']["edge_media_to_caption"]["edges"]) > 0:
            return data['node']["edge_media_to_caption"]["edges"][0]['node']['text']
        else:
            return ""


"""
Input: 
    Recibe como parametro un string con el usuario de instagram

#Retorna una lista de hasta 20 publicaciones (como máximo) de la página especificada.
#Cada publicación es una lista de imágenes (hasta 10 imágenes) y una descripción (opcional).
#Solo se incluyen las 2 publicaciones más recientes.
"""
def contenido(iniciativa):

    publicaciones = []
    directorio = os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/{iniciativa}"
    archivos = sorted(os.listdir(directorio))
    publicacion_actual = None
    imagenes = []
    descripciones = []

    # Recorre los archivos del directorio
    for archivo in archivos:
        # Si el archivo pertenece a una nueva publicación, agrega la anterior a la lista
        if publicacion_actual is None or not archivo.startswith(publicacion_actual):
            if imagenes:
                publicaciones.append([imagenes, descripciones])
                descripciones = []
                imagenes = []

            publicacion_actual = archivo[:24]

        # Si el archivo es una imagen, agrega su ruta a la lista de imágenes
        if archivo.endswith(".jpg"):
            imagenes.append(f"iniciativas/{iniciativa}/{archivo}")
        # Si el archivo es un JSON, lee su descripción y la agrega a la lista de descripciones
        elif archivo.endswith(".json"):
            descripcion = leer_archivo_json(os.path.join(directorio, archivo))
            descripciones.append(descripcion)

    # Agrega la última publicación a la lista (si existe)
    if imagenes:
        publicaciones.append([imagenes, descripciones])

    # Obtiene las 15 publicaciones más recientes, y las convierte a la lista de formato deseado
    formatted_publicaciones = []
    for publicacion in publicaciones[::-1][:14]:
        imagenes = [imagen for imagen in publicacion[0] if imagen.endswith(".jpg")]
        descripcion = publicacion[1][0] if publicacion[1] else ""
        formatted_publicaciones.append(imagenes + [descripcion])

    return formatted_publicaciones


"""
Resumen Función:
    La funcion recorre todas las publicaciones de todas las iniciativas y las ordena por fecha.

Input: 
    No recibe parametros

Returns:
    retorna una lista con las 4 publicaciones mas recientes de todas las iniciativas de la pagina
"""
def recientes():
    # Diccionario para almacenar la información de las publicaciones
    iniciativas = {}
    for iniciativa in INICIATIVAS:
        # Agregar información de primera y última publicación al diccionario
        iniciativas[iniciativa] = [contenido(iniciativa)[0][0], contenido(iniciativa)[0][-1]]
    # Lista de fechas y descripciones de publicaciones
    fechas = []
    for iniciativa in iniciativas:
        # Agregar fecha y descripción de cada publicación a la lista
        fecha = [iniciativas[iniciativa][0].split("/")[-1], iniciativas[iniciativa][-1][:150] + "..."]
        fechas.append([fecha, iniciativa])

    # Ordenar la lista por fecha, de más reciente a menos reciente
    fechas.sort(reverse=True)

    # Seleccionar las últimas 4 publicaciones de la lista
    fechas = fechas[:4]

    # Variables para generar el ID de cada publicación
    directorio = "\\{}\\{}"
    id = "wows1_{}"

    # Lista para almacenar la información de las nuevas publicaciones
    publicaciones_recientes = []
    for index, (fecha, iniciativa) in enumerate(fechas):
        # Agregar la información de la publicación a la lista, incluyendo el ID generado
        publicacion = {
            "pagina": iniciativa,
            "imagen": directorio.format(f"iniciativas/{iniciativa}", fecha[0]),
            "descripcion": fecha[-1],
            "id": id.format(index)
        }
        publicaciones_recientes.append(publicacion)

    # Devolver la lista de nuevas publicaciones
    return publicaciones_recientes

"""
Resumen Función:
    Limpia las iniciativas que ya no esten en iniciativas.py y borra las publicaciones más antiguas
    si supera el limite de publicaciones (MAX_PUBLICACIONES).
"""
def cleanup():
    # Obtener lista de carpetas en iniciativas
    carpetas = os.listdir(os.path.dirname("__file__") + "static/iniciativas")

    # Remueve las carpetas que no son iniciativas
    carpetas.remove("biografias.json")
    carpetas.remove("icons")

    # Loop principal de borrado
    for carpeta in carpetas:
        # Obtener los archivos de la carpeta
        archivos = os.listdir(os.path.dirname("__file__") + f"static/iniciativas/{carpeta}")

        # Remueve las iniciativas que ya no se encuentren en iniciativas.py
        if carpeta not in INICIATIVAS.keys():
            for archivo in archivos:
                os.remove(os.path.dirname("__file__") + f"static/iniciativas/{carpeta}/{archivo}")

            os.rmdir(os.path.dirname("__file__") + f"static/iniciativas/{carpeta}")
            continue

        # Reorganizar archivos para mantener los más recientes
        archivos.sort()
        archivos.reverse()

        exclude = "$"
        cont = 0
        for archivo in archivos:
            # Ignorar las primeras MAX_PUBLICACIONES de cada iniciativa
            if cont >= MAX_PUBLICACIONES:
                if exclude not in archivo:
                    os.remove(os.path.dirname("__file__") + f"static/iniciativas/{carpeta}/{archivo}")
                continue

            # Actualizar contador de publicaciones a ignorar
            if ".json" in archivo:
                cont += 1

                # Ignorar los archivos relacionados con la ultima publicacion más reciente
                if cont == MAX_PUBLICACIONES:
                    exclude = archivo[:-5]
