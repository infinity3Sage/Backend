from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from .models import Empresa, EmpresaModulo, EmpresaSubmodulo, EmpresaSubmodulo2
from apps.modulos.models import Modulo, Submodulo, Submodulo2
from apps.planta.models import  Planta
 
class PlantaInline(admin.TabularInline):
    model = Planta
    extra = 0
    can_delete = True

 
class EmpresaAdminForm(forms.ModelForm):
    modulos = forms.ModelMultipleChoiceField(
        queryset=Modulo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False
    )
    submodulos = forms.ModelMultipleChoiceField(
        queryset=Submodulo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required= False
    )
    submodulos2 = forms.ModelMultipleChoiceField(
        queryset=Submodulo2.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required= False
    )
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Empresa
        fields = '__all__'
 
 
class EmpresaAdmin(admin.ModelAdmin):
    form = EmpresaAdminForm
    inlines =[PlantaInline]
    list_display = ('id','nombre', 'api_endpoint', 'descripcion', 'suscripcion', 'usuarios_creados', 'limite_usuarios')
    readonly_fields = ('usuarios_creados', 'limite_usuarios','plantas_list',)
    filter_horizontal = ('submodulos',)
 
    def limite_usuarios(self, obj):
        return obj.limite_usuarios()
    limite_usuarios.short_description = 'Límite de Usuarios'
 
    def plantas_list(self, obj):
        return ", ".join([planta.nombre for planta in obj.plantas.all()])
    plantas_list.short_description = 'Plantas'
 
    def save_model(self, request, obj, form, change):
        if request.user.email !=  'asd@gmail.com':
            self.message_user(request, "No tienes permiso para modificar los accesos de los módulos y submódulos.", level='error')
            return
       
        if obj.usuarios_creados > obj.limite_usuarios():
            self.message_user(request, "El número de usuarios creados no puede exceder el límite de usuarios de la suscripción.", level='error')
            return
 
        super().save_model(request, obj, form, change)
 
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('filter-submodulos/', self.admin_site.admin_view(self.filter_submodulos), name='filter-submodulos'),
        ]
        return custom_urls + urls
    
    def filter_submodulos(self, request):
        modulo_ids = request.GET.get('modulos_ids', '').split(',')
        empresa_id = request.GET.get('empresa_id', None)
    
        if empresa_id:
            empresa = Empresa.objects.get(id=empresa_id)
            selected_submodulos = empresa.submodulos.values_list('id', flat=True)
        else:
            selected_submodulos = []
    
        submodulos = Submodulo.objects.filter(modulo_id__in=modulo_ids)
        data = [{'id': submodulo.id, 'nombre': submodulo.nombre, 'selected': submodulo.id in selected_submodulos} for submodulo in submodulos]
        return JsonResponse(data, safe=False)
    

    class Media:
        js = ('empresa/js/filter_submodulos.js',)
 
class EmpresaModuloAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'modulo')
 
    def has_change_permission(self, request, obj=None):
        if request.user.email !=  'asd@gmail.com':
            return False
        return super().has_change_permission(request, obj)
 
    def has_delete_permission(self, request, obj=None):
        if request.user.email !=  'asd@gmail.com':
            return False
        return super().has_delete_permission(request, obj)
   
class EmpresaSubmoduloAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'submodulo')
 
    def has_change_permission(self, request, obj=None):
        if request.user.email !=  'asd@gmail.com':
            return False
        return super().has_change_permission(request, obj)
 
    def has_delete_permission(self, request, obj=None):
        if request.user.email !=  'asd@gmail.com':
            return False
        return super().has_delete_permission(request, obj)
    
class EmpresaSubmodulo2Admin(admin.ModelAdmin):
    list_display = ('empresa', 'submodulo2')
 
    def has_change_permission(self, request, obj=None):
        if request.user.email !=  'asd@gmail.com':
            return False
        return super().has_change_permission(request, obj)
 
    def has_delete_permission(self, request, obj=None):
        if request.user.email !=  'asd@gmail.com':
            return False
        return super().has_delete_permission(request, obj)
 
 
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(EmpresaModulo)
admin.site.register(EmpresaSubmodulo)
admin.site.register(EmpresaSubmodulo2)
admin.site.register(Planta)