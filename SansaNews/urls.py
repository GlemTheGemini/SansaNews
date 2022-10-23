from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard")
]