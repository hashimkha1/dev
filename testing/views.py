import calendar,string
import itertools
from django import template
from django.shortcuts import get_object_or_404, redirect, render
from .models import Logs 
from django.contrib.auth import get_user_model
from django.db.models import Q
from testing.utils import target_date,live_currency
# User=settings.AUTH_USER_MODEL
User = get_user_model()
register = template.Library()


def testing(request):
    # cashapp_main()
    live_currency()
    deadline,year=target_date()
    context={
         "year":year,
         "deadline":deadline
    }
    return render (request, "testing/testing.html",context)


# ===============================RESEARCH==============================================
@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')

def task_url():
    one_list = ["one on one","one on one session","one on one sessions"]
    job_list =  ["job support","job_support"]
    onelist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in one_list] 
    joblist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in job_list] 

    for i,j in itertools.zip_longest(onelist,joblist):
        if i in onelist:
            print(i)
        elif j in joblist:
            print(j)
        else:
            print("no")

@register.filter(name='activitieslist')
def activitieslist(value, myactivities):
    return True if value in myactivities else False

def list(item, mylist):
    filter( lambda x: x in mylist, item)[0]

@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')

# def tasklist():
#     tasks=Task.objects.values_list("activity_name")
#     activity_list=[]
#     for word in tasks:
#         for letter in word:
#             activity_list.append(letter)
#     return activity_list

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


def LogsViewSet(request):
    logs = Logs.objects.all().order_by("-id")
    if request.user.is_superuser:
        return render(request, "testing/logs.html", {"logs": logs})

    else:
        return redirect("main:layout")