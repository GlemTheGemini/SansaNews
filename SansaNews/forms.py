from . import models
from django.contrib.auth.forms import UserCreationForm, forms


class avisos_forms(forms.ModelForm):
    class Meta:
        model = models.imagenes_avisos
        fields = ["descripcion","url"]
        labels = {"url": "", "descripcion": ""}
