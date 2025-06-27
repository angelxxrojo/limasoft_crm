#!/bin/sh

# Aplicar migraciones a la base de datos
poetry run python manage.py migrate

# Recolectar archivos estáticos
poetry run python manage.py collectstatic --noinput

# Ejecutar el comando recibido
exec "$@"
