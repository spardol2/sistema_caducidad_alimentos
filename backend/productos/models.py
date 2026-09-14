from django.conf import settings
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )

    unidad_medida = models.CharField(max_length=50)
    cantidad_presentacion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        if self.marca:
            return f'{self.nombre} - {self.marca}'
        return self.nombre


class ProductoCodigo(models.Model):
    class Tipo(models.TextChoices):
        EAN13 = 'EAN13', 'EAN-13'
        EAN8 = 'EAN8', 'EAN-8'
        UPC = 'UPC', 'UPC'
        QR = 'QR', 'Código QR'
        OTRO = 'OTRO', 'Otro'

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='codigos'
    )

    codigo = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.OTRO
    )

    class Meta:
        db_table = 'productos_codigos'
        verbose_name = 'Código de producto'
        verbose_name_plural = 'Códigos de producto'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.producto.nombre}'
class Inventario(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        AGOTADO = 'AGOTADO', 'Agotado'
        VENCIDO = 'VENCIDO', 'Vencido'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventario'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='inventarios'
    )

    compra = models.ForeignKey(
        'compras.Compra',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventarios'
    )

    cantidad_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cantidad_disponible = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fecha_compra = models.DateField()
    fecha_vencimiento = models.DateField()

    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventarios'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['fecha_vencimiento']

    def __str__(self):
        return (
            f'{self.producto.nombre} - '
            f'{self.usuario.email} - '
            f'Vence: {self.fecha_vencimiento}'
        )