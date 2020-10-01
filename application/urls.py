from django.urls import path
from . import views

urlpatterns = [
    path('career/', views.career, name='application-career'),
    path('application/', views.application, name='application-application'),
    path('interview/', views.interview, name='application-interview'),
    path('first_interview/', views.first_interview, name='application-first_interview'),
    path('second_interview/', views.second_interview, name='application-second_interview'),
    path('orientation/', views.orientation, name='application-orientation'),
    path('upload/', views.upload, name='application-upload'),
    path('apply/', views.apply, name='application-apply'),
    path('applicants/', views.applicants, name='application-applicants'),
   
]
