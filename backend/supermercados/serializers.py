from rest_framework import serializers

from .models import Supermercado


class SupermercadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supermercado
        fields = [
            'id',
            'nombre',
            'nit',
            'direccion',
            'telefono',
            'email',
            'activo',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = [
            'id',
            'fecha_creacion',
            'fecha_actualizacion',
        ]

    def validate_nombre(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'El nombre del supermercado es obligatorio.'
            )

        return value

    def validate_nit(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'El NIT es obligatorio.'
            )

        return value

    def validate_direccion(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'La dirección es obligatoria.'
            )

        return value