from django.urls import path
from . import views

urlpatterns = [
    #path('', views.layout, name='main-layout'),
    path('home/', views.home, name='projectmanagement-home'),
    path('construction/', views.construction, name='projectmanagement-construction'),
    #path('doc/', views.doc, name='main-doc')
]
