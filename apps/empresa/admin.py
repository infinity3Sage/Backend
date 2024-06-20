from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from .models import Empresa, EmpresaModulo, EmpresaSubmodulo
from apps.planta.models import  Planta

class PlantaInline(admin.TabularInline):
    model = Planta
    extra = 0
    can_delete = True

class EmpresaAdminForm(forms.ModelForm):
    descripcion = forms.CharField(widget=CKEditorUploadingWidget(config_name='default'))

    class Meta:
        model = Empresa
        fields = '__all__'


class EmpresaAdmin(admin.ModelAdmin):
    form = EmpresaAdminForm
    inlines =[PlantaInline]
    list_display = ('id','nombre', 'api_endpoint', 'descripcion', 'suscripcion', 'usuarios_creados', 'limite_usuarios')
    readonly_fields = ('usuarios_creados', 'limite_usuarios','plantas_list',)
    filter_horizontal = ('modulos', 'submodulos')

    def limite_usuarios(self, obj):
        return obj.limite_usuarios()
    limite_usuarios.short_description = 'Límite de Usuarios'

    def plantas_list(self, obj):
        return ", ".join([planta.nombre for planta in obj.plantas.all()])
    plantas_list.short_description = 'Plantas'

    def save_model(self, request, obj, form, change):
        if request.user.email != 'infinity3-sage@nunsys.com':
            self.message_user(request, "No tienes permiso para modificar los accesos de los módulos y submódulos.", level='error')
            return
        
        if obj.usuarios_creados > obj.limite_usuarios():
            self.message_user(request, "El número de usuarios creados no puede exceder el límite de usuarios de la suscripción.", level='error')
            return

        super().save_model(request, obj, form, change)

class EmpresaModuloAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'modulo')

    def has_change_permission(self, request, obj=None):
        if request.user.email != 'infinity3-sage@nunsys.com':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.email != 'infinity3-sage@nunsys.com':
            return False
        return super().has_delete_permission(request, obj)
    
class EmpresaSubmoduloAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'submodulo')

    def has_change_permission(self, request, obj=None):
        if request.user.email != 'infinity3-sage@nunsys.com':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.email != 'infinity3-sage@nunsys.com':
            return False
        return super().has_delete_permission(request, obj)


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(EmpresaModulo)
admin.site.register(EmpresaSubmodulo)
admin.site.register(Planta)