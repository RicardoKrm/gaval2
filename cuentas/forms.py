# cuentas/forms.py

from django import forms
from django.contrib.auth.models import User, Group

class UsuarioCreacionForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=150, widget=forms.TextInput(attrs={'class': 'custom-input'}))
    first_name = forms.CharField(label="Nombre", max_length=150, widget=forms.TextInput(attrs={'class': 'custom-input'}))
    last_name = forms.CharField(label="Apellido", max_length=150, widget=forms.TextInput(attrs={'class': 'custom-input'}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'custom-input'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'custom-input'}))
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name='Administrador'),
        label="Rol del Usuario",
        widget=forms.Select(attrs={'class': 'custom-input select2'})
    )

class UsuarioEdicionForm(forms.Form):
    first_name = forms.CharField(label="Nombre", max_length=150, widget=forms.TextInput(attrs={'class': 'custom-input'}))
    last_name = forms.CharField(label="Apellido", max_length=150, widget=forms.TextInput(attrs={'class': 'custom-input'}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'custom-input'}))
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name='Administrador'),
        label="Rol del Usuario",
        widget=forms.Select(attrs={'class': 'custom-input select2'})
    )

class TenantLoginForm(forms.Form):
    # Campo para el identificador de la empresa (el subdominio)
    tenant_identifier = forms.CharField(
        label='Identificador de Empresa',
        max_length=100,
        help_text='Ejemplo: "pulser" si tu dirección es pulser.pulser.cl' # Ajusta este help_text para tus clientes
    )
    username = forms.CharField(label='Nombre de Usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
