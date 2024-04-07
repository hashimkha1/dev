from django.urls import path
from . import views
from .views import (vListView,List,vCreateView,vUpdateView,vDeleteView
                #    customer_user_list,transaction_create_view,payments ,Transaction_list ,transaction_create               
                  )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('List', views.vListView, name='List'),
    path('List', views.List.as_view(), name='lt'),
    path('Create', views.vCreateView.as_view(), name='Create'),
    path('update/<int:pk>/', vUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', vDeleteView.as_view(), name='delete'),
    
    # path('join/', views.join, name='join'),
    # path('payments/', views.payments, name='payments'),
    # # #path('changepassword/',PasswordsChangeView.as_view(template_name='accounts/registration/password_Change_Form.html'), name='password_Change_Form'),
    # path('transactionlist/', views.Transaction_list, name='transactionlist'),
    # path('transaction/', views.transaction_create_view, name='transaction'),
    # path('transaction_create/', views.transaction_create, name='transaction_create'),
    # path('users/', views.customer_user_list, name='users'),
    # #path('generate-transactions/', generate_transactions_view, name='generate-transactions'),
    # # path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    # #path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
    # # #path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/registration/join.html'), name='user-update'),
    # # path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),
]