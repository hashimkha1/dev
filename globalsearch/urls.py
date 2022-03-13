from django.urls import path
from django.urls import re_path as url
from . import views

from .views import (
                    SearchInterviewView 
                    )

app_name = 'globalsearch'

urlpatterns = [
    path('', SearchInterviewView.as_view(), name='query'),
]