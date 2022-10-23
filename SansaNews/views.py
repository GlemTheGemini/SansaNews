from django.shortcuts import render
from .models import Carpetas 
# Create your views here.

def dashboard(request):
    return render(request,"dashboard.html")