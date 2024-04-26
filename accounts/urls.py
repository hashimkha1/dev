from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS==============================
    path('', views.home, name='home'),
    path('list/', views.list, name='list'),
]   
   