from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from apps.empresa.models import Empresa
from apps.empresa.serializers import EmpresaSerializer
from django.contrib.auth import get_user_model
from apps.modulos.serializers import ModuloSerializer, Submodulo2Serializer, SubmoduloSerializer

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    empresa = serializers.CharField(write_only=True)  # Acepta el nombre de la empresa como una cadena

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = '__all__'

    def validate(self, attrs):
        empresa_nombre = attrs.get('empresa')
        try:
            empresa = Empresa.objects.get(nombre=empresa_nombre)
        except Empresa.DoesNotExist:
            raise serializers.ValidationError('La empresa especificada no existe.')

        if empresa.usuarios_creados >= empresa.limite_usuarios():
            raise serializers.ValidationError('Se ha llegado al máximo de usuarios en tu nivel de subscripción.')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            empresa = Empresa.objects.get(nombre=request.user.empresa.nombre)  # Obtener la empresa del usuario autenticado
        else:
            raise serializers.ValidationError("El usuario no está autenticado.")

        validated_data['empresa'] = empresa
        user = super().create(validated_data)
        return user


class UserSerializer(BaseUserSerializer):
    empresa = EmpresaSerializer(read_only=True)
    modulos = ModuloSerializer(many=True, read_only=True)
    submodulos = SubmoduloSerializer(many=True, read_only=True)
    submodulos2 = Submodulo2Serializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.cliente_sage = validated_data.get('cliente_sage', instance.cliente_sage)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.empresa = validated_data.get('empresa', instance.empresa)
        instance.codigo_empleado = validated_data.get('codigo_empleado', instance.codigo_empleado)
        instance.codigo_moneda = validated_data.get('codigo_moneda', instance.codigo_moneda)
        instance.default_planta = validated_data.get('default_planta', instance.default_planta)
        instance.id_colaborador = validated_data.get('id_colaborador', instance.id_colaborador)
        instance.idioma = validated_data.get('idioma', instance.idioma)
        instance.default_poolid = validated_data.get('default_poolid', instance.default_poolid)
        instance.ubicacion_contenedores = validated_data.get('ubicacion_contenedores', instance.ubicacion_contenedores)
        instance.ubicacion_destino_produccion = validated_data.get('ubicacion_destino_produccion', instance.ubicacion_destino_produccion)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance
