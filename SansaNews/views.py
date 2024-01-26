# pylint: disable=C0114, C0116, E0401, W0702, W0613

import os
import json
import datetime
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render, redirect
from instagrapi import Client
from . import forms, models
from .api import iniciativa as api_iniciativa
from .api import posts as api_posts
from .api.iniciativa import TipoIniciativa

BASE = os.path.dirname(os.path.dirname(__file__))
DIRECTORIO = os.path.join(BASE, "static/iniciativas")
SESSION_PATH = Path(os.path.join(BASE, "SansaNews/api/session.json"))
MAX_POSTS = 5
MAX_SLIDER_POSTS = 4

INSTAGRAM = Client()

# Intentar logearse a la cuenta de instagram en session.json
try:
    print("[API]: Iniciando sesión en instagram...")
    INSTAGRAM.load_settings(SESSION_PATH)
except:
    print("[ERROR]: No se pudo iniciar sesión en instagram")
    print(f"[ERROR]: No se encontró sesión guardada en {SESSION_PATH}")
    print("[ERROR]: Intente logearse con login.py")

print("[API]: Sesión iniciada")
INSTAGRAM.delay_range = [1, 3]

def home(request):
    iniciativas = api_iniciativa.escanear(DIRECTORIO)
    slider = api_posts.ultimos(MAX_SLIDER_POSTS, DIRECTORIO, slider=True)

    agrupaciones = {
        TipoIniciativa.DEPORTE.value: {},
        TipoIniciativa.RECREACION.value: {},
        TipoIniciativa.CENTRO.value: {},
        TipoIniciativa.RED.value: {},
    }

    for usuario, data in iniciativas.items():
        agrupaciones[data["tipo"]][usuario] = data

    return render(request,"Home.html",{
        "recientes": slider,
        "agrupaciones": agrupaciones,
    })


def inicializar_iniciativas(request):
    lista_iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)
    carpetas: list = os.listdir(DIRECTORIO)

    for usuario, data in lista_iniciativas.items():
        if usuario not in carpetas:
            api_iniciativa.crear(INSTAGRAM, usuario, data, DIRECTORIO)

    return redirect("")


def limpiar_iniciativas(request):
    lista_iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)
    usuarios: list = list(lista_iniciativas.keys())
    carpetas: list = os.listdir(DIRECTORIO)

    for carpeta in carpetas:
        if carpeta not in usuarios:
            api_iniciativa.eliminar(carpeta, DIRECTORIO)

    return redirect("")


def iniciativa(request, usuario):
    iniciativa: dict = api_iniciativa.cargar(usuario, DIRECTORIO)
    iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)

    return render(request, "Molde.html", {
        "iniciativa": iniciativa,
        "iniciativas": iniciativas
    })


def actualizar_posts(request, usuario):
    api_iniciativa.actualizar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)
    return redirect(f"/{usuario}")


def actualizar_perfil(request, usuario: str):
    api_iniciativa.perfil(INSTAGRAM, usuario, DIRECTORIO)
    return redirect(f"/{usuario}")


def redescargar_posts(request, usuario: str):
    api_posts.redescargar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)
    return redirect(f"/{usuario}")


def about(request):
    return render(request,"about.html")


def avisos(request):
    lista = models.imagenes_avisos.objects.all().order_by("id").reverse()
    lista.reverse()
    slider = api_posts.ultimos(MAX_SLIDER_POSTS, DIRECTORIO, slider=True)
    return render(request,"Avisos.html",{"key": lista, "iniciativas": slider})



def subir_avisos(request, iniciativas=None):
    imagen = forms.avisos_forms(request.POST, request.FILES)
    slider = api_posts.ultimos(MAX_SLIDER_POSTS, DIRECTORIO, slider=True)

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
    lista_30 = api_posts.ultimos(MAX_POSTS, DIRECTORIO, fecha_limite=fecha_hace_30_dias)

    # Verificar si se ha proporcionado una fecha límite
    fecha_limite = request.session.get('fecha_limite')
    request.session.pop('fecha_limite', None)
    if fecha_limite is not None:
        lista_custom = api_posts.ultimos(fecha_limite, DIRECTORIO)
    else:
        lista_custom = []

    iniciativas = api_iniciativa.escanear(DIRECTORIO)

    return render(request, 'Publicaciones.html', {
        "fecha": fecha_limite, 
        "lista_30": lista_30, 
        "lista_custom": lista_custom, 
        "iniciativas": iniciativas
    })
