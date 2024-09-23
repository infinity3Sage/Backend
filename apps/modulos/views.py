from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Modulo, Submodulo
from apps.empresa.models import Empresa, EmpresaModulo, EmpresaSubmodulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Modulo, Submodulo, Submodulo2
from .serializers import ModuloSerializer, SubmoduloSerializer, Submodulo2Serializer

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

@api_view(['GET'])
def get_modulos(request):
    # Obtener todos los módulos, submódulos y sub-submódulos
    modulos = Modulo.objects.all()
    submodulos = Submodulo.objects.all()
    subsubmodulos = Submodulo2.objects.all()

    # Serializar los datos
    modulos_serializer = ModuloSerializer(modulos, many=True)
    submodulos_serializer = SubmoduloSerializer(submodulos, many=True)
    subsubmodulos_serializer = Submodulo2Serializer(subsubmodulos, many=True)

    return Response({
        'modulos': modulos_serializer.data,
        'submodulos': submodulos_serializer.data,
        'subsubmodulos': subsubmodulos_serializer.data
    })
