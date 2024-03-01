from django.urls import path
from . import views
from .views import (
                   Balancesheet_category_list,balancesheet_list,wcag_list_view,wcag_create_view            
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('wcaglist/', views.wcag_list_view, name='wcaglist'),
    path('wcagcreate/', views.wcag_create_view, name='wcagcreate'),
    # path('join/', views.join, name='join'),
]