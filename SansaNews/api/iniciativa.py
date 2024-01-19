"""
Modulo encargado de manejar las iniciativas, crear los json respectivos,
guardarlos cargar la información, actualizar las iniciativas, etc.
"""
#pylint: disable=E0401, W0702

import json
import os
from urllib import request
from enum import Enum
from instagrapi import Client
from . import posts as api_posts

class TipoIniciativa(Enum):
    '''
    Enum para clasificar las iniciativas según su tipo
    '''
    CENTRO = "Centro de Estudiantes"
    DEPORTE = "Deportes"
    RECREACION = "Recreación"
    RED = "Redes Oficiales"


def escanear(directorio: str) -> dict:
    '''
    Escanea "$DIRECTORIO/iniciativas.json" y carga las iniciativas en un 
    diccionario.

    Args:
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario de iniciativas
    '''
    json_path: str = os.path.join(directorio, "iniciativas.json")

    with open(json_path, "r", encoding="utf8") as iniciativas_json:
        print(f"[API]: Cargando lista de iniciativas desde {json_path}")
        iniciativas: dict = json.load(iniciativas_json)
        return iniciativas


def guardar(usuario: str, data: dict, directorio: str):
    '''
    Guarda el diccionario de la iniciativa en su json respectivo.

    Args:
        usuario (str): usuario de instagram de la iniciativa
        iniciativa (dict): diccionario con la información de la iniciativa
        directorio (str): carpeta donde guardar el json
    '''
    json_path: str = os.path.join(directorio, f"{usuario}/{usuario}.json")

    with open(json_path, "w", encoding="utf8") as iniciativa_json:
        print(f"[API]: Guardando información en {json_path}...")
        json.dump(data, iniciativa_json, ensure_ascii=False, indent="\t")

    print(f"[API]: Iniciativa {usuario} guardada en {json_path}")


def cargar(usuario: str, directorio: str) -> dict:
    '''
    Carga el json que contiene la información del usuario dado.

    Args:
        usuario (str): nombre de usuario de la iniciativa en instagram
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario con la información de la iniciativa
    '''
    json_path: str = os.path.join(directorio, f"{usuario}/{usuario}.json")

    with open(json_path, "r", encoding="utf8") as iniciativa_json:
        print(f"[API]: Cargando información de {json_path}...")
        iniciativa: dict = json.load(iniciativa_json)

    print(f"[API]: Información de la iniciativa {usuario} cargada")
    return iniciativa


def crear(client: Client, usuario: str, data: dict, directorio: str) -> dict:
    '''
    Inicializa una nueva iniciativa en el sistema, creando su carpeta,
    descargando su foto de perfil y obteniendo los datos necesarios para luego
    guardarlos en su json específico

    Args:
        client (Client): cliente de instagrapi
        usuario (str): nombre de usuario de la iniciativa
        data (dict): diccionario que contenga el nombre, el tipo y si es parte
            del slider de la iniciativa
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario con la información de la iniciativa
    '''
    iniciativa = {
        "usuario": usuario,
        "id": 0,
        "biografia": "",
        "nombre": data["nombre"],
        "tipo": data["tipo"],
        "slider": data["slider"],
        "posts": {},
    }

    # Guardar información de la iniciativa
    print(f"[API]: Adquiriendo información de {usuario}...")
    iniciativa_data: dict = client.user_info_by_username(usuario).model_dump()
    # print(f"[ERROR]: No se pudo obtener la información de {usuario}")
    # return iniciativa

    iniciativa["id"] = iniciativa_data["pk"]
    iniciativa["biografia"] = iniciativa_data["biography"]

    # Crear carpeta
    iniciativa_path: str = os.path.join(directorio, usuario)
    try:
        os.mkdir(iniciativa_path)
    except (FileExistsError, FileNotFoundError):
        print(f"[Error]: No se pudo crear la carpeta {iniciativa_path}")
        return iniciativa

    # Descargar foto de perfil
    pic_url = str(iniciativa_data['profile_pic_url'])
    pic_path: str = os.path.join(iniciativa_path, f"{usuario}.jpg")

    print(f"[API]: Descargando foto de perfil en {pic_url}...")
    request.urlretrieve(pic_url, pic_path)

    guardar(usuario, iniciativa, directorio)
    return iniciativa


def actualizar(client: Client, usuario: str, max_posts: int,
                          directorio: str) -> dict:
    '''
    Actualiza los posts de la iniciativa dada, descargando los más nuevos
    e eliminando los más viejos si se llegara a sobrepasar el limite de posts

    Args:
        client (Client): cliente de instragrapi
        usuario (str): usuario de instagram de la iniciativa
        max_posts (int): cantidad máxima de posts que puede tener una iniciativa
        directorio (str): directorio de iniciativas

    Returns:
        dict: iniciativa actualizada
    '''
    print(f"[API]: Verificando si {usuario} posee nuevos posts...")
    iniciativa: dict = cargar(usuario, directorio)

    try:
        raw_posts: list = client.user_medias(iniciativa["id"], max_posts)
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
    iniciativa: dict = api_posts.descargar(iniciativa, raw_posts, cantidad,
                                           directorio)

    iniciativa: dict = api_posts.limpiar(iniciativa, max_posts, directorio)
    guardar(usuario, iniciativa, directorio)
    print(f"[API]: Iniciativa {usuario} actualizada con exito")
    return iniciativa


def perfil(client: Client, usuario: str, directorio: str) -> dict:
    '''
    Actualiza la foto de perfil y la descripción del usuario dado mediante una
    llamada a la API

    Args:
        client (Client): cliente de instagrapi
        usuario (str): usuario al que actualizar su perfil
        directorio (str): directorio de iniciativas

    Returns:
        dict: diccionario con la información de la iniciativa
    '''
    iniciativa: dict = cargar(usuario, directorio)

    # Guardar información de la iniciativa
    try:
        print(f"[DEBUG]: Adquiriendo información de {usuario}...")
        iniciativa_data: dict = client.user_info_by_username(usuario).model_dump()
    except:
        print(f"[ERROR]: No se pudo obtener la información de {usuario}")
        return iniciativa

    iniciativa["id"] = iniciativa_data["pk"]
    iniciativa["biografia"] = iniciativa_data["biography"]

    # Descargar foto de perfil
    iniciativa_path: str = os.path.join(directorio, usuario)
    pic_url = str(iniciativa_data['profile_pic_url'])
    pic_path: str = os.path.join(iniciativa_path, f"{usuario}.jpg")

    print(f"[DEBUG]: Descargando foto de perfil en {pic_url}...")
    request.urlretrieve(pic_url, pic_path)

    guardar(usuario, iniciativa, directorio)
    print(f"[DEBUG]: Perfil de {usuario} actualizado con exito")
    return iniciativa


def eliminar(usuario: str, directorio: str):
    '''
    Elimina la iniciativa indicada del sistema

    Args:
        usuario (str): usuario de instagram de la iniciativa a eliminar
        directorio (str): directorio de iniciativas
    '''
    print(f"[DEBUG]: Eliminando iniciativa {usuario}...")
    iniciativa: dict = cargar(usuario, directorio)
    api_posts.limpiar(iniciativa, 99999, directorio)

    iniciativa_path = os.path.join(directorio, usuario)
    os.remove(os.path.join(iniciativa_path, f"{usuario}.json"))
    os.remove(os.path.join(iniciativa_path, f"{usuario}.jpg"))
    print(f"[DEBUG]: Iniciativa {usuario} eliminada")
