from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q, Min, Max  # <-- filtros/orden y rangos de precio
from django.template.loader import get_template
from io import BytesIO
from datetime import timedelta
from .forms import CustomUserCreationForm, LoginForm, RentForm
from .models import Vehicle, Reservation


def home(request):
    vehicles = Vehicle.objects.filter(available=True)

    # --- Filtros desde la querystring ---
    q = request.GET.get('q', '').strip()            # texto libre (marca/modelo/placa)
    vtype = request.GET.get('type', '').strip()     # categoría (Vehicle.CATEGORY_CHOICES)
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    year = request.GET.get('year', '').strip()
    sort = request.GET.get('sort', '').strip()

    if q:
        vehicles = vehicles.filter(
            Q(make__icontains=q) |
            Q(model__icontains=q) |
            Q(plate__icontains=q)
        )

    if vtype:
        # si el proyecto aún no tiene el campo category, esta línea no se ejecutará (usa el template acorde)
        vehicles = vehicles.filter(category=vtype)

    def to_int(val):
        try:
            return int(str(val).replace('.', '').replace(',', ''))
        except Exception:
            return None

    mp = to_int(min_price)
    if mp is not None:
        vehicles = vehicles.filter(price__gte=mp)

    xp = to_int(max_price)
    if xp is not None:
        vehicles = vehicles.filter(price__lte=xp)

    if year:
        try:
            vehicles = vehicles.filter(year=int(year))
        except Exception:
            pass

    order_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'year_desc': '-year',
        'year_asc': 'year',
        'newest': '-id',
    }
    if sort in order_map:
        vehicles = vehicles.order_by(order_map[sort])

    # Datos auxiliares para el formulario de filtros
    years = (Vehicle.objects
                    .filter(available=True)
                    .values_list('year', flat=True)
                    .distinct().order_by('-year'))
    categories = getattr(Vehicle, 'CATEGORY_CHOICES', [])
    price_bounds = Vehicle.objects.filter(available=True).aggregate(
        min=Min('price'), max=Max('price')
    )

    context = {
        'vehicles': vehicles,
        'filters': {
            'q': q, 'type': vtype, 'min_price': min_price,
            'max_price': max_price, 'year': year, 'sort': sort
        },
        'years': years,
        'categories': categories,
        'price_bounds': price_bounds,
    }
    return render(request, 'rentals/home.html', context)


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
                fecha_fin=form.cleaned_data['fecha_inicio'] + timedelta(days=form.cleaned_data['dias']),
                comentarios=form.cleaned_data['comentarios']
            )
            reservation.save()
            messages.success(request, f'¡Tu solicitud para rentar el {vehicle.make} {vehicle.model} ha sido enviada! Descargando comprobante...')
            return redirect('rentals:reservation_invoice_download', reservation.id)
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


# ---------- Comprobante / Factura PDF ----------
@login_required
def reservation_invoice(request, reservation_id):
    # Importación diferida para evitar errores si la librería no está instalada aún
    try:
        from xhtml2pdf import pisa  # type: ignore
    except Exception:
        pisa = None
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not (request.user.is_superuser or request.user.is_staff or reservation.user == request.user):
        return HttpResponseForbidden("No tienes permiso para ver este comprobante.")

    days = (reservation.fecha_fin - reservation.fecha_inicio).days
    days = max(1, days)
    total = reservation.vehicle.price * days

    context = {
        'reservation': reservation,
        'days': days,
        'total': total,
    }

    # Modo HTML con botón "Descargar PDF"
    template = get_template('rentals/invoice.html')
    html = template.render({**context, 'show_download': True})
    return HttpResponse(html)


@login_required
def reservation_invoice_download(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not (request.user.is_superuser or request.user.is_staff or reservation.user == request.user):
        return HttpResponseForbidden("No tienes permiso para descargar este comprobante.")

    days = (reservation.fecha_fin - reservation.fecha_inicio).days
    days = max(1, days)
    total = reservation.vehicle.price * days

    context = {
        'reservation': reservation,
        'days': days,
        'total': total,
    }

    template = get_template('rentals/invoice.html')
    html = template.render({**context, 'show_download': False})

    try:
        from xhtml2pdf import pisa  # type: ignore
    except Exception as e:
        return HttpResponse(f"No se pudo generar el PDF (librería faltante): {e}", status=500)

    result = BytesIO()
    pdf_status = pisa.CreatePDF(src=html, dest=result, encoding='utf-8')
    if pdf_status.err:
        return HttpResponse("Ocurrió un error al generar el PDF.", status=500)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = f"comprobante_reserva_{reservation.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
