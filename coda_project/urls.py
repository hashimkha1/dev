"""
coda_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import handler400
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from users import views as user_views


#===========ERROR HANDLING SECTION================
handler400='main.views.hendler400'
handler403='main.views.hendler403'
handler300='main.views.hendler300'
handler500='main.views.hendler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='user-register'),
    path('registered/', user_views.registered, name='user-registered'),
    path('profile/', user_views.profile, name='user-profile'),
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='accounts-login'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='user-logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('blog/', include('codablog.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('data/', include('data.urls')),
    path('getdata/', include('getdata.urls')),
    path('application/', include('application.urls')),
    path('projectmanagement/', include('projectmanagement.urls')),
    path('investing/', include('investing.urls')),
    path('store/', include('store.urls')),
    path('management/', include('management.urls'),name='management'),
    path('', include('main.urls')),
   # path('testing/', include('testing.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
