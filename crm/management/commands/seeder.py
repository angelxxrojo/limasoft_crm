import logging
import time
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Ejecuta todos los comandos necesarios para inicializar la aplicación CRM"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip", 
            nargs="+", 
            type=str, 
            help="Lista de comandos a omitir"
        )
        parser.add_argument(
            "--admin-username",
            type=str,
            default="admin",
            help="Nombre de usuario para el superusuario (default: admin)"
        )
        parser.add_argument(
            "--admin-email",
            type=str,
            default="admin@limasoft.com",
            help="Email para el superusuario (default: admin@limasoft.com)"
        )
        parser.add_argument(
            "--admin-password",
            type=str,
            default="admin123",
            help="Contraseña para el superusuario (default: admin123)"
        )

    def handle(self, *args, **options):
        start_time = time.time()
        skip_commands = options.get("skip") or []

        self.stdout.write(
            self.style.SUCCESS(
                "\n" + "="*60 +
                "\n🚀 INICIALIZANDO CRM LIMASOFT" +
                "\n" + "="*60
            )
        )

        # Define la secuencia de comandos a ejecutar
        commands_sequence = [
            {
                "name": "makemigrations",
                "description": "Generando migraciones",
                "args": [],
                "kwargs": {"verbosity": 1},
                "critical": True,
            },
            {
                "name": "migrate",
                "description": "Aplicando migraciones a la base de datos",
                "args": [],
                "kwargs": {"verbosity": 1},
                "critical": True,
            },
            {
                "name": "create_superuser_if_not_exists",
                "description": "Creando superusuario",
                "args": [],
                "kwargs": {
                    "username": options["admin_username"],
                    "email": options["admin_email"],
                    "password": options["admin_password"],
                },
                "critical": True,
                "custom": True,
            },
            {
                "name": "populate_data",
                "description": "Poblando base de datos con datos ficticios (esto puede tardar varios minutos...)",
                "args": [],
                "kwargs": {"verbosity": 1},
                "critical": True,
            },
        ]

        # Contador de éxitos y fallos
        success_count = 0
        failed_count = 0
        skipped_count = 0

        for cmd in commands_sequence:
            cmd_name = cmd["name"]

            if cmd_name in skip_commands:
                self.stdout.write(
                    self.style.WARNING(f"⏭️  Saltando comando: {cmd['description']}")
                )
                skipped_count += 1
                continue

            try:
                self.stdout.write(
                    self.style.HTTP_INFO(f"\n📦 {cmd['description']}...")
                )

                # Comando personalizado para crear superusuario
                if cmd.get("custom") and cmd_name == "create_superuser_if_not_exists":
                    self._create_superuser_if_not_exists(
                        cmd["kwargs"]["username"],
                        cmd["kwargs"]["email"], 
                        cmd["kwargs"]["password"]
                    )
                else:
                    call_command(
                        cmd_name, *cmd.get("args", []), **cmd.get("kwargs", {})
                    )

                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {cmd['description']} - Completado")
                )

            except Exception as e:
                failed_count += 1
                error_msg = f"❌ Error en {cmd['description']}: {str(e)}"

                if settings.DEBUG:
                    import traceback
                    error_msg += f"\n{traceback.format_exc()}"

                self.stdout.write(self.style.ERROR(error_msg))

                if cmd.get("critical", False):
                    self.stdout.write(
                        self.style.ERROR(
                            f"💥 Error crítico en {cmd['description']}. Deteniendo secuencia."
                        )
                    )
                    return

        # Resumen de ejecución
        elapsed_time = time.time() - start_time
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 PROCESO COMPLETADO EN {elapsed_time:.2f} SEGUNDOS"
                f"\n✅ Comandos exitosos: {success_count}"
                f"\n❌ Comandos fallidos: {failed_count}"
                f"\n⏭️  Comandos omitidos: {skipped_count}"
            )
        )

        if failed_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🚀 ¡CRM LIMASOFT LISTO PARA USAR!"
                    f"\n🌐 Accede en: http://localhost:8002/"
                    f"\n👤 Admin: {options['admin_username']}"
                    f"\n🔑 Password: {options['admin_password']}"
                    f"\n📊 Panel Admin: http://localhost:8002/admin/"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠️  Algunos comandos fallaron. Revisa los errores arriba."
                )
            )

        self.stdout.write("="*60 + "\n")

    def _create_superuser_if_not_exists(self, username, email, password):
        """Crea un superusuario solo si no existe"""
        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️  El superusuario '{username}' ya existe")
            )
            return
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️  Ya existe un usuario con email '{email}'")
            )
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name="Admin",
                last_name="LimaSoft"
            )
            self.stdout.write(
                self.style.SUCCESS(f"👤 Superusuario '{username}' creado exitosamente")
            )
        except Exception as e:
            raise Exception(f"Error al crear superusuario: {str(e)}")