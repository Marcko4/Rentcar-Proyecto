from django.contrib import admin
from .models import Vehicle, Reservation

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'plate', 'category', 'price', 'available')  
    list_filter = ('available', 'category', 'year')  
    search_fields = ('make', 'model', 'plate')       



@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'nombre', 'fecha_inicio', 'fecha_fin', 'status')
    list_filter = ('status',)
    search_fields = ('nombre', 'email', 'telefono')
    date_hierarchy = 'created_at'
