"""Modulo encargado de manejar los posts más recientes."""

import os
import json

def slider(cantidad: int, directorio: str) -> dict:
    '''
    Devuelve los posts más recientes de las iniciativas que están en el slider

    Args:
        cantidad (int): cantidad de posts recientes deseados
        directorio (str): directorio donde se encuentran las publicaciones
            recientes

    Returns:
        list: lista con los posts más recientes
    '''
    print(f"[API]: Cargando las {cantidad} más recientes...")
    recientes = cargar(directorio)

    slider_posts = {}
    count = 0
    for fecha, data in recientes.items():
        if cantidad <= 0:
            break

        if not data["slider"]:
            continue

        print(f"[API]: Cargando post {fecha} de {data['usuario']}")
        slider_posts[fecha] = data
        cantidad -= 1
        count += 1

    print(f"[API]: Los {count} posts más recientes han sido cargados")
    return slider_posts


def ultimos(fecha_limite: int, directorio: str) -> list:
    '''
    Obtiene todos los posts hasta la fecha indicada

    Args:
        fecha_limite (int): fecha limite de los posts
        directorio (str): directorio donde se encuentran las publicaciones
            recientes

    Returns:
        list: lista con los posts publicados despues de la fecha dada
    '''
    recientes = cargar(directorio)
    fechas = list(recientes.keys())
    fechas.sort()

    ultimos_posts = []
    for fecha in fechas:
        if int(fecha) < fecha_limite:
            break

        ultimos_posts.append(recientes[fecha])

    return ultimos_posts


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
