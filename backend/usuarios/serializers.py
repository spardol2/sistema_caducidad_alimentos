from django.contrib.auth import get_user_model
from rest_framework import serializers


Usuario = get_user_model()


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
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