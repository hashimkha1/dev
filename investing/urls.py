from django.urls import path

from getdata.views import options_play_cread_spread
from . import views

app_name = 'investing'
urlpatterns = [
    path('', views.home, name='home'),
    # path('testing/', views.testing, name='testing'),
    path('covered/', views.coveredcalls, name='covered'),
    path('training/', views.training, name='training'),
    path('layout/', views.layout, name='layout'),
    #path('doc/', views.doc, name='main-doc')
    path('upload/', views.upload, name='upload'),
    path('uploaded/', views.uploaded, name='uploaded'),
]