from django.urls import path
from django.conf.urls import url
from . import views

from .views import (
                    SearchInterviewView 
                    )

app_name = 'globalsearch'

urlpatterns = [
    path('', SearchInterviewView.as_view(), name='query'),
]