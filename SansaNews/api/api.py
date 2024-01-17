import json, os
from urllib import request
from enum import Enum
from instagrapi import Client

MAX_POSTS = 5
DIRECTORIO = os.path.join(os.path.dirname(__file__), "iniciativas")

class TipoIniciativa(Enum):
    '''
    Enum para clasificar las iniciativas según su tipo
    '''
    CENTRO = "Centro de Estudiantes"
    DEPORTE = "Deportes"
    RECREACION = "Recreación"
    RED = "Redes Oficiales"

def escanear_iniciativas() -> dict:
    '''
    Escanea "$DIRECTORIO/iniciativas.json" y carga las iniciativas en un 
    diccionario.

    Returns:
        dict: diccionario de iniciativas
    '''
    json_path: str = os.path.join(DIRECTORIO, "iniciativas.json")

    with open(json_path, "r", encoding="utf8") as iniciativas_json:
        print(f"Cargando lista de iniciativas desde {json_path}")
        iniciativas: dict = json.load(iniciativas_json)
        return iniciativas


def guardar_iniciativa(iniciativa: dict):
    '''
    Guarda el diccionario de la iniciativa en su json respectivo.

    Args:
        iniciativa (dict): diccionario con la información de la iniciativa
        path (str): carpeta donde guardar el json
    '''
    usuario: str = iniciativa["usuario"]
    json_path: str = os.path.join(DIRECTORIO, f"{usuario}/{usuario}.json")

    with open(json_path, "w", encoding="utf8") as iniciativa_json:
        print(f"[API]: Guardando información en {json_path}...")
        json.dump(iniciativa, iniciativa_json, ensure_ascii=False, indent="\t")

    print(f"[API]: Iniciativa {iniciativa['usuario']} guardada en {json_path}")


def cargar_iniciativa(usuario: str) -> dict:
    '''
    Carga el json que contiene la información del usuario dado.

    Args:
        usuario (str): nombre de usuario de la iniciativa en instagram

    Returns:
        dict: diccionario con la información de la iniciativa
    '''
    json_path: str = os.path.join(DIRECTORIO, f"{usuario}/{usuario}.json")

    with open(json_path, "r", encoding="utf8") as iniciativa_json:
        print(f"[API]: Cargando información de {json_path}...")
        iniciativa: dict = json.load(iniciativa_json)

    print(f"[API]: Información de la iniciativa {usuario} cargada")
    return iniciativa



def crear_iniciativa(client: Client, usuario: str, nombre: str, 
                     tipo: TipoIniciativa, slider: bool) -> dict:
    '''
    Inicializa una nueva iniciativa en el sistema, creando su carpeta,
    descargando su foto de perfil y obteniendo los datos necesarios para luego
    guardarlos en su json específico

    Args:
        client (Client): cliente de instagrapi
        usuario (str): nombre de usuario de la iniciativa
        nombre (str): nombre a mostrar en la página
        tipo (TipoIniciativa): tipo de iniciativa
        slider (bool): si la iniciativa aparecera en el slider

    Returns:
        dict: diccionario con la información de la iniciativa
    '''
    iniciativa = {
        "usuario": usuario,
        "id": 0,
        "biografia": "",
        "nombre": nombre,
        "tipo": tipo,
        "slider": slider,
        "posts": {},
    }

    # Guardar información de la iniciativa
    try:
        print(f"[API]: Adquiriendo información de {usuario}...")
        iniciativa_data: dict = client.user_info_by_username(usuario).model_dump()
    except:
        print(f"[ERROR]: No se pudo obtener la información de {usuario}")
        return iniciativa

    iniciativa["id"] = iniciativa_data["pk"]
    iniciativa["biografia"] = iniciativa_data["biography"]

    # Crear carpeta
    iniciativa_path: str = os.path.join(DIRECTORIO, usuario)
    try:
        os.mkdir(iniciativa_path)
    except:
        print(f"[Error]: No se pudo crear la carpeta {iniciativa_path}")
        return iniciativa

    # Descargar foto de perfil
    pic_url = str(iniciativa_data['profile_pic_url'])
    pic_path: str = os.path.join(iniciativa_path, f"{usuario}.jpg")

    print(f"[API]: Descargando foto de perfil en {pic_url}...")
    request.urlretrieve(pic_url, pic_path)

    guardar_iniciativa(iniciativa)
    return iniciativa


def descargar_posts(iniciativa: dict, posts: list, cantidad: int) -> dict:
    '''
    Descarga los posts más recientes de una iniciativa

    Args:
        iniciativa (dict): diccionario con la información de la iniciativa
        posts (list): lista de posts que da instragrapi
        cantidad (int): cantidad de posts a descargar

    Returns:
        dict: diccionario actualizado con la información de la iniciativa
    '''
    iniciativa_path: str = os.path.join(DIRECTORIO, iniciativa["usuario"])

    count = 0
    for post in posts:
        if count >= cantidad:
            break

        # Obtener datos del post
        post_data: dict = post.model_dump()
        datetime = int(post_data["taken_at"].timestamp())
        print(f"[API] Descargando post publicado en {datetime}...")

        # Crear carpeta de post
        post_folder: str = os.path.join(iniciativa_path, str(datetime))
        try:
            os.mkdir(post_folder)
        except:
            print(f"[ERROR]: No se pudo crear la carpeta del post {datetime}")
            continue

        post = {
            "descripcion": post_data["caption_text"],
            "media": []
        }

        # En caso de haber una sola imagen
        if len(post_data["resources"]) == 0:
            media_path: str = os.path.join(post_folder, f"{datetime}_0.jpg")
            media_url = str(post_data['thumbnail_url'])

            # Descargar imagen
            print(f"[API]: Descargando media {media_url}...")
            request.urlretrieve(media_url, media_path)

            # Añadir media al post
            post["media"].append(media_path)
            iniciativa["posts"][str(datetime)] = post
            continue

        # En caso de haber multiples imagenes
        index = 0
        for media in post_data["resources"]:
            media_path: str = os.path.join(post_folder, f"{datetime}_{index}.jpg")
            media_url = str(media['thumbnail_url'])

            # Descargar imagen
            print(f"[API]: Descargando media {media_url}...")
            request.urlretrieve(media_url, media_path)

            # Añadir media al post
            post["media"].append(media_path)
            index += 1

        # Añadir post al diccionario de la iniciativa
        iniciativa["posts"][str(datetime)] = post
        count += 1

    usuario: str = iniciativa["usuario"]
    print(f"[API]: Descarga de posts de la iniciativa {usuario} finalizada")
    return iniciativa


def limpiar_posts(iniciativa: dict, max_posts: int = MAX_POSTS) -> dict:
    '''
    Elimina los posts de una iniciativa en caso de que la iniciativa supere
    la cantidad de posts máximos

    Args:
        iniciativa (dict): diccionario con la información de la iniciativa
        max_posts (int): cantidad máxima de posts que puede tener una iniciativa
            descargados a la vez

    Returns:
        dict: diccionario con la información de la iniciativa actualizada
    '''
    usuario: str = iniciativa["usuario"]
    if len(iniciativa["posts"].keys()) <= MAX_POSTS:
        print(f"[API]: {usuario} no excede el límite de posts")
        return iniciativa

    iniciativa_path: str = os.path.join(DIRECTORIO, usuario)
    posts: list = os.listdir(iniciativa_path)
    posts.remove(f"{usuario}.json")
    posts.remove(f"{usuario}.jpg")
    posts.sort(reverse = True)

    # Eliminar posts
    print(f"[API]: Eliminando posts antiguos de {usuario}...")
    for post in posts:
        if len(posts) <= max_posts:
            break

        post_path: str = os.path.join(iniciativa_path, post)
        print(f"[API]: Eliminando post {post_path}...")
        medias: list = os.listdir(post_path)

        # Eliminar archivos
        for media in medias:
            os.remove(os.path.join(post_path, media))

        # Eliminar carpeta
        os.rmdir(post_path)

        iniciativa["posts"].pop(post)
        posts.remove(post)

    print(f"[API]: Posts de {usuario} limpiados con exito")
    return iniciativa


def actualizar_iniciativa(client: Client, usuario: str) -> dict:
    '''
    Actualiza los posts de la iniciativa dada, descargando los más nuevos
    e eliminando los más viejos si se llegara a sobrepasar el limite de posts

    Args:
        client (Client): cliente de instragrapi
        usuario: usuario de instagram de la iniciativa

    Returns:
        dict: iniciativa actualizada
    '''
    print(f"[API]: Verificando si {usuario} posee nuevos posts...")
    iniciativa: dict = cargar_iniciativa(usuario)

    try:
        raw_posts: list = client.user_medias(iniciativa["id"], MAX_POSTS)
    except:
        print(f"[ERROR]: No se pudo obtener la información de {usuario}")
        return iniciativa

    # Determinar si hay posts nuevos mediante la fecha de subida
    posts: dict = iniciativa["posts"]
    if len(posts) == 0:
        current_update = 0
    else:
        current_update: int = list(posts.keys())[0]

    last_update = int(raw_posts[0].model_dump()["taken_at"].timestamp())
    if last_update <= current_update:
        print(f"[API]: {usuario} no posee nuevos posts")
        return iniciativa

    # Contar cantidad de posts nuevos para posterior descarga
    cantidad = 0
    for raw_post in raw_posts:
        post: dict = raw_post.model_dump()
        if post["taken_at"].timestamp() <= current_update:
            break

        cantidad += 1

    print(f"[API]: {usuario} tiene {cantidad} nuevos posts")
    iniciativa: dict = descargar_posts(iniciativa, raw_posts, cantidad)

    iniciativa: dict = limpiar_posts(iniciativa)
    guardar_iniciativa(iniciativa)
    print(f"[API]: Iniciativa {usuario} actualizada con exito")
    return iniciativa

