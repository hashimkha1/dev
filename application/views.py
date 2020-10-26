from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm,ApplicantForm,RatingForm
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .models import Application,Rating


#Interview description data

interview_descs=[

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
	'Description':'Understanding Company Projects, Values and Other Tools	',
	'Duration':'3 Days	',
	'Lead':'HR Manager'
},
{
	'Inteview':'Third Interview',
	'Concentration':'History,Values & Systems',
	'Description':'Understanding about our history and Key Systems in CODA	',
	'Duration':'2 Days	',
	'Lead':'HR Manager',
},

{
	'Inteview':'Final Interview',
	'Concentration':'Data Analysis 1-1 Sessions',
	'Description':'Measuring,assessing Time sensitivity.',
	'Duration':'7 Days',
	'Lead':'Scrum Master'
}
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def interview(request):
    context = {
        'interview_descs': interview_descs
    }
    return render(request, 'application/interview.html', {'title': 'interview'}, context)

# Create your views here.
class application(TemplateView):
    template_name='application.html'

#saving uploaded file to file system under media
def upload(request):
    if request.method== "POST":
        uploaded_file=request.FILES["document"]
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        #print(uploaded_file.name)
    return render(request, 'application/upload.html')

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

# Create your views here.
def career(request):
    return render(request, 'application/career.html', {'title': 'career'})

def interview(request):
    return render(request, 'application/interview.html', {'title': 'interview'})

def first_interview(request):
    return render(request, 'application/first_interview.html', {'title': 'first_interview'})

def second_interview(request):
    return render(request, 'application/second_interview.html', {'title': 'second_interview'})

def orientation(request):
    return render(request, 'application/orientation.html', {'title': 'orientation'})

def rating(request):
    ratings=Rating.objects.all().order_by('-total_score')
    return render(request, 'application/rating.html', {'ratings': ratings })

def rate(request):
    if request.method== "POST":
        form=RatingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-rating')
    else:
        form=RatingForm()
    return render(request, 'application/rate.html',{'form':form})