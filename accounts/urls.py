from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('sCredentialCategorys_list/', views.sCredentialCategorys_list, name='sCredentialCategorys_list'),
    path('sCredentialCategorys_create/', views.sCredentialCategorys_create, name='sCredentialCategorys_create'),
    path('update_departments_id/<int:pk>/', views.update_departments_id, name='update_departments_id'),
    path('delete_departments_id/<int:pk>/', views.delete_departments_id, name='update_delete_departments_id'),
]

