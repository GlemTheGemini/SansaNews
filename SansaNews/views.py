from django.shortcuts import render, redirect
from . import API
from . import forms
from . import models
# Create your views here.

def gbu_usm(request):
    pagina = "gbu_usm"
    lista = API.contenido(pagina)
    return render(request,"GBU.html",{"key": lista})

def fablab(request):
    pagina = "fablab_utfsm"
    lista = API.contenido(pagina)
    return render(request,"FabLab.html",{"key": lista})

def ceeinf(request):
    pagina = "ceeinf_sj"
    lista = API.contenido(pagina)
    return render(request,"CEEINF.html",{"key": lista})

def geek(request):
    pagina = "geekusm"
    lista = API.contenido(pagina)
    return render(request,"GeekUSM.html",{"key": lista})

def movimiento(request):
    pagina = "movimiento.0"
    lista = API.contenido(pagina)
    return render(request,"Movimiento.html",{"key": lista})

def primos(request):
    pagina = "primos_usmsj"
    lista = API.contenido(pagina)
    return render(request,"Primos.html",{"key": lista})

def rocket(request):
    pagina = "rocketscience_usm"
    lista = API.contenido(pagina)
    return render(request,"RocketScienceUSM.html",{"key": lista})

def cubesat(request):
    pagina = "usm.cubesat.team"
    lista = API.contenido(pagina)
    return render(request,"USM-Cubesat-Team.html",{"key": lista})

def xumbra(request):
    pagina = "xumbra_utfsm"
    lista = API.contenido(pagina)
    return render(request,"XumbraUTFSM.html",{"key": lista})

def yotecuido(request):
    pagina = "yotecuidousm"
    lista = API.contenido(pagina)
    return render(request,"Yo-Te-Cuido.html",{"key": lista})

def sansanews(request):
    pagina = "sansanews"
    API.actualizar(pagina)
    lista = API.contenido(pagina)
    return render(request,"SansaNews.html",{"key": lista})

def home(request):
    lista = API.recientes()
    return render(request,"Home.html",{"key": lista})

def molde(request):
    return render(request,"Molde.html")

def test(request):
    API.actualizar_2()
    lista = API.recientes()
    return render(request,"Test.html",{"key": lista})

def subir_avisos(request, id=None):

    imagen = forms.avisos_forms(request.POST, request.FILES)

    if request.method == "POST":
        if imagen.is_valid():
            imagen.save()
            return redirect(avisos)
    context = {"imagen": imagen}
    return render(request, 'Subir_Avisos.html', context)

def avisos(request):
    lista = models.imagenes_avisos.objects.all().order_by("id").reverse()
    lista.reverse()
    return render(request,"Avisos.html",{"key": lista})

def ergon(request):
    pagina = "ergon_usm"
    lista = API.contenido(pagina)
    return render(request,"ergon.html",{"key": lista})
