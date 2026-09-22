import re

from django.contrib.auth import get_user_model
from rest_framework import serializers


Usuario = get_user_model()


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Usuario
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
        ]
        read_only_fields = ['id']

    def validate_password(self, value):
        """
        Valida que la contraseña cumpla los requisitos
        de seguridad establecidos para FreshTrack.
        """

        if len(value) < 8:
            raise serializers.ValidationError(
                'La contraseña debe tener mínimo 8 caracteres.'
            )

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                'La contraseña debe contener al menos una letra mayúscula.'
            )

        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                'La contraseña debe contener al menos un número.'
            )

        if not re.search(r'[^A-Za-z0-9]', value):
            raise serializers.ValidationError(
                'La contraseña debe contener al menos un símbolo.'
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        usuario = Usuario.objects.create_user(
            password=password,
            **validated_data
        )

        return usuario


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'rol',
            'fecha_registro',
        ]
        read_only_fields = [
            'id',
            'email',
            'rol',
            'fecha_registro',
        ]