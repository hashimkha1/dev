from django.contrib.auth.mixins import LoginRequiredMixin #,UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.urls.conf import include
from django.utils.timezone import datetime
from dateutil.parser import parse
import calendar
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                UpdateView)
from .models import Employee ,Department,Category, Activity

from .forms import TransactionForm
from .models import Transaction



def home(request):
    return render(request, 'management/home.html',{'title': 'home'})

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
    template_name='management/employees.html'  #<app>/<model>_<viewtype>
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
        return reverse('management:employee-list') 
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

def construction(request):
    return render(request, 'projectmanagement/construction.html', {'title': 'construction'})


# -------------------------transactions Section-------------------------------------#

def transact(request):
    if request.method== "POST":
        form=TransactionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/management/transaction/')
    else:
        form=TransactionForm()
    return render(request, 'management/company_finances/transact.html',{'form':form})

def transaction(request):
    transactions=Transaction.objects.all().order_by('-activity_date')
    return render(request, 'management/company_finances/transaction.html', {'transactions': transactions})


# -------------------------DAF Section-------------------------------------#

def all_activities(request):
    activities =Activity.activities.all()
    return render(request, 'management/home.html', {'activities': activities})


def department_list(request, department_slug=None):
    department = get_object_or_404(Department, slug=department_slug)
    categories = Category.objects.filter(department=department)
    context ={
                'department': department,
                'categories': categories,
             }
    return render(request, 'management/company_finances/department.html', context)




def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    #activities = Activity.objects.filter(category__in=category.get_descendants(include_self=True))
    #activities=Activity.objects.get(category__pk__in=category.get_descendants(include_self=True).values_list('pk'))
    activities = Activity.objects.filter(category=category)
    #activities = Activity.objects.filter(
       # category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    #)
    today = datetime.today()
    deadline_date=datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
    deadline=datetime.date(deadline_date)
 

    context ={
                'category': category,
                'activities': activities,
                'deadline':deadline
             }
    return render(request, 'management/company_finances/category.html', context)

def activity_detail(request,slug,category_slug=None):
    activity = get_object_or_404(Activity, slug=slug, is_active=True)
    today = datetime.today()
    deadline_date=datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
    deadline=datetime.date(deadline_date)

    context ={
                'activity': activity,
                'deadline':deadline
             }
    return render(request, 'management/company_finances/activity.html',context)

class ActivityUpdateView(LoginRequiredMixin,UpdateView):
    model=Activity
    #fields=['category','created_by','activity_name','description','slug','earning','point','mx_point','submission','created','updated']
    fields=['activity_name','point','submission']
    #success_url='/management/category/{slug}/'
    #success_url="/parent/{parent_id}/" 
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    
'''
    def get_success_url(self):
        return reverse('management:category_list', kwargs={
            'category_slug': self.object.category_slug,
        })

    def get_success_url(self):
        return self.request.GET.get('next', '/management/')

    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False
    '''  