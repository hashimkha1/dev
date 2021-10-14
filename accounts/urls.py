from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='account-home'),
    path('join/', views.join, name='account-join'),
    path('clients/', views.clients, name='account-clients'),
]  