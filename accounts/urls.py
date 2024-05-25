from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('Departments_id_list/', views.Departments_id_list, name='Departments_id_list'),
    path('login/', views.login_view, name='account-login'),
    path('profile/', views.profile, name='account-profile'),
]