from django.urls import path
from . import views
from .views import (
                   Balancesheet_category_list,balancesheet_list,exception_list,exception_create                  
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('exception_list/', views.exception_list, name='exception_list'),
    path('exception_create/', views.exception_create, name='exception_create'),
    # path('join/', views.join, name='join'),
]