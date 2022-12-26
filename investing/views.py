from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from .forms import DocumentForm, UploadForm
from .models import Document, Uploads


# Create your views here.
def home(request):
    return render(request, 'main/home_templates/investing_home.html', {'title': 'home'})

def coveredcalls(request):
    return render(request, 'investing/covered_call.html', {'title': 'covered Calls'})

def sauti(request):
    return render(request, 'investing/sauti.html', {'title': 'sauti'})

def layout(request):
    return render(request, 'investing/layout.html', {'title': 'layout'})

def training(request):
    return render(request, 'investing/training.html', {'title': 'training'})


# Saving uploaded information to database
def upload(request):
    if request.method== "POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('investing:uploaded')
    else:
        form=UploadForm()
    return render(request, 'main/doc_templates/upload.html',{'form':form})


def uploaded(request):
    documents=Uploads.objects.all().order_by('-document_date')
    return render(request, 'main/doc_templates/uploaded.html', {'documents': documents})

