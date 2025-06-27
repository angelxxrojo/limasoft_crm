FROM python:3.12-slim

# Configuraciones de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Configuración de Poetry
ENV POETRY_VERSION=1.5.1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Python y PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/poetry

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock ./

# Instalar dependencias del proyecto usando Poetry
RUN poetry install --no-interaction --no-ansi

# Copiar el resto de los archivos del proyecto
COPY . /app/

# Exponer el puerto 8002
EXPOSE 8002

# Configurar el comando predeterminado
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8002"]
