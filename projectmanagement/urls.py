from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='projectmanagement-home'),
    path('construction/', views.construction, name='projectmanagement-construction'),

]
