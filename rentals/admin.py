from django.contrib import admin
from .models import Vehicle, Reservation

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'plate', 'price', 'available')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'nombre', 'fecha_inicio', 'fecha_fin', 'status')
    list_filter = ('status',)
    search_fields = ('nombre', 'email', 'telefono')
    date_hierarchy = 'created_at'
