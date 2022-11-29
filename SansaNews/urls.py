from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("GBU/",views.gbu_usm,name="gbu"),
    path("FabLab/",views.fablab,name="fablab"),
    path("CEEINF/",views.ceeinf,name="ceeinf"),
    path("Usm-CubeSat-Team/",views.cubesat,name="cubesat"),
    path("GeekUSM/",views.geek,name="geek"),
    path("Movimiento-0/",views.movimiento,name="movimiento"),
    path("Primos/",views.primos,name="primos"),
    path("RocketScience-USM/",views.rocket,name="rocket"),
    path("Yo-Te-Cuido/",views.yotecuido,name="yotecuido"),
    path("Xumbra-UTFSM/",views.xumbra,name="xumbra"),
    path("SansaNews/",views.sansanews,name="sansanews"),
    path("Home/" ,views.home,name="home"),
    path("Molde/" ,views.molde,name="molde"),
    path("Test/" ,views.test,name="test"),
    path("Subir-Avisos/",views.subir_avisos,name="subir-avisos"),
    path("Avisos/",views.avisos,name="avisos"),
    path("Ergon/",views.ergon,name="ergon"),
]