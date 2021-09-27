from django.urls import path
from .views import EmployeeCreateView,EmployeeListView ,EmployeeDetailView,EmployeeUpdateView,EmployeeDeleteView

from . import views

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/new/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employees-update'),
    #path('employee/edit/<int:pk>', views.EmployeeEdit, name='employee-edit'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

]

#<app>/<model>_<viewtype>