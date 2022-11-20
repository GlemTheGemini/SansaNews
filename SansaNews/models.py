from django.db import models

class imagenes_avisos(models.Model):
    descripcion = models.TextField(max_length=200, null=True)
    url = models.FileField(upload_to="Avisos/" ,max_length=200)
    def str(self) -> str:
        return '{} {}'.format(self.descripcion, self.url)

    class Meta:
        db_table = 'Avisos'
