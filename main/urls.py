from django.urls import path

from . import views
from .views import TransactionListView  # ,TransactionUpdateView

app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    path('about/', views.about, name='about'),
    path('about_us/', views.about_us, name='about_us'),
    path('team/', views.team, name='team'),

    #==============DEPARTMENTS==============================================
        #---------------HUMAN RESOURCE--------------------#

        #---------------FINANCE--------------------#

        #---------------MANAGEMENT--------------------#
        path('it/', views.it, name='it'),

        #---------------IT--------------------#

    path('coach_profile/', views.coach_profile, name='coach'),
    path('contact/', views.contact, name='contact'),
    path('report/', views.report, name='report'),
    path('project/', views.project, name='project'),
    path('training/', views.training, name='training'),
    # transactions url patterns
    #path('transact/', views.transact, name='transact'),
    #path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    #path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-updated'),
    #path('documents/', views.codadocuments, name='documents'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.pay, name='pay'),
    path("payment_complete/", views.paymentComplete, name="payment_complete"),
    path('image/', views.ImageCreateView.as_view(template_name='main/form.html'), name='image'),
    path('image/<int:pk>/', views.ImageUpdateView.as_view(template_name='main/form.html'), name='updateimage'),
    path('images/', views.images, name='images'),
    path('testing/', views.testing, name='testing'),
    path('interview/', views.interview, name='interview'),

   #==============ERRORS==============================================
    path('400Error/', views.error400, name='400error'),
    path('403Error/', views.error403, name='403error'),
    path('404Error/', views.error404, name='404error'),
    path('500Error/', views.error500, name='500error'),
    # path('result/', views.result, name='result'),
    # path('noresult/', views.noresult, name='noresult'),

    path('400/', views.hendler400, name='400-error'),
    path('403/', views.hendler403, name='403-error'),
    path('404/', views.hendler404, name='404-error'),
    path('500/', views.hendler500, name='500-error'),

]
