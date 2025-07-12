from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as tms_gaval_views
from flota import views as flota_views # Solo para landing_page

urlpatterns = [
    # Admin global (para gaval)
    path('admin/', admin.site.urls),

    # Nuevo Login Centralizado para Clientes (Desde la Landing Page)
    path('iniciar-sesion/', tms_gaval_views.tenant_login_view, name='tenant_login'),

    # Logout estándar de Django (puede seguir apuntando a tu nueva página de login)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Considera redirigir a 'tenant_login' o 'landing' en LOGOUT_REDIRECT_URL en settings.py
    
    # Tu landing page (la principal, localhost:8000)
    path('', flota_views.landing_page, name='landing'),
    
    # Aquí podrían ir otras URLs públicas, como registro de nuevas empresas (tenants), etc.
]