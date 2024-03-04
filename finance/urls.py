from django.urls import path
from . import views
from .views import (
                    PaymentCreateView,#PaymentListView,
                    TransanctionDetailView,TransactionListView,
                    TransactionUpdateView,TransactionDeleteView,
                    UserInflowListView,InflowDetailView,InflowUpdateView,InflowDeleteView,
                    DefaultPaymentUpdateView,DefaultPaymentListView,
                    LoanListView,LoanUpdateView,LoanCreateView,userLoanListView,
)
app_name = 'finance'
urlpatterns = [
    #=============================FINANCES=====================================
    path('statements/', views.openai_balancesheet, name='open_statements'),
    path('send_invoice/', views.send_invoice, name='send_invoice'),
    path('finance_report/', views.finance_report, name='finance_report'),
    path('add_budget_item/', views.add_budget_item, name='add_budget_item'),
    path('budget/', views.budget, name='budget'),
    path('budget/<int:pk>/update/', views.BudgetUpdateView.as_view(), name='budget-update'),
    path('investment_report/', views.investment_report, name='investment_report'),
    path('transact/', views.transact, name='finance-transact'),
    path('transaction/', views.outflows, name='transaction-list'),
    path('transaction/<int:pk>/', TransanctionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(template_name="finance/payments/transaction_form.html"), name='transaction-update'),
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(template_name="finance/payments/transaction_confirm_delete.html"), name='transaction-delete'),
     #-----------CASHINFLOW---------------------------------------
    path('inflow_entry/', views.inflow, name='entry_inflow'),
    path('inflows/', views.inflows, name='inflow-list'),
    path('user_inflow/', UserInflowListView.as_view(), name='user-list'),
    path('inflow/<int:pk>/', InflowDetailView.as_view(), name='inflow-detail'),
    path('inflow/<int:pk>/delete/', InflowDeleteView.as_view(), name='inflow-delete'),
    path('inflow/<int:pk>/update/', InflowUpdateView.as_view(), name='inflow-update'),
    #=============================DC 48 CASHFLOW=====================================
    path('newinflow/', views.DC48InflowCreateView.as_view(), name='dcinflow'),
    path('updateinflow/<int:pk>/update/', views.DC48InflowUpdateView.as_view(), name='dcinflow-update'),
    path('deleteinflow/<int:pk>/delete/', views.DC48InflowDeleteView.as_view(), name='dcinflow-delete'),
    path('clientinflows/<str:username>/', views.clientinflows, name='userclientinflows'),
    path('listinflow/', views.dcinflows, name='dcklist'),
    #=============================CLIENT CONTRACT FORM SUBMISSIONS=====================================
    
    path('contract_data/', views.contract_data_submission, name='contract_data_submission'),
    path('investment_submission/', views.contract_investment_submission, name='investment_submission'),
    path('mycontract/<str:username>/', views.mycontract, name='mycontract'),
    path('newcontract/<str:username>/', views.new_contract, name='newcontract'),
    path('newoptioncontract/<str:username>/', views.new_option_contract, name='newoptioncontract'),
    # path('newtrainingcontract/<str:username>/', views.new_training_contract, name='newtrainingcontract'),
    #Pay URLS   
    # path('userpay/', views.userpay, name='userpay'),
    path('pay/', views.pay, name='pay'),
    path('payment/<int:service>/', views.pay, name='service_pay'),
    path('payment_method/<str:method>/', views.payment, name='payment_method'),
    path("payment_complete/", views.paymentComplete, name="payment_complete"),
    path('payments/', views.payments, name='payments'),
    path('mpesa-payment/', views.MpesaPaymentView, name='mpesa_payment'),
    path('otp-confirmation/', views.verify_otp, name='otp_confirmation'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('pay/<int:pk>/', views.PaymentInformationUpdateView.as_view(), name='updatepay'),
    
    path('defaultpayments/', DefaultPaymentListView.as_view(template_name='finance/payments/defaultpayments.html'), name='defaultpayments'),
    path('newpayment/', PaymentCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpayment'),
    path('payment/<int:pk>/update/', DefaultPaymentUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='payment-update'),
    #Pay configs URLS
    path('newpaymentconfigs/',views.PaymentConfigCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpaymentconfigs'),
    path('paymentconfigs/', views.PaymentConfigListView.as_view(), name='paymentconfigs'),
    path('paymentconfigs/<int:pk>/update/', views.PaymentConfigUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='paymentconfigs-update'),
    #Loans URLS
    path('loans/', LoanListView.as_view(template_name='finance/payments/loans.html'), name='trainingloans'),
    # path('newpay/', views.loan, name='newpay'),
    path('newpay/', LoanCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpay'),
    path('loanuser/', views.userLoanListView.as_view(), name='loanuser'),
    path('loan/<int:pk>/update/', LoanUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='loan-update'),
     #FOOD & SUPPLIERS
    path(
        "newsupplies/",
        views.FoodCreateView.as_view(
            template_name='main/snippets_templates/generalform.html'
        ),
        name="newsupplies",
    ),
    path(
        "newsupplier/",
        views.SupplierCreateView.as_view(
            template_name='main/snippets_templates/generalform.html'
        ),
        name="newsupplier",
    ),
    path("supplier/update/<int:pk>/",views.SupplierUpdateView.as_view(template_name='main/snippets_templates/generalform.html'),name="update-supplier"),
    path("food/<int:pk>/update",views.FoodUpdateView.as_view(template_name='main/snippets_templates/generalform.html'),name="update-food"),
    path("suppliers/",views.SupplierListView.as_view(),name="suppliers"),    
    path("food/",views.foodlist,name="supplies"),
    path("foodhistory/",views.food_history_view,name="foodhistory"),
    path("foodhistoryupdate/<int:pk>/",views.food_history_update,name="foodhistoryupdate"),
]