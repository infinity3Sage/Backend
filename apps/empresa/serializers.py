from rest_framework import serializers
from apps.modulos.models import Modulo, Submodulo, Submodulo2
from apps.modulos.serializers import ModuloSerializer, Submodulo2Serializer, SubmoduloSerializer
from .models import Empresa
from rest_framework import serializers
from apps.modulos.models import Modulo, Submodulo, Submodulo2
from .models import Empresa, EmpresaModulo, EmpresaSubmodulo, EmpresaSubmodulo2

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'

class SubmoduloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submodulo
        fields = '__all__'

class Submodulo2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Submodulo2
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    modulos = serializers.SerializerMethodField()
    submodulos = serializers.SerializerMethodField()
    submodulos2 = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = '__all__'

    def get_modulos(self, obj):
        modulos_activos = obj.modulos.filter(empresamodulo__activo=True)
        return ModuloSerializer(modulos_activos, many=True).data

    def get_submodulos(self, obj):
        submodulos_activos = obj.submodulos.filter(empresasubmodulo__activo=True)
        return SubmoduloSerializer(submodulos_activos, many=True).data

    def get_submodulos2(self, obj):
        submodulos2_activos = obj.submodulos2.filter(empresasubmodulo2__activo=True)
        return Submodulo2Serializer(submodulos2_activos, many=True).data

class EmpresaModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaModulo
        fields = '__all__'

class EmpresaSubmoduloSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaSubmodulo
        fields = '__all__'

class EmpresaSubmodulo2Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaSubmodulo2
        fields = '__all__'
