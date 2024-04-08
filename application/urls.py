from django.urls import path
from . import views
from .views import (
                  clientListView,clientList,clientUpdateView,clientDeleteView, Balancesheet_category_list,balancesheet_list                  
                   )
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('balancelist/', views.Balancesheet_category_list, name='balancelist'),
    path('balancesheetlist/', views.balancesheet_list, name='balancesheetlist'),
    path('List', views.clientListView, name='List'),
    path('Create', views.clientCreateView.as_view(), name='Create'),
    path('List', views.clientList.as_view(), name='lt'),
    #path('update/<int:pk>/', xUpdateView.as_view(), name='update'),
    path('update/<int:pk>/', clientUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', clientDeleteView.as_view(), name='delete'),






    # path('join/', views.join, name='join'),
]