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
from.models import WCAG_STANDARD_WEBSITE
from.forms import WCAG_STANDARD_WEBSITEForm
# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model()


#==============================create your views here===============


def WCAG_STANDARD_WEBSITE_List(request):
    wcag = WCAG_STANDARD_WEBSITE.objects.all()
    print('chech========',wcag)
    return render(request,"application/applications/wcaglist.html",{'wcag':wcag})


def WCAG_STANDARD_WEBSITE_create(request):   
    if request.method=='POST':
        form = WCAG_STANDARD_WEBSITEForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application:wcaglist')
    else:
        form = WCAG_STANDARD_WEBSITEForm
    return render(request,"application/applications/wcagcreate.html",{'form':form})


def WCAG_STANDARD_WEBSITE_Update(request, pk):
    wcag = get_object_or_404(WCAG_STANDARD_WEBSITE, pk=pk)
    if request.method == 'POST':
        form = WCAG_STANDARD_WEBSITEForm(request.POST, instance=wcag)
        if form.is_valid():
            form.save()
            return redirect('application:wcaglist')
    else:
        form = WCAG_STANDARD_WEBSITEForm(instance=wcag)
    return render(request, "application/applications/wcagupdateview.html", {'form': form, 'wcag': wcag})
  

def WCAG_STANDARD_WEBSITE_delete(request,pk):
    wcag = get_object_or_404(WCAG_STANDARD_WEBSITE,pk=pk)
    if request.method == 'POST':
        wcag.delete()
        return redirect('application:wcaglist')
    return render(request,"application/applications/wcagdelete.html",{'wcag':wcag})




















