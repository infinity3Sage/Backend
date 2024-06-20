from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from apps.empresa.models import Empresa
from apps.empresa.serializers import EmpresaSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all(), required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'cliente_sage',
            'telefono',
            'direccion',
            'empresa',
            'imagen_usuario',
            'is_active',
            'is_staff',
            'password',
        ]

    def validate(self, attrs):
        empresa_id = attrs.get('empresa')
        try:
            empresa = Empresa.objects.get(id=empresa_id)
        except Empresa.DoesNotExist:
            raise serializers.ValidationError('La empresa especificada no existe.')

        if empresa.usuarios_creados >= empresa.limite_usuarios():
            raise serializers.ValidationError('Se ha llegado al máximo de usuarios en tu nivel de subscripción.')
        return attrs

    def create(self, validated_data):
        empresa = validated_data.pop('empresa')
        user = super().create(validated_data)
        user.empresa = empresa
        user.save()
        return user

class UserSerializer(BaseUserSerializer):
    empresa = EmpresaSerializer(read_only=True)  # Usa el EmpresaSerializer

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'cliente_sage',
            'telefono',
            'direccion',
            'empresa',
            'imagen_usuario',
            'is_active',
            'is_staff',
        ]

