from rest_framework import serializers

from .models import Categoria, Producto, ProductoCodigo


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