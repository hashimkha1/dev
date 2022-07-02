from django.urls import path
from . import views
from .views import (
                    UserUpdateView,UserDeleteView,SuperuserUpdateView,
                    ClientUpdateView,ClientDeleteView,ClientDetailView,
                    Employeelist,
                    TrackCreateView, TrackDeleteView, TrackDetailView,
                    TrackListView, TrackUpdateView,
                    )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    path('login/', views.login_view, name='account-login'),
    #path('changepassword/',PasswordsChangeView.as_view(template_name='accounts/registration/password_Change_Form.html'), name='password_Change_Form'),
    path('profile/', views.profile, name='account-profile'),
    path('users/', views.users, name='accounts-users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
    #path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/registration/join.html'), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),

    #=============================CLIENTS VIEWS=====================================
    path('clients/', views.clientlist, name='clients'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    #path('applicants/', views.applicantlist, name='applicants'),
    #=============================EMPLOYEES VIEWS=====================================
    path('employees/', views.Employeelist, name='employees'),
    # path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    # path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    # path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    #path('applicants/', views.applicantlist, name='applicants'),
    #=============================CLIENTS WORK=====================================
    path('tracker/', TrackListView.as_view(), name='tracker-list'),
    #path('user/<str:username>', UserTrackListView.as_view(), name='user-list'),
    #path('user_tracker/', UserTrackListView.as_view(), name='single-list'),
    path('client/<str:username>/', views.usertracker, name='user-list'),
    path('track/new/', TrackCreateView.as_view(), name='tracker-create'),
    path('track/<int:pk>/', TrackDetailView.as_view(), name='tracker-detail'),
    path('track/<int:pk>/update/', TrackUpdateView.as_view(), name='tracker-update'),
    path('track/<int:pk>/delete/', TrackDeleteView.as_view(), name='tracker-delete'),
    path('thank/',views.thank, name='thank-you'),
]