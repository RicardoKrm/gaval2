from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, F, Avg, Count
from .models import OrdenDeTrabajo, CargaCombustible, Vehiculo

def calcular_costo_km_para_vehiculos(vehiculos, periodo_dias):
    """
    Calcula el costo por kilómetro para una lista de vehículos en un período determinado.
    Devuelve un diccionario {vehiculo_id: costo_por_km}.
    """
    fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
    resultados = {}

    for vehiculo in vehiculos:
        ots_periodo = OrdenDeTrabajo.objects.filter(
            vehiculo=vehiculo,
            estado='FINALIZADA',
            fecha_cierre__gte=fecha_inicio
        )

        costo_total = ots_periodo.aggregate(total=Sum('costo_total'))['total'] or 0

        km_recorridos = 0
        if ots_periodo.exists():
            km_max = ots_periodo.order_by('-kilometraje_cierre').first().kilometraje_cierre
            km_min = ots_periodo.order_by('kilometraje_cierre').first().kilometraje_cierre
            km_recorridos = km_max - km_min if km_max and km_min else 0

        if costo_total > 0 and km_recorridos > 0:
            resultados[vehiculo.id] = costo_total / km_recorridos
        else:
            resultados[vehiculo.id] = 0

    return resultados

def calcular_consumo_combustible_para_vehiculos(vehiculos, periodo_dias):
    """
    Calcula el consumo de combustible (L/100km) para una lista de vehículos.
    Devuelve un diccionario {vehiculo_id: consumo}.
    """
    fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
    resultados = {}

    for vehiculo in vehiculos:
        rendimiento_promedio = CargaCombustible.objects.filter(
            vehiculo=vehiculo,
            fecha_carga__gte=fecha_inicio,
            rendimiento_calculado_kml__isnull=False
        ).aggregate(avg_rendimiento=Avg('rendimiento_calculado_kml'))['avg_rendimiento']

        if rendimiento_promedio and rendimiento_promedio > 0:
            # Convertir de Km/L a L/100km
            consumo_l100km = (1 / rendimiento_promedio) * 100
            resultados[vehiculo.id] = consumo_l100km
        else:
            resultados[vehiculo.id] = 0

    return resultados

def calcular_frecuencia_falla_para_vehiculos(vehiculos, tipo_falla, periodo_dias):
    """
    Calcula la cantidad de veces que ha ocurrido un tipo de falla para un grupo de vehículos.
    Devuelve un diccionario {vehiculo_id: cantidad_de_fallas}.
    """
    fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
    resultados = {}

    for vehiculo in vehiculos:
        conteo_fallas = OrdenDeTrabajo.objects.filter(
            vehiculo=vehiculo,
            tipo='CORRECTIVA',
            tipo_falla=tipo_falla,
            fecha_creacion__gte=fecha_inicio
        ).count()
        resultados[vehiculo.id] = conteo_fallas

    return resultados
