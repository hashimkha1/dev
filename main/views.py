from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Expenses
from .forms import TransactionForm
# Create your views here.
def test(request):
    return render(request, 'main/test.html', {'title': 'test'})

def checkout(request):
    return render(request, 'main/checkout.html', {'title': 'checkout'})

def layout(request):
    return render(request, 'main/layout.html', {'title': 'layout'})

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


# -------------------------transactions Section-------------------------------------#
def transact(request):
    if request.method== "POST":
        form=TransactionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projectmanagement-transaction')
    else:
        form=TransactionForm()
    return render(request, 'projectmanagement/transact.html',{'form':form})

def transaction(request):
    transactions=Expenses.objects.all().order_by('-activity_date')
    return render(request, 'projectmanagement/transaction.html', {'transactions': transactions})


#-----------------------------Documents---------------------------------
'''
def codadocuments(request):
    codadocuments=Codadoc.objects.all().order_by('-date_uploaded')
    return render(request, 'main/documentation.html', {'codadocuments': codadocuments})


def doc(request):
    if request.method== "POST":
        form=CodadocumentsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main-documents')
    else:
        form=CodadocumentsForm()
    return render(request, 'main/doc.html',{'form':form})
'''