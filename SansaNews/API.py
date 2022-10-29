#Importar los modulos a usar y ponemos el contexto.
import instaloader; import os; from os import path; from os.path import join,isdir ; import json

def actualizar():
    L = instaloader.Instaloader(post_metadata_txt_pattern="",compress_json=False)
    #Descargamos los archivos necesarios de los usuarios que se encuentran en el archivo señalado
    Archivo_Iniciativas = open("Iniciativas_tester.txt")
    for linea in Archivo_Iniciativas:
        profile = linea.strip()
        L.download_profile(profile, fast_update=True, profile_pic=False)
    Archivo_Iniciativas.close()
    return()

def contenido(pagina):
    diccionario = {}
    contador = 0
    contenido = os.listdir()
    m = ""
    #A partir de aquí ni yo entiendo qué estoy haciendo.
    directorio = os.path.dirname("Iniciativas_tester.txt") + "{}/"
    lista = []
    lista_multi_imagenes = []
    lista_descripción = []
    contenido_in_carpeta = sorted(os.listdir(directorio.format(pagina)))
    formato_temp = os.path.dirname(directorio.format(pagina)) + "/{}"
    for file in contenido_in_carpeta:
        if m == "":
            m = file[:24]
            if file.endswith(".jpg"):
                    lista_multi_imagenes.append(formato_temp.format(file))
            if file.endswith(".json"):
                archivo_json = open(formato_temp.format(file))
                data = json.load(archivo_json)
                if "edge_media_to_caption" not in data['node']:
                    trash = 0 #LOL
                elif len(data['node']["edge_media_to_caption"]["edges"]) == 0:
                    lista_descripción.append("")
                else:
                    lista_descripción.append(data['node']["edge_media_to_caption"]["edges"][0]['node']['text'])
        else:
            if file.startswith(m):
                if file.endswith(".jpg"):
                        lista_multi_imagenes.append(formato_temp.format(file))
                if file.endswith(".json"):
                    archivo_json = open(formato_temp.format(file))
                    data = json.load(archivo_json)
                    if "edge_media_to_caption" not in data['node']:
                        trash = 0 #LOL
                    elif len(data['node']["edge_media_to_caption"]["edges"]) == 0:
                        lista_descripción.append("")
                    else:
                        lista_descripción.append(data['node']["edge_media_to_caption"]["edges"][0]['node']['text'])
            else:
                m = ""
                lista_descripción = []
                lista_multi_imagenes = []
                lista_publicación = []
                lista_publicación.append(lista_multi_imagenes); lista_publicación.append(lista_descripción)
                lista.append(lista_publicación) ; lista_publicación = []
                #'''
                if file.endswith(".jpg"):
                        lista_multi_imagenes.append(formato_temp.format(file))
                if file.endswith(".json"):
                    archivo_json = open(formato_temp.format(file))
                    data = json.load(archivo_json)
                    if "edge_media_to_caption" not in data['node']:
                        trash = 0 #LOL
                    elif len(data['node']["edge_media_to_caption"]["edges"]) == 0:
                        lista_descripción.append("")
                    else:
                        lista_descripción.append(data['node']["edge_media_to_caption"]["edges"][0]['node']['text'])
                #Juaco: oye, yo conozco ese código...
                #Benja: ehe.
                #'''
    if pagina not in diccionario:
        diccionario[pagina] = lista
    return diccionario