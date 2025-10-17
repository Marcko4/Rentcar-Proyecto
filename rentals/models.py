from django.db import models


class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    plate = models.CharField(max_length=20, unique=True)
    image = models.CharField(max_length=200, blank=True, help_text='Ruta relativa en static/images, p.ej. cars/car1.svg')
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text='Precio en guaraníes (PYG)')
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate})"


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('X', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva {self.id} - {self.vehicle} para {self.client}"
