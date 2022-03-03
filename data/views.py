from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template import context
from django.contrib.auth import get_user_model,login,authenticate
from django.views.generic import (CreateView,DeleteView,ListView,TemplateView, DetailView,UpdateView)


from .forms import InterviewForm, UploadForm
from .models import InterviewUpload, Upload
from .filters import InterviewFilter

#User=settings.AUTH_USER_MODEL
User = get_user_model()

def analysis(request):
    return render(request, 'main/home_templates/analysis_home.html', {'title': 'analysis'})

def deliverable(request):
        return render(request, 'data/deliverable/deliverable.html', {'title': 'deliverable'})

@login_required
def training(request):
    return render(request, 'data/training/training.html', {'title': 'training'})

@login_required
def bitraining(request):
    return render(request, 'data/training/bitraining.html', {'title': 'training'})

@login_required
def interview(request):
    return render(request, 'data/interview/interview.html')  

def payroll(request):
    return render(request, 'data/deliverable/payroll.html', {'title': 'payroll'})

def financialsystem(request):
    return render(request, 'data/deliverable/financialsystem.html', {'title': 'financialsystem'})

def project(request):
    return render(request, 'data/deliverable/project.html', {'title': 'project'})

    
# views on samples reports.
def report(request):
    return render(request, 'data/documents/report.html', {'title': 'report'})
def database(request):
    return render(request, 'data/database.html', {'title': 'report'})

def etl(request):
    return render(request, 'data/etl.html', {'title': 'etl'})  

def getdata(request):
    return render(request, 'data/getdata.html', {'title': 'getdata'}) 

def pay(request):
    return render(request, 'data/pay.html', {'title': 'pay'}) 

# Views on interview Section
@login_required
def uploadinterview(request):
    if request.method== "POST":
        form=InterviewForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data:iuploads')
    else:
        form=InterviewForm()
    return render(request, 'data/interview/uploadinterview.html',{'form':form})

#for uploading interviews
@login_required
def iuploads(request):
    uploads=InterviewUpload.objects.all().order_by('-upload_date')
    myFilter=InterviewFilter(request.GET, queryset=uploads)
    uploads=myFilter.qs
    context={
              'uploads': uploads,
              'myFilter':myFilter
            }
    return render(request, 'data/interview/iuploads.html',context)

# Saving uploaded information to database
def upload(request):
    if request.method== "POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data-uploaded')
    else:
        form=UploadForm()
    return render(request, 'main/doc_templates/upload.html',{'form':form})

def uploaded(request):
    documents=Upload.objects.all().order_by('-document_date')
    return render(request, 'main/doc_templates/uploaded.html', {'documents': documents})


