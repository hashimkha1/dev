from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm,UploadForm
from django.core.files.storage import FileSystemStorage
from .models import Document,Uploads

# Create your views here.
def home(request):
    return render(request, 'investing/home.html', {'title': 'home'})

def testing(request):
    return render(request, 'investing/testing.html', {'title': 'testing'})


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
    documents=Uploads.objects.all().order_by('-document_date')
    return render(request, 'investing/uploaded.html', {'documents': documents})
