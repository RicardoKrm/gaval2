# TMS GAVAL - Sistema de Gestión de Flotas Multi-Tenant

## 1. Resumen del Proyecto

Este proyecto es una aplicación web integral desarrollada en Django para la gestión de flotas de vehículos. Su principal característica es una **arquitectura multi-tenant**, que permite a múltiples empresas (clientes) utilizar una única instancia de la aplicación de forma completamente segura y aislada, cada una con su propia base de datos, usuarios y datos.

El sistema está diseñado no solo para registrar información, sino para ser una herramienta proactiva de gestión, optimización y análisis a través de sus diversos módulos.

---

## 2. Guía de Instalación Local Completa

Esta guía detalla todos los pasos necesarios para configurar el proyecto en un entorno de desarrollo local desde cero.

### 2.1. Requisitos Previos

Asegúrate de tener el siguiente software instalado en tu sistema:
*   **Python:** Versión 3.10 o superior.
*   **PostgreSQL:** Versión 12 o superior.
*   **Git:** Para clonar el repositorio.
*   **Redis:** (Opcional para desarrollo básico, pero **requerido** para que funcionen las tareas asíncronas y el caché).

### 2.2. Configuración de la Base de Datos

Antes de tocar el código de Django, es fundamental preparar la base de datos.

1.  Abre una terminal de `psql` o una herramienta gráfica como pgAdmin.
2.  Ejecuta los siguientes comandos SQL para crear el usuario y la base de datos. Reemplaza `'Karma627'` si vas a usar una contraseña diferente.

    ```sql
    -- (Opcional) Borra la base de datos y el usuario si ya existen
    -- DROP DATABASE IF EXISTS gavaldb_utf8;
    -- DROP USER IF EXISTS gaval;

    -- 1. Crea el usuario que gestionará la base de datos
    CREATE USER gaval WITH PASSWORD 'Karma627';

    -- 2. Crea la base de datos principal del proyecto
    CREATE DATABASE gavaldb_utf8
        WITH
        OWNER = gaval
        ENCODING = 'UTF8'
        -- Asegúrate de que la localización coincida con la de tu sistema
        LC_COLLATE = 'Spanish_Spain.1252' -- Windows
        -- LC_COLLATE = 'es_ES.UTF-8' -- Linux/macOS
        LC_CTYPE = 'Spanish_Spain.1252' -- Windows
        -- LC_CTYPE = 'es_ES.UTF-8' -- Linux/macOS
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1;
    ```

### 2.3. Configuración del Proyecto

1.  **Clona el Repositorio:**
    ```bash
    # Reemplaza <URL_DEL_REPOSITORIO> con la URL real
    git clone <URL_DEL_REPOSITORIO> gaval-tms
    cd gaval-tms
    ```

2.  **Crea y Activa un Entorno Virtual:**
    ```bash
    # Crea el entorno
    python -m venv .venv

    # Actívalo (el comando varía según tu sistema operativo)
    # En Windows:
    .\.venv\Scripts\activate
    # En macOS/Linux:
    # source .venv/bin/activate
    ```

3.  **Instala las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura el Archivo de Entorno (`.env`):**
    Crea un archivo llamado `.env` en la raíz del proyecto y añade el siguiente contenido. **Asegúrate de que los datos de `DATABASE_URL` coincidan con los que creaste en el paso 2.2.**

    ```
    # Clave secreta de Django (puedes generar una nueva)
    SECRET_KEY='django-insecure-una-clave-secreta-muy-larga-y-dificil-de-adivinar'

    # Activar el modo debug solo para desarrollo
    DEBUG=True

    # URL de conexión a la base de datos PostgreSQL
    DATABASE_URL='postgresql://gaval:Karma627@localhost:5432/gavaldb_utf8'

    # URL de conexión a Redis (usada por Celery y el caché)
    # Usa la base de datos 0 para Celery y la 1 para el caché, es una buena práctica.
    CELERY_BROKER_URL='redis://localhost:6379/0'
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    REDIS_URL='redis://localhost:6379/1'
    ```

### 2.4. Inicialización de la Aplicación

Estos comandos prepararán la base de datos de Django y crearán tu primer cliente (tenant).

1.  **Ejecuta las Migraciones:**
    Este comando creará todas las tablas necesarias en el esquema `public` (el esquema principal).
    ```bash
    python manage.py migrate_schemas --shared
    ```

2.  **Crea el Primer Tenant:**
    Vamos a crear una empresa de ejemplo llamada "Pulser".
    ```bash
    python manage.py create_tenant --schema_name=pulser --domain_url=pulser.localhost --tenant_name="Empresa Pulser"
    ```
    *   `--schema_name`: Identificador técnico en la BD.
    *   `--domain_url`: El subdominio que usarás para acceder (`pulser.localhost` para desarrollo).
    *   `--tenant_name`: El nombre comercial de la empresa.

3.  **Crea un Superusuario para el Tenant:**
    Este será el primer usuario administrador para la "Empresa Pulser".
    ```bash
    python manage.py create_tenant_superuser --schema_name=pulser --username=admin_pulser --email=admin@pulser.com
    ```
    El sistema te pedirá que introduzcas y confirmes una contraseña.

4.  **Crea un Superusuario para el Sistema (Dueño del Proyecto):**
    Este usuario es para el **Panel de Super Administrador** y no pertenece a ningún tenant.
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones para crear tu usuario administrador global.

### 2.5. Ejecución de los Servicios

Para que todas las funcionalidades del sistema operen, necesitas ejecutar 3 procesos, cada uno en su **propia terminal**.

1.  **Terminal 1: Servidor de Django:**
    ```bash
    # Asegúrate de que tu entorno virtual esté activado
    python manage.py runserver
    ```
    Esto inicia la aplicación web, normalmente en `http://localhost:8000`.

2.  **Terminal 2: Worker de Celery:**
    Este proceso se encarga de ejecutar las tareas en segundo plano (reportes, alertas, etc.).
    ```bash
    # Asegúrate de que tu entorno virtual esté activado
    celery -A tms_gaval worker -l info
    ```

3.  **Terminal 3: Celery Beat (Planificador):**
    Este proceso se encarga de decirle al worker *cuándo* ejecutar las tareas periódicas.
    ```bash
    # Asegúrate de que tu entorno virtual esté activado
    celery -A tms_gaval beat -l info
    ```

### 2.6. ¡A Probar!

*   **Aplicación Principal:**
    1.  Abre tu navegador y ve a `http://localhost:8000`.
    2.  Haz clic en "Iniciar Sesión".
    3.  Usa:
        *   Identificador de Empresa: `pulser.localhost`
        *   Usuario: `admin_pulser`
        *   Contraseña: la que creaste.
    4.  Serás redirigido a `http://pulser.localhost:8000/dashboard/`.

*   **Admin de Tenant:**
    *   Ve a `http://pulser.localhost:8000/admin/` e inicia sesión con `admin_pulser`.

*   **Admin Global (para el dueño del proyecto):**
    *   Ve a `http://localhost:8000/admin/` e inicia sesión con el superusuario que creaste con `createsuperuser`.
