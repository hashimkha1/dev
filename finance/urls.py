from django.urls import path
from . import views
<<<<<<< HEAD

=======
from .views import (
                    PaymentCreateView,PaymentListView,
                    DefaultPaymentUpdateView,DefaultPaymentListView,
                    #FeaturedActivityCreateView,FeaturedActivityLinksCreateView,PaymentUpdateView
)
>>>>>>> d17b85afee3f2e68d2228ce39218044690d0ca24
app_name = 'finance'
urlpatterns = [
    #=============================CLIENT CONTRACT FORM SUBMISSIONS=====================================
    path('contract_form/', views.contract_form_submission, name='finance-contract_form_submission'),
<<<<<<< HEAD
    
=======
    path('payments/', PaymentListView.as_view(template_name='finance/payments/payments.html'), name='payments'),
    path('defaultpayments/', DefaultPaymentListView.as_view(template_name='finance/payments/defaultpayments.html'), name='defaultpayments'),
    path('newpayment/', PaymentCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpayment'),
    path('payment/<int:pk>/update/', DefaultPaymentUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='payment-update'),
>>>>>>> d17b85afee3f2e68d2228ce39218044690d0ca24
]