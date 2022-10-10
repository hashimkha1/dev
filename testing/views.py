import calendar,string
import itertools
from django import template
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q
from mail.custom_email import send_email
from .forms import (
    DepartmentForm,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import (
    Services,
)
from data.models import DSU

from django.conf import settings
from django.contrib.auth import get_user_model
from finance.models import Transaction,Inflow,TrainingLoan
from accounts.models import Tracker,Department, TaskGroups
from management.models import Task
from coda_project import settings
from datetime import date, timedelta
from django.db.models import Q
from testing.utils import target_date
# User=settings.AUTH_USER_MODEL
User = get_user_model()
register = template.Library()


def pay(request):
    deadline,year=target_date()
    context={
         "year":year,
         "deadline":deadline
    }
    return render (request, "testing/testing.html",context)
class ServicesListView(ListView):
    queryset=Services.objects.all()
    template_name="testing/display.html"

def Services_List(request):
    services = Services.objects.all()
    context={
        "services":services
    }
    return render (request, "testing/display.html",context)

class ServicesDetailView(DetailView):
    queryset=Services.objects.all()
    template_name="testing/resume.html"



# ===============================RESEARCH==============================================


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')
# activities=["one one one","one one one session","one one one sessions"]
# myactivities=["oneoneone","oneoneonesession","oneoneonesessions"]
# activitiesmodified= [activity.lower().translate({ord(c): None for c in string.whitespace}) for activity in activities] 
# print(activitiesmodified)

def task_url():
    one_list = ["one on one","one on one session","one on one sessions"]
    job_list =  ["job support","job_support"]
    onelist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in one_list] 
    joblist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in job_list] 
    # activity=self.activity_name.lower().translate({ord(c): None for c in string.whitespace})
    # for i in onelist:
    #     print(i)
    #     if(i == "oneonone"):
    #         print("year")
    #     else:
    #         print("no")
    #     #     return reverse("management:new_evidence", args=[self.id])
    for i,j in itertools.zip_longest(onelist,joblist):
        if i in onelist:
            print(i)
        elif j in joblist:
            print(j)
        else:
            print("no")

        # if(i == "oneonone"):
        #     print("oneonone")
        # elif(i == "oneononesession"):
        #     print("oneononesession")
        # elif(i == "oneononesessions"):
        #     print("oneononesessions")
        # else:
        #     print("no")
    # for i,j in zip(onelist,joblist):
    #     print(i)
    
        # print(j)
        # print(i,j)
        # if(i == "oneonone"):
        #     print("year")
        # else:
        #     print("no")
        # if(i == "oneonone"):
        #     print("year")
        # else:
        #     print("no")
        # if(i == "oneonone"):
        #     print("year")
        # else:
        #     print("no")
# task_url()
@register.filter(name='activitieslist')
def activitieslist(value, myactivities):
    return True if value in myactivities else False

def list(item, mylist):
    filter( lambda x: x in mylist, item)[0]

@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')

# activities=["one one one","one one one session","one one one sessions"]
# myactivities=["oneoneone","oneoneonesession","oneoneonesessions"]
# activitiesmodified= [activity.lower().translate({ord(c): None for c in string.whitespace}) for activity in activities] 
# print(activitiesmodified)
def tasklist():
    tasks=Task.objects.values_list("activity_name")
    activity_list=[]
    for word in tasks:
        for letter in word:
            activity_list.append(letter)
    return activity_list

# tasklist()
def task():
    one_list = ["one on one","one on one session","one on one sessions"]
    job_list =  ["job support","job_support"]
    onelist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in one_list] 
    joblist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in job_list]
    # checklist=tasklist()
    activity= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in tasklist()]
    # print(checklist)
    # print(activity)
    for i,j,k in itertools.zip_longest(onelist,joblist,activity):
        # print(i,j,k)
        if i==k:
            print(i,k)
        if j==k:
            print(j,k)
        else:
            print(i,k)

# task()




