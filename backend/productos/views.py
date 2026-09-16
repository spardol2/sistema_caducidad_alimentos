from datetime import timedelta

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Categoria, Inventario, Producto, ProductoCodigo
from .serializers import (
    CategoriaSerializer,
    InventarioSerializer,
    ProductoCodigoCreateSerializer,
    ProductoSerializer,
)


class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class CategoriaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.select_related(
        'categoria'
    ).prefetch_related(
        'codigos'
    )
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]


class ProductoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Producto.objects.select_related(
        'categoria'
    ).prefetch_related(
        'codigos'
    )
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]


class ProductoCodigoListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductoCodigoCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductoCodigo.objects.filter(
            producto_id=self.kwargs['producto_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            producto_id=self.kwargs['producto_id']
        )


class BuscarProductoPorCodigoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        codigo = request.query_params.get('codigo')

        if not codigo:
            return Response(
                {'detail': 'El parámetro codigo es obligatorio.'},
                status=400
            )

        try:
            producto_codigo = ProductoCodigo.objects.select_related(
                'producto__categoria'
            ).prefetch_related(
                'producto__codigos'
            ).get(codigo=codigo)
        except ProductoCodigo.DoesNotExist:
            return Response(
                {'detail': 'No se encontró ningún producto con ese código.'},
                status=404
            )

        serializer = ProductoSerializer(producto_codigo.producto)

        return Response(serializer.data)


class InventarioListCreateView(generics.ListCreateAPIView):
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inventario.objects.filter(
            usuario=self.request.user
        ).select_related(
            'producto',
            'producto__categoria'
        ).order_by(
            'fecha_vencimiento'
        )

    def perform_create(self, serializer):
        serializer.save(
            usuario=self.request.user
        )


class InventarioDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inventario.objects.filter(
            usuario=self.request.user
        ).select_related(
            'producto',
            'producto__categoria'
        )

    def perform_update(self, serializer):
        inventario = serializer.save()

        if inventario.cantidad_disponible <= 0:
            inventario.cantidad_disponible = 0
            inventario.estado = Inventario.Estado.AGOTADO

        elif inventario.fecha_vencimiento < timezone.localdate():
            inventario.estado = Inventario.Estado.VENCIDO

        else:
            inventario.estado = Inventario.Estado.ACTIVO

        inventario.save(
            update_fields=[
                'cantidad_disponible',
                'estado',
                'fecha_actualizacion',
            ]
        )


class InventarioProximoVencimientoView(generics.ListAPIView):
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hoy = timezone.localdate()
        fecha_limite = hoy + timedelta(days=30)

        return Inventario.objects.filter(
            usuario=self.request.user,
            cantidad_disponible__gt=0,
            fecha_vencimiento__gte=hoy,
            fecha_vencimiento__lte=fecha_limite,
        ).select_related(
            'producto',
            'producto__categoria'
        ).order_by(
            'fecha_vencimiento'
        )