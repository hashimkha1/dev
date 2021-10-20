from django.urls import path

from . import views
from .views import (ActivityUpdateView, EmployeeCreateView, EmployeeDeleteView,
                    EmployeeDetailView, EmployeeListView, EmployeeUpdateView)

app_name = 'management'
#<app>/<model>_<viewtype>
urlpatterns = [
    path('', views.home, name='management-home'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/new/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employees-update'),
    
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('construction/', views.construction, name='management-construction'),
    path('transact/', views.transact, name='management-transact'),
    path('transaction/', views.transaction, name='management-transaction'),


    #path('activities', views.all_activities, name='all_activities'),
    path('activity/<slug:slug>/', views.activity_detail, name='activity-detail'),
    #path('department/<slug:department_slug>/', views.department_list, name='department_list'),
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),
    path('activity/update/<int:pk>/', ActivityUpdateView.as_view(), name='activity-edit'),
]
