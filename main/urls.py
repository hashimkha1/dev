from django.urls import path

from . import views
from .views import TransactionListView  # ,TransactionUpdateView

app_name = "main"
urlpatterns = [
    path("", views.layout, name="layout"),
    path("about/", views.about, name="about"),
    path("about_us/", views.about_us, name="about_us"),
    path("team/", views.team, name="team"),
    # ==============DEPARTMENTS==============================================
    # ---------------HUMAN RESOURCE--------------------#
    # ---------------FINANCE--------------------#
    # ---------------MANAGEMENT--------------------#
    path("it/", views.it, name="it"),
    # ---------------IT--------------------#
    path("coach_profile/", views.coach_profile, name="coach"),
    path("contact/", views.contact, name="contact"),
    path("report/", views.report, name="report"),
    path("project/", views.project, name="project"),
    path("training/", views.training, name="training"),
    path("pay/", views.pay, name="pay"),
    # transactions url patterns
    # path('transact/', views.transact, name='transact'),
    # path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    # path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-updated'),
    # path('documents/', views.codadocuments, name='documents'),
    path("checkout/", views.checkout, name="checkout"),
    path("testing/", views.testing, name="testing"),
    path("payment_complete/", views.paymentComplete, name="payment_complete"),
]
