#Importar los modulos a usar y ponemos el contexto.
import instaloader; import os; from os import path; import json;
def actualizar(pagina):
    L = instaloader.Instaloader(post_metadata_txt_pattern="",compress_json=False,dirname_pattern=(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\static\\"+ "{}\\").format(pagina))
    #Descargamos los archivos necesarios de los usuarios que se encuentran en el archivo señalado
    L.download_profile(pagina, fast_update=True, profile_pic=False)
    return()

def contenido(pagina):
    diccionario = {}
    m = ""
    #Gracias stackoverflow
    directorio = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\static\\" + "{}\\"
    lista = []
    lista_multi_imagenes = []
    lista_descripción = []
    contenido_in_carpeta = sorted(os.listdir(directorio.format(pagina)))
    formato_temp = os.path.dirname(directorio.format(pagina)) + "\\{}"
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
    #Se añade la lista al diccionario
    if pagina not in diccionario:
        diccionario[pagina] = lista
    #Se transforma el diccionario en una lista con formato especifico y se retorna
    lista_4 = []
    lista_5 = []
    for llave in diccionario:
        for publicacion in diccionario[llave]:
            if len(publicacion[0]) != 0:
                for imagen in publicacion[0]: 
                    lista_5 += [imagen]
                lista_5 += publicacion[1]
                lista_4 += [lista_5]
                lista_5 = []
    lista_4.reverse()
    return lista_4