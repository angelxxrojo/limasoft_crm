from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Customer, Interaction

def customer_list(request):
    """Vista principal del CRM con lista de clientes"""
    
    # Obtener parámetros de filtro y ordenamiento
    search_query = request.GET.get('search', '')
    birthday_filter = request.GET.get('birthday_filter', '')
    sort_by = request.GET.get('sort', 'first_name')
    
    # Optimizar consulta con select_related y prefetch_related
    customers = Customer.objects.select_related(
        'company', 'sales_rep'
    ).prefetch_related(
        Prefetch(
            'interactions',
            queryset=Interaction.objects.order_by('-interaction_date')[:1],
            to_attr='latest_interaction'
        )
    )
    
    # Aplicar filtros de búsqueda
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    # Aplicar filtros de cumpleaños
    if birthday_filter:
        today = timezone.now().date()
        
        if birthday_filter == 'this_week':
            # Cumpleaños esta semana
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            customers = customers.filter(
                Q(birth_date__month=start_of_week.month, birth_date__day__gte=start_of_week.day) |
                Q(birth_date__month=end_of_week.month, birth_date__day__lte=end_of_week.day)
            )
            
        elif birthday_filter == 'this_month':
            # Cumpleaños este mes
            customers = customers.filter(birth_date__month=today.month)
            
        elif birthday_filter == 'next_month':
            # Cumpleaños el próximo mes
            next_month = today.replace(day=1) + timedelta(days=32)
            customers = customers.filter(birth_date__month=next_month.month)
    
    # Aplicar ordenamiento
    if sort_by == 'company':
        customers = customers.order_by('company__name')
    elif sort_by == 'birthday':
        customers = customers.order_by('birth_date')
    elif sort_by == 'last_interaction':
        # Ordenar por última interacción requiere subconsulta
        from django.db.models import Max
        customers = customers.annotate(
            last_interaction_date=Max('interactions__interaction_date')
        ).order_by('-last_interaction_date')
    elif sort_by == 'first_name':
        customers = customers.order_by('first_name', 'last_name')
    elif sort_by == 'last_name':
        customers = customers.order_by('last_name', 'first_name')
    else:
        customers = customers.order_by('first_name', 'last_name')
    
    # Paginación
    paginator = Paginator(customers, 25)  # 25 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas rápidas
    total_customers = Customer.objects.count()
    total_companies = Customer.objects.values('company').distinct().count()
    total_interactions = Interaction.objects.count()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'birthday_filter': birthday_filter,
        'sort_by': sort_by,
        'total_customers': total_customers,
        'total_companies': total_companies,
        'total_interactions': total_interactions,
        'birthday_filter_choices': [
            ('', 'All birthdays'),
            ('this_week', 'This week'),
            ('this_month', 'This month'),
            ('next_month', 'Next month'),
        ],
        'sort_choices': [
            ('first_name', 'First Name'),
            ('last_name', 'Last Name'),
            ('company', 'Company'),
            ('birthday', 'Birthday'),
            ('last_interaction', 'Last Interaction'),
        ]
    }
    
    return render(request, 'crm/customer_list.html', context)