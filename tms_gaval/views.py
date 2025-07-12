# tms_gaval/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
# Asegúrate de que 'tenant_context' esté importado, que ya lo estaba
from django_tenants.utils import get_tenant_model, get_tenant_domain_model, tenant_context 
from django.contrib.auth import authenticate, login

# Importa el formulario desde su nueva ubicación en cuentas/forms.py
from cuentas.forms import TenantLoginForm

# Vista para tu landing page (la página principal de localhost:8000)
# Asumiendo que tu landing page está en templates/landing.html
def landing_page(request):
    return render(request, 'landing.html')

# Vista para el login personalizado de tenants
def tenant_login_view(request):
    Tenant = get_tenant_model() # Tu modelo Empresa
    Domain = get_tenant_domain_model() # Tu modelo Domain

    if request.method == 'POST':
        form = TenantLoginForm(request.POST)
        if form.is_valid():
            tenant_identifier = form.cleaned_data['tenant_identifier']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # 1. Intentar encontrar el dominio asociado al identificador de empresa
                domain = Domain.objects.get(domain=tenant_identifier)
                tenant = domain.tenant
            except Domain.DoesNotExist:
                messages.error(request, 'Identificador de empresa o dominio incorrecto. Por favor, verifica el nombre de tu empresa.')
                return render(request, 'flota/tenant_login.html', {'form': form})

            # 2. Autenticar dentro del contexto del tenant encontrado
            # ¡LÍNEA CORREGIDA! Usamos 'tenant_context' que es compatible con tu versión de django-tenants.
            with tenant_context(tenant): 
                user = authenticate(request, username=username, password=password)

            if user is not None:
                # 3. Si la autenticación en el tenant fue exitosa
                if user.is_active:
                    # Loguear al usuario
                    login(request, user)
                    messages.success(request, f'Bienvenido a {tenant.nombre}, {user.username}!')
                    
                    # 4. Redirigir al usuario al DASHBOARD de su TENANT
                    # Usamos el dominio completo (subdominio.localhost:8000)
                    # Ojo: Hardcodeamos el puerto 8000, considera que en producción el puerto podría no ser visible.
                    return redirect(f'http://{domain.domain}:8000/dashboard/')
                else:
                    messages.error(request, 'Tu cuenta de usuario está inactiva. Contacta al soporte.')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos para tu empresa. Por favor, verifica tus credenciales.')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else: # Si el método es GET, muestra el formulario vacío
        form = TenantLoginForm()

    return render(request, 'flota/tenant_login.html', {'form': form}) # Asegúrate que esta es la ruta de tu plantilla de login