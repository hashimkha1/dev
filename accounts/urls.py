from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('Departments_id_list/', views.Departments_id_list, name='Departments_id_list'),
    path('create_departments_id/', views.create_departments_id, name='account-create_departments_id'),
    path('profile/', views.profile, name='account-profile'),
]