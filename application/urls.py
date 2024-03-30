from django.urls import path
from . import views
from .views import (
                   workers_exceptionListView,Balancesheet_category_list,balancesheet_list                  
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('workersList/', views.workers_exceptionListView, name='workersList'),
    # path('join/', views.join, name='join'),
]