from rest_framework import serializers
from .models import Modulo, Submodulo, Submodulo2

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id', 'nombre']

class SubmoduloSerializer(serializers.ModelSerializer):
    modulo_nombre = serializers.CharField(source='modulo.nombre', read_only=True)

    class Meta:
        model = Submodulo
        fields = ['id','nombre', 'modulo_nombre']

class Submodulo2Serializer(serializers.ModelSerializer):
    submodulo_nombre = serializers.CharField(source='submodulo.nombre', read_only=True)

    class Meta:
        model = Submodulo2
        fields = ['id','nombre', 'submodulo_nombre']