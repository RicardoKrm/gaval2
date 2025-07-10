# settings.py

import os
from pathlib import Path
import locale
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- CONFIGURACIÓN BASE ---

BASE_DIR = Path(__file__).resolve().parent.parent

# Lee la SECRET_KEY y el modo DEBUG desde el archivo .env
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = ['*'] # En desarrollo está bien, en producción sé más específico.

# ====================================================================
# *** CONFIGURACIÓN CORRECTA DE SHARED_APPS y TENANT_APPS ***
# ====================================================================

SHARED_APPS = [
    'django_tenants',
    'tenants',  # Tu app para los modelos de tenant (Empresa, Domain)

    # Apps de Django que son COMPARTIDAS (globales) y VIVEN EN EL ESQUEMA PUBLIC
    # Sus tablas solo existen en el esquema 'public'.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes', # contenttypes también suele ser compartido para Foreign Keys
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # ¡IMPORTANTE! 'flota' y 'cuentas' NO VAN AQUÍ si son por tenant.
]

TENANT_APPS = [
    # Las apps que son ESPECÍFICAS de CADA TENANT.
    # Sus tablas se crean y gestionan de forma independiente en cada esquema de tenant.
    # Aquí es donde deben estar 'flota' y 'cuentas' para el modelo multi-tenant.
    
    # Tus APPS ESPECÍFICAS de NEGOCIO (para cada tenant)
    'flota',
    'cuentas',
]

# Esta línea es correcta y así es como django-tenants las usa internamente.
# Asegura que INSTALLED_APPS contenga todas las apps sin duplicados.
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# ====================================================================


# =================== DEBUG: VERIFICACIÓN FINAL DE APPS ===================
print("--- DEBUG: VERIFICANDO LISTAS DE APPS CARGADAS ---")
print(f"DEBUG: SHARED_APPS_CARGADAS  = {SHARED_APPS}")
print(f"DEBUG: TENANT_APPS_CARGADAS = {TENANT_APPS}")
print("--------------------------------------------------")
# =========================================================================


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
]

# --- URLS Y TENANTS ---

ROOT_URLCONF = 'tms_gaval.urls' # Ajusta 'tms_gaval' al nombre de tu carpeta de proyecto si es diferente

TENANT_MODEL = "tenants.Empresa"
TENANT_DOMAIN_MODEL = "tenants.Domain"


# =================== BLOQUE DE DEPURACIÓN (DEBUGGING) ===================
# Vamos a imprimir las variables para ver exactamente qué está leyendo Django
print("--- DEBUG: LEYENDO VARIABLES DE ENTORNO ---")
print(f"DEBUG: DB_NAME    = '{os.getenv('DB_NAME')}'")
print(f"DEBUG: DB_USER    = '{os.getenv('DB_USER')}'")
print(f"DEBUG: DB_PASSWORD = '{os.getenv('DB_PASSWORD')}'")
print(f"DEBUG: DB_HOST    = '{os.getenv('DB_HOST')}'")
print(f"DEBUG: DB_PORT    = '{os.getenv('DB_PORT')}'")
print("---------------------------------------------")
# ========================================================================


# --- BASE DE DATOS (Configurada para leer desde .env) ---

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend', # Motor para multi-tenant
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# --- PLANTILLAS (TEMPLATES) ---

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',       
                # Importante: El context processor de 'flota' debe eliminarse si 'flota' es TENANT_APP
                # ya que intentaría consultar tablas que no existen en el esquema 'public'.
                # 'flota.context_processors.notificaciones_processor', # <-- ASEGÚRATE DE QUE ESTÉ COMENTADO O ELIMINADO
            ],
        },
    },
]

# --- INTERNACIONALIZACIÓN Y LOCALIZACIÓN ---

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Configuración de localización para el idioma español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252') # Alternativa para Windows
    except locale.Error:
        print("Advertencia: No se pudo establecer la localización en español. Las fechas pueden aparecer en inglés.")

# --- ARCHIVOS ESTÁTICOS ---

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# --- AUTENTICACIÓN Y REDIRECCIONES ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]