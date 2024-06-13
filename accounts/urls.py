from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('JobDetails_list/', views.JobDetails_list, name='account-JobDetails_list'),  # Corrected URL pattern
    path('login/', views.login_view, name='account-login'),
    path('profile/', views.profile, name='account-profile'),
]
