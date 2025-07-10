# flota/context_processors.py

from .models import Notificacion
from .decorators import es_personal_operativo, es_administrador, es_gerente, es_mecanico, es_supervisor
from django_tenants.utils import get_tenant_model # <-- Añadir esta importación
from django.db import connection # <-- Añadir esta importación

def notificaciones_processor(request):
    # Inicializa todas las banderas a False y contadores a 0
    context = {
        'es_mecanico': False, 'es_supervisor': False, 'es_administrador': False,
        'es_gerente': False, 'es_personal_operativo': False,
        'notificaciones_no_leidas_count': 0, 'notificaciones_recientes_no_leidas': []
    }

    if not request.user.is_authenticated:
        return context # Si no está autenticado, devuelve el contexto básico

    # Lógica de Roles (estas funciones de decorators.py no dependen del esquema de DB)
    context['es_mecanico'] = es_mecanico(request.user)
    context['es_supervisor'] = es_supervisor(request.user)
    context['es_administrador'] = es_administrador(request.user)
    context['es_gerente'] = es_gerente(request.user)
    context['es_personal_operativo'] = es_personal_operativo(request.user)

    # Lógica de Notificaciones: ¡SOLO si estamos en un esquema de TENANT!
    # request.tenant estará disponible si TenantMainMiddleware ha encontrado un tenant por el dominio.
    # connection.schema_name nos dice en qué esquema de DB estamos actualmente.
    if hasattr(request, 'tenant') and connection.schema_name != 'public':
        try:
            # Las notificaciones se buscan en el esquema del tenant actual
            notificaciones_no_leidas_count = Notificacion.objects.filter(usuario_destino=request.user, leida=False).count()
            notificaciones_recientes_no_leidas = Notificacion.objects.filter(usuario_destino=request.user, leida=False).order_by('-fecha_creacion')[:5]

            context['notificaciones_no_leidas_count'] = notificaciones_no_leidas_count
            context['notificaciones_recientes_no_leidas'] = notificaciones_recientes_no_leidas
        except Exception as e:
            # Esto captura si la tabla Notificacion no existe en el esquema actual (ej. si es un tenant nuevo sin migrar)
            print(f"DEBUG: Error al obtener notificaciones en context_processor: {e}")
            # Mantiene los contadores en 0
    
    return context