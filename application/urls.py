from django.urls import path
from . import views
from .views import (
                   Balancesheet_category_list,balancesheet_list,investList,investUp,investDel,investDet,policy_list            
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),

    path('List', views.investList, name='List'),
    path('Create', views.investCreat.as_view(), name='Create'),
    path('List', views.List.as_view(), name='lt'),


    path('update/<int:pk>/', investUp.as_view(), name='update'),
    path('delete/<int:pk>/', investDel.as_view(), name='delete'),
    path('investmentstrat/<int:pk>/', investDet.as_view(), name='detail'),
    path('codalist', views.policy_list, name='codalist'),

    # path('join/', views.join, name='join'),
]