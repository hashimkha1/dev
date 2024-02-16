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
from.models import Company_Rating

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model()

#=================create your views here=============

def Company_Rating_list(request):
    rating = Company_Rating.objects.all()
    return render (request,"application/training/ratinglist.html",{'rating':rating})

def companyrating_create(request):
  if request.method=='POST':
      form = CompanyRatingForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('finance:ratinglist')
  else:
    form = CompanyRatingForm
    return render(request,"application/training/ratingcreate.html",{'form':form})

  
