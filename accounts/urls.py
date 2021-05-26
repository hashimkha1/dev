from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='account-join'),
    #path('joined/', views.joined, name='account-joined'),
    path('clients/', views.clients, name='account-clients'),
    #path('join/', views.join, name='account-join'),
    #path('application/', views.application, name='application-application'),
    #path('interview/', views.interview, name='application-interview'),
    #path('test/', views.test, name='application-test'),
]  
