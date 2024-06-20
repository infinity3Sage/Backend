from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from ckeditor_uploader.fields import RichTextUploadingField


class Empresa(models.Model):
    SUSCRIPCION_NIVELES = [
        tuple(nivel.split(':')) for nivel in settings.SUSCRIPCION_NIVELES
    ]

    nombre = models.CharField(max_length=255,default='', null=False, blank=False)
    api_endpoint = models.URLField(max_length=500, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    descripcion = RichTextUploadingField(null=True, blank=True)
    imagen_background = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    imagen_corporativa = models.ImageField(upload_to='corporativas/', null=True, blank=True)
    modulos = models.ManyToManyField('modulos.Modulo', through='EmpresaModulo')
    submodulos = models.ManyToManyField('modulos.Submodulo', through='EmpresaSubmodulo')
    suscripcion = models.CharField(max_length=10, choices=SUSCRIPCION_NIVELES, default='FREE', null=False, blank=False)
    usuarios_creados = models.PositiveIntegerField(default=0, null=False, blank=False)
    # TODO: Inicio de separación
    campo_familia = models.CharField(max_length=255, null=True, blank=True)
    campo_subfamilia = models.CharField(max_length=255, null=True, blank=True)
    codigo_tabla_traducciones = models.CharField(max_length=255, null=True, blank=True)
    decimales_consumo = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    decimales_stock = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    end_point = models.URLField(max_length=500, null=True, blank=True)
    mostrar_articulos_activos = models.BooleanField(default=True)
    mostrar_clientes_activos = models.BooleanField(default=True)
    mostrar_proveedores_activos = models.BooleanField(default=True)
    passwordws = models.CharField(max_length=255, null=True, blank=True)
    tipo_pedido_catalogo = models.CharField(max_length=255, null=True, blank=True)
    usuariows = models.CharField(max_length=255, null=True, blank=True)
    # TODO: Fin de separación

    def __str__(self):
        return self.nombre
    
    def limite_usuarios(self):
        return settings.LIMITE_USUARIOS.get(self.suscripcion, 0)
    
    def save(self, *args, **kwargs):
        if self.usuarios_creados > self.limite_usuarios():
            raise ValueError("El número de usuarios creados no puede exceder el límite de usuarios de la suscripción.")
        super().save(*args, **kwargs)

class EmpresaModulo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    modulo = models.ForeignKey('modulos.Modulo', on_delete=models.CASCADE, null=False, blank=False)
    activo = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f"{self.empresa} - {self.modulo}"

class EmpresaSubmodulo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    submodulo = models.ForeignKey('modulos.Submodulo', on_delete=models.CASCADE, null=False, blank=False)
    activo = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f"{self.empresa} - {self.submodulo}"