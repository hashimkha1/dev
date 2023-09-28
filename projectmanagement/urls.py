from django.urls import path

from . import views

app_name = 'projectmanagement'
#<app>/<model>_<viewtype>
urlpatterns = [
    path('', views.home, name='management-home'),
]
