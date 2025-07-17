from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from tenants.models import Empresa
from flota.models import Vehiculo, OrdenDeTrabajo

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser)
def dashboard_superadmin(request):
    """
    Dashboard principal para el Super Administrador.
    Agrega datos de todos los tenants.
    """
    all_tenants = Empresa.objects.all()
    stats_por_tenant = []

    total_vehiculos_global = 0
    total_ots_global = 0

    for tenant in all_tenants:
        connection.set_tenant(tenant)

        num_vehiculos = Vehiculo.objects.count()
        num_ots = OrdenDeTrabajo.objects.count()

        stats_por_tenant.append({
            'tenant': tenant,
            'num_vehiculos': num_vehiculos,
            'num_ots': num_ots,
        })

        total_vehiculos_global += num_vehiculos
        total_ots_global += num_ots

    # Volver al esquema público al final
    connection.set_schema_to_public()

    context = {
        'stats_por_tenant': stats_por_tenant,
        'total_tenants': all_tenants.count(),
        'total_vehiculos_global': total_vehiculos_global,
        'total_ots_global': total_ots_global,
    }

    return render(request, 'superadmin/dashboard.html', context)
