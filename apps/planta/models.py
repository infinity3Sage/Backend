from django.db import models
from apps.empresa.models import Empresa

class Planta(models.Model):
    nombre = models.CharField(max_length=255, null=False, blank=False)
    codigo_sage = models.CharField(max_length=255, null=False, blank=False)
    empresa = models.ForeignKey(Empresa, related_name='plantas', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre