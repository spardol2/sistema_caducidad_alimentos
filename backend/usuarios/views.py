from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import PerfilUsuarioSerializer, RegistroUsuarioSerializer


class RegistroUsuarioView(generics.CreateAPIView):
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]


class PerfilUsuarioView(generics.RetrieveAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user