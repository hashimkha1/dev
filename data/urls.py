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
    path('deliverable/', views.deliverable, name='data-deliverable'),
    path('consultancy/', views.consultancy, name='data-consultancy'),
    path('getdata/', views.getdata, name='data-getdata'),


]
