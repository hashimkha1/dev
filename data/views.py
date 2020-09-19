from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# views on training.
def course(request):
    return render(request, 'data/course.html', {'title': 'course'})
    
def training(request):
    return render(request, 'data/training.html', {'title': 'training'})
def project(request):
    return render(request, 'data/project.html', {'title': 'project'})

# views on samples reports.
def report(request):
    return render(request, 'data/report.html', {'title': 'report'})
def database(request):
    return render(request, 'data/database.html', {'title': 'report'})

def etl(request):
    return render(request, 'data/etl.html', {'title': 'etl'})  