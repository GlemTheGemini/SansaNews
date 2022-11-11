from django.shortcuts import render
from . import API
# Create your views here.

def gbu_usm(request):
    pagina = "gbu_usm"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"GBU.html",{"key": lista})

def fablab(request):
    pagina = "fablab_utfsm"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"FabLab.html",{"key": lista})

def ceeinf(request):
    pagina = "ceeinf_sj"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"CEEINF.html",{"key": lista})

def geek(request):
    pagina = "geekusm"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"GeekUSM.html",{"key": lista})

def movimiento(request):
    pagina = "movimiento.0"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"Movimiento.html",{"key": lista})

def primos(request):
    pagina = "primos_usmsj"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"Primos.html",{"key": lista})

def rocket(request):
    pagina = "rocketscience_usm"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"RocketScienceUSM.html",{"key": lista})

def cubesat(request):
    pagina = "usm.cubesat.team"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"USM-Cubesat-Team.html",{"key": lista})

def xumbra(request):
    pagina = "xumbra_utfsm"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"XumbraUTFSM.html",{"key": lista})

def yotecuido(request):
    pagina = "yotecuidousm"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"Yo-Te-Cuido.html",{"key": lista})

def sansanews(request):
    pagina = "sansanews"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"SansaNews.html",{"key": lista})

def home(request):
    return render(request,"Home.html")

def molde(request):
    return render(request,"Molde.html")
