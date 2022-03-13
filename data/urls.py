from django.urls import path
from . import views



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


]

''' 
    path('uploadinterview/', views.uploadinterview, name='uploadinterview'),
    path('iuploads/', UploadListView.as_view(), name='iuploads'),
    path('iuploads/', views.iuploads, name='iuploads'),
    path('upload/', views.upload, name='upload'),
    path('uploaded/', views.uploaded, name='uploaded'),
    path('deliverable/', views.deliverable, name='deliverable'),
    path('getdata/', views.getdata, name='getdata'),
    path('pay/', views.pay, name='pay'),
'''