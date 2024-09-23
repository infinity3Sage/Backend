from rest_framework import serializers
from apps.modulos.models import Modulo, Submodulo, Submodulo2

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id', 'nombre']

class SubmoduloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submodulo
        fields = ['id', 'nombre']

class Submodulo2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Submodulo2
        fields = ['id', 'nombre']