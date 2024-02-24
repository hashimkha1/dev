from django.db.models import Q
from django.utils.text import capfirst
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import (
CreateView,
DeleteView,
ListView,
DetailView,
UpdateView,
)
from.models import InvestmentStrategy
from .forms import strategyForm

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model

def investStrategyList(request):
    strategy = InvestmentStrategy.objects.all()
    print("strategy====>",strategy)
    return render(request,"application/strategylist.html",{'strategy':strategy})

def investStrategyCreate(request):
    if request.method == 'POST':
        form =strategyForm(request.POST)
        if form.is_valid():
            form.save
            return redirect("application:strategylist")
    else:
        form = strategyForm()
        print("form ====>",form)
        return render(request,"application/strategycreate.html", {'form': form})


def investStrategyUpdate(request,pk):
    strategy = get_object_or_404(InvestmentStrategy,pk=pk)
    if request.method =='POST':
        form =strategyForm(request.POST,instance = strategy)
        if form.is_valid():
            form.save()
            return redirect("application:strategylist")
    else:
        form = strategyForm(instance= strategy)
        return render(request,"application/strategyupdate.html",{'form':form,'strategy':strategy})


def investStrategyDelete(request,pk):
    strategy = get_object_or_404(InvestmentStrategy,pk=pk)
    if request.method =='POST':
        strategy.delete()
        return redirect("application:strategylist")
        return render(request,"application/strategydelete.html",{'strategy':strategy})























