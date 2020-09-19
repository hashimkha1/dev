from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report, name='data-report'),
    path('etl/', views.etl, name='data-etl'),
    path('database/', views.database, name='data-database'),
    path('project/', views.project, name='data-project'),
    path('training/', views.training, name='data-training'),
    path('course/', views.course, name='data-course'),

]
