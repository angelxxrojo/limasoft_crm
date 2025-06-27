from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime

class User(AbstractUser):
    """Representantes de ventas"""
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Company(models.Model):
    """Compañías de los clientes"""
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    """Clientes asociados a compañías y representantes"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def birthday_formatted(self):
        """Formato: February 5"""
        return self.birth_date.strftime("%B %d")
    
    def get_last_interaction(self):
        """Obtiene la última interacción del cliente"""
        return self.interactions.order_by('-interaction_date').first()
    
    @property
    def last_interaction_display(self):
        """Formato: 1 day ago (Phone)"""
        last_interaction = self.get_last_interaction()
        if not last_interaction:
            return "No interactions"
        
        # Calcular diferencia de tiempo
        now = timezone.now()
        diff = now - last_interaction.interaction_date
        
        if diff.days == 0:
            if diff.seconds < 3600:  # menos de 1 hora
                minutes = diff.seconds // 60
                time_str = f"{minutes} minutes ago"
            else:  # menos de 1 día
                hours = diff.seconds // 3600
                time_str = f"{hours} hours ago"
        elif diff.days == 1:
            time_str = "1 day ago"
        else:
            time_str = f"{diff.days} days ago"
        
        return f"{time_str} ({last_interaction.interaction_type})"

class Interaction(models.Model):
    """Registros de interacciones con clientes"""
    INTERACTION_TYPES = [
        ('Call', 'Phone Call'),
        ('Email', 'Email'),
        ('SMS', 'Text Message'),
        ('Facebook', 'Facebook Message'),
        ('WhatsApp', 'WhatsApp'),
        ('LinkedIn', 'LinkedIn Message'),
        ('Meeting', 'In-person Meeting'),
        ('Video Call', 'Video Conference'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    interaction_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-interaction_date']
    
    def __str__(self):
        return f"{self.interaction_type} with {self.customer.full_name} on {self.interaction_date.strftime('%Y-%m-%d')}"