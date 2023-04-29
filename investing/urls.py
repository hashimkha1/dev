from django.urls import path

from getdata.views import options_play_cread_spread
from . import views

app_name = 'investing'
urlpatterns = [
    path('', views.home, name='home'),
    path('covered/', views.coveredcalls, name='covered'),
    path('training/', views.training, name='training'),

]