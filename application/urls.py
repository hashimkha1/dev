from django.urls import path
from . import views

urlpatterns = [
    # For Applicants
    path('career/', views.career, name='application-career'),
    path('application/', views.application, name='application-application'),
    path('apply/', views.apply, name='application-apply'),
    path('applicants/', views.applicants, name='application-applicants'),
    path('interview/', views.interview, name='application-interview'),
    path('first_interview/', views.first_interview, name='application-first_interview'),
    path('second_interview/', views.second_interview, name='application-second_interview'),
    path('orientation/', views.orientation, name='application-orientation'),
    # For Internal Use Only
    path('policy/', views.policy, name='application-policy'),
    path('policies/', views.policies, name='application-policies'),
    path('trainee/', views.trainee, name='application-trainee'),
    path('trainees/', views.trainees, name='application-trainees'),
    path('rating/', views.rating, name='application-rating'),
    path('rate/', views.rate, name='application-rate'),
    path('firstupload/', views.firstupload, name='application-firstupload'),
    path('fupload/', views.fupload, name='application-fupload'),
    #path('uploaded/', views.uploaded, name='application-uploaded'),
    path('employee_insert/', views.employee_form, name='application-emp_insert'),
    path('<int:id>/', views.employee_form, name='application-emp_update'),
    path('<int:id>/', views.employee_delete, name='application-emp_delete'),
    path('employee_list/', views.employee_list, name='application-emp_list'),
    #path('test/', views.test, name='application-test'),
]  
