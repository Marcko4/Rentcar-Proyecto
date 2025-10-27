
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'rentals'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='rentals/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='rentals:home'), name='logout'),
    path('rent/<int:vehicle_id>/', views.rent_vehicle, name='rent_vehicle'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('admin/rentals/', views.admin_rentals, name='admin_rentals'),
    path('admin/rentals/<int:reservation_id>/update-status/', views.update_reservation_status, name='update_reservation_status'),
]
