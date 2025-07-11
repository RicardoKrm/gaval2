#!/usr/bin/env bash

# Exit on error
set -o errexit

echo "--- Iniciando script de despliegue ---"

# CRÍTICO: Cargar variables de entorno desde .env (lo hará settings.py)
echo "Cargando variables de entorno desde .env (a través de settings.py)..."
# No necesitas `export $(grep ...)` aquí, ya que settings.py lo maneja.

# 1. Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# 3. Aplicar migraciones para el esquema public
# ¡CRÍTICO! Usar el comando correcto de django-tenants para migraciones compartidas
echo "Aplicando migraciones para el esquema 'public' usando migrate_schemas --shared..."
python manage.py migrate_schemas --shared --noinput # <--- ¡CAMBIO CRÍTICO AQUÍ!

# 4. Crear el superusuario GLOBAL 'gaval' de forma no interactiva si no existe
echo "Creando/actualizando superusuario 'gaval'..."
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(username='gaval').exists())"; then
  python manage.py createsuperuser --username gaval --email admin@pulser.com --noinput || true
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); user=User.objects.get(username='gaval'); user.set_password('pulseradmin123'); user.save()"
  echo "Superusuario 'gaval' creado con contraseña temporal 'pulseradmin123'."
else
  echo "Superusuario 'gaval' ya existe. Omitiendo creación."
fi

echo "--- Script de despliegue completado ---"