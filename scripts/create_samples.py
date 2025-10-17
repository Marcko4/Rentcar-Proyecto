import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentcar.settings')
django.setup()

from rentals.models import Vehicle

# Eliminar vehículos de ejemplo si existen
Vehicle.objects.filter(plate__in=['ABC123','DEF456','GHI789']).delete()

# Crear vehículos con las nuevas imágenes
Vehicle.objects.create(make='Toyota', model='Corolla', plate='ABC123', price=250000, image='car1.jpg', year=2019)
Vehicle.objects.create(make='Hyundai', model='Accent', plate='DEF456', price=220000, image='car2.jpg', year=2018)
Vehicle.objects.create(make='Kia', model='Rio', plate='GHI789', price=230000, image='car3.jpg', year=2020)
print('created sample vehicles')
