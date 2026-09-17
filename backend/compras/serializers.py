from django.db import transaction
from rest_framework import serializers

from .models import Compra, DetalleCompra


class DetalleCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )

    class Meta:
        model = DetalleCompra
        fields = [
            'id',
            'producto',
            'producto_nombre',
            'cantidad',
            'precio_unitario',
            'subtotal',
        ]
        read_only_fields = [
            'id',
            'producto_nombre',
            'subtotal',
        ]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'La cantidad debe ser mayor que cero.'
            )
        return value

    def validate_precio_unitario(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                'El precio unitario no puede ser negativo.'
            )
        return value


class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    supermercado_nombre = serializers.CharField(
        source='supermercado.nombre',
        read_only=True
    )

    class Meta:
        model = Compra
        fields = [
            'id',
            'supermercado',
            'supermercado_nombre',
            'fecha_compra',
            'total',
            'observaciones',
            'detalles',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'total',
            'fecha_creacion',
        ]

    def validate_detalles(self, value):
        if not value:
            raise serializers.ValidationError(
                'La compra debe tener al menos un producto.'
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        usuario = self.context['request'].user

        compra = Compra.objects.create(
            usuario=usuario,
            **validated_data
        )

        total = 0

        for detalle_data in detalles_data:
            cantidad = detalle_data['cantidad']
            precio_unitario = detalle_data.get('precio_unitario')
            subtotal = detalle_data.get('subtotal')

            if subtotal is None and precio_unitario is not None:
                subtotal = cantidad * precio_unitario

            DetalleCompra.objects.create(
                compra=compra,
                producto=detalle_data['producto'],
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )

            if subtotal is not None:
                total += subtotal

        compra.total = total
        compra.save(update_fields=['total'])

        return compra


class CompraDetalleSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True, read_only=True)
    supermercado_nombre = serializers.CharField(
        source='supermercado.nombre',
        read_only=True
    )

    class Meta:
        model = Compra
        fields = [
            'id',
            'supermercado',
            'supermercado_nombre',
            'fecha_compra',
            'total',
            'observaciones',
            'detalles',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'supermercado_nombre',
            'total',
            'detalles',
            'fecha_creacion',
        ]