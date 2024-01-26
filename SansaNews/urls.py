from django.urls import path #, include
from . import views
# from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("" ,views.home,name="home"),
    path('redireccion', views.redireccion, name='redireccion'),
    path('publicaciones', views.publicaciones, name='publicaciones'),
    path("about-us", views.about,name="about-us"),
    path("Avisos", views.avisos,name="avisos"),
    path("Subir-Avisos", views.subir_avisos,name="subir-avisos"),

    # Debug de iniciativas
    path("iniciativas/inicializar", views.iniciativas_inicializar),
    path("iniciativas/actualizar", views.iniciativas_actualizar),
    path("iniciativas/limpiar", views.iniciativas_limpiar),

    # Páginas de Iniciativas
    path("<str:usuario>", views.iniciativa),

    ## Debug de perfiles
    path("<str:usuario>/perfil/actualizar", views.perfil_actualizar),
    path("<str:usuario>/perfil/borrar", views.perfil_borrar),

    ## Debug de posts
    path("<str:usuario>/posts/actualizar", views.posts_actualizar),
    path("<str:usuario>/posts/redescargar", views.posts_redescargar),
    path("<str:usuario>/posts/borrar/<str:post_id>", views.posts_borrar),
]
