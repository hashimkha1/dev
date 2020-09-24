from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm,ApplicantForm
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .models import Application

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
    applicants=Application.objects.all()
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