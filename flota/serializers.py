from rest_framework import serializers
from .models import Vehiculo, OrdenDeTrabajo, Neumatico, Repuesto, DashboardConfig, DashboardWidgetInstance, Widget

class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'nombre', 'descripcion', 'template_name']

class DashboardWidgetInstanceSerializer(serializers.ModelSerializer):
    widget = WidgetSerializer(read_only=True)
    widget_id = serializers.PrimaryKeyRelatedField(
        queryset=Widget.objects.all(), source='widget', write_only=True
    )

    class Meta:
        model = DashboardWidgetInstance
        fields = ['id', 'widget', 'widget_id', 'pos_x', 'pos_y', 'width', 'height']

class DashboardConfigSerializer(serializers.ModelSerializer):
    widgets = DashboardWidgetInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = DashboardConfig
        fields = ['id', 'usuario', 'nombre', 'widgets']


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class OrdenDeTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeTrabajo
        fields = '__all__'

class NeumaticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neumatico
        fields = '__all__'

class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = '__all__'
