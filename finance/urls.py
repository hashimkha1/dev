from django.urls import path
from . import views
from .views import (
                    PaymentCreateView,PaymentListView,
                    DefaultPaymentUpdateView,DefaultPaymentListView,
                    LoanListView,LoanUpdateView
)
app_name = 'finance'
urlpatterns = [
    #=============================CLIENT CONTRACT FORM SUBMISSIONS=====================================
    path('contract_form/', views.contract_form_submission, name='finance-contract_form_submission'),
    path('mycontract/<str:username>/', views.mycontract, name='mycontract'),
    path('new_contract/<str:username>/', views.newcontract, name='newcontract'),
    path('payments/', PaymentListView.as_view(template_name='finance/payments/payments.html'), name='payments'),
    path('defaultpayments/', DefaultPaymentListView.as_view(template_name='finance/payments/defaultpayments.html'), name='defaultpayments'),
    path('newpayment/', PaymentCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpayment'),
    path('payment/<int:pk>/update/', DefaultPaymentUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='payment-update'),
     # Loans URLS
    path('loans/', LoanListView.as_view(template_name='finance/payments/loans.html'), name='trainingloans'),
    path('newpay/', views.loan, name='newpay'),
    path('loan/<int:pk>/update/', LoanUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='loan-update'),
 
]