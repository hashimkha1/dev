from django.urls import path
from . import views
from .views import (
                   Balancesheet_category_list,balancesheet_list,exception_list                
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('exceptionList/', views.exception_list, name='exceptionList'),

    # path('join/', views.join, name='join'),
]