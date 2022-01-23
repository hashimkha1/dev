import calendar

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import datetime
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import TransactionForm
from .models import Activity, Category, Employee, Transaction,Department


def home(request):
    return render(request, 'main/home_templates/management_home.html',{'title': 'home'})

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
        return reverse('projectmanagement:employee-list') 
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
    return render(request, 'projectmanagement/company_finances/transact.html',{'form':form})

def transaction(request):
    transactions=Transaction.objects.all().order_by('-activity_date')
    return render(request, 'projectmanagement/company_finances/transaction.html', {'transactions': transactions})


# -------------------------DAF Section-------------------------------------#
@login_required
def all_activities(request):
    activities =Activity.activities.all()
    return render(request, 'main/home_templates/management_home.html', {'activities': activities})
    
@login_required
def department_list(request, department_slug=None):
    department = get_object_or_404(Department, slug=department_slug)
    categories = Category.objects.filter(department=department)
    context ={
                'department': department,
                'categories': categories,
             }
    return render(request, 'projectmanagement/company_finances/department.html', context)

@login_required
def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    activities = Activity.objects.filter(category=category)
    today = datetime.today()
    deadline_date=datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
    deadline=datetime.date(deadline_date)

    context ={
                'category': category,
                'activities': activities,
                'deadline':deadline
             }
    return render(request, 'projectmanagement/company_finances/category.html', context)

@login_required
def activity_detail(request,slug,category_slug=None):
    activity = get_object_or_404(Activity, slug=slug, is_active=True)
    today = datetime.today()
    deadline_date=datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
    deadline=datetime.date(deadline_date)

    context ={
                'activity': activity,
                'deadline':deadline
             }
    return render(request, 'projectmanagement/company_finances/activity.html',context)

class ActivityUpdateView(LoginRequiredMixin,UpdateView):
    model=Activity
    #fields=['category','created_by','activity_name','description','slug','earning','point','mx_point','submission','created','updated']
    fields=['activity_name','description','point']
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        agent_slug = self.object.category.slug
        return reverse_lazy('projectmanagement:category_list', kwargs={'category_slug': agent_slug})

'''
    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False
    '''  

