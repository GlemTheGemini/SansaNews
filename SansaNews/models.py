from django.db import models

# Create your models here.

class Carpetas(models.Model):
    pagina = models.FileField()
    fecha = models.DateTimeField(auto_now = True)