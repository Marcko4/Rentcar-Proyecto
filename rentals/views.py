
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .models import Vehicle
from .rent_forms import RentForm

def rent_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            # Aquí podrías guardar la reserva en la base de datos
            messages.success(request, f"¡Solicitud enviada para rentar el {vehicle.make} {vehicle.model}!")
            return redirect('rentals:home')
    else:
        form = RentForm()
    return render(request, 'rentals/rent_form.html', {'form': form, 'vehicle': vehicle})


def home(request):
    vehicles = Vehicle.objects.all()[:10]
    return render(request, 'rentals/home.html', {'vehicles': vehicles})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada correctamente. Ahora puedes iniciar sesión.')
            return redirect('rentals:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rentals/register.html', {'form': form})
