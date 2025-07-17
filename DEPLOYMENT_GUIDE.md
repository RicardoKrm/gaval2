# Guía de Despliegue en la Nube con Render.com

Esta guía detalla el proceso paso a paso para desplegar el proyecto TMS GAVAL en la plataforma en la nube [Render.com](https://render.com/). Render es una opción moderna y sencilla para desplegar aplicaciones Django con PostgreSQL y Redis.

## 1. Requisitos Previos

*   Una cuenta de GitHub con el código del proyecto en un repositorio.
*   Una cuenta creada en [Render.com](https://render.com/).

## 2. Creación de los Servicios en Render

El proyecto necesita tres servicios para funcionar: una base de datos **PostgreSQL**, un **servidor de Redis** y el **Servicio Web** que ejecutará la aplicación Django.

### 2.1. Crear la Base de Datos PostgreSQL

1.  En tu dashboard de Render, haz clic en **"New"** -> **"PostgreSQL"**.
2.  Dale un nombre único a tu base de datos (ej. `gaval-db`).
3.  Selecciona la región más cercana a tus usuarios.
4.  Asegúrate de que la versión de PostgreSQL sea 13 o superior.
5.  Haz clic en **"Create Database"**.

Una vez creada, Render te proporcionará los detalles de conexión. Busca la **"Internal Database URL"**. La necesitaremos en un momento.

### 2.2. Crear el Servidor de Redis

1.  En tu dashboard, haz clic en **"New"** -> **"Redis"**.
2.  Dale un nombre único (ej. `gaval-redis`).
3.  Selecciona la misma región que tu base de datos.
4.  Haz clic en **"Create Redis"**.

Render te proporcionará la **"Internal Redis URL"**.

## 3. Configuración del Servicio Web (La Aplicación Django)

Este es el servicio principal que ejecutará tu código.

1.  En tu dashboard, haz clic en **"New"** -> **"Web Service"**.
2.  Conecta tu cuenta de GitHub y selecciona el repositorio del proyecto.
3.  Dale un nombre a tu servicio (ej. `gaval-tms-app`).
4.  Configura los siguientes campos:
    *   **Region:** La misma que los otros servicios.
    *   **Branch:** La rama que quieres desplegar (ej. `main` o `feature/full-refactor-and-features`).
    *   **Runtime:** `Python 3` (Render usará el `runtime.txt` para elegir la versión exacta).
    *   **Build Command:** `bash render_deploy.sh` (Usaremos un script para automatizar el build).
    *   **Start Command:** `gunicorn tms_gaval.wsgi` (Este comando inicia el servidor de producción).

### 3.1. Configuración de las Variables de Entorno

Esta es la parte más **crítica**. En la pestaña **"Environment"** de tu Servicio Web, añade las siguientes variables:

*   **`SECRET_KEY`**:
    *   **Key:** `SECRET_KEY`
    *   **Value:** Genera una nueva clave secreta larga y aleatoria. No uses la de desarrollo.
*   **`DEBUG`**:
    *   **Key:** `DEBUG`
    *   **Value:** `False` (¡Muy importante para producción!)
*   **`DATABASE_URL`**:
    *   **Key:** `DATABASE_URL`
    *   **Value:** Pega la **"Internal Database URL"** que obtuviste de tu servicio de PostgreSQL en Render.
*   **`CELERY_BROKER_URL`** y **`CELERY_RESULT_BACKEND`**:
    *   **Key:** `CELERY_BROKER_URL`
    *   **Value:** Pega la **"Internal Redis URL"** y añade `/0` al final (ej. `redis://red-xxxxxxxxxx:6379/0`).
    *   **Key:** `CELERY_RESULT_BACKEND`
    *   **Value:** Usa la misma URL de Redis.
*   **`REDIS_URL`**:
    *   **Key:** `REDIS_URL`
    *   **Value:** Pega la **"Internal Redis URL"** y añade `/1` al final para el caché (ej. `redis://red-xxxxxxxxxx:6379/1`).
*   **`ALLOWED_HOSTS`**:
    *   **Key:** `ALLOWED_HOSTS`
    *   **Value:** El dominio que Render te asigna automáticamente (ej. `gaval-tms-app.onrender.com`) y, eventualmente, tu dominio personalizado.
*   **`CSRF_TRUSTED_ORIGINS`**:
    *   **Key:** `CSRF_TRUSTED_ORIGINS`
    *   **Value:** `https://` seguido de tu dominio de Render (ej. `https://gaval-tms-app.onrender.com`).

Haz clic en **"Create Web Service"**. El primer despliegue fallará porque aún no hemos creado el script de build, pero no te preocupes.

## 4. Creación del Script de Despliegue

En la raíz de tu repositorio, crea un archivo llamado `render_deploy.sh`. Este script le dirá a Render cómo preparar la aplicación en cada despliegue.

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar las dependencias
pip install -r requirements.txt

# 2. Recolectar los archivos estáticos
python manage.py collectstatic --no-input

# 3. Aplicar las migraciones a la base de datos
python manage.py migrate_schemas --shared
```
**Importante:** Asegúrate de que el archivo tenga permisos de ejecución. En Git, puedes hacerlo con `git add .` y `git commit`, no necesitas `chmod` directamente si trabajas en Windows.

## 5. Despliegue Final y Pasos Post-Despliegue

1.  **Haz commit y push** de los nuevos archivos (`render_deploy.sh`, `DEPLOYMENT_GUIDE.md`, etc.) a tu repositorio de GitHub.
2.  Render detectará el nuevo push y comenzará un nuevo despliegue automáticamente. Esta vez, debería ser exitoso.
3.  Una vez que el despliegue esté "Live", necesitas crear tu primer tenant y el superusuario en el entorno de producción.
    *   Ve a la pestaña **"Shell"** de tu servicio web en Render.
    *   Ejecuta los mismos comandos que en local:
        ```bash
        python manage.py create_tenant --schema_name=nombrecliente --nombre="Nombre del Cliente"
        python manage.py create_domain --schema_name=nombrecliente --domain=nombrecliente.onrender.com --is_primary
        python manage.py create_tenant_superuser --schema_name=nombrecliente --username=admin_cliente --email=...
        ```
    *   **Nota:** Reemplaza `nombrecliente.onrender.com` con el subdominio que desees sobre tu dominio principal de Render.

¡Felicidades! Tu aplicación TMS GAVAL está ahora desplegada en la nube.
