from django.urls import path
from . import views

urlpatterns = [
    path('registered/', views.registered, name='user-registered'),
]
