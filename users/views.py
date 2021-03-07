from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.models import User,Group
from .decorators import unauthenticated_user,allowed_users

# Create your views here..
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def registered(request):
    clients=User.objects.all().order_by('-first_name')
    return render(request, 'users/registered.html', {'clients': clients})

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'username OR Password is incorrect')
        form = UserRegisterForm(request.POST)
    context={}
    return render(request, 'users/login.html', context)

    
@login_required(login_url='user-login')
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def home(request):
    return render(request, 'main/home.html')