from django import forms

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
