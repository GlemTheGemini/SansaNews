# Leer archivo JSON para sacar url de la foto y caption.
# Se importa json y se abre el archivo a leer.
import json
import os
from os import path
from os.path import isfile,join,isdir

def leer_json(archivo):
    archivo_json = open(archivo)
    #Convertimos el JSON a diccionario.
    if "json" not in archivo:
        return 0
    data = json.load(archivo_json)

    #Verifica si hay mas URL's
    if "edge_sidecar_to_children" in data["node"]:
        cantidad = len(data['node']["edge_sidecar_to_children"]["edges"])
        contador = 0
        while contador < cantidad:
            print("Esta es la URL",contador + 1,":",data['node']["edge_sidecar_to_children"]["edges"][contador]["node"]["display_url"],"\n")
            contador += 1
    elif "display_url" not in data['node']:
        print("Final de los links")
    else:
        print("Esta es la única URL:",data['node']["display_url"])

    # Lee la descripcion.
    if "edge_media_to_caption" not in data['node']:
        print("Final de las descripciones\n")
    elif len(data['node']["edge_media_to_caption"]["edges"]) == 0:
        print("No hay descripccion\n")
    else:
        print("Esta es la descripción:",data['node']["edge_media_to_caption"]["edges"][0]['node']['text'],"\n\n","-----------------------------------------------------------------------------")
    #Se cierra el archivo
    archivo_json.close()

#Define la ruta en donde se guardan las carpetas extraidas a partir de instaloader
nombre= "json_reader.py"
ruta = path.abspath(nombre)
lista = ruta.split("\\")
del lista[-1]
texto = ""
for elemento in lista:
	texto += elemento+"/"
ruta_carpeta = texto + "{}/"

#Este es el contenido de lo que hay en la ruta texto
contenido = os.listdir(texto)
#obtener carpetas
carpetas = [nombre for nombre in contenido if isdir(join(texto,nombre))]
contador = 0
while contador < len(carpetas):
    texto = ruta_carpeta
    texto = texto.format(carpetas[contador])
    #obtener archivos
    contenido = os.listdir(texto)
    archivos = [nombre for nombre in contenido if isfile(join(texto,nombre))]
    contador_2 = 0
    while contador_2 < len(archivos):
        directorio = texto + archivos[contador_2]
        prints = leer_json(directorio)
        contador_2 += 1
    contador += 1