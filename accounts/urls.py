from django.urls import path
from . import views
from . views import companytracker_List

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    path('login/', views.login_view, name='account-login'),
    path('profile/', views.profile, name='account-profile'),
     path('companylist/', views.companytracker_List, name='companylist'),
]