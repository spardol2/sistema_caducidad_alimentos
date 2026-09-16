from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegistroUsuarioSerializer


class RegistroUsuarioView(generics.CreateAPIView):
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]