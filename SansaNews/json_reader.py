# Leer archivo JSON para sacar url de la foto y caption.
# Se importa json y se abre el archivo a leer.
import json
import os
from os import path
from os.path import isfile,join,isdir

def leer_json(archivo):

    if "json" not in archivo:
        pagina = "Null"
        lista = ["vacia"]
        return pagina,lista
    #Convertimos el JSON a diccionario.
    archivo_json = open(archivo)
    data = json.load(archivo_json)

    #obtiene el nombre de la pagina, se crea el diccionario y las listas vacias
    if "owner" in data['node']:
        pagina = data['node']["owner"]["username"]
    else:
        pagina = data['node']["username"]
    lista = []
    #Verifica si hay mas URL's
    if "edge_sidecar_to_children" in data["node"]:
        cantidad = len(data['node']["edge_sidecar_to_children"]["edges"])
        contador = 0
        while contador < cantidad:
            lista.append(data['node']["edge_sidecar_to_children"]["edges"][contador]["node"]["display_url"])
            contador += 1
    elif "display_url" not in data['node']:
        basura = 0
    else:
        lista.append(data['node']["display_url"])

    # Lee la descripcion.
    if "edge_media_to_caption" not in data['node']:
        basura = 0
    elif len(data['node']["edge_media_to_caption"]["edges"]) == 0:
        lista.append(["Sin descripcion"])
    else:
        lista.append(data['node']["edge_media_to_caption"]["edges"][0]['node']['text'])
    #Se cierra el archivo
    archivo_json.close()
    return pagina,lista
    
#Este es el contenido de lo que hay en la ruta
def contenido(texto,ruta_carpeta):
    contenido = os.listdir(texto)
    #obtener carpetas
    carpetas = [nombre for nombre in contenido if isdir(join(texto,nombre))]
    contador = 0
    dicc = {}
    while contador < len(carpetas):
        texto = ruta_carpeta
        texto = texto.format(carpetas[contador])
        #obtener archivos
        contenido = os.listdir(texto)
        archivos = [nombre for nombre in contenido if isfile(join(texto,nombre))]
        contador_2 = 0
        while contador_2 < len(archivos):
            directorio = texto + archivos[contador_2]
            pagina,lista = leer_json(directorio)
            if pagina not in dicc:
                dicc[pagina]=[lista]
            else:
                dicc[pagina]+=[lista]
            contador_2 += 1
        contador += 1
    return dicc