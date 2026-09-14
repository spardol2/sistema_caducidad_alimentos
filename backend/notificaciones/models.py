from django.db import models


class Dispositivo(models.Model):
    class Plataforma(models.TextChoices):
        ANDROID = 'ANDROID', 'Android'
        IOS = 'IOS', 'iOS'
        OTRO = 'OTRO', 'Otro'

    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='dispositivos'
    )

    token_fcm = models.CharField(
        max_length=500,
        unique=True
    )

    plataforma = models.CharField(
        max_length=10,
        choices=Plataforma.choices,
        default=Plataforma.OTRO
    )

    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dispositivos'
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['-ultimo_acceso']

    def __str__(self):
        return f'{self.usuario.email} - {self.plataforma}'


class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        VENCIMIENTO = 'VENCIMIENTO', 'Vencimiento'
        INFORMACION = 'INFORMACION', 'Información'
        SISTEMA = 'SISTEMA', 'Sistema'

    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )

    inventario = models.ForeignKey(
        'productos.Inventario',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones'
    )

    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()

    tipo = models.CharField(
        max_length=15,
        choices=Tipo.choices,
        default=Tipo.INFORMACION
    )

    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_enviada = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notificaciones'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.titulo} - {self.usuario.email}'