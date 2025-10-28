from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('AUTO', 'Auto'),
        ('SUV', 'SUV'),
        ('PICKUP', 'Camioneta'),
        ('MOTO', 'Moto'),
        ('VAN', 'Van'),
        ('CAMION', 'Camión'),
        ('OTRO', 'Otro'),
    ]

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    plate = models.CharField(max_length=20, unique=True)

    # CAMBIADO: antes era CharField. Ahora ImageField (aparece input con explorador de archivos)
    image = models.ImageField(
        upload_to='vehicles/', blank=True, null=True, verbose_name='Foto'
    )

    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text='Precio en guaraníes (PYG)')
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)

    # Tipo/categoría 
    category = models.CharField(
        max_length=12, choices=CATEGORY_CHOICES, blank=True, null=True, verbose_name='Tipo'
    )

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate})"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comentarios = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reserva de {self.vehicle} por {self.user.username}"
