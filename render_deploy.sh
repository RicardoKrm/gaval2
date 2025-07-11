#!/usr/bin/env bash

# Exit on error
set -o errexit

echo "--- Iniciando script de despliegue ---"

# 1. Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# 3. Aplicar migraciones para el esquema public (solo para las shared_apps)
# ¡CRÍTICO! Usamos public_schema_only para evitar el error de set_schema
echo "Aplicando migraciones para el esquema 'public'..."
python manage.py public_schema_only migrate --noinput

# 4. Crear el superusuario GLOBAL 'gaval' de forma no interactiva si no existe
echo "Creando/actualizando superusuario 'gaval'..."
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(username='gaval').exists())"; then
  python manage.py createsuperuser --username gaval --email admin@pulser.com --noinput || true
  # Establecer la contraseña de 'gaval' de forma no interactiva
  # ADVERTENCIA: La contraseña quedará aquí, cámbiala INMEDIATAMENTE después del despliegue inicial en el admin.
  # Idealmente, usa una variable de entorno para la contraseña también.
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); user=User.objects.get(username='gaval'); user.set_password('pulseradmin123'); user.save()"
  echo "Superusuario 'gaval' creado con contraseña temporal 'pulseradmin123'."
else
  echo "Superusuario 'gaval' ya existe. Omitiendo creación."
fi

echo "--- Script de despliegue completado ---"