from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# views on training.
def home(request):
    return render(request, 'data/home.html', {'title': 'home'})

def deliverable(request):
        return render(request, 'data/deliverable.html', {'title': 'deliverable'})

def training(request):
    return render(request, 'data/training.html', {'title': 'training'})

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