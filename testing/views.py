from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse
from .models import Employee
from .forms import EmployeeForm


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model=Employee
    fields=['name','email','contact']

    def form_valid(self,form):
        form.instance.name=str(self.request.user)
        return super().form_valid(form)  

    #def get_success_url(self):
   #     return reverse('employees') 

class EmployeeListView(ListView):
    model=Employee
    template_name='testing/employees.html'  #<app>/<model>_<viewtype>
    context_object_name='employees'
    ordering=['-entry_date']

class EmployeeDetailView(DetailView):
    model=Employee



class EmployeeUpdateView(LoginRequiredMixin,UpdateView):
    model=Employee
    fields=['email','contact']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('employee-list') 

'''
    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False

'''


class EmployeeDeleteView(LoginRequiredMixin,DeleteView):
    model=Employee

    def get_success_url(self):
        return reverse('employee-list') 


'''
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

'''