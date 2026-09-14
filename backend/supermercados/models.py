from django.db import models


class Supermercado(models.Model):
    nombre = models.CharField(max_length=150)
    nit = models.CharField(max_length=30, unique=True)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supermercados'
        verbose_name = 'Supermercado'
        verbose_name_plural = 'Supermercados'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre