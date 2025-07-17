import csv
from io import StringIO
from datetime import datetime
from celery import shared_task
from django.core.files.base import ContentFile
from django.urls import reverse

from .models import OrdenDeTrabajo, Notificacion, User, Neumatico, ReglaAlerta, Vehiculo
from django.contrib.auth.models import Group
from .logic import (
    calcular_costo_km_para_vehiculos,
    calcular_consumo_combustible_para_vehiculos,
    calcular_frecuencia_falla_para_vehiculos
)

@shared_task
def generar_reporte_ots_task(user_id, filtros):
    """
    Tarea asíncrona de Celery para generar un reporte de OTs en formato CSV.
    """
    try:
        # Reconstruir el queryset basado en los filtros pasados
        # Nota: Pasamos valores simples (IDs, strings) en lugar de objetos complejos.
        ordenes = OrdenDeTrabajo.objects.filter(estado='FINALIZADA')

        start_date_str = filtros.get('start_date')
        end_date_str = filtros.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            ordenes = ordenes.filter(fecha_cierre__date__range=[start_date, end_date])

        # Aquí se podrían añadir más filtros si se pasaran en el diccionario 'filtros'

        ordenes = ordenes.select_related(
            'vehiculo', 'vehiculo__modelo', 'responsable', 'tipo_falla'
        ).prefetch_related('tareas_realizadas').order_by('-fecha_creacion')

        # Usar StringIO para crear el archivo CSV en memoria
        string_io = StringIO()
        writer = csv.writer(string_io, delimiter=';')

        # Escribir encabezados
        writer.writerow([
            'Folio OT', 'Estado', 'Tipo', 'Vehiculo Numero', 'Vehiculo Patente',
            'Fecha Creacion', 'Fecha Cierre', 'Kilometraje Apertura', 'Kilometraje Cierre',
            'Responsable', 'Costo Total', 'TFS (Minutos)', 'Tipo de Falla', 'Tareas'
        ])

        # Escribir datos
        for ot in ordenes:
            tareas_str = ", ".join([tarea.descripcion for tarea in ot.tareas_realizadas.all()])
            writer.writerow([
                ot.folio,
                ot.get_estado_display(),
                ot.get_tipo_display(),
                ot.vehiculo.numero_interno,
                ot.vehiculo.patente or '',
                ot.fecha_creacion.strftime('%d-%m-%Y %H:%M') if ot.fecha_creacion else '',
                ot.fecha_cierre.strftime('%d-%m-%Y %H:%M') if ot.fecha_cierre else '',
                ot.kilometraje_apertura or '',
                ot.kilometraje_cierre or '',
                ot.responsable.username if ot.responsable else 'N/A',
                f"{ot.costo_total:.2f}".replace('.',','),
                ot.tfs_minutos,
                ot.tipo_falla.descripcion if ot.tipo_falla else 'N/A',
                tareas_str
            ])

        # Crear una notificación para el usuario cuando el reporte esté listo
        usuario = User.objects.get(pk=user_id)

        # Guardar el archivo en un modelo o en el sistema de archivos y generar un enlace
        # Por simplicidad aquí, no guardaremos el archivo, solo notificaremos.
        # En una implementación real, se guardaría el archivo y se proporcionaría un enlace de descarga.
        # Por ejemplo:
        # from django.core.files.storage import default_storage
        # file_name = f"reportes/ots_{usuario.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        # file_content = ContentFile(string_io.getvalue().encode('utf-8'))
        # file_path = default_storage.save(file_name, file_content)
        # download_url = default_storage.url(file_path)

        mensaje = "Tu reporte de Órdenes de Trabajo está listo."
        # url_destino = download_url # En una implementación real
        url_destino = reverse('reportes_dashboard') # Por ahora, lo mandamos de vuelta al dashboard

        Notificacion.objects.create(
            usuario_destino=usuario,
            mensaje=mensaje,
            url_destino=url_destino
        )

        return f"Reporte generado para el usuario {user_id} con {ordenes.count()} OTs."

    except Exception as e:
        # En caso de error, podríamos notificar al usuario también
        usuario = User.objects.get(pk=user_id)
        Notificacion.objects.create(
            usuario_destino=usuario,
            mensaje=f"Error al generar tu reporte: {e}",
            url_destino=reverse('reportes_dashboard')
        )
        return f"Error al generar reporte para el usuario {user_id}: {e}"

@shared_task
def revisar_estado_neumaticos_task():
    """
    Tarea periódica para revisar el estado de los neumáticos y generar alertas.
    """
    KILOMETRAJE_ALERTA = 80000 # Umbral de KM para alerta, podría ser un campo en el modelo Neumatico en el futuro

    # Obtener los usuarios que deben ser notificados (Supervisores y Administradores)
    try:
        grupos_destino = Group.objects.filter(name__in=['Supervisor', 'Administrador'])
        usuarios_destino = User.objects.filter(groups__in=grupos_destino).distinct()
    except Group.DoesNotExist:
        return "No se encontraron los grupos de destino. No se enviarán notificaciones."

    if not usuarios_destino.exists():
        return "No hay usuarios en los grupos de destino. No se enviarán notificaciones."

    # Encontrar neumáticos que necesiten atención
    neumaticos_para_revisar = Neumatico.objects.exclude(estado='DESECHADO')

    notificaciones_creadas = 0
    for neumatico in neumaticos_para_revisar:
        mensaje = None
        # Comprobar desgaste
        if neumatico.profundidad_surco_actual_mm <= neumatico.profundidad_surco_limite_mm:
            mensaje = f"Alerta de Desgaste: El neumático {neumatico.dot} ha alcanzado el límite de profundidad del surco ({neumatico.profundidad_surco_actual_mm}mm)."

        # Comprobar kilometraje
        elif neumatico.kilometraje_acumulado >= KILOMETRAJE_ALERTA:
            mensaje = f"Alerta de Kilometraje: El neumático {neumatico.dot} ha superado los {KILOMETRAJE_ALERTA} km de uso ({neumatico.kilometraje_acumulado} km)."

        # Si se generó un mensaje, crear las notificaciones
        if mensaje:
            for usuario in usuarios_destino:
                # Evitar crear notificaciones duplicadas si ya existe una similar reciente
                if not Notificacion.objects.filter(usuario_destino=usuario, mensaje=mensaje).exists():
                    Notificacion.objects.create(
                        usuario_destino=usuario,
                        mensaje=mensaje,
                        url_destino=reverse('neumatico_detail', kwargs={'pk': neumatico.pk})
                    )
                    notificaciones_creadas += 1

    return f"Revisión de neumáticos completada. Se crearon {notificaciones_creadas} notificaciones."


@shared_task
def evaluar_reglas_alerta_task():
    """
    Tarea periódica que evalúa todas las Reglas de Alerta activas.
    """
    reglas_activas = ReglaAlerta.objects.filter(activa=True)
    if not reglas_activas.exists():
        return "No hay reglas de alerta activas para evaluar."

    usuarios_destino = User.objects.filter(groups__name__in=['Supervisor', 'Administrador']).distinct()
    if not usuarios_destino.exists():
        return "No hay usuarios supervisores/administradores para notificar."

    for regla in reglas_activas:
        # Determinar el conjunto de vehículos a evaluar
        if regla.modelo_vehiculo.exists():
            vehiculos_a_evaluar = Vehiculo.objects.filter(modelo__in=regla.modelo_vehiculo.all())
        else:
            vehiculos_a_evaluar = Vehiculo.objects.all()

        # Calcular la métrica para los vehículos
        resultados_metricas = {}
        if regla.metrica == 'COSTO_KM':
            resultados_metricas = calcular_costo_km_para_vehiculos(vehiculos_a_evaluar, regla.periodo_dias)
        elif regla.metrica == 'CONSUMO_COMBUSTIBLE':
            resultados_metricas = calcular_consumo_combustible_para_vehiculos(vehiculos_a_evaluar, regla.periodo_dias)
        elif regla.metrica == 'FRECUENCIA_FALLA':
            if regla.tipo_falla_asociada:
                resultados_metricas = calcular_frecuencia_falla_para_vehiculos(vehiculos_a_evaluar, regla.tipo_falla_asociada, regla.periodo_dias)

        # Evaluar la regla para cada vehículo
        for vehiculo_id, valor_actual in resultados_metricas.items():
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
            condicion_cumplida = False
            if regla.operador == 'MAYOR_QUE' and valor_actual > regla.valor_umbral:
                condicion_cumplida = True
            elif regla.operador == 'MENOR_QUE' and valor_actual < regla.valor_umbral:
                condicion_cumplida = True
            elif regla.operador == 'IGUAL_A' and valor_actual == regla.valor_umbral:
                condicion_cumplida = True

            if condicion_cumplida:
                mensaje = f"Alerta '{regla.nombre}': El vehículo {vehiculo.numero_interno} ha registrado un valor de {valor_actual:.2f}, superando el umbral de {regla.valor_umbral}."
                for usuario in usuarios_destino:
                    if not Notificacion.objects.filter(usuario_destino=usuario, mensaje=mensaje).exists():
                        Notificacion.objects.create(
                            usuario_destino=usuario,
                            mensaje=mensaje,
                            url_destino=reverse('historial_vehiculo', kwargs={'pk': vehiculo.pk})
                        )

    return f"Evaluación de {reglas_activas.count()} reglas de alerta completada."
