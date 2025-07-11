#!/usr/bin/env bash

# Exit on error
set -o errexit

echo "--- Iniciando script de despliegue ---"

# ¡CRÍTICO! Cargar variables de entorno desde .env y EXPORTARLAS al shell
echo "Cargando variables de entorno desde .env..."
if [ -f .env ]; then
    # Lee cada línea no comentada del .env y la exporta como variable de entorno
    # Esto hace que las variables estén disponibles para los comandos de Python que siguen
    while IFS='=' read -r key value; do
        if [[ ! "$key" =~ ^# && -n "$key" ]]; then
            eval "$key=\"$value\""
            export "$key"
        fi
    done < .env
    echo ".env cargado y variables exportadas."
else
    echo "ERROR CRÍTICO: Archivo .env no encontrado en el directorio del proyecto."
    echo "Asegúrate de que /opt/pulser_app/.env existe y contiene las variables de producción."
    exit 1 # Salir con error
fi

# 1. Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic 

# 3. Aplicar migraciones para el esquema public
echo "Aplicando migraciones para el esquema 'public'..."
python manage.py migrate_schemas --shared  # <--- ESTE ES EL COMANDO CRÍTICO

# 4. Crear el superusuario GLOBAL 'gaval' de forma no interactiva si no existe
echo "Creando/actualizando superusuario 'gaval'..."
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(username='gaval').exists())"; then
  python manage.py createsuperuser --username gaval --email admin@pulser.com  || true
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); user=User.objects.get(username='gaval'); user.set_password('pulseradmin123'); user.save()"
  echo "Superusuario 'gaval' creado con contraseña temporal 'pulseradmin123'."
else
  echo "Superusuario 'gaval' ya existe. Omitiendo creación."
fi

echo "--- Script de despliegue completado ---"