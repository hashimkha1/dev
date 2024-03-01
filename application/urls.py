from django.urls import path
from . import views
from .views import (
                   Balancesheet_category_list,balancesheet_list,TracckerList                 
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('traccker/', views.TracckerList, name='traccker'),
    # path('join/', views.join, name='join'),
]