from django.contrib import admin
from .models import Modulo, Submodulo

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Submodulo)
class SubmoduloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'modulo')