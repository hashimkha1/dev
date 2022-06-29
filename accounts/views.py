import datetime
from datetime import date ,timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.urls import reverse, reverse_lazy
#from django.contrib.auth.views import PasswordChangeView ,PasswordSetView
#from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user
from django.db.models.aggregates import Avg, Sum
from .forms import UserForm,LoginForm # , TimeForm  , SignUpForm, UserLoginForm, UserRegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from .models import CustomerUser,Tracker
from django.db.models import Q
from management.models import Task
from application.models import Applicant_Profile
# Create your views here..

#@allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, 'main/home_templates/layout.html')
    

#@allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, 'accounts/clients/thank.html')
#---------------ACCOUNTS VIEWS----------------------

@unauthenticated_user
def join(request):
    if request.method== "POST":
        form=UserForm(request.POST,request.FILES)

        if form.is_valid():
            print("category",form.cleaned_data.get('category'))

            # if form.cleaned_data.get('category') == 1: # Applicant
            #     form.instance.is_applicant = True
            # elif form.cleaned_data.get('category') == 2:# Staff
            #     form.instance.is_employee = True 
            # elif form.cleaned_data.get('category') == 3:# Client
            #     form.instance.is_client = True 
            # else:
            #     form.instance.is_admin = True 

            if form.cleaned_data.get('category') == 2:# Staff-->Full,Agent,Other
                if form.cleaned_data.get('sub_category') == 6:
                    form.instance.is_admin = True
                    form.instance.is_superuser = True 
                else:
                    form.instance.is_employee = True 
            elif form.cleaned_data.get('category') == 3:# Client
                form.instance.is_client = True 
            else:
                form.instance.is_applicant = True
            form.save()

            # print("request user data",form.instance.id)
            # custom_get = CustomerUser.objects.get(id=form.instance.id)
            # Applicant_Profile.objects.create(applicant=custom_get,section="",image="")

            username = form.cleaned_data.get('username')
            category = form.cleaned_data.get('category')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:account-login')
    else:
        msg = 'error validating form'
        form=UserForm()
        print(msg)
    return render(request, 'accounts/registration/join.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            account = authenticate(username=username, password=password)
        
            # If Category is Staff/employee
            if account is not None and account.category==2:
                if account.sub_category==2:# contractual
                    login(request, account)
                    return redirect('management:requirements-active')
                else:# parttime (agents) & Fulltime
                    login(request, account)
                    return redirect('management:user_task', username=request.user )
            # If Category is client/customer
            elif account is not None and account.category==3:
                if account.sub_category==1:# Job Support
                    login(request, account)
                    return redirect('accounts:user-list', username=request.user)
                else:# Student
                    login(request, account)
                    return redirect('data:bitraining')
            # If Category is applicant
            elif account is not None and account.category==1:
                if account.country in ('KE','UG','RW','TZ'):# Male
                    if account.gender==1:
                        login(request, account)
                        return redirect('application:firstinterview')
                    else:
                        login(request, account)
                        return redirect('application:first_interview')
                else:
                    login(request, account)
                    return redirect('application:firstinterview')

            elif account is not None and account.is_admin:
                login(request, account)
                return redirect('main:layout')
            else:
                messages.success(request,f'Invalid credentials.Kindly Try again!!')
    return render(request, 'accounts/registration/login.html', {'form': form, 'msg': msg})

#================================USERS SECTION================================
def users(request):
    users=CustomerUser.objects.all().order_by('-date_joined')
    if request.user.is_superuser:
        return render(request, 'accounts/admin/users.html', {'users': users})
    else:
        return redirect('accounts:account-login')
class UserUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=CustomerUser
    success_url="/accounts/users"
    #fields=['category','address','city','state','country']
    fields=[
            'category','sub_category','first_name','last_name','date_joined',
            'email','gender','phone','address','city','state','country','is_superuser',
            'is_admin','is_employee','is_client','is_applicant', 'is_active','is_staff',
            ]
    def form_valid(self,form):
        #form.instance.username=self.request.user
        # if request.user.is_authenticated:
         if self.request.user.is_superuser: #or self.request.user.is_authenticated :
             return super().form_valid(form)
        #  elif self.request.user.is_authenticated:
        #      return super().form_valid(form)
         return False

    def test_func(self):
        user = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser: #or self.request.user == user.username:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class UserDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=CustomerUser
    success_url='/accounts/users'

    def test_func(self):
        user = self.get_object()
        #if self.request.user == user.username:
        if self.request.user.is_superuser:
            return True
        return False

def PasswordResetCompleteView(request):
    return render(request, 'accounts/registration/password_reset_complete.html')
    
''' 
class PasswordsChangeView(PasswordChangeView):
    #model=CustomerUser
    from_class=PasswordChangeForm
    template_name='accounts/registration/password_change_form.html'
    success_url=reverse_lazy('accounts:account-login')

class PasswordsSetView(PasswordChangeView):
    #model=CustomerUser
    from_class=SetPasswordForm
    success_url=reverse_lazy('accounts:account-login')

def reset_password(email, from_email, template='registration/password_reset_email.html'):
    """
    Reset the password for all (active) users with given E-Mail adress
    """
    form = PasswordResetForm({'email': email})
    #form = PasswordResetForm({'email':'sample@sample.com'})
    return form.save(from_email=from_email, email_template_name=template)
''' 
#================================CLIENT SECTION================================
def clientlist(request):
    clients=CustomerUser.objects.filter(category = 3).order_by('-date_joined')
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
    form=UserForm
    def form_valid(self,form):
        #form.instance.username=self.request.user
        # if request.user.is_authenticated:
         if self.request.user.is_superuser or self.request.user.is_authenticated :
             return super().form_valid(form)
        #  elif self.request.user.is_authenticated:
        #      return super().form_valid(form)
         return False
    def test_func(self):
        client = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser or self.request.user == client.username:
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

@login_required(login_url='accounts:account-login')
def profile(request):
    return render(request,'accounts/profile.html')

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
    #total_time=Tracker.objects.all().aggregate(Your_Total_Time=Sum('duration'))

def usertracker(request, user=None, *args, **kwargs):
    #trackers=Tracker.objects.all().order_by('-login_date')
    #user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
    #trackers=Tracker.objects.filter(author=request.user).order_by('-login_date')
    user = get_object_or_404(CustomerUser, username=kwargs.get('username'))
    trackers=Tracker.objects.all().filter(author=user).order_by('-login_date')
    num =trackers.count()
    my_time=trackers.aggregate(Assigned_Time=Avg('time')) 
    Used=trackers.aggregate(Used_Time=Sum('duration'))  
    Usedtime=Used.get('Used_Time')
    plantime=my_time.get('Assigned_Time')
    try:
        delta=round(plantime-Usedtime)
    except (TypeError, AttributeError):
        delta=0
        return render(request, 'accounts/tracker.html')
    context = {
                'trackers': trackers,
                'num':num,
                'plantime': plantime,
                'Usedtime':Usedtime,
                'delta':delta
                
              }
              
    return render(request, 'accounts/usertracker.html', context)     
"""     if request.user == user:
        return render(request, 'accounts/usertracker.html', context)
    elif request.user.is_superuser:
        return render(request, 'accounts/usertracker.html', context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")
 """

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
    success_url="/accounts/tracker"
    #success_url="usertime"
    #fields=['category','task','duration']
    fields=['employee','author','category','task','duration','plan']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)  
''' 
@method_decorator(login_required, name='dispatch')
class TrackCreateView(LoginRequiredMixin, CreateView):
    model=Tracker
    success_url="/accounts/tracker"
    #success_url="usertime"
    # There is need to look at the column for client to get the id
    fields=['employee','author','category','task','duration','plan']

    def form_valid(self,form):
        form.instance.author=self.request.user
        total_duration_fil = Tracker.objects.filter(author=self.request.user)
        total_duration = 0
        for data in total_duration_fil.all():
            total_duration += data.duration
        # Needs a validation message if the employee does not have tasks

        #print("total_duration",total_duration)
        #x=Task.objects.values_list("mxpoint",flat=True).get(employee=self.request.user)
        #print("Values",x)
        if form.instance.duration+total_duration > Task.objects.values_list("mxpoint",flat=True).get(employee=self.request.user): 
            messages.error(self.request, "Total duration is greater than maximum assigned points.")
            return super().form_invalid(form)
        return super().form_valid(form)  
'''
@method_decorator(login_required, name='dispatch')
class TrackUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Tracker
    success_url="/accounts/tracker"

    fields=['employee','author','plan','category','task','duration','time']
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

#=======================TESTING=======================
'''
@method_decorator(login_required, name='dispatch')
class CustomerUserCreateView(LoginRequiredMixin, CreateView):
    model=CustomerUser
    success_url="/accounts/tracker"
    #success_url="usertime"
    #fields=['username','task','duration']
    fields=['first_name','last_name','date_joined','email','gender','phone','address','city','state','country','category']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)  

@login_required
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:account-login')
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
                return redirect('accounts:account-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

'''