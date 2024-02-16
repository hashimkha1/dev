from django.urls import path
from . import views
from .views import Company_Rating_list,companyrating_create
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    #path('', views.home, name='home'),
    path('ratinglist/', views.Company_Rating_list, name='ratinglist'),
    path('ratingcreate/', views.companyrating_create, name='ratingcreate'),
    
]