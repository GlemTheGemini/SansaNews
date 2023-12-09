from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import API
from .iniciativas import INICIATIVAS
from . import forms
from . import models
import os
import json

# Create your views here.

def home(request):
    recientes = API.recientes()
    return render(request,"Home.html",{"key": recientes, "iniciativas": INICIATIVAS})

def iniciativa(request, usuario):
    with open(os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/biografias.json", "r", encoding='utf-8') as archivo:
        biografias = json.load(archivo)
        biografia = biografias[usuario]

    publicaciones= API.contenido(usuario)

    return render(request, "Molde.html", {
        "usuario": usuario,
        "nombre": INICIATIVAS[usuario],
        "biografia": biografia,
        "key": publicaciones,
        "iniciativas": INICIATIVAS
    })

def about(request):
    return render(request,"about.html")

def avisos(request):
    lista = models.imagenes_avisos.objects.all().order_by("id").reverse()
    lista.reverse()
    return render(request,"Avisos.html",{"key": lista, "iniciativas": INICIATIVAS})

def subir_avisos(request, id=None):
    imagen = forms.avisos_forms(request.POST, request.FILES)

    if request.method == "POST":
        if imagen.is_valid():
            imagen.save()
            return redirect(avisos)
    context = {"imagen": imagen, "iniciativas": INICIATIVAS}
    return render(request, 'Subir_Avisos.html', context)

def test(request):
    biografias = {}

    for iniciativa in INICIATIVAS:
        biografias[iniciativa] = API.actualizar_perfil(iniciativa)
        API.actualizar_publicaciones(iniciativa)

    with open(os.path.dirname(os.path.dirname(__file__)) + f"/static/iniciativas/biografias.json", "w", encoding='utf-8') as archivo:
        json.dump(biografias, archivo, indent=2)

    API.cleanup()
    
    return HttpResponse("Iniciativas Actualizadas")
