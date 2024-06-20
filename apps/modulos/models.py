from django.db import models

class Modulo(models.Model):
    nombre = models.CharField(max_length=255, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Submodulo(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='submodulos', on_delete=models.CASCADE, null=False, blank=False)
    nombre = models.CharField(max_length=255, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre