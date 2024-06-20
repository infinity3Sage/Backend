from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Modulo, Submodulo, EmpresaModulo, EmpresaSubmodulo
from empresa.models import Empresa
from user.models import UserAccount

@login_required
def modify_access(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    user = request.user

    if not user.can_modify_access():
        return HttpResponseForbidden("No tienes permisos para modificar los accesos.")

    if request.method == "POST":
        modulos = request.POST.getlist('modulos')
        submodulos = request.POST.getlist('submodulos')

        EmpresaModulo.objects.filter(empresa=empresa).delete()
        EmpresaSubmodulo.objects.filter(empresa=empresa).delete()

        for modulo_id in modulos:
            modulo = get_object_or_404(Modulo, id=modulo_id)
            EmpresaModulo.objects.create(empresa=empresa, modulo=modulo)

        for submodulo_id in submodulos:
            submodulo = get_object_or_404(Submodulo, id=submodulo_id)
            EmpresaSubmodulo.objects.create(empresa=empresa, submodulo=submodulo)

        return redirect('some_success_url')

    available_modulos = Modulo.objects.all()
    available_submodulos = Submodulo.objects.all()
    empresa_modulos = empresa.modulos.all()
    empresa_submodulos = empresa.submodulos.all()

    context = {
        'empresa': empresa,
        'available_modulos': available_modulos,
        'available_submodulos': available_submodulos,
        'empresa_modulos': empresa_modulos,
        'empresa_submodulos': empresa_submodulos
    }
    return render(request, 'modulos/modify_access.html', context)
