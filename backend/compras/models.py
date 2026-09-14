from django.conf import settings
from django.db import models


class Compra(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compras'
    )

    supermercado = models.ForeignKey(
        'supermercados.Supermercado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='compras'
    )

    fecha_compra = models.DateField()
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'compras'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-fecha_compra', '-fecha_creacion']

    def __str__(self):
        return f'Compra #{self.id} - {self.usuario.email}'


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.PROTECT,
        related_name='detalles_compra'
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'detalles_compra'
        verbose_name = 'Detalle de compra'
        verbose_name_plural = 'Detalles de compra'

    def __str__(self):
        return f'{self.producto.nombre} - Compra #{self.compra.id}'