from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from . import API
from .iniciativas import INICIATIVAS
from . import forms
from . import models
import os
import json


def home(request):
    recientes = API.recientes()
    return render(request,"Home.html",{"primera": [recientes[0]],"publicaciones": recientes[1:], "iniciativas": INICIATIVAS})

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

    return HttpResponse("Iniciativas Actualizadas")
def publicaciones(request):
    recientes = API.recientes()
    return render(request, 'Publicaciones.html',{"primera": [recientes[0]],"publicaciones": recientes[1:], "iniciativas": INICIATIVAS})


def actualizar_fecha_view(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        fecha_limite = data.get('fechaFormateada') + ".jpg"
        publicaciones = API.recientes_publicaciones(fecha_limite)
        
        # Aquí puedes realizar los procesos necesarios en el backend utilizando fecha_formateada
        # Por ejemplo, guardarla en la base de datos, realizar cálculos, etc.


        # Devolver una respuesta JSON al frontend para indicar que se ha procesado la fecha de ingreso
        return JsonResponse({'message': 'Fecha de ingreso recibida y procesada correctamente.',"fecha":fecha_limite,'test':publicaciones})
    else:
        return JsonResponse({'status': 'error', 'message': 'Metodo no permitido'})