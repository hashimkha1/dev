
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
from.models import wcagsWebsite
from .forms import wcagForm
#from. utils import analyze_website_for_wcag_compliance

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model

def wcagsWebsite_list_view(request):
    wcaglist=wcagsWebsite.objects.all().order_by("updated_at")
    
    return render(request,"application/wcaglist.html",{"wcaglist":wcaglist})

def wcagsWebsite_create_view(request):
    if request.method == 'POST':
        form =  wcagForm(request.POST)
        if form.is_valid():
            form.save            
            return redirect("application:wcaglist")
    else:
        form = wcagForm()
        print("form ====>",form) 
    return render(request,"application\wcagcreate.html", {'form': form})