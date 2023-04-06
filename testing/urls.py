from django.urls import path
from . import views

app_name = 'testing'
urlpatterns = [
    path('testing/', views.testing, name='testing-pay'),
    path('all_logs/', views.LogsViewSet, name='all_logs'),
]  