from django.urls import path

from . import views

urlpatterns = [
    #path('', views.layout, name='main-layout'),
    path('', views.home, name='investing-home'),
    path('testing/', views.testing, name='investing-testing'),
    path('training/', views.training, name='investing-training'),
    path('layout/', views.layout, name='investing-layout'),
    #path('doc/', views.doc, name='main-doc')
    path('upload/', views.upload, name='investing-upload'),
    path('uploaded/', views.uploaded, name='investing-uploaded'),
]