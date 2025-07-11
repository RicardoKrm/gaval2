#!/usr/bin/env bash

# Exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 3. Aplicar migraciones para el esquema public
# CAMBIADO: Usamos 'migrate --schema=public' que suele ser compatible con 2.x
python manage.py migrate --schema=public --noinput # <--- ¡LÍNEA MODIFICADA!

# 4. Crear el superusuario GLOBAL 'gaval' de forma no interactiva si no existe
# ... (resto del script sin cambios) ...
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(username='gaval').exists())"; then
  python manage.py createsuperuser --username gaval --email admin@pulser.com --noinput || true
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); user=User.objects.get(username='gaval'); user.set_password('pulseradmin123'); user.save()"
fi

echo "Despliegue inicial completado."