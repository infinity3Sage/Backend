from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
         if not email:
            raise ValueError('Users must have an email address')
         
         email = self.normalize_email(email)
         user = self.model(email=email, **extra_fields)
         user.set_password(password)
         user.save()

         return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email,password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True,default="", null=False, blank=False)
    first_name = models.CharField(max_length=255,default="", null=False, blank=False)
    last_name = models.CharField(max_length=255,default="", null=False, blank=False)
    cliente_sage = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey('empresa.Empresa', related_name='usuarios', default="", on_delete=models.RESTRICT , null=False, blank=False)
    imagen_usuario = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    # TODO: Separación
    codigo_empleado = models.CharField(max_length=255, null=True, blank=True) #*Nuevo_app
    codigo_moneda = models.CharField(max_length= 255, null=True, blank=True) #*Nuevo_app
    default_planta = models.ForeignKey('planta.Planta', related_name='default_planta',default="", on_delete=models.RESTRICT, null=True, blank=True) #*Nuevo_app, default
    id_colaborador = models.CharField(max_length=255, null=True, blank=True) #*Nuevo_app
    idioma = models.CharField(max_length=255, null=True, blank=True) #*Nuevo_app
    default_poolid = models.CharField(max_length=255, null=True, blank=True) #*Nuevo_app, default
    ubicacion_contenedores = models.CharField(max_length=255, null=True, blank=True) #*Nuevo_app
    ubicacion_destino_produccion = models.CharField(max_length=255, null=True, blank=True) #*Nuevo_app
    # TODO: Fin de separación

    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False, null=False, blank=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','cliente_sage','empresa']

    def __str__(self):
        return self.email
    
    def can_modify_access(self):
        return self.email == 'infinity3-sage@nunsys.com'
    
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
        empresa.usuarios_creados = empresa.usuarios.count()
        empresa.save()