from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from apps.empresa.models import Empresa, EmpresaModulo, EmpresaSubmodulo
from apps.modulos.models import Modulo, Submodulo, Submodulo2

class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Los usuarios deben tener un nombre de usuario')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, default="", null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, default="", null=True, blank=True)
    first_name = models.CharField(max_length=255, default="", null=True, blank=True)
    last_name = models.CharField(max_length=255, default="", null=True, blank=True)
    interno = models.BooleanField(default=False, null=False, blank=False)
    partner = models.BooleanField(default=False, null=False, blank=False)
    cliente_sage = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, related_name='usuarios', on_delete=models.RESTRICT, null=True, blank=True)
    imagen_usuario = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    modulos = models.ManyToManyField(Modulo, through='UsuarioModulo')
    submodulos = models.ManyToManyField(Submodulo, through='UsuarioSubmodulo')
    submodulos2 = models.ManyToManyField(Submodulo2, through='UsuarioSubmodulo2')
    codigo_empleado = models.CharField(max_length=255, null=True, blank=True)
    codigo_moneda = models.CharField(max_length=255, null=True, blank=True)
    default_planta = models.CharField(max_length=255, null=True, blank=True)
    id_colaborador = models.CharField(max_length=255, null=True, blank=True)
    idioma = models.CharField(max_length=255, null=True, blank=True)
    default_poolid = models.CharField(max_length=255, null=True, blank=True)
    ubicacion_contenedores = models.CharField(max_length=255, null=True, blank=True)
    ubicacion_destino_produccion = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False, null=False, blank=False)
    objects = UserAccountManager()
 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'cliente_sage', 'empresa']

    def __str__(self):
        return self.username
    
    def can_modify_access(self):
        return self.username == 'Gnis'
    
    def clean(self):
        if self.default_planta and self.empresa and self.default_planta.empresa != self.empresa:
            raise ValidationError("La planta predeterminada debe pertenecer a la misma empresa que el usuario.")

    def save(self, *args, **kwargs):
        try:
            old_instance = UserAccount.objects.get(pk=self.pk)
        except UserAccount.DoesNotExist:
            old_instance = None

        old_empresa = old_instance.empresa if old_instance else None
        new_empresa = self.empresa
        was_active = old_instance.is_active if old_instance else False
        is_active = self.is_active

        super().save(*args, **kwargs)

        if old_empresa and old_empresa != new_empresa:
            if was_active:
                old_empresa.usuarios_creados -= 1
                old_empresa.save()
            if is_active:
                new_empresa.usuarios_creados += 1
                new_empresa.save()
        elif old_empresa == new_empresa:
            if was_active and not is_active:
                new_empresa.usuarios_creados -= 1
                new_empresa.save()
            elif not was_active and is_active:
                new_empresa.usuarios_creados += 1
                new_empresa.save()
        elif not old_instance and is_active:
            new_empresa.usuarios_creados += 1
            new_empresa.save()
    
    def delete(self, *args, **kwargs):
        empresa = self.empresa
        super().delete(*args, **kwargs)
        if empresa:
            empresa.usuarios_creados = empresa.usuarios.count()
            empresa.save()

class UsuarioModulo(models.Model):
    usuario = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

class UsuarioSubmodulo(models.Model):
    usuario = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    submodulo = models.ForeignKey(Submodulo, on_delete=models.CASCADE)

class UsuarioSubmodulo2(models.Model):
    usuario = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    submodulo = models.ForeignKey(Submodulo2, on_delete=models.CASCADE)