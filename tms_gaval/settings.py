# settings.py

import os
from pathlib import Path
import locale
from dotenv import load_dotenv
import dj_database_url # <--- NUEVO: Importar para la DB de Render

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- CONFIGURACIÓN BASE ---

BASE_DIR = Path(__file__).resolve().parent.parent

# Lee la SECRET_KEY y el modo DEBUG desde el archivo .env
# ¡CRÍTICO PARA SEGURIDAD en producción! Deben ser variables de entorno en Render.
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# ALLOWED_HOSTS: ¡CRÍTICO PARA SEGURIDAD en producción!
# Permitirá el dominio de Render (ej. your-app-name.onrender.com)
# En desarrollo, '*' es seguro si DEBUG es True.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',') # <--- MODIFICADO: Lee de ENV

# ====================================================================
# *** CONFIGURACIÓN CORRECTA DE SHARED_APPS y TENANT_APPS ***
# (Esta configuración ya está confirmada y es correcta para tu proyecto)
# ====================================================================

SHARED_APPS = [
    'django_tenants',
    'tenants',  # Tu app para los modelos de tenant (Empresa, Domain)

    # Apps que REALMENTE son GLOBALES
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Las apps de AUTH y ADMIN NO van aquí; se gestionan por tenant.
]

TENANT_APPS = [
    # Las apps que son ESPECÍFICAS de CADA TENANT.
    # Sus tablas se crean y gestionan de forma independiente en cada esquema de tenant.
    'django.contrib.admin',        # Admin por tenant
    'django.contrib.auth',         # Autenticación por tenant (usuarios, grupos, permisos)
    'django.contrib.contenttypes', # Contenttypes por tenant (necesario para auth)
    'django.contrib.sessions',     # Sesiones por tenant
    'django.contrib.messages',     # Mensajes por tenant
    
    # Tus APPS ESPECÍFICAS de NEGOCIO (para cada tenant)
    'flota',
    'cuentas',
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', # Debe estar al principio
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- NUEVO: Para servir estáticos en producción (importante para Render)
]

# --- URLS Y TENANTS ---

ROOT_URLCONF = 'tms_gaval.urls' # Ajusta 'tms_gaval' al nombre de tu carpeta de proyecto si es diferente

TENANT_MODEL = "tenants.Empresa"
TENANT_DOMAIN_MODEL = "tenants.Domain"


# =================== BLOQUE DE DEPURACIÓN (DEBUGGING) ===================
# Vamos a imprimir las variables para ver exactamente qué está leyendo Django
# (Estos prints solo aparecerán en desarrollo, no en Render si DEBUG es False)
print("--- DEBUG: LEYENDO VARIABLES DE ENTORNO ---")
print(f"DEBUG: DB_NAME    = '{os.getenv('DB_NAME')}'")
print(f"DEBUG: DB_USER    = '{os.getenv('DB_USER')}'")
print(f"DEBUG: DB_PASSWORD = '{os.getenv('DB_PASSWORD')}'")
print(f"DEBUG: DB_HOST    = '{os.getenv('DB_HOST')}'")
print(f"DEBUG: DB_PORT    = '{os.getenv('DB_PORT')}'")
print("---------------------------------------------")
# ========================================================================


# --- BASE DE DATOS ---
# MODIFICADO: Usa dj_database_url para parsear la DATABASE_URL de Render
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgresql://gaval:Karma627@localhost:5432/gavaldb_utf8'), # Tu URL local como default
        conn_max_age=600 # Opcional: Reutiliza conexiones por hasta 10 minutos
    )
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# --- PLANTILLAS (TEMPLATES) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Busca plantillas en tu carpeta templates/ de la raíz
        'APP_DIRS': True, # Busca plantillas en carpetas templates/ de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',       
                'flota.context_processors.notificaciones_processor', # <-- Este ya está bien modificado y debe estar DESCOMENTADO
            ],
        },
    },
]

# --- INTERNACIONALIZACIÓN Y LOCALIZACIÓN ---

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Configuración de localización para el idioma español (sin cambios)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252') # Alternativa para Windows
    except locale.Error:
        print("Advertencia: No se pudo establecer la localización en español. Las fechas pueden aparecer en inglés.")

# --- ARCHIVOS ESTÁTICOS ---
# Configuración para Whitenoise en producción
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # <--- Dónde Collectstatic copiará los archivos para servir
STATICFILES_DIRS = [BASE_DIR / 'static'] # Tus archivos estáticos de desarrollo (CSS, JS, imágenes)


# --- AUTENTICACIÓN Y REDIRECCIONES ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'tenant_login'          # Apunta a tu login centralizado
LOGIN_REDIRECT_URL = 'dashboard'    # Redirige al dashboard después de login exitoso
LOGOUT_REDIRECT_URL = 'tenant_login' # Redirige al login después de logout

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]