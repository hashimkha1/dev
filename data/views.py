from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import InterviewUpload,Upload
from .forms import InterviewForm,UploadForm



posts=[

{
	'Concentration':'Questions',
	'Description':'Key Questions on each role listed below	',
	'Duration':'5 Days	',
	'Lead':'Interview Coach'
},
{
	'Concentration':'Responses',
	'Description':'End to end guide on how to respond to interview questions.	',
	'Duration':'5 Days	',
	'Lead':'Interview Coach'
},

{
	'Concentration':'Past Interviews',
	'Description':'Review your interview skills using recorded real interviews.',
	'Duration':'7 Days',
	'Lead':'Interview Coach'
},

{
	'Concentration':'Mock Sessions',
	'Description':'Do 10 Mock Interview with experienced coaches and Data Analysts in the Field',
	'Duration':'7 Days',
	'Lead':'Interview Coach'
}
]


def home(request):
    return render(request, 'data/home.html', {'title': 'home'})

def deliverable(request):
        return render(request, 'data/deliverable.html', {'title': 'deliverable'})

@login_required
def training(request):
    return render(request, 'data/training.html', {'title': 'training'})

@login_required
def interview(request):
    context = {
        'posts': posts
    }
    return render(request, 'data/interview.html', context)  

def payroll(request):
    return render(request, 'data/payroll.html', {'title': 'payroll'})

def financialsystem(request):
    return render(request, 'data/financialsystem.html', {'title': 'financialsystem'})

def project(request):
    return render(request, 'data/project.html', {'title': 'project'})

def consultancy(request):
    return render(request, 'data/consultancy.html', {'title': 'consultancy'})
    
# views on samples reports.
def report(request):
    return render(request, 'data/report.html', {'title': 'report'})
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
            return redirect('data-uploads')
    else:
        form=InterviewForm()
    return render(request, 'data/uploadinterview.html',{'form':form})

#for uploading interviews
@login_required
def iuploads(request):
    uploads=InterviewUpload.objects.all().order_by('-upload_date')
    return render(request, 'data/iuploads.html', {'uploads': uploads})

# Saving uploaded information to database
def upload(request):
    if request.method== "POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('investing-uploaded')
    else:
        form=UploadForm()
    return render(request, 'investing/upload.html',{'form':form})


def uploaded(request):
    documents=Upload.objects.all().order_by('-document_date')
    return render(request, 'investing/uploaded.html', {'documents': documents})


def testing(request):
    context = {
        'posts': posts
    }
    return render(request, 'data/testing.html', context)  


