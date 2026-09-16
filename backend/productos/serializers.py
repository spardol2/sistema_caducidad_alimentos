from django.utils import timezone
from rest_framework import serializers

from .models import Categoria, Inventario, Producto, ProductoCodigo

from datetime import timedelta
import random


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'descripcion',
            'activo',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'fecha_creacion',
        ]


class ProductoCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCodigo
        fields = [
            'id',
            'codigo',
            'tipo',
        ]
        read_only_fields = [
            'id',
        ]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )
    codigos = ProductoCodigoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'marca',
            'descripcion',
            'categoria',
            'categoria_nombre',
            'unidad_medida',
            'cantidad_presentacion',
            'activo',
            'codigos',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = [
            'id',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
class ProductoCodigoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCodigo
        fields = [
            'id',
            'codigo',
            'tipo',
        ]
        read_only_fields = [
            'id',
        ]
class InventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )

    categoria_nombre = serializers.CharField(
        source='producto.categoria.nombre',
        read_only=True
    )

    tiempo_restante_segundos = serializers.SerializerMethodField()
    tiempo_restante = serializers.SerializerMethodField()

    class Meta:
        model = Inventario
        fields = [
            'id',
            'producto',
            'producto_nombre',
            'categoria_nombre',
            'cantidad_inicial',
            'cantidad_disponible',
            'fecha_compra',
            'fecha_vencimiento',
            'estado',
            'tiempo_restante',
            'tiempo_restante_segundos',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = [
            'id',
            'fecha_vencimiento',
            'estado',
            'tiempo_restante',
            'tiempo_restante_segundos',
            'fecha_creacion',
            'fecha_actualizacion',
        ]

    def create(self, validated_data):
        fecha_compra = validated_data.get(
            'fecha_compra',
            timezone.localdate()
        )

        dias_vencimiento = random.randint(7, 60)

        validated_data['fecha_vencimiento'] = (
            fecha_compra + timedelta(days=dias_vencimiento)
        )

        validated_data['estado'] = Inventario.Estado.ACTIVO

        return super().create(validated_data)

    def get_tiempo_restante_segundos(self, obj):
        ahora = timezone.now()
        vencimiento = timezone.make_aware(
            timezone.datetime.combine(
                obj.fecha_vencimiento,
                timezone.datetime.min.time()
            )
        )

        segundos = int((vencimiento - ahora).total_seconds())

        return max(segundos, 0)

    def get_tiempo_restante(self, obj):
        segundos = self.get_tiempo_restante_segundos(obj)

        dias = segundos // 86400
        horas = (segundos % 86400) // 3600
        minutos = (segundos % 3600) // 60
        segundos_restantes = segundos % 60

        return (
            f'{dias} días '
            f'{horas:02d}:'
            f'{minutos:02d}:'
            f'{segundos_restantes:02d}'
        )