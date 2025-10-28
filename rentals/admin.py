from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicle, Reservation

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    # Lista SIN la foto
    list_display = ('make', 'model', 'plate', 'category', 'price', 'available')
    # Asegura que haciendo clic en 'make' abre la edición
    list_display_links = ('make',)

    list_filter = ('available', 'category', 'year')
    search_fields = ('make', 'model', 'plate')

    # En el formulario de edición: mostramos la vista previa debajo del campo imagen
    fields = (
        'make', 'model', 'plate', 'category', 'price', 'year', 'available',
        'image', 'image_preview'
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:180px;border-radius:8px;" />',
                obj.image.url
            )
        return "Sin imagen"
    image_preview.short_description = "Vista previa"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'nombre', 'fecha_inicio', 'fecha_fin', 'status')
    list_filter = ('status',)
    search_fields = ('nombre', 'email', 'telefono')
    date_hierarchy = 'created_at'
