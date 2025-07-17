from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import (
    VehiculoViewSet, OrdenDeTrabajoViewSet, NeumaticoViewSet, RepuestoViewSet,
    DashboardConfigViewSet, DashboardWidgetInstanceViewSet, WidgetViewSet,
    GPSDataWebhook
)

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'ordenes-trabajo', OrdenDeTrabajoViewSet)
router.register(r'neumaticos', NeumaticoViewSet)
router.register(r'repuestos', RepuestoViewSet)
router.register(r'dashboards', DashboardConfigViewSet, basename='dashboardconfig')
router.register(r'dashboard-widgets', DashboardWidgetInstanceViewSet, basename='dashboardwidgetinstance')
router.register(r'widgets', WidgetViewSet)


urlpatterns = [
    path('gps-webhook/', GPSDataWebhook.as_view(), name='gps_webhook'),
] + router.urls
