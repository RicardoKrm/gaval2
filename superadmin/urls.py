from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_superadmin, name='superadmin_dashboard'),
    # Aquí se añadirán más URLs para las comparativas específicas
]
