
# Prueba técnica Django
Sistema de gestión de relaciones con clientes (CRM) desarrollado en Django como parte de una prueba técnica. El sistema maneja 1,000 clientes, 36 compañías y más de 500,000 interacciones con una interfaz web moderna y optimizada.



## Descripción del Reto Técnico
El proyecto fue desarrollado siguiendo los siguientes requerimientos:
- ✅ Modelado de base de datos con 4 entidades principales
- ✅ Generación de datos ficticios masivos (500k+ interacciones)
- ✅ Vista estilo CRM con filtros avanzados y ordenamiento
- ✅ Optimización de rendimiento para manejar grandes volúmenes de datos
- ✅ Interfaz responsive con Bootstrap 5

| Componentes  | Cantidad | Descripción |
| ------------- | ---------- |---------|
| User  | 36  | Representantes de ventas |
| Companies  | Content Cell  | Compañias ficticios |
| Customers  | 1000  | Clientes distribuidos entre compañías |
| Interactions  | ~500,000  | Promedio de 500 por cliente |


## Instalacion

Este manual tiene como objetivo ayudar a cualquier persona a desplegar el proyecto en una nueva máquina. Siga estos pasos para instalar y ejecutar el proyecto correctamente.

- Python 3.11 o superior
- pip (administrador de paquetes de Python)
- Git

Clonar el proyecto
```bash
git remote add origin https://github.com/angelxxrojo/limasoft_crm.git
```
## Con docker

```bash
docker-compose build
docker-compose up
```
Para este comandos, solo es esperar a que se pueda poblar los datos para poder ingresar a 
http://localhost:8002/

## De la Forma Tradicional

Crear y Activar un Entorno Virtual
```bash
python -m venv limasoft_venv
# Para Windows
limasoft_venv\Scripts\activate
# Para Linux/Mac
source limasoft_venv/bin/activate
```
```bash
cd limasoft_crm
```
Instalar Requerimientos
```bash
pip install -r requirements.txt
```
```bash
python manage.py makemigrations
python manage.py migrate
```
```bash
python manage.py populate_data
- La ejecucion de este comando tarada aproximadamente 10 minutos, dado que tiene que crear un numero elevado de medio millon de registros.
```

Create un super usuario
```bash
python manage.py createsuperuser
```
## Deployment

Para despliegue de aplicativo

```bash
  python manage.py runserver
```

Visita http://localhost:8002/


