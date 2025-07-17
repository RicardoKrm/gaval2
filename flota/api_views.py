from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vehiculo, OrdenDeTrabajo, Neumatico, Repuesto, DashboardConfig, DashboardWidgetInstance, Widget
from .serializers import (
    VehiculoSerializer, OrdenDeTrabajoSerializer, NeumaticoSerializer, RepuestoSerializer,
    DashboardConfigSerializer, DashboardWidgetInstanceSerializer, WidgetSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from .authentication import APIKeyAuthentication

from rest_framework.throttling import ScopedRateThrottle

class GPSDataWebhook(APIView):
    """
    Endpoint para recibir datos de kilometraje desde un proveedor de GPS.
    """
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny] # La autenticación se maneja con la clave de API, no con usuarios.
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'gps_webhook'

    def post(self, request, *args, **kwargs):
        # El tenant se establece automáticamente por el middleware de django-tenants
        # gracias a la cabecera X-Tenant-Schema que validamos en APIKeyAuthentication.

        data = request.data
        vehicle_identifier = data.get('vehicle_identifier')
        odometer_km = data.get('odometer_km')
        timestamp_str = data.get('timestamp')

        if not all([vehicle_identifier, odometer_km, timestamp_str]):
            return Response(
                {"error": "Faltan datos requeridos (vehicle_identifier, odometer_km, timestamp)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            vehiculo = Vehiculo.objects.get(numero_interno=vehicle_identifier)

            # Validar y convertir datos
            odometer_km = int(odometer_km)
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

            # Actualizar kilometraje solo si es mayor
            if odometer_km > vehiculo.kilometraje_actual:
                vehiculo.kilometraje_actual = odometer_km
                vehiculo.save(update_fields=['kilometraje_actual'])

            # Registrar el evento
            HistorialGPS.objects.create(
                vehiculo=vehiculo,
                kilometraje_reportado=odometer_km,
                timestamp_dato=timestamp,
                payload_completo=data
            )

            return Response({"status": "ok", "message": f"Datos recibidos para el vehículo {vehicle_identifier}."}, status=status.HTTP_200_OK)

        except Vehiculo.DoesNotExist:
            return Response({"error": f"Vehículo con identificador '{vehicle_identifier}' no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError) as e:
            return Response({"error": f"Error en el formato de los datos: {e}"}, status=status.HTTP_400_BAD_REQUEST)


class DashboardConfigViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardConfigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Un usuario solo puede ver y modificar su propio dashboard
        return DashboardConfig.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Asignar el dashboard al usuario actual al crearlo
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'], url_path='widgets')
    def add_widget(self, request, pk=None):
        dashboard = self.get_object()
        serializer = DashboardWidgetInstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dashboard=dashboard)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardWidgetInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardWidgetInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Un usuario solo puede modificar widgets de su propio dashboard
        return DashboardWidgetInstance.objects.filter(dashboard__usuario=self.request.user)

class WidgetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para listar los widgets disponibles.
    """
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
    permission_classes = [IsAuthenticated]

class NeumaticoViewSet(viewsets.ModelViewSet):
    queryset = Neumatico.objects.all()
    serializer_class = NeumaticoSerializer
    permission_classes = [IsAuthenticated]

class RepuestoViewSet(viewsets.ModelViewSet):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer
    permission_classes = [IsAuthenticated]
