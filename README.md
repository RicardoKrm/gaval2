# TMS GAVAL - Sistema de Gestión de Flotas Multi-Tenant

Este proyecto es una aplicación web desarrollada en Django para la gestión integral de flotas de vehículos, diseñada con una arquitectura multi-tenant que permite a múltiples empresas utilizar el sistema de forma aislada y segura.

## Características Principales

*   **Arquitectura Multi-Tenant:** Cada empresa cliente opera en su propio esquema de base de datos, garantizando total aislamiento de los datos.
*   **Gestión de Flota:** Seguimiento detallado de vehículos, incluyendo kilometraje, mantenimientos, y estado general.
*   **Órdenes de Trabajo (OTs):** Creación y seguimiento de OTs preventivas, correctivas y evaluativas.
*   **Control de Inventario:** Gestión de repuestos, stock y movimientos asociados a las OTs.
*   **Programación y Planificación:** Calendario interactivo para programar OTs y asignar recursos.
*   **Dashboards y KPIs:** Paneles de control visuales para el análisis de rendimiento de la flota, costos y RR.HH.
*   **Control de Combustible:** Registro y análisis de cargas de combustible para calcular el rendimiento.
*   **Sistema de Notificaciones:** Alertas para eventos importantes dentro de la aplicación.
*   **Gestión de Usuarios y Roles:** Sistema de permisos basado en roles (Administrador, Supervisor, Mecánico).

---

## Guía de Instalación y Prueba Local

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno de desarrollo local.

### Requisitos Previos

*   Python 3.10 o superior.
*   PostgreSQL (versión 12 o superior recomendada).
*   Git.

### Paso 1: Clonar el Repositorio

Si aún no tienes el proyecto, clónalo desde el repositorio. Asegúrate de estar en la rama correcta que contiene los últimos cambios.

```bash
# Reemplaza <URL_DEL_REPOSITORIO> con la URL real de tu repositorio Git
git clone <URL_DEL_REPOSITORIO> -b feature/full-refactor-and-features gaval-tms
cd gaval-tms
```

### Paso 2: Configurar la Base de Datos en PostgreSQL

Es fundamental crear un usuario y una base de datos dedicada para el proyecto antes de continuar.

1.  Abre una terminal de `psql` o utiliza una herramienta gráfica como pgAdmin.
2.  Ejecuta los siguientes comandos SQL:

```sql
-- (Opcional) Borra la base de datos y el usuario si existen de una instalación anterior
-- DROP DATABASE IF EXISTS gavaldb_utf8;
-- DROP USER IF EXISTS gaval;

-- 1. Crea el usuario con la contraseña que usarás en el archivo .env
CREATE USER gaval WITH PASSWORD 'Karma627';

-- 2. Crea la base de datos con el encoding y propietario correctos
CREATE DATABASE gavaldb_utf8
    WITH
    OWNER = gaval
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252' -- Ajusta a la localización de tu sistema si es diferente
    LC_CTYPE = 'Spanish_Spain.1252'   -- Ajusta a la localización de tu sistema si es diferente
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
```
**Nota:** Si no estás en Windows, tu localización podría ser `es_CL.UTF-8` o similar.

### Paso 3: Configurar el Entorno Virtual y Dependencias

Aislaremos las dependencias del proyecto en un entorno virtual.

```bash
# 1. Crea un nuevo entorno virtual en el directorio del proyecto
python -m venv .venv

# 2. Activa el entorno virtual
#    En Windows (cmd/powershell):
.\.venv\Scripts\activate
#    En macOS/Linux:
#    source .venv/bin/activate

# 3. Instala todas las dependencias del proyecto
pip install -r requirements.txt
```

### Paso 4: Configurar el Archivo de Entorno (`.env`)

Crea un archivo llamado `.env` en la raíz del proyecto. Este archivo contendrá las variables de configuración sensibles.

Copia y pega el siguiente contenido en tu archivo `.env`:
```
# Clave secreta de Django (puedes generar una nueva)
SECRET_KEY='una-clave-secreta-muy-larga-y-dificil-de-adivinar-para-produccion'

# Activar el modo debug solo para desarrollo
DEBUG=True

# URL de conexión a la base de datos PostgreSQL
# Asegúrate de que el usuario, contraseña, host, puerto y nombre de la BD coincidan con el Paso 2
DATABASE_URL='postgresql://gaval:Karma627@localhost:5432/gavaldb_utf8'
```

### Paso 5: Ejecutar las Migraciones

Este comando preparará la base de datos, aplicando las migraciones al esquema público (`public`).

```bash
python manage.py migrate_schemas --shared
```

### Paso 6: Crear tu Primer Tenant (Empresa Cliente)

Ahora, registraremos la primera empresa en el sistema.

```bash
# Puedes cambiar los valores según tus necesidades
python manage.py create_tenant --schema_name=pulser --domain_url=pulser.localhost --tenant_name="Empresa Pulser"
```
*   `--schema_name`: Identificador técnico único para la empresa en la BD (ej. `pulser`).
*   `--domain_url`: El subdominio que usarás para acceder localmente (ej. `pulser.localhost`).
*   `--tenant_name`: El nombre comercial de la empresa (ej. `Empresa Pulser`).

El sistema clonará la estructura del esquema público y aplicará las migraciones. Si encuentras un error de "tabla ya existe", ejecuta `python manage.py migrate_schemas --fake-initial` para solucionarlo.

### Paso 7: Crear un Superusuario para el Tenant

Para poder iniciar sesión y administrar el tenant, crea un usuario administrador dentro de él.

```bash
python manage.py create_tenant_superuser --schema_name=pulser --username=admin_pulser --email=admin@pulser.com
```
El sistema te pedirá que introduzcas y confirmes una contraseña para este nuevo usuario.

### Paso 8: Ejecutar el Servidor de Desarrollo

¡Todo está listo para lanzar la aplicación!

```bash
python manage.py runserver
```

### Paso 9: Probar en el Navegador

1.  **Accede a la Landing Page:** Abre tu navegador y ve a `http://localhost:8000`.
2.  **Accede a la Página de Login:** Haz clic en el botón "Iniciar Sesión".
3.  **Inicia Sesión con tus credenciales de tenant:**
    *   **Identificador de Empresa:** `pulser.localhost`
    *   **Nombre de Usuario:** `admin_pulser`
    *   **Contraseña:** La contraseña que creaste en el paso 7.
4.  **Verificación:** Tras un inicio de sesión exitoso, serás redirigido al dashboard de la aplicación en `http://pulser.localhost:8000/dashboard/`.

¡Felicidades! El sistema está funcionando en tu entorno local.
