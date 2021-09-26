from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomerUser,Employee
from .forms import CustomerForm,EmployeeForm
from .decorators import unauthenticated_user
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse
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


# Create your views here. 
'''
def addnew(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('accounts/show')  
            except:  
                pass 
    else:  
        form = EmployeeForm()  
    return render(request,'accounts/addnew.html',{'form':form})  

''' 

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model=Employee
    fields=['name','email','contact']

    def form_valid(self,form):
        form.instance.name=str(self.request.user)
        return super().form_valid(form)  

    def get_success_url(self):
        return reverse('employee-records') 

class EmployeeUpdateView(LoginRequiredMixin,UpdateView):
    model=Employee
    fields=['name','email','contact']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('employee-records') 

'''
    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False

'''

def show(request):  
    employees = Employee.objects.all()  
    return render(request,"accounts/employees.html",{'employees':employees})  


class EmployeeDeleteView(LoginRequiredMixin,DeleteView):
    model=Employee

    def get_success_url(self):
        return reverse('employee-records') 


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


