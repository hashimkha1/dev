from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect, render

from .decorators import unauthenticated_user
from .forms import CustomerForm  # , SignUpForm, UserLoginForm, UserRegisterForm
from .models import CustomerUser

# Create your views here..

#---------------Test----------------------
@unauthenticated_user
def join(request):
    if request.method== "POST":
        form=CustomerForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            category = form.cleaned_data.get('category')
            messages.success(request, f'Account created for {username}!')
            if category == "Applicant":
                return render(request, 'application/first_interview.html')
            else:
                return redirect('account-login')
    else:
        form=CustomerForm()
    return render(request, 'accounts/registration/join.html', {'form': form})
    
#@allowed_users(allowed_roles=['admin'])

def home(request):
    return render(request, 'main/home_templates/layout.html')

def clients(request):
    clients=CustomerUser.objects.filter(category = 1)|CustomerUser.objects.filter(category = 2).order_by('-date_joined')
    return render(request, 'accounts/clients.html', {'clients': clients})

@login_required(login_url='account-login')
def profile(request):
    return render(request,'accounts/profile.html')

'''
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(request,username=username, password=password)
        if account is not None:
            login(request,account)
            return redirect('main-layout')
        else:
            messages.info(request, 'USERNAME OR PASSWORD is incorrect!Please try again')
    context={}
    return render(request, 'accounts/login.html', context)
@login_required
 
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('account-login')
    else:
        form = SignUpForm(request.POST)
    return render(request, 'users/register.html',{'form':form})

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
                return redirect('account-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def registered(request):
    clients=User.objects.all().order_by('-first_name')
    return render(request, 'users/registered.html', {'clients': clients})
'''
