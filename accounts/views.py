from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.utils.timezone import datetime
import calendar
from django.views.generic import (CreateView, DeleteView,UpdateView)

from .forms import CustomerForm
from .models import CustomerUser


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
    clients=CustomerUser.objects.filter(category = 1)|CustomerUser.objects.filter(category = 2).order_by('-date_joined')
    return render(request, 'accounts/clients.html', {'clients': clients})
 