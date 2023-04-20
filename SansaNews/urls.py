from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("" ,views.home,name="home"),
    path("Test/" ,views.test,name="test"),
    path("about-us/",views.about,name="about-us"),
    path("Avisos/",views.avisos,name="avisos"),
    path("Subir-Avisos/",views.subir_avisos,name="subir-avisos"),
    path("<str:usuario>/", views.iniciativa),
]
