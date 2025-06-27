import random
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import transaction
from crm.models import User, Company, Customer, Interaction

class Command(BaseCommand):
    help = 'Populate database with sample data for CRM (optimized for concurrent access)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of records to create per batch (default: 100)'
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=1000,
            help='Number of customers to create (default: 1000)'
        )
        parser.add_argument(
            '--interactions-per-customer',
            type=int,
            default=500,
            help='Number of interactions per customer (default: 500)'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        num_customers = options['customers']
        interactions_per_customer = options['interactions_per_customer']
        
        self.stdout.write(self.style.SUCCESS('Starting optimized data population...'))
        
        # Verificar si ya existen datos
        if Customer.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Skipping population.'))
            return
        
        # Crear usuarios (representantes de ventas) en una transacción pequeña
        self.stdout.write('Creating sales representatives...')
        self._create_users()
        
        # Crear compañías en transacciones pequeñas
        self.stdout.write('Creating companies...')
        self._create_companies()
        
        # Crear clientes en lotes pequeños para permitir acceso concurrente
        self.stdout.write(f'Creating {num_customers} customers in batches of {batch_size}...')
        self._create_customers_in_batches(num_customers, batch_size)
        
        # Crear interacciones en lotes pequeños
        self.stdout.write(f'Creating interactions in batches of {batch_size}...')
        self._create_interactions_in_batches(interactions_per_customer, batch_size)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nData population completed successfully!\n'
                f'Created:\n'
                f'- 3 sales representatives\n'
                f'- 36 companies\n'
                f'- {num_customers} customers\n'
                f'- ~{num_customers * interactions_per_customer} interactions\n'
            )
        )

    def _create_users(self):
        """Crear usuarios en una transacción pequeña"""
        users_data = [
            {'username': 'juan_sales', 'first_name': 'Juan', 'last_name': 'Pérez', 'email': 'juan@company.com'},
            {'username': 'maria_sales', 'first_name': 'María', 'last_name': 'García', 'email': 'maria@company.com'},
            {'username': 'carlos_sales', 'first_name': 'Carlos', 'last_name': 'López', 'email': 'carlos@company.com'},
        ]
        
        with transaction.atomic():
            for user_data in users_data:
                User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'email': user_data['email'],
                        'password': make_password('password123'),
                        'is_admin': False
                    }
                )

    def _create_companies(self):
        """Crear compañías en transacciones pequeñas"""
        company_names = [
            'TechCorp Solutions', 'Innovate Industries', 'Global Dynamics', 'Future Systems',
            'Digital Ventures', 'Smart Technologies', 'Advanced Solutions', 'NextGen Corp',
            'Quantum Innovations', 'Synergy Group', 'ProActive Solutions', 'Elite Systems',
            'Alpha Technologies', 'Beta Industries', 'Gamma Solutions', 'Delta Corp',
            'Epsilon Ventures', 'Zeta Systems', 'Eta Innovations', 'Theta Group',
            'Iota Solutions', 'Kappa Technologies', 'Lambda Industries', 'Mu Corp',
            'Nu Solutions', 'Xi Systems', 'Omicron Group', 'Pi Innovations',
            'Rho Technologies', 'Sigma Solutions', 'Tau Industries', 'Upsilon Corp',
            'Phi Ventures', 'Chi Systems', 'Psi Group', 'Omega Solutions'
        ]
        
        # Crear en lotes de 10 compañías
        for i in range(0, len(company_names), 10):
            with transaction.atomic():
                batch = company_names[i:i+10]
                for name in batch:
                    Company.objects.get_or_create(name=name)

    def _create_customers_in_batches(self, total_customers, batch_size):
        """Crear clientes en lotes pequeños para permitir acceso concurrente"""
        first_names = [
            'Ana', 'Luis', 'Carmen', 'Miguel', 'Elena', 'David', 'Sofia', 'Pedro',
            'Isabel', 'Francisco', 'Laura', 'Antonio', 'Marta', 'José', 'Cristina',
            'Manuel', 'Pilar', 'Alejandro', 'Teresa', 'Javier', 'Rosa', 'Daniel',
            'Beatriz', 'Fernando', 'Gloria', 'Sergio', 'Amparo', 'Roberto', 'Dolores',
            'Andrés', 'Concepción', 'Raúl', 'Mercedes', 'Ángel', 'Josefa'
        ]
        
        last_names = [
            'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez',
            'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Ruiz', 'Hernández',
            'Díaz', 'Moreno', 'Álvarez', 'Muñoz', 'Romero', 'Alonso', 'Gutierrez',
            'Navarro', 'Torres', 'Domínguez', 'Vázquez', 'Ramos', 'Gil', 'Ramírez',
            'Serrano', 'Blanco', 'Suárez', 'Molina', 'Morales', 'Ortega', 'Delgado',
            'Castro', 'Ortiz', 'Rubio', 'Marín', 'Sanz', 'Iglesias'
        ]

        users = list(User.objects.all())
        companies = list(Company.objects.all())
        
        for i in range(0, total_customers, batch_size):
            customers_batch = []
            
            # Preparar el lote
            for j in range(batch_size):
                if i + j >= total_customers:
                    break
                    
                # Generar fecha de nacimiento aleatoria (entre 25 y 65 años)
                start_date = datetime.date.today() - datetime.timedelta(days=65*365)
                end_date = datetime.date.today() - datetime.timedelta(days=25*365)
                random_days = random.randint(0, (end_date - start_date).days)
                birth_date = start_date + datetime.timedelta(days=random_days)
                
                customer = Customer(
                    first_name=random.choice(first_names),
                    last_name=random.choice(last_names),
                    birth_date=birth_date,
                    company=random.choice(companies),
                    sales_rep=random.choice(users)
                )
                customers_batch.append(customer)
            
            # Crear el lote en una transacción
            with transaction.atomic():
                Customer.objects.bulk_create(customers_batch)
            
            # Mostrar progreso
            created_so_far = min(i + batch_size, total_customers)
            self.stdout.write(f'Created {created_so_far}/{total_customers} customers...')
            
            # Pequeña pausa para permitir otras operaciones
            import time
            time.sleep(0.1)

    def _create_interactions_in_batches(self, interactions_per_customer, batch_size):
        """Crear interacciones en lotes pequeños"""
        interaction_types = ['Call', 'Email', 'SMS', 'Facebook', 'WhatsApp', 'LinkedIn', 'Meeting', 'Video Call']
        customers = Customer.objects.all()
        
        interaction_count = 0
        interactions_batch = []
        
        for customer in customers:
            # Crear un número variable de interacciones por cliente (450-550)
            num_interactions = random.randint(450, 550)
            
            for j in range(num_interactions):
                # Generar fecha de interacción en los últimos 2 años
                start_date = timezone.now() - datetime.timedelta(days=730)
                end_date = timezone.now()
                random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
                interaction_date = start_date + datetime.timedelta(seconds=random_seconds)
                
                interaction = Interaction(
                    customer=customer,
                    interaction_type=random.choice(interaction_types),
                    interaction_date=interaction_date,
                    notes=f"Sample interaction {j+1} with {customer.full_name}"
                )
                interactions_batch.append(interaction)
                interaction_count += 1
                
                # Crear en lotes para permitir acceso concurrente
                if len(interactions_batch) >= batch_size:
                    with transaction.atomic():
                        Interaction.objects.bulk_create(interactions_batch)
                    interactions_batch = []
                    
                    # Mostrar progreso
                    customer_num = list(customers).index(customer) + 1
                    self.stdout.write(f'Created interactions for customer {customer_num}/{len(customers)} (Total: {interaction_count})')
                    
                    # Pequeña pausa para permitir otras operaciones
                    import time
                    time.sleep(0.05)
        
        # Crear las interacciones restantes
        if interactions_batch:
            with transaction.atomic():
                Interaction.objects.bulk_create(interactions_batch)