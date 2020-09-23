from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'main/home.html', {'title': 'home'})

def about(request):
    return render(request, 'main/about.html', {'title': 'about'})

def about_us(request):
    return render(request, 'main/about_us.html', {'title': 'about_us'})


def team(request):
    return render(request, 'main/team.html', {'title': 'team'})

def coach_profile(request):
    return render(request, 'main/coach_profile.html', {'title': 'coach_profile'})

def contact(request):
    return render(request, 'main/contact.html', {'title': 'contact'})

def report(request):
    return render(request, 'main/report.html', {'title': 'report'})

def pay(request):
    return render(request, 'main/pay.html', {'title': 'pay'})
    
def training(request):
    return render(request, 'main/training.html', {'title': 'training'})

def project(request):
    return render(request, 'main/project.html', {'title': 'project'})