from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Compra
from .serializers import CompraDetalleSerializer, CompraSerializer


class CompraListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompraSerializer

    def get_queryset(self):
        return Compra.objects.filter(
            usuario=self.request.user
        ).select_related(
            'supermercado'
        ).prefetch_related(
            'detalles__producto'
        )


class CompraDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompraDetalleSerializer

    def get_queryset(self):
        return Compra.objects.filter(
            usuario=self.request.user
        ).select_related(
            'supermercado'
        ).prefetch_related(
            'detalles__producto'
        )