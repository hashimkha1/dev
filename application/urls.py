from django.urls import path
from . import views

urlpatterns = [
    path('career/', views.career, name='application-career'),
    path('apply/', views.apply, name='application-apply'),
    path('application/', views.application, name='application-application'),
    path('interview/', views.interview, name='application-interview'),
    path('upload/', views.upload, name='application-upload'),
    path('upload_resume/', views.upload_resume, name='application-upload_resume'),
    path('applicants/', views.applicants, name='application-applicants'),
   
]
