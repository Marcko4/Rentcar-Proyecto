from django.db import migrations
from django.contrib.auth import get_user_model


def fill_reservation_data(apps, schema_editor):
    Reservation = apps.get_model('rentals', 'Reservation')
    User = get_user_model()
    
    # Obtener el primer superuser o usuario como fallback
    default_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    if default_user:
        # Actualizar reservas sin usuario
        Reservation.objects.filter(user__isnull=True).update(
            user=default_user,
            nombre=default_user.get_full_name() or default_user.username,
            email=default_user.email or 'admin@example.com',
            telefono='000000000'
        )


def reverse_fill_reservation_data(apps, schema_editor):
    pass  # No necesitamos revertir esto


class Migration(migrations.Migration):
    dependencies = [
        ('rentals', '0003_remove_reservation_client_alter_reservation_options_and_more'),
    ]

    operations = [
        migrations.RunPython(fill_reservation_data, reverse_fill_reservation_data),
    ]