from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#from django.db.models import Q
# Create your views here.
from .models import CustomerUser
from .forms import CustomerForm
from .decorators import unauthenticated_user
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
                return redirect('user-login')
    else:
        form=CustomerForm()
    return render(request, 'accounts/join.html', {'form': form})
'''
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('main-home')
        else:
            messages.info(request, 'USERNAME OR PASSWORD is incorrect!Please try again')
    context={}
    return render(request, 'accounts/login.html', context)
'''
@login_required
#@allowed_users(allowed_roles=['admin'])
def clients(request):
    #clients=CustomerUser.objects.all().order_by('-date_joined')
    clients=CustomerUser.objects.filter(category = 1)|CustomerUser.objects.filter(category = 2).order_by('-date_joined')
    return render(request, 'accounts/clients.html', {'clients': clients})


