from django.urls import path
from . import views

app_name = 'finance'
urlpatterns = [
    #=============================CLIENT CONTRACT FORM SUBMISSIONS=====================================
    path('contract_form/', views.contract_form_submission, name='finance-contract_form_submission'),

]