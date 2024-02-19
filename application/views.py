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
#from.models import WCAGSTANDARD_WEBSITE
#from.forms import WCAGSTANDARDForm
# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model()

#=================create your views here=============

# #def WCAG_list(request):
#     rating = WCAGSTANDARD_WEBSITE.objects.all()
#     return render (request,"application/applications/WCAGlist.html",{'wcag':wcag})

# def companyrating_create(request):
#   if request.method=='POST':
#       form = CompanyRatingForm(request.POST)
#       if form.is_valid():
#         form.save()
#         return redirect('application:ratinglist')
#   else:
#     form = CompanyRatingForm
#     return render(request,"application/training/ratingcreate.html",{'form':form})
  
# def companyrating_update(request, pk):
#     rating = get_object_or_404(Company_Rating, pk=pk)
#     if request.method == 'POST':
#         form = CompanyRatingForm(request.POST, instance=rating)
#         if form.is_valid():
#             form.save()
#             return redirect('application:ratinglist')
#     else:
#         form = CompanyRatingForm(instance=rating)
   
#     return render(request, "application/training/ratingupdate.html", {'form': form, 'rating': rating})
        
# def companyrating_delete(request,pk):
#     rating = get_object_or_404(Company_Rating,pk=pk)
#     if request.method == 'POST':
#        rating.delete()
#        return redirect('application:ratinglist')
#     return render(request,"application/training/ratingdeletehtml",{'rating':rating})

# def companyrating_detailview(request,pk):
#    object_list = get_object_or_404(Company_Rating,pk=pk)
#    return render(request,"application/training/ratingdetailview.html",{'object_list':object_list})



  

