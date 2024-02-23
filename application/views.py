import math
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import WCAG_TAB_Form
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse
from .models import WCAG_TAB

def WCAG_TAB_list(request):
    wcaglist = WCAG_TAB.objects.all()
    return render(request,"application/applications/wcagtablist.html",{'wcaglist':wcaglist})

def WCAGTABcreate_view(request):
    if request.method == 'POST':
        form =WCAG_TAB_Form(request.POST)
        if form.is_valid():
            form.save            
            return redirect("application:wcaglist")
    else:
        form = WCAG_TAB_Form()
        print("form ====>",form) 
    return render(request,"application/applications/wcagtabcreate.html", {'form': form})  