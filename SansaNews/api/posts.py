import os
from urllib import request
from instagrapi import Client
from . import iniciativa as api_iniciativa

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
                post["media"].append(media_path)
                index += 1

        # Añadir post al diccionario de la iniciativa
        iniciativa["posts"][str(datetime)] = post
        count += 1

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
