# empresa/serializers.py
from rest_framework import serializers
from .models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['nombre','descripcion','imagen_background', 'imagen_corporativa', 'logo', 'api_endpoint']
