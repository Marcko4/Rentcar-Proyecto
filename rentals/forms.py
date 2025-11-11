# rentals/forms.py
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@ejemplo.com'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario o email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'contraseña'})
    )


class RentForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de contacto'})
    )

    fecha_inicio = forms.DateField(
        label="Fecha de inicio",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    fecha_fin = forms.DateField(
        required=False,
        label="Fecha de fin",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    dias = forms.IntegerField(
        required=False,
        label="Días de renta",
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad de días',
            'min': 1
        })
    )

    comentarios = forms.CharField(
        label="Comentarios",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Detalles adicionales',
            'rows': 2
        })
    )

    def clean(self):
        cleaned = super().clean()

        fecha_inicio = cleaned.get('fecha_inicio')
        fecha_fin = cleaned.get('fecha_fin')
        dias = cleaned.get('dias')

        if not fecha_inicio:
            raise forms.ValidationError("Debes indicar la fecha de inicio.")

        if fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError("La fecha de fin debe ser posterior o igual a la fecha de inicio.")
            cleaned['dias'] = max(1, (fecha_fin - fecha_inicio).days)
            return cleaned

        if dias:
            cleaned['fecha_fin'] = fecha_inicio + timedelta(days=dias)
            return cleaned

        raise forms.ValidationError("Indica al menos uno: 'fecha_fin' o 'dias'.")
