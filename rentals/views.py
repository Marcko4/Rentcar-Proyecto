from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, LoginForm, RentForm
from .models import Vehicle, Reservation


def home(request):
    vehicles = Vehicle.objects.filter(available=True)
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


@login_required
def rent_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            reservation = Reservation(
                vehicle=vehicle,
                user=request.user,
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono'],
                fecha_inicio=form.cleaned_data['fecha_inicio'],
                fecha_fin=form.cleaned_data['fecha_fin'],
                comentarios=form.cleaned_data['comentarios']
            )
            reservation.save()
            messages.success(request, f'¡Tu solicitud para rentar el {vehicle.make} {vehicle.model} ha sido enviada!')
            return redirect('rentals:my_rentals')
    else:
        initial_data = {
            'nombre': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email
        }
        form = RentForm(initial=initial_data)
    return render(request, 'rentals/rent_form.html', {'form': form, 'vehicle': vehicle})


@login_required
def my_rentals(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'rentals/my_rentals.html', {'reservations': reservations})


def is_admin(user):
    return user.is_superuser or user.is_staff


@user_passes_test(is_admin)
def admin_rentals(request):
    filter_status = request.GET.get('filter')
    reservations = Reservation.objects.all()
    
    if filter_status and filter_status != 'all':
        reservations = reservations.filter(status=filter_status)
    
    context = {
        'reservations': reservations,
        'status_choices': Reservation.STATUS_CHOICES
    }
    return render(request, 'rentals/admin_rentals.html', context)


@user_passes_test(is_admin)
def update_reservation_status(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        new_status = request.POST.get('status')
        if new_status in dict(Reservation.STATUS_CHOICES):
            reservation.status = new_status
            reservation.save()
            messages.success(request, f'Estado de la reserva actualizado a {reservation.get_status_display()}')
    return redirect('rentals:admin_rentals')