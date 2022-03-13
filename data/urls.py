from django.urls import path
from . import views
from .views import (
                    InterviewDetailView ,InterviewUpdateView ,InterviewDeleteView
                    #TrackCreateView, TrackDeleteView, TrackDetailView,
                    #TrackListView, InterviewUpdateView #,UserTrackListView
                    )


app_name = 'data'
urlpatterns = [
    path('', views.analysis, name='home'),
    path('report/', views.report, name='report'),
    path('etl/', views.etl, name='etl'),
    path('database/', views.database, name='database'),
    path('financialsystem/', views.financialsystem, name='finance'),
    path('payroll/', views.payroll, name='payroll'),
    path('project/', views.project, name='project'),
    path('training/', views.training, name='training'),
    path('bitraining/', views.bitraining, name='bitraining'),
    path('interview/', views.interview, name='interview'),

    path('deliverable/', views.deliverable, name='deliverable'),
    path('getdata/', views.getdata, name='getdata'),
    path('pay/', views.pay, name='pay'),

    #Interview/Assignment Section
    path('uploadinterview/', views.uploadinterview, name='uploadinterview'),
    path('iuploads/', views.iuploads, name='iuploads'),
    path('upload/<int:pk>/',InterviewDetailView.as_view(), name='interview-detail'),
    path('interview/<int:pk>/update', InterviewUpdateView.as_view(), name='interview-update'),
    path('interview/<int:pk>/delete', InterviewDeleteView.as_view(), name='delete-interview'),
    #path('iuploads/', UploadListView.as_view(), name='iuploads'),
    #path('upload/', views.upload, name='upload'),
    #path('uploaded/', views.uploaded, name='uploaded'),
]
