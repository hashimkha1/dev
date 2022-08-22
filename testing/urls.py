from django.urls import path
from . import views
from .views import (
                        ServicesListView,
                     )

app_name = 'testing'
urlpatterns = [
    path('', views.Services_List, name='testing-home'),
    #-----------COMPANY REPORTS---------------------------------------
    path('display/', views.Services_List, name='services'),
]