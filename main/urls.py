from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('about/', views.about, name='main-about'),
    path('team/', views.team, name='main-team'),
    path('coach_profile/', views.coach_profile, name='main-coach_profile'),
    path('contact/', views.contact, name='main-contact'),
    path('report/', views.report, name='main-report'),
    path('project/', views.project, name='main-project'),
    path('training/', views.training, name='main-training'),
    path('pay/', views.pay, name='main-pay'),
]
