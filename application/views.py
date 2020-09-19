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
def upload_resume(request):
    if request.method== "POST":
        form=ApplicantForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-applicants')
    else:
        form=ApplicantForm()
    return render(request, 'application/upload_resume.html',{'form':form})


def applicants(request):
    applicants=Application.objects.all()
    return render(request, 'application/applicants.html', {'applicants': applicants})


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('application-interview')
    else:
        form = ApplicationForm()
    return render(request, 'application/apply.html', {'form': form})

@login_required
def applicant_profile(request):
    return render(request, 'application/applicant_profile.html')

# Create your views here.
def career(request):
    return render(request, 'application/career.html', {'title': 'career'})

def interview(request):
    return render(request, 'application/interview.html', {'title': 'interview'})