import os
from urllib import request
from . import api
from instagrapi import Client


def redescargar_posts(client: Client, usuario: str):
    '''
    Fuerza la redescarga de los posts del usuario dado, borrando todos los
    posts previamente descargados y descargandolos de nuevo
    
    Args:
        usuario: usuario de instagram al que redescargar los posts
    '''
    print(f"[DEBUG]: Redescargando posts de {usuario}")

    iniciativa: dict = api.cargar_iniciativa(usuario)
    api.limpiar_posts(iniciativa, 99999)
    api.actualizar_iniciativa(client, usuario)

    print(f"[DEBUG]: Posts de {usuario} redescargados con exito")


def actualizar_perfil(client: Client, usuario: str):
    '''
    Actualiza la foto de perfil y la descripción del usuario dado mediante una
    llamada a la API

    Args:
        client (Client): cliente de instagrapi
        usuario (str): usuario al que actualizar su perfil
    '''
    iniciativa: dict = api.cargar_iniciativa(usuario)

    # Guardar información de la iniciativa
    try:
        print(f"[DEBUG]: Adquiriendo información de {usuario}...")
        iniciativa_data: dict = client.user_info_by_username(usuario).model_dump()
    except:
        print(f"[ERROR]: No se pudo obtener la información de {usuario}")
        return

    iniciativa["id"] = iniciativa_data["pk"]
    iniciativa["biografia"] = iniciativa_data["biography"]

    # Descargar foto de perfil
    iniciativa_path: str = os.path.join(api.DIRECTORIO, usuario)
    pic_url = str(iniciativa_data['profile_pic_url'])
    pic_path: str = os.path.join(iniciativa_path, f"{usuario}.jpg")

    print(f"[DEBUG]: Descargando foto de perfil en {pic_url}...")
    request.urlretrieve(pic_url, pic_path)

    api.guardar_iniciativa(iniciativa)
    print(f"[DEBUG]: Perfil de {usuario} actualizado con exito")


def eliminar_iniciativa(usuario: str):
    '''
    Elimina la iniciativa indicada del sistema

    Args:
        usuario (str): usuario de instagram de la iniciativa a eliminar
    '''
    print(f"[DEBUG]: Eliminando iniciativa {usuario}...")
    iniciativa: dict = api.cargar_iniciativa(usuario)
    api.limpiar_posts(iniciativa, 99999)

    iniciativa_path = os.path.join(api.DIRECTORIO, usuario)
    os.remove(os.path.join(iniciativa_path, f"{usuario}.json"))
    os.remove(os.path.join(iniciativa_path, f"{usuario}.jpg"))
    print(f"[DEBUG]: Iniciativa {usuario} eliminada")

