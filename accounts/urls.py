from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('departments_id_list/', views.Departments_id_list, name='departments_id_list'),
    path('create_departments_id/', views.create_departments_id, name='create_departments_id'),
    path('update_departments_id/<int:pk>/', views.update_departments_id, name='update_departments_id'),
    path('delete_departments_id/<int:pk>/', views.delete_departments_id, name='update_delete_departments_id'),
]

