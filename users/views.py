from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import SignUpForm, UserLoginForm, UserRegisterForm

#from .decorators import unauthenticated_user,allowed_users

# Create your views here..
# @unauthenticated_user

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('user-login')
    else:
        form = SignUpForm(request.POST)
    return render(request, 'users/register.html',{'form':form})
'''
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not none:
            login(request,user)
            return redirect(home)
        else:
            messages.info(request, 'USERNAME OR PASSWORD is incorrect!Please try again')
    context={ }
    return render(request, 'users/register.html', context)

'''
'''
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            category = form.cleaned_data.get('category')
            messages.success(request, f'Account created for {username}!')
            if category == Applicant:
                return render(request, 'users/register.html', {'form': form})
            else:
                return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

'''
def registered(request):
    clients=User.objects.all().order_by('-first_name')
    return render(request, 'users/registered.html', {'clients': clients})

@login_required(login_url='user-login')
def profile(request):
    return render(request,'users/profile.html')



