import datetime
from datetime import date ,timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user
from django.db.models.aggregates import Avg, Sum
from .forms import CustomerForm  # , TimeForm  , SignUpForm, UserLoginForm, UserRegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from .models import CustomerUser,Tracker

# Create your views here..

#@allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, 'main/home_templates/layout.html')

#---------------ACCOUNTS VIEWS----------------------
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
    
def clientlist(request):
    clients=CustomerUser.objects.filter(category = 1)|CustomerUser.objects.filter(category = 2).order_by('-date_joined')
    return render(request, 'accounts/clients/clientlist.html', {'clients': clients})

@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    template_name='accounts/clients/client_detail.html'
    model=CustomerUser
    ordering=['-date_joined ']

class ClientUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=CustomerUser
    success_url="/accounts/clients"
    fields=['category','address','city','state','country']
    form=CustomerForm
    def form_valid(self,form):
        #form.instance.username=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        return False
    def test_func(self):
        client = self.get_object()
        #if self.request.user == client.username:
        if self.request.user.is_superuser:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class ClientDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=CustomerUser
    success_url='/accounts/clients'

    def test_func(self):
        client = self.get_object()
        #if self.request.user == client.username:
        if self.request.user.is_superuser:
            return True
        return False


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
            return redirect('main:layout')
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


#----------------------TIME TRACKING CLASS-BASED VIEWS--------------------------------
@method_decorator(login_required, name='dispatch')
class TrackDetailView(DetailView):
    model=Tracker
    ordering=['-login_date']

@method_decorator(login_required, name='dispatch')
class TrackListView(ListView):
    model=Tracker
    template_name='accounts/tracker.html'
    context_object_name='trackers'
    ordering=['-login_date']
    


def usertracker(request):
    #trackers=Tracker.objects.all().order_by('-login_date')
    #user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
    trackers=Tracker.objects.filter(author=request.user).order_by('-login_date')
    #total_duration=Tracker.objects.all().aggregate(Sum('duration'))
    #total_communication=Rated.objects.all().aggregate(Sum('communication'))
    total_time=Tracker.objects.all().aggregate(Your_Total_Time=Sum('duration'))
    time=total_time.get('Your_Total_Time')
    context = {
                'trackers': trackers,
                'total_time':total_time,
                'time':time
                
              }
    return render(request, 'accounts/usertracker.html', context)
    
''' 
@method_decorator(login_required, name='dispatch')
class UserTrackListView(ListView):
    model=Tracker
    template_name='accounts/user_tracker.html'
    context_object_name='trackers'
    ordering=['-login_date']

    def get_queryset(self):
        user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
        return Tracker.objects.filter(author=user).order_by('-login_date')
'''

@method_decorator(login_required, name='dispatch')
class TrackCreateView(LoginRequiredMixin, CreateView):
    model=Tracker
    success_url="/accounts/usertracker"
    fields=['category','task','duration']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)    

@method_decorator(login_required, name='dispatch')
class TrackUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Tracker
    success_url="/accounts/tracker"
    fields=['author','category','task','duration']

    def form_valid(self,form):
        #form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        track = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==track.author:
            return True
        return False
        
@method_decorator(login_required, name='dispatch')
class TrackDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Tracker
    success_url="/accounts/tracker"

    def test_func(self):
        #timer = self.get_object()
        #if self.request.user == timer.author:
        #if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False
