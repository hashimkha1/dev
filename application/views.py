from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm,ApplicantForm,RatingForm,InterviewUploadForm,EmployeeForm,InterviewForm
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .models import Application,Rated,InteviewUploads,Employee,FirstUpload

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

'''saving uploaded file to file system under media
def upload(request):
    if request.method== "POST":
        uploaded_file=request.FILES["document"]
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        #print(uploaded_file.name)
    return render(request, 'application/upload.html')
'''
# Saving uploaded information to database
def apply(request):
    if request.method== "POST":
        form=ApplicantForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-interview')
    else:
        form=ApplicantForm()
    return render(request, 'application/apply.html',{'form':form})



def applicants(request):
    applicants=Application.objects.all().order_by('-application_date')
    return render(request, 'application/applicants.html', {'applicants': applicants})

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

# -------------------------Uploads Section-------------------------------------#
'''
def firstupload(request):
    if request.method== "POST":
        form=InterviewUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-second_interview')
    else:
         form=InterviewUploadForm()
    return render(request, 'application/firstupload.html',{'form':form})

def upload(request):
    iuploads=InteviewUploads.objects.all().order_by('-upload_date')
    return render(request, 'application/upload.html', {'iuploads': iuploads})
'''

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
    ratings=Rated.objects.all().order_by('-punctuality')
    return render(request, 'application/rating.html', {'ratings': ratings})
'''
def employee_form(request,id=0):
    if request.method == "GET":
        if id==0:
            form=EmployeeForm()
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(instance=employee)
        return render(request, 'application/employee_form.html',{'form':form})
    else:
        form=EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return redirect('application-employee_list')

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
'''
# -------------------------testing Section-------------------------------------#
'''
def test(request):
    pass

def uploaded(request):
    pass
'''