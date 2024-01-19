from django.urls import path #, include
from . import views
# from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("" ,views.home,name="home"),
    path('redireccion/', views.redireccion, name='redireccion'),
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path("about-us/", views.about,name="about-us"),
    path("Avisos/", views.avisos,name="avisos"),
    path("Subir-Avisos/", views.subir_avisos,name="subir-avisos"),
    path("debug/actualizar/", views.actualizar_iniciativas),
    path("debug/limpiar/", views.limpiar_iniciativas),
    path("debug/inicializar/", views.inicializar_iniciativas),
    path("<str:usuario>/", views.iniciativa),
    path("<str:usuario>/debug/actualizar", views.actualizar_posts),
    path("<str:usuario>/debug/perfil", views.actualizar_perfil),
    path("<str:usuario>/debug/redescargar", views.redescargar_posts),
]
