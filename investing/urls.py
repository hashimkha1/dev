from django.urls import path

from . import views

app_name = 'investing'
urlpatterns = [
    path('', views.home, name='home'),
    path('testing/', views.testing, name='testing'),
    path('training/', views.training, name='training'),
    path('layout/', views.layout, name='layout'),
    #path('doc/', views.doc, name='main-doc')
    path('upload/', views.upload, name='upload'),
    path('uploaded/', views.uploaded, name='uploaded'),
]