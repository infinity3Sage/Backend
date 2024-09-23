from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Empresa, EmpresaModulo, EmpresaSubmodulo, EmpresaSubmodulo2
from .serializers import EmpresaSerializer, ModuloSerializer, SubmoduloSerializer, Submodulo2Serializer
from .serializers import EmpresaModuloSerializer, EmpresaSubmoduloSerializer, EmpresaSubmodulo2Serializer

# Existing views for listing and detail of Empresa
class EmpresaListAPIView(generics.ListAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EmpresaDetailAPIView(generics.RetrieveAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

# New views for updating activation status
@api_view(['PUT'])
def update_empresa_modulo(request, empresa_id, modulo_id):
    try:
        empresa_modulo = EmpresaModulo.objects.get(empresa_id=empresa_id, modulo_id=modulo_id)
    except EmpresaModulo.DoesNotExist:
        return Response({'error': 'EmpresaModulo not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmpresaModuloSerializer(empresa_modulo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_empresa_submodulo(request, empresa_id, submodulo_id):
    try:
        empresa_submodulo = EmpresaSubmodulo.objects.get(empresa_id=empresa_id, submodulo_id=submodulo_id)
    except EmpresaSubmodulo.DoesNotExist:
        return Response({'error': 'EmpresaSubmodulo not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmpresaSubmoduloSerializer(empresa_submodulo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_empresa_submodulo2(request, empresa_id, submodulo2_id):
    try:
        empresa_submodulo2 = EmpresaSubmodulo2.objects.get(empresa_id=empresa_id, submodulo2_id=submodulo2_id)
    except EmpresaSubmodulo2.DoesNotExist:
        return Response({'error': 'EmpresaSubmodulo2 not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmpresaSubmodulo2Serializer(empresa_submodulo2, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
