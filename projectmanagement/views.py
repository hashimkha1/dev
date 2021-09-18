from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .models import Expenses,Expense

# Create your views here.
def home(request):
    return render(request, 'projectmanagement/home.html', {'title': 'home'})

def construction(request):
    return render(request, 'projectmanagement/construction.html', {'title': 'construction'})

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

