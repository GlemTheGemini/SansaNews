from django.shortcuts import render
from . import json_reader
# Create your views here.

def gbu_usm(request):
    ruta_carpeta = "C:/Users/PlayF/Desktop/App Web/SansaNews/SansaNews/Iniciativas/" + "{}/"
    texto = "C:/Users/PlayF/Desktop/App Web/SansaNews/SansaNews/Iniciativas/"
    diccionario = json_reader.contenido(texto,ruta_carpeta)
    pagina = "gbu_usm"
    return render(request,"GBU.html",context={ "llave" : diccionario[pagina]})