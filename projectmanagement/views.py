from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'projectmanagement/home.html', {'title': 'home'})

def construction(request):
    return render(request, 'projectmanagement/construction.html', {'title': 'construction'})