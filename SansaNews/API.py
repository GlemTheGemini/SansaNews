from instaloader import Instaloader, Profile
from .iniciativas import INICIATIVAS
import os
import json

MAX_PUBLICACIONES = 20

def actualizar_publicaciones(iniciativa):
    LOADER = Instaloader(post_metadata_txt_pattern="", compress_json=False, dirname_pattern=(os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/{iniciativa}"))

    #Descargamos los archivos necesarios de los usuarios que se encuentran en el archivo señalado
    perfil = Profile.from_username(LOADER.context, iniciativa)
    publicaciones = perfil.get_posts()
    LOADER.posts_download_loop(publicaciones, iniciativa, fast_update=True, max_count=(MAX_PUBLICACIONES + 1))

def actualizar_perfil(iniciativa):
    LOADER = Instaloader(post_metadata_txt_pattern="", compress_json=False, dirname_pattern=(os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/icons"))
    perfil = Profile.from_username(LOADER.context, iniciativa)

    # Descargar foto de perfil de iniciativa
    LOADER.context.get_and_write_raw(perfil.profile_pic_url, f"static/iniciativas/icons/{iniciativa}.jpg")

    # Actualizar biografía
    return perfil.biography


def leer_archivo_json(ruta_archivo):
    #Lee un archivo JSON y retorna el texto en el campo "edge_media_to_caption" de la primera publicación.

    with open(ruta_archivo) as archivo_json:
        data = json.load(archivo_json)
        if "edge_media_to_caption" in data['node'] and len(data['node']["edge_media_to_caption"]["edges"]) > 0:
            return data['node']["edge_media_to_caption"]["edges"][0]['node']['text']
        else:
            return ""

def contenido(iniciativa):

    #Retorna una lista de hasta 20 publicaciones (como máximo) de la página especificada.
    #Cada publicación es una lista de imágenes (hasta 10 imágenes) y una descripción (opcional).
    #Solo se incluyen las 2 publicaciones más recientes.

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
