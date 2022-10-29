from django.shortcuts import render
from . import API
# Create your views here.

def gbu_usm(request):
    pagina = "gbu_usm"
    lista = API.contenido(pagina)
    return render(request,"GBU.html",{"key": lista})
    #context={ "llave" : [diccionario[pagina][-2],diccionario[pagina][-3],diccionario[pagina][-4],diccionario[pagina][-5],diccionario[pagina][-6]]}