from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
import os

from .models import Vehicle, Reservation


def _scan_vehicle_images():
    results = set()

    static_dirs = getattr(settings, 'STATICFILES_DIRS', []) or []
    for base in static_dirs:
        images_root = os.path.join(base, 'images')
        vehicles_dir = os.path.join(images_root, 'vehicles')
        if os.path.isdir(vehicles_dir):
            for root, _, files in os.walk(vehicles_dir):
                for f in files:
                    abs_path = os.path.join(root, f)
                    rel_to_images = os.path.relpath(abs_path, images_root).replace('\\', '/')
                    results.add(rel_to_images)

    app_images_root = os.path.join(settings.BASE_DIR, 'rentals', 'static', 'images')
    app_vehicles_dir = os.path.join(app_images_root, 'vehicles')
    if os.path.isdir(app_vehicles_dir):
        for root, _, files in os.walk(app_vehicles_dir):
            for f in files:
                abs_path = os.path.join(root, f)
                rel_to_images = os.path.relpath(abs_path, app_images_root).replace('\\', '/')
                results.add(rel_to_images)

    return sorted(results)


class VehicleAdminForm(forms.ModelForm):
    image = forms.ChoiceField(choices=[], required=False, label="Imagen")

    class Meta:
        model = Vehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = []
        for p in _scan_vehicle_images():
            filename = os.path.basename(p)
            options.append((p, filename))
        self.fields['image'].choices = [('', '--- Sin imagen ---')] + options


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'plate', 'category', 'price', 'available')
    list_display_links = ('make',)
    list_filter = ('available', 'category', 'year')
    search_fields = ('make', 'model', 'plate')
    form = VehicleAdminForm

    fields = (
        'make', 'model', 'plate', 'category', 'price', 'year', 'available',
        'image', 'image_preview'
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            try:
                url = staticfiles_storage.url(f'images/{obj.image}')
                return format_html('<img src="{}" style="max-height:180px;border-radius:8px;" />', url)
            except Exception:
                return f"No se pudo resolver: images/{obj.image}"
        return "Sin imagen"
    image_preview.short_description = "Vista previa"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'nombre', 'fecha_inicio', 'fecha_fin', 'status')
    list_filter = ('status',)
    search_fields = ('nombre', 'email', 'telefono')
    date_hierarchy = 'created_at'
