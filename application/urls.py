from django.urls import path

from . import views
from .views import (ApplicantDeleteView, ApplicantListView, TraineeDeleteView,
                    TraineeUpdateView)

urlpatterns = [
    # For Applicants
    path('', views.career, name='application-career'),
    #path('application/', views.application, name='application-application'),
    path('apply/', views.apply, name='application-apply'),
    #path('applicants/', views.applicants, name='application-applicants'),
    path('interview/', views.interview, name='application-interview'),
    path('first_interview/', views.first_interview, name='application-first_interview'),
    path('second_interview/', views.second_interview, name='application-second_interview'),
    path('orientation/', views.orientation, name='application-orientation'),
    path('internal_training/', views.internal_training, name='application-internal'),
    # For Internal Use Only
    path('policy/', views.policy, name='application-policy'),
    path('policies/', views.policies, name='application-policies'),
    path('trainee/', views.trainee, name='application-trainee'),
    path('trainees/', views.trainees, name='application-trainees'),
    path('trainee/<int:pk>/update/', TraineeUpdateView.as_view(), name='trainee-update'),
    path('trainee/<int:pk>/delete/', TraineeDeleteView.as_view(), name='trainee-delete'),
    path('rating/', views.rating, name='application-rating'),
    path('rate/', views.rate, name='application-rate'),
    path('firstupload/', views.firstupload, name='application-firstupload'),
    path('fupload/', views.fupload, name='application-fupload'),

    #path('uploaded/', views.uploaded, name='application-uploaded'),
    path('applicants/', ApplicantListView.as_view(), name='applicant-list'),
    path('applicant/<int:pk>/delete/', ApplicantDeleteView.as_view(), name='applicant-delete'),
    #path('<int:id>/', views.employee_form, name='application-emp_update'),
    #path('<int:id>/', views.employee_delete, name='application-emp_delete'),
    #path('employee_list/', views.employee_list, name='application-emp_list'),
    #path('test/', views.test, name='application-test'),

    #API data
    #path('applicants', views.applicants, name='applicants'),
	#path('applicationapi/', views.ApplicationDataAPI),
	#path('get_total/', views.get_total),

	#Create activity
	#path('createactivity/', views.createActivity),

	#path('updateapplication/', views.updateApplication),

	#path('deleteapplication/', views.deleteApplication),
]  
