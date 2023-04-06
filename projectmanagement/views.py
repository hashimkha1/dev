from django.contrib.auth.decorators import login_required
from django.shortcuts import  render
from django.contrib.auth import get_user_model

#User=settings.AUTH_USER_MODEL
User = get_user_model()

@login_required
def home(request):
    return render(request, 'main/home_templates/management_home.html',{'title': 'home'})

@login_required
def construction(request):
    return render(request, 'projectmanagement/construction.html', {'title': 'construction'})
