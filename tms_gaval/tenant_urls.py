# tms_gaval/tenant_urls.py
from django.urls import path, include
from flota import views as flota_views
from cuentas import views as cuentas_views # Importar vistas de cuentas

urlpatterns = [
    # Dashboard principal
    path('dashboard/', flota_views.dashboard_flota, name='dashboard'),

    # URLs de la aplicación 'flota'
    path('api/ot-eventos/', flota_views.ot_eventos_api, name='ot_eventos_api'),
    path('inventario/', flota_views.repuesto_list, name='repuesto_list'),
    path('inventario/nuevo/', flota_views.repuesto_create, name='repuesto_create'),
    path('inventario/<int:pk>/', flota_views.repuesto_detail, name='repuesto_detail'),
    path('inventario/<int:pk>/editar/', flota_views.repuesto_update, name='repuesto_update'),
    path('inventario/<int:repuesto_pk>/registrar-movimiento/', flota_views.registrar_movimiento, name='registrar_movimiento'),
    path('ordenes/', flota_views.orden_trabajo_list, name='ot_list'),
    path('ordenes/<int:pk>/', flota_views.orden_trabajo_detail, name='ot_detail'),
    path('ordenes/<int:ot_pk>/pdf/', flota_views.generar_ot_pdf, name='generar_ot_pdf'),

    # URLs de acciones para OT
    path('ordenes/<int:ot_pk>/cargar-pauta/', flota_views.cargar_tareas_pauta_ot, name='cargar_tareas_pauta_ot'),
    path('ordenes/<int:ot_pk>/pausar/', flota_views.pausar_ot, name='pausar_ot'),
    path('ordenes/<int:ot_pk>/guardar-diagnostico/', flota_views.guardar_diagnostico_ot, name='guardar_diagnostico_ot'),
    path('ordenes/<int:ot_pk>/asignar-tarea/', flota_views.asignar_tarea_ot, name='asignar_tarea_ot'),
    path('ordenes/<int:ot_pk>/agregar-insumo/', flota_views.agregar_insumo_manual_ot, name='agregar_insumo_manual_ot'),
    path('ordenes/<int:ot_pk>/asignar-personal/', flota_views.asignar_personal_ot, name='asignar_personal_ot'),
    path('ordenes/<int:ot_pk>/cambiar-estado/', flota_views.cambiar_estado_ot_accion, name='cambiar_estado_ot'),
    path('ordenes/<int:ot_pk>/cerrar-mecanico/', flota_views.cerrar_ot_mecanico, name='cerrar_ot_mecanico'),
    path('ordenes/<int:ot_pk>/solicitar-tarea/', flota_views.solicitar_nueva_tarea_ot, name='solicitar_nueva_tarea_ot'),
    path('ordenes/<int:ot_pk>/guardar-prueba-ruta/', flota_views.guardar_prueba_de_ruta_ot, name='guardar_prueba_de_ruta_ot'),

    path('pizarra-programacion/', flota_views.pizarra_programacion, name='pizarra_programacion'),
    path('vehiculo/<int:pk>/actualizar-km/', flota_views.actualizar_km_vehiculo, name='actualizar_km'),
    path('indicadores/', flota_views.indicadores_dashboard, name='indicadores_dashboard'),
    path('analisis-fallas/', flota_views.analisis_fallas, name='analisis_fallas'),
    path('analisis-avanzado/', flota_views.analisis_avanzado, name='analisis_avanzado'),
    path('carga-masiva/', flota_views.carga_masiva, name='carga_masiva'),
    path('vehiculo/<int:pk>/historial/', flota_views.historial_vehiculo, name='historial_vehiculo'),
    path('vehiculo/<int:pk>/analisis-km/', flota_views.analisis_km_vehiculo, name='analisis_km_vehiculo'),
    path('orden-trabajo/<int:ot_pk>/eliminar-tarea/<int:tarea_pk>/', flota_views.eliminar_tarea_ot, name='eliminar_tarea_ot'),
    path('orden-trabajo/<int:ot_pk>/eliminar-insumo/<int:detalle_pk>/', flota_views.eliminar_insumo_ot, name='eliminar_insumo_ot'),
    path('api/mecanicos-recursos/', flota_views.mecanicos_recursos_api, name='mecanicos_recursos_api'),
    path('api/ot-actualizar-fecha/<int:pk>/', flota_views.actualizar_fecha_ot_api, name='actualizar_fecha_ot_api'),
    path('api/repuestos/search/', flota_views.repuesto_search_api, name='repuesto_search_api'),
    path('api/ots/add-repuesto/', flota_views.add_repuesto_a_ot_api, name='add_repuesto_a_ot_api'),
    path('pizarra-combustible/', flota_views.pizarra_combustible, name='pizarra_combustible'),
    path('combustible/registrar/', flota_views.registrar_carga_combustible, name='registrar_carga_combustible'),
    path('ot/<int:pk>/autorizar-horas-extra/', flota_views.autorizar_horas_extra, name='autorizar_horas_extra'),
    path('notificaciones/', flota_views.lista_notificaciones, name='lista_notificaciones'),
    path('api/notificaciones/marcar-leidas/', flota_views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),
    path('kpi-rrhh/', flota_views.kpi_rrhh_dashboard, name='kpi_rrhh_dashboard'),
    path('reportes/', flota_views.reportes_dashboard, name='reportes_dashboard'),
    path('exportar/vehiculos-csv/', flota_views.export_vehiculos_csv, name='export_vehiculos_csv'),
    path('exportar/repuestos-csv/', flota_views.export_repuestos_csv, name='export_repuestos_csv'),
    path('exportar/ots-csv/', flota_views.export_ots_csv, name='export_ots_csv'),

    # URLs de Administración de Usuarios (ahora apuntan a cuentas.views)
    path('administracion/usuarios/', cuentas_views.lista_usuarios, name='lista_usuarios'),
    path('administracion/usuarios/crear/', cuentas_views.crear_usuario, name='crear_usuario'),
    path('administracion/usuarios/editar/<int:user_id>/', cuentas_views.editar_usuario, name='editar_usuario'),

    # URLs de la app 'cuentas' (login, logout, perfil)
    path('', include('cuentas.urls')),
]
