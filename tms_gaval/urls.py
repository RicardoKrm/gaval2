from django.contrib import admin
from django.urls import path, include # Asegúrate de que 'include' esté importado
from django.contrib.auth import views as auth_views # Lo mantendremos para el logout estándar
# Importa las vistas que acabamos de crear en tms_gaval/views.py (Paso 2 del plan anterior)
from . import views as tms_gaval_views # Alias para tus vistas principales

# Si tu landing_page y dashboard_flota están en flota.views, asegúrate que se importen desde ahí
from flota import views as flota_views

urlpatterns = [
    # Admin global (para gaval)
    path('admin/', admin.site.urls),

    # Nuevo Login Centralizado para Clientes (Desde la Landing Page)
    path('iniciar-sesion/', tms_gaval_views.tenant_login_view, name='tenant_login'), # <--- NUEVA URL

    # Logout estándar de Django (puede seguir apuntando a tu nueva página de login)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Tu landing page (la principal, localhost:8000)
    # Asumo que landing_page sigue en flota_views como en tu código original
    path('', flota_views.landing_page, name='landing'),
    
    # Dashboard principal (accesible desde el tenant, ej: pulser.localhost:8000/dashboard/)
    path('dashboard/', flota_views.dashboard_flota, name='dashboard'),
    
    # El resto de tus rutas de la aplicación 'flota' permanecen igual
    # (Estas serán accesibles sólo cuando el dominio sea de un tenant, ej: pulser.localhost:8000/inventario/)
    path('api/ot-eventos/', flota_views.ot_eventos_api, name='ot_eventos_api'),
    path('inventario/', flota_views.repuesto_list, name='repuesto_list'),
    path('inventario/nuevo/', flota_views.repuesto_create, name='repuesto_create'),
    path('inventario/<int:pk>/', flota_views.repuesto_detail, name='repuesto_detail'),
    path('inventario/<int:pk>/editar/', flota_views.repuesto_update, name='repuesto_update'),
    path('inventario/<int:repuesto_pk>/registrar-movimiento/', flota_views.registrar_movimiento, name='registrar_movimiento'),
    path('ordenes/', flota_views.orden_trabajo_list, name='ot_list'),
    path('ordenes/<int:pk>/', flota_views.orden_trabajo_detail, name='ot_detail'),
    path('ordenes/<int:pk>/cambiar-estado/', flota_views.cambiar_estado_ot, name='cambiar_estado_ot'),
    path('ordenes/<int:pk>/pdf/', flota_views.generar_ot_pdf, name='generar_ot_pdf'),
    path('pizarra-programacion/', flota_views.pizarra_programacion, name='pizarra_programacion'),
    path('vehiculo/<int:pk>/actualizar-km/', flota_views.actualizar_km_vehiculo, name='actualizar_km'),
    path('indicadores/', flota_views.indicadores_dashboard, name='indicadores_dashboard'),
    path('analisis-fallas/', flota_views.analisis_fallas, name='analisis_fallas'),
    path('analisis-avanzado/', flota_views.analisis_avanzado, name='analisis_avanzado'),
    path('carga-masiva/', flota_views.carga_masiva, name='carga_masiva'),
    path('vehiculo/<int:pk>/historial/', flota_views.historial_vehiculo, name='historial_vehiculo'),
    path('vehiculo/<int:pk>/analisis-km/', flota_views.analisis_km_vehiculo, name='analisis_km_vehiculo'), # Usar flota_views
    path('orden-trabajo/<int:ot_pk>/eliminar-tarea/<int:tarea_pk>/', flota_views.eliminar_tarea_ot, name='eliminar_tarea_ot'), # Usar flota_views
    path('orden-trabajo/<int:ot_pk>/eliminar-insumo/<int:detalle_pk>/', flota_views.eliminar_insumo_ot, name='eliminar_insumo_ot'), # Usar flota_views
    path('api/mecanicos-recursos/', flota_views.mecanicos_recursos_api, name='mecanicos_recursos_api'),
    path('api/ot-actualizar-fecha/<int:pk>/', flota_views.actualizar_fecha_ot_api, name='actualizar_fecha_ot_api'),
    path('api/repuestos/search/', flota_views.repuesto_search_api, name='repuesto_search_api'),
    path('api/ots/add-repuesto/', flota_views.add_repuesto_a_ot_api, name='add_repuesto_a_ot_api'),
    path('pizarra-combustible/', flota_views.pizarra_combustible, name='pizarra_combustible'),
    path('combustible/registrar/', flota_views.registrar_carga_combustible, name='registrar_carga_combustible'),
    path('ot/<int:pk>/autorizar-horas-extra/', flota_views.autorizar_horas_extra, name='autorizar_horas_extra'),
    path('notificaciones/', flota_views.lista_notificaciones, name='lista_notificaciones'),
    path('api/notificaciones/marcar-leidas/', flota_views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),
    path('administracion/usuarios/', flota_views.lista_usuarios, name='lista_usuarios'),
    path('administracion/usuarios/crear/', flota_views.crear_usuario, name='crear_usuario'),
    path('administracion/usuarios/editar/<int:user_id>/', flota_views.editar_usuario, name='editar_usuario'),
    path('kpi-rrhh/', flota_views.kpi_rrhh_dashboard, name='kpi_rrhh_dashboard'),
    path('reportes/', flota_views.reportes_dashboard, name='reportes_dashboard'),
    path('exportar/vehiculos-csv/', flota_views.export_vehiculos_csv, name='export_vehiculos_csv'),
    path('exportar/repuestos-csv/', flota_views.export_repuestos_csv, name='export_repuestos_csv'),
    path('exportar/ots-csv/', flota_views.export_ots_csv, name='export_ots_csv'),
]