from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Sum
from django.db.models.aggregates import Avg, Sum
from django.shortcuts import  redirect, render
from django.urls import reverse
from django.views.generic import (DeleteView,ListView,TemplateView, UpdateView)
from .forms import (ApplicantForm, PolicyForm, RatingForm, ReportingForm)
from accounts.forms import (UserForm)
from .models import (Application, Policy, Rated,Reporting)
from .utils import (posts, alteryx_list,dba_list,tableau_list)

#from .filters import RatingFilter

# Create your views here.

#=============================APPLICATION VIEWS=====================================
#@unauthenticated_user
def apply(request):
    if request.method== "POST":
        form=UserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #category = form.cleaned_data.get('category')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            messages.success(request, f'Account created for {username}!')
            if country in ('KE','UG','RW','TZ'): #  Male East Africa
                if gender==1: #  Males in East Africa
                    return redirect('application:firstinterview')
                    #return render(request, 'application/interview_process/firstinterview.html') 
                elif gender==2: # Females in East Africa
                    return redirect('application:firstinterview')
            #  Everyone outside East Africa
            else:
                return redirect('application:firstinterview')
    else:
        messages.success(request, f'Account Not Created, Please Try Again!!')
        form=UserForm()
    return render(request, 'application/applications/application.html', {'form': form})

class ApplicantListView(ListView):
    model=Application
    template_name='application/applications/applicants.html'  #<app>/<model>_<viewtype>
    context_object_name='applicants'
    ordering=['-application_date']

class application(TemplateView):
    template_name='application.html'

class ApplicantDeleteView(LoginRequiredMixin,DeleteView):
    model=Application
    template_name='application/applications/applicants.html'

    def get_success_url(self):
        return reverse('applicant-list')

'''
def applicantlist(request):
    applicants=CustomerUser.objects.filter(category = 2).order_by('-date_joined')
    return render(request, 'accounts/applications/applicantlist.html', {'applicants': applicants})

class ApplicantDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Application
    success_url='/application/applications/applicants.html'

    def test_func(self):
        applicant = self.get_object()
        if self.request.user == 'admin':
            return True
        return False
'''     
@login_required
def applicant_profile(request):
    return render(request, 'application/applications/applicant_profile.html')

#------------------------Interview Section-------------------------------------#.
def career(request):
    return render(request, 'application/applications/career.html', {'title': 'career'})

def interview(request):
    context = {
        'posts': posts
    }
    return render(request, 'application/interview_process/interview.html', context)
    
def first_interview(request):
    return render(request, 'application/interview_process/first_interview.html', {'title': 'first_interview'})

def firstinterview(request):
    context = {
        'alteryx_list': alteryx_list,
        'dba_list': dba_list,
        'tableau_list': tableau_list
    }
    return render(request, 'application/interview_process/firstinterview.html', context)

def second_interview(request):
    return render(request, 'application/interview_process/second_interview.html', {'title': 'second_interview'})

def orientation(request):
    return render(request, 'application/orientation/orientation.html', {'title': 'orientation'})

def internal_training(request):
    return render(request, 'application/orientation/internal_training.html', {'title': 'orientation'})

def policy(request):
    if request.method== "POST":
        form=PolicyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-policies')
    else:
        form=PolicyForm()
    return render(request, 'application/orientation/policy.html',{'form':form})

def policies(request):
    reporting_date = date.today() + timedelta(days=7)
    uploads=Policy.objects.all().order_by('upload_date')
    context = {
        'uploads': uploads,
        'reporting_date': reporting_date
    }
    return render(request, 'application/orientation/policies.html',context)

def info(request):
    reporting_date = date.today() + timedelta(days=7)
    uploads=Policy.objects.all().order_by('upload_date')
    context = {
        'uploads': uploads,
        'reporting_date': reporting_date
    }
    return render(request, 'application/orientation/applicant_info.html',context)

# -------------------------Uploads Section-------------------------------------#
def firstupload(request):
    if request.method== "POST":
        form=InterviewForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-second_interview')
    else:
        form=InterviewForm()
    return render(request, 'application/interview_process/firstupload.html',{'form':form})

def fupload(request):
    iuploads=FirstUpload.objects.all().order_by('-upload_date')
    return render(request, 'application/interview_process/fupload.html', {'iuploads': iuploads})

# -------------------------rating Section-------------------------------------#
def rate(request):
    if request.method== "POST":
        form=RatingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-rating')
    else:
        form=RatingForm()
    return render(request, 'application/orientation/rate.html',{'form':form})

def rating(request):
    ratings=Rated.objects.all().order_by('-rating_date')
    total_punctuality=Rated.objects.all().aggregate(Sum('punctuality'))
    total_communication=Rated.objects.all().aggregate(Sum('communication'))
    total_understanding=Rated.objects.all().aggregate(Total_Understanding=Sum('understanding'))
    context = {
                'ratings': ratings
                ,'total_punctuality': total_punctuality
                ,'total_communication': total_communication
                ,'total_understanding': total_understanding
              }
    return render(request, 'application/orientation/rating.html', context)


# -------------------------rating Section-------------------------------------#
def trainee(request):
    if request.method== "POST":
        form=ReportingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application:trainees')
    else:
        form=ReportingForm()
    return render(request, 'application/orientation/trainee.html',{'form':form})

def trainees(request):
    trainees=Reporting.objects.all().order_by('-update_date')
    return render(request, 'application/orientation/trainees.html', {'trainees': trainees})


class TraineeUpdateView(LoginRequiredMixin,UpdateView):
    model=Reporting
    fields = ['first_name','last_name','gender','reporting_date','method','interview_type','comment']
    form=ReportingForm()
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('application:trainees') 
    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False
        

class TraineeDeleteView(LoginRequiredMixin,DeleteView):
    model=Reporting
    def get_success_url(self):
        return reverse('application:trainees') 


#============JQUERY IMPLEMENTATION======================================
'''

def applicants(request):
    return render(request, 'application/applications/applicants.html')
  
def get_total(request):
    title = 'All Applicants'
    queryset = Application.objects.all()
    total_earning = Application.objects.aggregate(Sum("mx_earning"))
    context = {
    "title": title,
    "queryset": queryset,
    "total_earning": total_earning,
    }
    return render(request, 'application/table.html', context)


#API data
def ApplicationDataAPI(request):
    data = Application.objects.all().order_by('-application_date')
    dataList = []
    for i in data:
        dataList.append({
                            'id':i.id,
                            'username':i.username,
                            'first_name':i.first_name,
                            'last_name':i.last_name,
                            'phone':i.phone,
                            'submitted':i.submitted,
                            'phone':i.phone,
                            'country':i.country,
                         })
    
    return JsonResponse(dataList, safe=False)

@csrf_exempt
def updateApplication(request):
    objId = request.POST.get('id')
    point = request.POST.get('point')
    application = Application.objects.get(id=objId)
    application.point = point
    application.save()

    return JsonResponse('Application Updated!', safe=False)

@csrf_exempt
def deleteApplication(request):
	print('Delete called!')
	objId = request.POST.get('id')
	application = Application.objects.get(id=objId)
	application.delete()

	return JsonResponse('Application Deleted!', safe=False)




#============EMPLOYEE IMPLEMENTATION======================================

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
    return render(request, 'application/orientation/rate.html',{'form':form})

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
'''