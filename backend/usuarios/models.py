from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        CONSUMIDOR = 'CONSUMIDOR', 'Consumidor'
        SUPERMERCADO = 'SUPERMERCADO', 'Supermercado'
        ADMIN = 'ADMIN', 'Administrador'

    username = None
    email = models.EmailField(unique=True)

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.CONSUMIDOR
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} - {self.rol}'