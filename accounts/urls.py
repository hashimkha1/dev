from django.urls import path
from . import views
#from .views import (
 #                   UserUpdateView,UserDeleteView,SuperuserUpdateView                   
 #                   )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    # path('join/', views.join, name='join'),
    # #path('login/', views.login_view, name='account-login'),
    # #path('changepassword/',PasswordsChangeView.as_view(template_name='accounts/registration/password_Change_Form.html'), name='password_Change_Form'),
    # # path('profile/', views.profile, name='account-profile'),
    # path('users/', views.users, name='accounts-users'),
    # path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    # path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
    # #path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/registration/join.html'), name='user-update'),
    # path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),
]