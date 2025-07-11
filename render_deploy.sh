#!/usr/bin/env bash

# Exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 3. Aplicar migraciones para el esquema public (solo para las shared_apps)
# --noinput: No pedir confirmación
python manage.py migrate --schema=public --noinput

# 4. Crear el superusuario GLOBAL 'gaval' de forma no interactiva si no existe
# Esto es CRÍTICO para que puedas acceder al admin global.
# ADVERTENCIA: La contraseña quedará aquí, cámbiala INMEDIATAMENTE después del despliegue inicial.
# Idealmente, usa una variable de entorno para la contraseña también.
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(username='gaval').exists())"; then
  python manage.py createsuperuser --username gaval --email admin@pulser.com --noinput || true
  # Establecer la contraseña de 'gaval' de forma no interactiva
  # (Usaremos 'pulseradmin123' como contraseña TEMPORAL para gaval, cámbiala por una segura en Render.com/admin)
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); user=User.objects.get(username='gaval'); user.set_password('pulseradmin123'); user.save()"
fi

echo "Despliegue inicial completado."