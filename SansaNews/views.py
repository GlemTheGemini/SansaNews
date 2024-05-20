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


def iniciativas_inicializar(request):
    '''
    Inicializa las iniciativas a las que le falta crear su carpeta específica
    con su json y su foto de perfil, toma los datos de "iniciativas.json" en el
    directorio.
    '''
    lista_iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)
    carpetas: list = os.listdir(DIRECTORIO)

    for usuario, data in lista_iniciativas.items():
        if usuario not in carpetas:
            api_iniciativa.crear(INSTAGRAM, usuario, data, DIRECTORIO)

    return redirect("")


def iniciativas_limpiar(request):
    '''
    Elimina aquellas carpetas de iniciativas que ya no se encuentren en el
    "iniciativas.json" junto con todo su contenido.
    '''
    lista_iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)
    usuarios: list = list(lista_iniciativas.keys())
    carpetas: list = os.listdir(DIRECTORIO)

    for carpeta in carpetas:
        if carpeta not in usuarios:
            api_iniciativa.eliminar(carpeta, DIRECTORIO)

    return redirect("")


def iniciativas_actualizar(request):
    '''
    ! LLAMA A LA API UNA VEZ POR CADA INICIATIVA, no sobreusar.

    Actualiza los posts de todas las iniciativas disponibles.
    '''
    iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)

    for usuario in iniciativas.keys():
        api_iniciativa.actualizar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)

    return redirect("")


def iniciativa(request, usuario):
    iniciativa_data: dict = api_iniciativa.cargar(usuario, DIRECTORIO)
    iniciativas: dict = api_iniciativa.escanear(DIRECTORIO)

    return render(request, "Molde.html", {
        "iniciativa": iniciativa_data,
        "iniciativas": iniciativas
    })


def perfil_actualizar(request, usuario):
    '''
    ! LLAMA A LA API 1 VEZ, no sobreusar.

    Actualiza el perfil de la iniciativa sin descargar posts, obtiene la
    biografia, los datos básicos y descarga la foto de perfil.

    Una vez actualizado el perfil vuelve a la página normal de la iniciativa.

    Args:
        request: http request
        usuario: usuario de instagram de la iniciativa
    '''
    api_iniciativa.perfil(INSTAGRAM, usuario, DIRECTORIO)
    return redirect(f"/{usuario}")


def perfil_borrar(request, usuario):
    '''
    Borra los datos básicos y la foto de perfil de la iniciativa, no borra los
    posts.

    Una vez borrado el perfil vuelve a la página normal de la iniciativa.

    Args:
        request: http request
        usuario: usuario de instagram de la iniciativa
    '''
    print(f"[API]: Removiendo {DIRECTORIO}/{usuario}/{usuario}.json")
    os.remove(os.path.join(DIRECTORIO, f"{usuario}/{usuario}.json"))
    print(f"[API]: Removiendo {DIRECTORIO}/{usuario}/{usuario}.jpg")
    os.remove(os.path.join(DIRECTORIO, f"{usuario}/{usuario}.jpg"))
    print(f"[API]: Borrado de perfil {usuario} completado")
    return redirect(f"/{usuario}")


def posts_actualizar(request, usuario):
    '''
    ! LLAMA A LA API 1 VEZ, no sobreusar.

    Descarga los últimos posts del usuario dado, borrando los posts más viejos
    si se llega a sobrepasar el límite de posts máximos por iniciativa.

    Una vez actualizado los posts vuelve a la página normal de la iniciativa.

    Args:
        request: http request
        usuario: usuario de instagram de la iniciativa
    '''
    api_iniciativa.actualizar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)
    return redirect(f"/{usuario}")


def posts_redescargar(request, usuario: str):
    '''
    ! LLAMA A LA API 1 VEZ, no sobreusar.

    Redescarga los últimos posts del usuario dado, borrando todos los posts
    primero, y luego volviendolos a descargar.

    Una vez redescargados los posts vuelve a la página normal de la iniciativa.

    Args:
        request: http request
        usuario: usuario de instagram de la iniciativa
    '''
    api_posts.redescargar(INSTAGRAM, usuario, MAX_POSTS, DIRECTORIO)
    return redirect(f"/{usuario}")


def posts_borrar(request, usuario: str, post_id: str):
    '''
    Borra todos los posts descargados de la iniciativa.

    Una vez borrados los posts vuelve a la página normal de la iniciativa.

    Args:
        request: http request
        usuario (str): usuario de instagram de la iniciativa
        post_id (str): id del post a borrar, "todos" si se quieren borrar todos
    '''
    api_posts.borrar(usuario, post_id, DIRECTORIO)
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
