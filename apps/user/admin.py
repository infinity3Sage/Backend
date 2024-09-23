from django import forms
from django.contrib import admin
from .models import UserAccount, UsuarioModulo, UsuarioSubmodulo, UsuarioSubmodulo2
from apps.empresa.models import Empresa, EmpresaModulo, EmpresaSubmodulo, EmpresaSubmodulo2

class UsuarioModuloInline(admin.TabularInline):
    model = UsuarioModulo
    extra = 0

class UsuarioSubmoduloInline(admin.TabularInline):
    model = UsuarioSubmodulo
    extra = 0

class UsuarioSubmodulo2Inline(admin.TabularInline):
    model = UsuarioSubmodulo2
    extra = 0    

class UserAccountAdminForm(forms.ModelForm):
    modulos = forms.ModelMultipleChoiceField(
        queryset=EmpresaModulo.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    submodulos = forms.ModelMultipleChoiceField(
        queryset=EmpresaSubmodulo.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    submodulos2 = forms.ModelMultipleChoiceField(
        queryset=EmpresaSubmodulo2.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserAccount
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            empresa = kwargs['instance'].empresa
            if empresa:
                self.fields['modulos'].queryset = empresa.modulos.all()
                self.fields['submodulos'].queryset = empresa.submodulos.all()
                self.fields['submodulos2'].queryset = empresa.submodulos2.all()

class UserAccountAdmin(admin.ModelAdmin):
    form = UserAccountAdminForm
    inlines = [UsuarioModuloInline, UsuarioSubmoduloInline, UsuarioSubmodulo2Inline]
    list_display = ('email', 'first_name', 'last_name', 'empresa', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'empresa')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(empresa__in=request.user.empresas.all())
        else:
            return queryset.none()

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if not obj or request.user.is_superuser or request.user.is_staff:
            return inline_instances
        else:
            return []

    class Media:
        js = ('user/js/filter_submodulos.js',)

admin.site.register(UserAccount, UserAccountAdmin)
