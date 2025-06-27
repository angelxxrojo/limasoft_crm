#!/bin/sh

echo "🐳 Iniciando contenedor de CRM LimaSoft..."

# Esperar a que la base de datos esté disponible (si usas PostgreSQL)
if [ "$DATABASE_URL" ]; then
    echo "⏳ Esperando a que la base de datos esté disponible..."
    
    # Función para esperar PostgreSQL
    wait_for_postgres() {
        until python -c "
import psycopg2
import os
import sys
from urllib.parse import urlparse

try:
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url.startswith('postgres://'):
        parsed = urlparse(db_url)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:]
        )
        conn.close()
        print('✅ PostgreSQL está disponible')
except Exception as e:
    print(f'❌ PostgreSQL no disponible: {e}')
    sys.exit(1)
        "; do
            echo "⏳ PostgreSQL no está listo - esperando..."
            sleep 2
        done
    }
    
    # Solo esperar PostgreSQL si la URL contiene 'postgres'
    if echo "$DATABASE_URL" | grep -q "postgres"; then
        wait_for_postgres
    fi
fi

# Ejecutar el comando seeder para inicializar todo
echo "🚀 Ejecutando comando seeder para inicializar la aplicación..."
poetry run python manage.py seeder

# Si se especificó un comando, ejecutarlo; si no, ejecutar runserver
if [ $# -eq 0 ]; then
    echo "🌐 Iniciando servidor de desarrollo..."
    exec poetry run python manage.py runserver 0.0.0.0:8002
else
    echo "▶️  Ejecutando comando personalizado: $@"
    exec "$@"
fi