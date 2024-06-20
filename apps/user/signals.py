from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.empresa.models import Empresa

User = get_user_model()

""" @receiver(post_save, sender=User)
def incrementar_contador_usuarios(sender, instance, created, **kwargs):
    if created and instance.empresa:
        empresa = instance.empresa
        empresa.usuarios_creados += 1
        empresa.save()

@receiver(post_delete, sender=User)
def decrementar_contador_usuarios(sender, instance, **kwargs):
    if instance.empresa:
        empresa = instance.empresa
        empresa.usuarios_creados -= 1
        empresa.save()
 """