import os, json, datetime
from django.http import JsonResponse #, HttpResponseRedirect
# from django.urls import reverse
from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from . import API
from .api import api, debug
from . import forms
from . import models
from instagrapi import Client

SRC = os.path.dirname(os.path.dirname(__file__))
api.DIRECTORIO = os.path.join(SRC, "/static/iniciativas")

INSTAGRAM = Client()
INSTAGRAM.delay_range = [1, 3]

iniciativas = []
slider = []
recientes = []
agrupaciones = {
    "deportes": [],
    "recreacion": [],
    "centros": [],
    "redes": [],
}


def home(request):
    recientes = API.recientes(4)
    iniciativas = api.escanear_iniciativas()

    for usuario, data in iniciativas.keys():
        if data["slider"]:
            slider.append(usuario)

        match data["tipo"]:
            case api.TipoIniciativa.DEPORTE:
                agrupaciones["deportes"].append(usuario)
            case api.TipoIniciativa.RECREACION:
                agrupaciones["recreacion"].append(usuario)
            case api.TipoIniciativa.CENTRO:
                agrupaciones["centros"].append(usuario)
            case api.TipoIniciativa.RED:
                agrupaciones["redes"].append(usuario)

    return render(request,"Home.html",{
        "primera": [recientes[0]],
        "publicaciones": recientes[1:],
        "deportes" : agrupaciones["deportes"],
        "recreacion" : agrupaciones["recreacion"],
        "centros" : agrupaciones["centros"],
        "redes" : agrupaciones["redes"]
    })


def actualizar_iniciativas(request):
    iniciativas: dict = api.escanear_iniciativas()
    carpetas: list = os.listdir(api.DIRECTORIO)

    for usuario, data in iniciativas.items():
        if usuario not in carpetas:
            api.crear_iniciativa(INSTAGRAM, usuario, data["nombre"],
                                data["tipo"], data["slider"])

    return home(request)


def limpiar_iniciativas(request):
    iniciativas: dict = api.escanear_iniciativas()
    usuarios: list = list(iniciativas.keys())
    carpetas: list = os.listdir(api.DIRECTORIO)

    for carpeta in carpetas:
        if carpeta not in usuarios:
            debug.eliminar_iniciativa(carpeta)

    return home(request)


def iniciativa(request, usuario):
    iniciativa: dict = api.cargar_iniciativa(usuario)
    return render(request, "Molde.html", {
        "usuario": usuario,
        "nombre": iniciativa["nombre"],
        "biografia": iniciativa["biografia"],
        "publicaciones": iniciativa["posts"],
        "iniciativas": iniciativas
    })


def actualizar_posts(request, usuario):
    api.actualizar_iniciativa(INSTAGRAM, usuario)
    return iniciativa(request, usuario)


def actualizar_perfil(request, usuario: str):
    debug.actualizar_perfil(INSTAGRAM, usuario)
    return iniciativa(request, usuario)


def redescargar_posts(request, usuario: str):
    debug.redescargar_posts(INSTAGRAM, usuario)
    return iniciativa(request, usuario)


def about(request):
    return render(request,"about.html")


def avisos(request):
    lista = models.imagenes_avisos.objects.all().order_by("id").reverse()
    lista.reverse()
    return render(request,"Avisos.html",{"key": lista, "iniciativas": slider})



def subir_avisos(request, iniciativas=None):
    imagen = forms.avisos_forms(request.POST, request.FILES)

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
    else:
        return render(request, 'Redireccion.html')


def publicaciones(request):
    #Se deben otener siempre las ultimas publicaciones del mes.

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Calcular la fecha hace 30 días atrás
    fecha_hace_30_dias = fecha_actual - datetime.timedelta(days=30)

    # Formatear la fecha como una cadena personalizada
    formato_fecha = fecha_hace_30_dias.strftime('%Y-%m-%d_%H-%M-%S')

    # Obtener las publicaciones que se han hecho desde hace 30 días
    lista_30 = API.recientes_publicaciones(formato_fecha)

    # Verificar si se ha proporcionado una fecha límite
    fecha_limite = request.session.get('fecha_limite')
    request.session.pop('fecha_limite', None)
    if fecha_limite is not None:
        lista_custom = API.recientes_publicaciones(fecha_limite)
    else:
        lista_custom = []

    return render(request, 'Publicaciones.html', {
        "fecha": fecha_limite, 
        "lista_30": lista_30, 
        "lista_custom": lista_custom, 
        "iniciativas": iniciativas
    })

