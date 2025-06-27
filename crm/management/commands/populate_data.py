import random
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from crm.models import User, Company, Customer, Interaction

class Command(BaseCommand):
    help = 'Populate database with sample data for CRM'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Limpiar datos existentes
        self.stdout.write('Cleaning existing data...')
        Interaction.objects.all().delete()
        Customer.objects.all().delete()
        Company.objects.all().delete()
        User.objects.all().delete()
        
        # Crear usuarios (representantes de ventas)
        self.stdout.write('Creating sales representatives...')
        users_data = [
            {'username': 'juan_sales', 'first_name': 'Juan', 'last_name': 'Pérez', 'email': 'juan@company.com'},
            {'username': 'maria_sales', 'first_name': 'María', 'last_name': 'García', 'email': 'maria@company.com'},
            {'username': 'carlos_sales', 'first_name': 'Carlos', 'last_name': 'López', 'email': 'carlos@company.com'},
        ]
        
        users = []
        for user_data in users_data:
            user = User.objects.create(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=make_password('password123'),
                is_admin=False
            )
            users.append(user)
        
        # Crear compañías
        self.stdout.write('Creating companies...')
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
        
        companies = []
        for name in company_names:
            company = Company.objects.create(name=name)
            companies.append(company)
        
        # Crear clientes
        self.stdout.write('Creating customers...')
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
        
        customers = []
        for i in range(1000):
            # Generar fecha de nacimiento aleatoria (entre 25 y 65 años)
            start_date = datetime.date.today() - datetime.timedelta(days=65*365)
            end_date = datetime.date.today() - datetime.timedelta(days=25*365)
            random_days = random.randint(0, (end_date - start_date).days)
            birth_date = start_date + datetime.timedelta(days=random_days)
            
            customer = Customer.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                birth_date=birth_date,
                company=random.choice(companies),
                sales_rep=random.choice(users)
            )
            customers.append(customer)
            
            if (i + 1) % 100 == 0:
                self.stdout.write(f'Created {i + 1} customers...')
        
        # Crear interacciones
        self.stdout.write('Creating interactions...')
        interaction_types = ['Call', 'Email', 'SMS', 'Facebook', 'WhatsApp', 'LinkedIn', 'Meeting', 'Video Call']
        
        interaction_count = 0
        for customer in customers:
            # Crear entre 450 y 550 interacciones por cliente (promedio 500)
            num_interactions = random.randint(450, 550)
            
            for j in range(num_interactions):
                # Generar fecha de interacción en los últimos 2 años
                start_date = timezone.now() - datetime.timedelta(days=730)
                end_date = timezone.now()
                random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
                interaction_date = start_date + datetime.timedelta(seconds=random_seconds)
                
                Interaction.objects.create(
                    customer=customer,
                    interaction_type=random.choice(interaction_types),
                    interaction_date=interaction_date,
                    notes=f"Sample interaction {j+1} with {customer.full_name}"
                )
                interaction_count += 1
            
            if (customers.index(customer) + 1) % 50 == 0:
                self.stdout.write(f'Created interactions for {customers.index(customer) + 1} customers... (Total interactions: {interaction_count})')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nData population completed successfully!\n'
                f'Created:\n'
                f'- {len(users)} sales representatives\n'
                f'- {len(companies)} companies\n'
                f'- {len(customers)} customers\n'
                f'- {interaction_count} interactions\n'
            )
        )