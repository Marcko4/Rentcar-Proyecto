from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'email@ejemplo.com'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add bootstrap classes
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario o email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'contraseña'}))


class RentForm(forms.Form):
    nombre = forms.CharField(label="Nombre completo", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Tu nombre completo'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    telefono = forms.CharField(label="Teléfono", max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Tu número de contacto'}))
    fecha_inicio = forms.DateField(label="Fecha de inicio", widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(label="Fecha de fin", widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date'}))
    comentarios = forms.CharField(label="Comentarios", required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Detalles adicionales', 'rows': 2}))

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")
