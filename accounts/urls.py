from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    #============================= USERS VIEWS ==============================
    path('', views.home, name='home'),
    path('list/', views.list, name='list'),
    path('create_view/', views.create_view, name='create_view'),  # Updated for consistency
     path('payment/update/<int:pk>/', views.update_payments, name='payment_information_update'), 
    # ... other patterns for the accounts app
]

   
   