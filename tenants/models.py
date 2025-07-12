# tenants/models.py
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Empresa(TenantMixin):
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=200, blank=True, null=True)
    creado_en = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def __str__(self):
        return self.nombre

class Domain(DomainMixin):
    # Modelo para asociar dominios/subdominios a un tenant.
    # Ej: 'cliente1.gaval.com', 'cliente2.gaval.com'
    pass

