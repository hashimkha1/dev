from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.db.models.aggregates import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import (ApplicantForm, ApplicationForm, EmployeeForm,
                    InterviewForm, InterviewUploadForm, PolicyForm, RatingForm,
                    ReportingForm)
from .models import (Application, Employee, FirstUpload, InteviewUploads,
                     Policy, Rated, Reporting)

#from .filters import RatingFilter

#Interview description data
posts=[

{
	'Inteview':'First   Interview',
	'Concentration':'Data Analysis',
	'Description':'Understanding SQL,Tableau & Alteryx	',
	'Duration':'5 Days	',
	'Lead':'HR Manager'
},

{
	'Inteview':'Second Interview',
	'Concentration':'General Tools& Company Projects',
	'Description':'Understanding Company Projects, Values & Systems	',
	'Duration':'5 Days	',
	'Lead':'HR Manager'
},

{
	'Inteview':'Final Interview',
	'Concentration':'Data Analysis 1-1 Sessions',
	'Description':'Measuring,assessing Time sensitivity.',
	'Duration':'7 Days',
	'Lead':'Scrum Master'
}
]


# Create your views here.
class application(TemplateView):
    template_name='application.html'

# Saving uploaded information to database
def apply(request):
    if request.method== "POST":
        form=ApplicantForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-policies')
    else:
        form=ApplicantForm()
    return render(request, 'application/apply.html',{'form':form})

class ApplicantListView(ListView):
    model=Application
    template_name='application/applicants.html'  #<app>/<model>_<viewtype>
    context_object_name='applicants'
    ordering=['-application_date']

class ApplicantDeleteView(LoginRequiredMixin,DeleteView):
    model=Application

    def get_success_url(self):
        return reverse('applicant-list')

@login_required
def applicant_profile(request):
    return render(request, 'application/applicant_profile.html')

# # ------------------------Interview Section-------------------------------------#.
def career(request):
    return render(request, 'application/career.html', {'title': 'career'})

def interview(request):
    context = {
        'posts': posts
    }
    return render(request, 'application/interview.html', context)
    
def first_interview(request):
    return render(request, 'application/first_interview.html', {'title': 'first_interview'})

def second_interview(request):
    return render(request, 'application/second_interview.html', {'title': 'second_interview'})

def orientation(request):
    return render(request, 'application/orientation.html', {'title': 'orientation'})


def internal_training(request):
    return render(request, 'application/internal_training.html', {'title': 'orientation'})


def policy(request):
    if request.method== "POST":
        form=PolicyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-policies')
    else:
        form=PolicyForm()
    return render(request, 'application/policy.html',{'form':form})

def policies(request):
    reporting_date = date.today() + timedelta(days=7)
    uploads=Policy.objects.all().order_by('upload_date')
    context = {
        'uploads': uploads,
        'reporting_date': reporting_date
    }
    return render(request, 'application/policies.html',context)

# -------------------------Uploads Section-------------------------------------#
def firstupload(request):
    if request.method== "POST":
        form=InterviewForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-second_interview')
    else:
        form=InterviewForm()
    return render(request, 'application/firstupload.html',{'form':form})

def fupload(request):
    iuploads=FirstUpload.objects.all().order_by('-upload_date')
    return render(request, 'application/fupload.html', {'iuploads': iuploads})

# -------------------------rating Section-------------------------------------#
def rate(request):
    if request.method== "POST":
        form=RatingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-rating')
    else:
        form=RatingForm()
    return render(request, 'application/rate.html',{'form':form})

def rating(request):
   
    ratings=Rated.objects.all().order_by('-rating_date')
    #total_customers = customers.count()
	#total_orders = orders.count()
	#delivered = orders.filter(status='Delivered').count()
	#pending = orders.filter(status='Pending').count()
    total_punctuality=Rated.objects.all().aggregate(Sum('punctuality'))
    total_communication=Rated.objects.all().aggregate(Sum('communication'))
    #total_understanding=Rated.objects.filter(user=self.request.user).aggregate(total_credit=Sum('subject__credit'))
    total_understanding=Rated.objects.all().aggregate(Total_Understanding=Sum('understanding'))
    #total_ratings=ratings.count()
    #myFilter = RatingFilter(request.GET, queryset=ratings)
    #ratings = myFilter.qs 
    context = {'ratings': ratings
    #,'myFilter':myFilter
    ,'total_punctuality': total_punctuality
    ,'total_communication': total_communication
    ,'total_understanding': total_understanding}
    return render(request, 'application/rating.html', context)

def employee_form(request,id=0):
    if request.method == "GET":
        if id == 0:
            form=EmployeeForm()
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(instance=employee)
        return render(request, 'application/employee_form.html',{'form':form})
    else:
        if id==0:
            form=EmployeeForm(request.POST,request.FILES)
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(request.POST,request.FILES,instance=employee)
        if form.is_valid():
            form.save()
        return redirect('application-emp_list')

def employee_insert(request):
    if request.method== "POST":
        form=Employee(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-update')
    else:
        form=EmployeeForm()
    return render(request, 'application/rate.html',{'form':form})

def employee_list(request):
    context={'employees': Employee.objects.all().order_by('-punctuality')}
    return render(request, 'application/employee_list.html',context)


def employee_delete(request,id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('application-emp_list')


#------------------------testing Section-----------------------------------------#

def success_stories(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'codablog/success.html', context)

# -------------------------rating Section-------------------------------------#
def trainee(request):
    if request.method== "POST":
        form=ReportingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-trainees')
    else:
        form=ReportingForm()
    return render(request, 'application/trainee.html',{'form':form})

def trainees(request):
    trainees=Reporting.objects.all().order_by('-update_date')
    return render(request, 'application/trainees.html', {'trainees': trainees})


class TraineeUpdateView(LoginRequiredMixin,UpdateView):
    model=Reporting
    fields = ['first_name','last_name','gender','reporting_date','method','interview_type','comment']
    form=ReportingForm()
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('application-trainees') 
'''
    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False

'''
class TraineeDeleteView(LoginRequiredMixin,DeleteView):
    model=Reporting

    def get_success_url(self):
        return reverse('application-trainees') 