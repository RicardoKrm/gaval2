import os
from celery import Celery

# Establecer el módulo de configuración de Django para el programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tms_gaval.settings')

app = Celery('tms_gaval')

# Usar un string aquí significa que el worker no tiene que serializar
# el objeto de configuración a los procesos hijos.
# - namespace='CELERY' significa que todas las claves de configuración de Celery
#   deben tener un prefijo `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar automáticamente los módulos de tasks.py de todas las apps registradas en Django.
app.autodiscover_tasks()
