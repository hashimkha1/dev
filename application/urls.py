from django.urls import path
from . import views
from .views import (
                   Balancesheet_category_list,balancesheet_list ,wcag_website_list,wcag_website_create                 
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('wcaglist/', views.wcag_website_list, name='wcaglist'),
    path('wcagcreate/', views.wcag_website_create, name='wcagcreate'),
    # path('join/', views.join, name='join'),
]