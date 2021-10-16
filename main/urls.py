from django.urls import path

from . import views
from .views import TransactionListView  # ,TransactionUpdateView

urlpatterns = [
    path('', views.layout, name='main-layout'),
    path('about/', views.about, name='main-about'),
    path('about_us/', views.about_us, name='main-about_us'),
    path('team/', views.team, name='main-team'),
    path('coach_profile/', views.coach_profile, name='main-coach_profile'),
    path('contact/', views.contact, name='main-contact'),
    path('report/', views.report, name='main-report'),
    path('project/', views.project, name='main-project'),
    path('training/', views.training, name='main-training'),
    path('test/', views.test, name='main-test'),
    path('pay/', views.pay, name='main-pay'),
    # transactions url patterns
    path('transact/', views.transact, name='main-transact'),
    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    #path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-updated'),
    #path('documents/', views.codadocuments, name='main-documents'),
    path('checkout/', views.checkout, name='main-checkout')

]
