from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Supermercado
from .serializers import SupermercadoSerializer


class SupermercadoListCreateView(generics.ListCreateAPIView):
    queryset = Supermercado.objects.all()
    serializer_class = SupermercadoSerializer
    permission_classes = [IsAuthenticated]


class SupermercadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Supermercado.objects.all()
    serializer_class = SupermercadoSerializer
    permission_classes = [IsAuthenticated]