from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'investing/home.html', {'title': 'home'})

def testing(request):
    return render(request, 'investing/testing.html', {'title': 'testing'})