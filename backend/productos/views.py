from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Categoria, Producto, ProductoCodigo
from .serializers import (
    CategoriaSerializer,
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