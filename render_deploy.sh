#!/usr/bin/env bash

# Exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
python manage.py collectstatic --noinput

echo "Build y collectstatic completados."