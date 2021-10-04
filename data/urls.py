from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='data-home'),
    path('report/', views.report, name='data-report'),
    path('etl/', views.etl, name='data-etl'),
    path('database/', views.database, name='data-database'),
    path('financialsystem/', views.financialsystem, name='data-financialsystem'),
    path('payroll/', views.payroll, name='data-payroll'),
    path('project/', views.project, name='data-project'),
    path('training/', views.training, name='data-training'),
    path('interview/', views.interview, name='data-interview'),
    path('uploadinterview/', views.uploadinterview, name='data-uploadinterview'),
    path('iuploads/', views.iuploads, name='data-uploads'),
    path('upload/', views.upload, name='data-upload'),
    path('uploaded/', views.uploaded, name='data-uploaded'),
    path('testing/', views.testing, name='data-testing'),
    path('deliverable/', views.deliverable, name='data-deliverable'),
    path('consultancy/', views.consultancy, name='data-consultancy'),
    path('getdata/', views.getdata, name='data-getdata'),
    path('pay/', views.pay, name='data-pay'),


]
