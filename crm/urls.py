from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
]