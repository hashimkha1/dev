from django.urls import path
from . import views 
from .views import EmployeeCreateView ,EmployeeUpdateView,EmployeeDeleteView 

urlpatterns = [
    path('join/', views.join, name='account-join'),
    path('clients/', views.clients, name='account-clients'),
    path('show/ ', views.show, name='employee-records'),
    path('employee/new',EmployeeCreateView.as_view(), name='employee-add'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-edit'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee-deleted'), 

]  
