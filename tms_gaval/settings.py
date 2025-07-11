# settings.py

import os
from pathlib import Path
import locale
from dotenv import load_dotenv
import dj_database_url # Para parsear la URL de la base de datos de Hostinger

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- CONFIGURACIÓN BASE ---

BASE_DIR = Path(__file__).resolve().parent.parent

# Lee la SECRET_KEY y el modo DEBUG desde el archivo .env
# ¡CRÍTICO PARA SEGURIDAD en producción! Deben ser variables de entorno en Hostinger.
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# ALLOWED_HOSTS: ¡CRÍTICO PARA SEGURIDAD en producción!
# Permitirá tu dominio real (ej. pulser.cl y *.pulser.cl)
# En desarrollo, '*' es seguro si DEBUG es True.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',') # <--- Lee de ENV para flexibilidad

# ====================================================================
# *** CONFIGURACIÓN DEFINITIVA DE SHARED_APPS y TENANT_APPS ***
# (Roles por Tenant, Datos por Tenant)
# ====================================================================

SHARED_APPS = [
    'django_tenants',
    'tenants',  # Tu app para los modelos de tenant (Empresa, Domain)

    # Apps que REALMENTE son GLOBALES (NO se replican por tenant)
    'django.contrib.staticfiles', # Gestión de archivos estáticos (es global)
    'django.contrib.humanize',    # Para formato de números (es global)
    # Las apps de AUTENTICACIÓN, ADMIN y MENSAJES van en TENANT_APPS para ser por cliente
]

TENANT_APPS = [
    # Las apps que son ESPECÍFICAS de CADA TENANT.
    # Sus tablas se crean y gestionan de forma independiente en cada esquema de tenant.
    'django.contrib.admin',        # Admin del tenant (con sus propios usuarios y grupos)
    'django.contrib.auth',         # Autenticación del tenant (usuarios, grupos, permisos)
    'django.contrib.contenttypes', # Contenttypes del tenant (necesario para auth)
    'django.contrib.sessions',     # Sesiones del tenant
    'django.contrib.messages',     # Mensajes del tenant
    
    # Tus APPS ESPECÍFICAS de NEGOCIO (para cada tenant)
    'flota',
    'cuentas',
]

# Esta línea es correcta y así es como django-tenants las usa internamente.
# Asegura que INSTALLED_APPS contenga todas las apps sin duplicados.
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', # Debe estar al principio para la identificación del tenant
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Para manejo de sesiones
    'django.middleware.common.CommonMiddleware',            # Para manejo de URLs, etc.
    'django.middleware.csrf.CsrfViewMiddleware',            # Para protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Para manejo de autenticación
    'django.contrib.messages.middleware.MessageMiddleware', # Para mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Para protección clickjacking
    'whitenoise.middleware.WhiteNoiseMiddleware',           # <--- Para servir estáticos en producción (Hostinger)
]

# --- URLS Y TENANTS ---

ROOT_URLCONF = 'tms_gaval.urls' # Ajusta 'tms_gaval' al nombre de tu carpeta de proyecto si es diferente

TENANT_MODEL = "tenants.Empresa"          # Tu modelo personalizado de tenant
TENANT_DOMAIN_MODEL = "tenants.Domain"    # Tu modelo personalizado de dominio

# =================== BLOQUE DE DEPURACIÓN (DEBUGGING) ===================
# Estos prints solo aparecerán en desarrollo (si DEBUG es True), no en producción.
print("--- DEBUG: LEYENDO VARIABLES DE ENTORNO ---")
print(f"DEBUG: DB_NAME    = '{os.getenv('DB_NAME')}'")
print(f"DEBUG: DB_USER    = '{os.getenv('DB_USER')}'")
print(f"DEBUG: DB_PASSWORD = '{os.getenv('DB_PASSWORD')}'")
print(f"DEBUG: DB_HOST    = '{os.getenv('DB_HOST')}'")
print(f"DEBUG: DB_PORT    = '{os.getenv('DB_PORT')}'")
print("---------------------------------------------")
# ========================================================================


# --- BASE DE DATOS ---
# Usa dj_database_url para parsear la DATABASE_URL (Hostinger la proporcionará)
DATABASES = {
    'default': dj_database_url.config(
        # ¡CRÍTICO! El motor debe ser explícitamente el de django-tenants.
        engine='django_tenants.postgresql_backend', # <--- ¡AÑADE ESTA LÍNEA!
        default=os.getenv('DATABASE_URL', 'postgresql://gaval:Karma627@localhost:5432/gavaldb_utf8'),
        conn_max_age=600
    )
}

# Router de base de datos para django-tenants (sin cambios)
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# --- PLANTILLAS (TEMPLATES) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Busca plantillas en tu carpeta templates/ de la raíz del proyecto
        'APP_DIRS': True, # Busca plantillas en carpetas templates/ de cada app instalada
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Context processor de flota: activado y seguro (maneja esquemas public/tenant)
                'flota.context_processors.notificaciones_processor',
            ],
        },
    },
]

# --- INTERNACIONALIZACIÓN Y LOCALIZACIÓN ---

LANGUAGE_CODE = 'es-cl' # Idioma de tu aplicación
TIME_ZONE = 'America/Santiago' # Zona horaria
USE_I18N = True # Habilitar internacionalización
USE_TZ = True # Habilitar soporte para zonas horarias

# Configuración de localización para el idioma español (sin cambios)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252') # Alternativa para Windows
    except locale.Error:
        print("Advertencia: No se pudo establecer la localización en español. Las fechas pueden aparecer en inglés.")

# --- ARCHIVOS ESTÁTICOS ---
# Configuración para Whitenoise en producción (Hostinger)
STATIC_URL = '/static/'                  # URL base para servir archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'   # Directorio donde `collectstatic` copiará todos los estáticos
STATICFILES_DIRS = [BASE_DIR / 'static'] # Tus carpetas de estáticos durante el desarrollo

# --- AUTENTICACIÓN Y REDIRECCIONES ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Tipo de campo por defecto para IDs de modelos
LOGIN_URL = 'tenant_login'          # URL de tu login personalizado para clientes
LOGIN_REDIRECT_URL = 'dashboard'    # Redirección después de login exitoso (al dashboard del tenant)
LOGOUT_REDIRECT_URL = 'tenant_login' # Redirección después de logout (de nuevo al login centralizado)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Backend de autenticación estándar de Django
]

# Configuración de email (ejemplo, ajustar según tu proveedor)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.tudominio.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu_correo@tudominio.com'
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = 'no-reply@tudominio.com'

# Opcional: Configuración de LOGGING para producción
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'INFO',
#         },
#     },
# }