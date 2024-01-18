# pylint: disable=C0114, C0116, E0401

import os
import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from instagrapi import Client
import api.iniciativa
import api.posts
import api.recientes
from api.iniciativa import TipoIniciativa
from . import forms, models

SRC = os.path.dirname(os.path.dirname(__file__))
DIRECTORIO = os.path.join(SRC, "/static/iniciativas")
MAX_POSTS = 5
MAX_SLIDER_POSTS = 4

INSTAGRAM = Client()
INSTAGRAM.delay_range = [1, 3]

def home(request):
    iniciativas = api.iniciativa.escanear(DIRECTORIO)
    slider = api.recientes.slider(MAX_SLIDER_POSTS, DIRECTORIO)

    agrupaciones = {
        "deportes": [],
        "recreacion": [],
        "centros": [],
        "redes": [],
    }

    for usuario, data in iniciativas.keys():
        match data["tipo"]:
            case TipoIniciativa.DEPORTE:
                agrupaciones["deportes"].append(usuario)
            case TipoIniciativa.RECREACION:
                agrupaciones["recreacion"].append(usuario)
            case TipoIniciativa.CENTRO:
                agrupaciones["centros"].append(usuario)
            case TipoIniciativa.RED:
                agrupaciones["redes"].append(usuario)

    return render(request,"Home.html",{
        "primera": [slider[0]],
        "publicaciones": slider[1:],
        "deportes" : agrupaciones["deportes"],
        "recreacion" : agrupaciones["recreacion"],
        "centros" : agrupaciones["centros"],
        "redes" : agrupaciones["redes"]
    })


def actualizar_iniciativas(request):
    lista_iniciativas: dict = api.iniciativa.escanear(DIRECTORIO)
    carpetas: list = os.listdir(DIRECTORIO)

    for usuario, data in lista_iniciativas.items():
        if usuario not in carpetas:
            api.iniciativa.crear(INSTAGRAM, usuario, data, DIRECTORIO)

    return home(request)


def limpiar_iniciativas(request):
    lista_iniciativas: dict = api.iniciativa.escanear(DIRECTORIO)
    usuarios: list = list(lista_iniciativas.keys())
    carpetas: list = os.listdir(DIRECTORIO)

    for carpeta in carpetas:
        if carpeta not in usuarios:
            api.iniciativa.eliminar(carpeta, DIRECTORIO)

    return home(request)


def iniciativa(request, usuario):
    data: dict = api.iniciativa.cargar(usuario, DIRECTORIO)
    iniciativas: dict = api.iniciativa.escanear(DIRECTORIO)

    return render(request, "Molde.html", {
        "usuario": usuario,
        "nombre": data["nombre"],
        "biografia": data["biografia"],
        "publicaciones": data["posts"],
        "iniciativas": iniciativas
    })


def actualizar_posts(request, usuario):
    api.iniciativa.actualizar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)
    return iniciativa(request, usuario)


def actualizar_perfil(request, usuario: str):
    api.iniciativa.perfil(INSTAGRAM, usuario, DIRECTORIO)
    return iniciativa(request, usuario)


def redescargar_posts(request, usuario: str):
    api.posts.redescargar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)
    return iniciativa(request, usuario)


def about(request):
    return render(request,"about.html")


def avisos(request):
    lista = models.imagenes_avisos.objects.all().order_by("id").reverse()
    lista.reverse()
    slider = api.recientes.slider(MAX_SLIDER_POSTS, DIRECTORIO)
    return render(request,"Avisos.html",{"key": lista, "iniciativas": slider})



def subir_avisos(request, iniciativas=None):
    imagen = forms.avisos_forms(request.POST, request.FILES)
    slider = api.recientes.slider(MAX_SLIDER_POSTS, DIRECTORIO)

    if request.method == "POST":
        if imagen.is_valid():
            imagen.save()
            return redirect(avisos)
    context = {"imagen": imagen, "iniciativas": slider}
    return render(request, 'Subir_Avisos.html', context)


def redireccion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fecha_limite = data.get('fechaFormateada')
        request.session['fecha_limite'] = fecha_limite
        return JsonResponse({'success': True})

    return render(request, 'Redireccion.html')


def publicaciones(request):
    #Se deben otener siempre las ultimas publicaciones del mes.

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Calcular la fecha hace 30 días atrás
    fecha_hace_30_dias = fecha_actual - datetime.timedelta(days=30)
    fecha_hace_30_dias = int(fecha_hace_30_dias.timestamp())

    # Obtener las publicaciones que se han hecho desde hace 30 días
    lista_30 = api.recientes.ultimos(fecha_hace_30_dias, DIRECTORIO)

    # Verificar si se ha proporcionado una fecha límite
    fecha_limite = request.session.get('fecha_limite')
    request.session.pop('fecha_limite', None)
    if fecha_limite is not None:
        lista_custom = api.recientes.ultimos(fecha_limite, DIRECTORIO)
    else:
        lista_custom = []

    iniciativas = api.iniciativa.escanear(DIRECTORIO)

    return render(request, 'Publicaciones.html', {
        "fecha": fecha_limite, 
        "lista_30": lista_30, 
        "lista_custom": lista_custom, 
        "iniciativas": iniciativas
    })
