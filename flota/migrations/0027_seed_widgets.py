from django.db import migrations

def create_initial_widgets(apps, schema_editor):
    Widget = apps.get_model('flota', 'Widget')

    WIDGETS = [
        {
            "nombre": "KPIs de Disponibilidad de Flota",
            "descripcion": "Muestra los KPIs de Disponibilidad, Confiabilidad y Utilización.",
            "template_name": "widgets/kpi_disponibilidad.html"
        },
        {
            "nombre": "KPIs de Mantenimiento",
            "descripcion": "Muestra la cantidad de OTs preventivas vs. correctivas.",
            "template_name": "widgets/kpi_mantenimiento.html"
        },
        {
            "nombre": "Análisis de Pareto de Fallas",
            "descripcion": "Muestra el diagrama de Pareto para las fallas más comunes.",
            "template_name": "widgets/pareto_fallas.html"
        },
        {
            "nombre": "Lista de OTs Pendientes",
            "descripcion": "Una lista compacta de las órdenes de trabajo que están pendientes.",
            "template_name": "widgets/ots_pendientes.html"
        },
    ]

    for widget_data in WIDGETS:
        Widget.objects.get_or_create(template_name=widget_data['template_name'], defaults=widget_data)


class Migration(migrations.Migration):

    dependencies = [
        ("flota", "0026_reglaalerta"),
    ]

    operations = []
