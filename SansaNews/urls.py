from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("GBU/",views.gbu_usm,name="gbu")
]