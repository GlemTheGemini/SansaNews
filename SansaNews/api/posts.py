"""Modulo encargado del manejo de posts, descarga, redescarga, limpieza, etc."""
# pylint: disable=E0401

import os
import json
from urllib import request
from instagrapi import Client
from . import iniciativa as api_iniciativa

def cargar(directorio: str) -> dict:
    '''
    Carga las publicaciones más recientes desde "directorio/posts.json"

    Args:
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario con los posts ordenados por los más recientes
    '''
    recientes_path = os.path.join(directorio, "posts.json")

    print(f"[API]: Cargando {recientes_path}...")
    with open(recientes_path, "r", encoding="utf8") as recientes_json:
        recientes = json.load(recientes_json)

    return recientes


def guardar(recientes: dict, directorio: str):
    '''
    Guarda las publicaciones más recientes a "directorio/posts.json"

    Args:
        directorio (str): directorio de iniciativas
    '''
    recientes_path = os.path.join(directorio, "posts.json")

    print(f"[API]: Guardando recientes en {recientes_path}...")
    with open(recientes_path, "w", encoding="utf8") as recientes_json:
        json.dump(recientes, recientes_json, ensure_ascii=False, indent="\t", sort_keys=True)


def descargar(iniciativa: dict, posts: list, cantidad: int,
                    directorio: str) -> dict:
    '''
    Descarga los posts más recientes de una iniciativa

    Args:
        iniciativa (dict): diccionario con la información de la iniciativa
        posts (list): lista de posts que da instragrapi
        cantidad (int): cantidad de posts a descargar
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario actualizado con la información de la iniciativa
    '''
    iniciativa_path: str = os.path.join(directorio, iniciativa["usuario"])
    posts_json: dict = cargar(directorio)

    count = 0
    for post in posts:
        if count >= cantidad:
            break

        # Obtener datos del post
        post_data: dict = post.model_dump()
        datetime = str(int(post_data["taken_at"].timestamp()))
        print(f"[API] Descargando post publicado en {datetime}...")

        # Crear carpeta de post
        post_folder: str = os.path.join(iniciativa_path, datetime)
        try:
            os.mkdir(post_folder)
        except (FileExistsError, FileNotFoundError):
            print(f"[ERROR]: No se pudo crear la carpeta {post_folder}")
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

            post["media"].append(f"{datetime}_0.jpg")

        # En caso de haber multiples imagenes
        else:
            index = 0
            for media in post_data["resources"]:
                media_path: str = os.path.join(post_folder, f"{datetime}_{index}.jpg")
                media_url = str(media['thumbnail_url'])

                # Descargar imagen
                print(f"[API]: Descargando media {media_url}...")
                request.urlretrieve(media_url, media_path)

                # Añadir media al post
                post["media"].append(f"{datetime}_{index}.jpg")
                index += 1

        # Añadir post a lista de posts
        posts_json[datetime] = {
            "descripcion": post["descripcion"],
            "usuario": iniciativa["usuario"],
            "slider": iniciativa["slider"]
        }

        # Añadir post al diccionario de la iniciativa
        iniciativa["posts"][str(datetime)] = post
        count += 1

    guardar(posts_json, directorio)

    usuario: str = iniciativa["usuario"]
    print(f"[API]: Descarga de posts de la iniciativa {usuario} finalizada")
    return iniciativa


def redescargar(client: Client, usuario: str, max_posts: int,
                directorio: str) -> dict:
    '''
    Fuerza la redescarga de los posts del usuario dado, borrando todos los
    posts previamente descargados y descargandolos de nuevo
    
    Args:
        client (Client): cliente de instagrapi
        usuario (str): usuario de instagram al que redescargar los posts
        max_posts (int): cantidad máxima de posts de la iniciativa
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario con la información de la iniciativa
    '''
    print(f"[DEBUG]: Redescargando posts de {usuario}")

    iniciativa: dict = api_iniciativa.cargar(usuario, directorio)
    limpiar(iniciativa, 99999, directorio)
    iniciativa = api_iniciativa.actualizar(client, usuario, max_posts,
                                           directorio)

    print(f"[DEBUG]: Posts de {usuario} redescargados con exito")
    return iniciativa


def limpiar(iniciativa: dict, max_posts: int, directorio: str) -> dict:
    '''
    Elimina los posts de una iniciativa en caso de que la iniciativa supere
    la cantidad de posts máximos

    Args:
        iniciativa (dict): diccionario con la información de la iniciativa
        max_posts (int): cantidad máxima de posts que puede tener una iniciativa
            descargados a la vez
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario con la información de la iniciativa actualizada
    '''
    usuario: str = iniciativa["usuario"]
    if len(iniciativa["posts"].keys()) <= max_posts:
        print(f"[API]: {usuario} no excede el límite de posts")
        return iniciativa

    iniciativa_path: str = os.path.join(directorio, usuario)
    posts: list = os.listdir(iniciativa_path)
    posts.remove(f"{usuario}.json")
    posts.remove(f"{usuario}.jpg")
    posts.sort(reverse = True)

    posts_json: dict = cargar(directorio)

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
        posts_json.pop(post)
        posts.remove(post)

    guardar(posts_json, directorio)

    print(f"[API]: Posts de {usuario} limpiados con exito")
    return iniciativa


def ultimos(cantidad: int, directorio: str, fecha_limite: int = 0,
            slider: bool = False) -> dict:
    '''
    Obtiene todos los posts más recientes, filtrandolos según los parametros
    indicados

    Args:
        cantidad (int): cantidad máxima de posts
        directorio (str): directorio donde se encuentran las publicaciones
            recientes
        fecha_limite (int): fecha limite máxima de un posts
        slider (bool): si los posts deben de estar en el slider

    Returns:
        list: lista con los posts publicados despues de la fecha dada
    '''
    posts = cargar(directorio)

    print("[API]: Cargando los posts más recientes...")
    posts_filtrados = {}
    count = 0
    for fecha, data in posts.items():
        if count >= cantidad or int(fecha) < fecha_limite:
            break
        if slider and not data["slider"]:
            continue

        print(f"[API]: Cargando post {fecha} de {data['usuario']}")
        posts_filtrados[fecha] = data
        count += 1

    print(f"[API]: Los {count} posts más recientes han sido cargados")
    return posts_filtrados
