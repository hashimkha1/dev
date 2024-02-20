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
from.models import WCAGStandardWebsite
from .forms import wcagForm

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model

def wcag_list_view(request):
    wcaglists=WCAGStandardWebsite.objects.all().order_by("updated_at")
    
    return render(request, "application/wcag.html",{"wcaglists":wcaglists})

def wcag_create_view(request):
    if request.method == 'POST':
        form =wcagForm(request.POST)
        if form.is_valid():
            form.save            
            return redirect("application:wcaglist")
    else:
        form = wcagForm()
        print("form ====>",form) 
    return render(request,"application/wcagcreate.html", {'form': form})    


# def work_departmentList(request):
#     departments = work_department.objects.all()        
#     return render(request,"application/departmentlist.html",{'departments':departments})


#def company_propertiesCreate(request):
    # if request.method == 'POST':
    #     form =propertiesForm(request.POST)
    #     if form.is_valid():
    #         form.save            
    #         return redirect("application:propertylist")
    # else:
    #     form = propertiesForm()
    #     print("form ====>",form) 
    # return render(request,"application/propertycreate.html", {'form': form})

#def company_properties_update(request,pk):
    #properties = get_object_or_404(company_properties,pk=pk)
    #if request.method =='POST':
        #form =propertiesForm(request.POST,instance = properties)
        #if form.is_valid():
            #form.save()
            #return redirect("application:propertylist")
    #else:
        #form = propertiesForm(instance= properties)
        #return render(request,"application/propertyupdate.html",{'form':form,'properties':properties})


#def company_properties_delete(request,pk):
    #properties = get_object_or_404(company_properties,pk=pk) 
    #if request.method =='POST':
        #properties.delete()
        #return redirect("application:propertylist")
    #return render(request,"application/propertydelete.html",{'properties':properties})

#def company_properties_detail(request,pk):
    #properties = get_object_or_404(company_properties,pk=pk)            
    #return render(request,"application/propertydetail.html",{'properties':properties})




