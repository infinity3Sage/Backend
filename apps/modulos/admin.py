from django.contrib import admin
from .models import Modulo, Submodulo, Submodulo2

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Submodulo)
class SubmoduloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'modulo')

@admin.register(Submodulo2)
class Submodulo2Admin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'submodulo')