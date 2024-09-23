from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from apps.modulos.models import Modulo, Submodulo, Submodulo2

class Empresa(models.Model):
    SUSCRIPCION_NIVELES = [
        tuple(nivel.split(':')) for nivel in settings.SUSCRIPCION_NIVELES
    ]

    nombre = models.CharField(max_length=255, default='', null=False, blank=False)
    api_endpoint = models.URLField(max_length=500, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    descripcion = CKEditor5Field('Text', config_name='extends')
    imagen_background = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    imagen_corporativa = models.ImageField(upload_to='corporativas/', null=True, blank=True)
    modulos = models.ManyToManyField(Modulo, through='EmpresaModulo')
    submodulos = models.ManyToManyField(Submodulo, through='EmpresaSubmodulo')
    submodulos2 = models.ManyToManyField(Submodulo2, through='EmpresaSubmodulo2')
    suscripcion = models.CharField(max_length=10, choices=SUSCRIPCION_NIVELES, default='FREE', null=False, blank=False)
    usuarios_creados = models.PositiveIntegerField(default=0, null=False, blank=False)
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

    def __str__(self):
        return self.nombre
    
    def limite_usuarios(self):
        return settings.LIMITE_USUARIOS.get(self.suscripcion, 0)
    
    def clean(self):
        super().clean()
        if self.usuarios_creados > self.limite_usuarios():
            raise models.ValidationError("El número de usuarios creados no puede exceder el límite de usuarios de la suscripción.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Validar antes de guardar
        super().save(*args, **kwargs)


class EmpresaModulo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, null=False, blank=False)
    activo = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        unique_together = ('empresa', 'modulo')

    def __str__(self):
        return f"{self.empresa} - {self.modulo}"


class EmpresaSubmodulo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    submodulo = models.ForeignKey(Submodulo, on_delete=models.CASCADE, null=False, blank=False)
    activo = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        unique_together = ('empresa', 'submodulo')

    def __str__(self):
        return f"{self.empresa} - {self.submodulo}"

class EmpresaSubmodulo2(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    submodulo2 = models.ForeignKey(Submodulo2, on_delete=models.CASCADE, null=False, blank=False)
    activo = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        unique_together = ('empresa', 'submodulo2')

    def __str__(self):
        return f"{self.empresa} - {self.submodulo2}"