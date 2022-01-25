from django.urls import path

from . import views

#from .views import (ActivityUpdateView, EmployeeCreateView, EmployeeDeleteView,
                   # EmployeeDetailView, EmployeeListView, EmployeeUpdateView)

app_name = 'projectmanagement'
#<app>/<model>_<viewtype>
urlpatterns = [
    path('', views.home, name='management-home'),
    path('transact/', views.transact, name='management-transact'),
    path('transaction/', views.transaction, name='management-transaction'),

]
