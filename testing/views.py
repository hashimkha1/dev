import calendar,string
import itertools
from django import template
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum, F
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
    Services, Logs #,  ProcessJustification, ProcessBreakdown,  # Supplier,Food
)
from data.models import DSU
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from finance.models import Transaction,Inflow,TrainingLoan
from accounts.models import Tracker,Department, TaskGroups
from management.models import Task, Requirement
from coda_project import settings
from datetime import date, timedelta
from django.db.models import Q
from testing.utils import target_date,live_currency
from gapi.gservices import cashapp_main
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
class ServicesListView(ListView):
    queryset=Services.objects.all()
    template_name="testing/display.html"

def Services_List(request):
    # services = Services.objects.all()
    # context={
    #     "services":services
    # }
    return render (request, "testing/display.html",context)

class ServicesDetailView(DetailView):
    queryset=Services.objects.all()
    template_name="testing/resume.html"


# ==================================TESTING FOOD VIEWS==========================
# @method_decorator(login_required, name="dispatch")
# class FoodCreateView(LoginRequiredMixin, CreateView):
#     model = Food
#     success_url = "/testing/food"
#     fields = "__all__"

#     def form_valid(self, form):
#         if self.request.user:
#             return super().form_valid(form)

# class SupplierCreateView(LoginRequiredMixin, CreateView):
#     model = Supplier
#     success_url = "/testing/food"
#     fields = "__all__"

#     def form_valid(self, form):
#         if self.request.user:
#             return super().form_valid(form)


# @method_decorator(login_required, name="dispatch")
# class SupplierUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Supplier
#     success_url = "/testing/food"
#     # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
#     fields = "__all__"

#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         Supplier = self.get_object()
#         if self.request.user.is_superuser:
#             return True
#         elif self.request.user == Supplier.added_by:
#             return True
#         return redirect("testing:food")


# @method_decorator(login_required, name="dispatch")
# class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Food
#     success_url = "/testing/food"
#     fields = "__all__"

#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         Food = self.get_object()
#         if self.request.user.is_superuser:
#             return True
#         elif self.request.user == Food.added_by:
#             return True
#         return redirect("testing:food")


# class SupplierListView(ListView):
#     model = Supplier
#     template_name = "testing/food.html"
#     context_object_name = "suppliers"
#     ordering = ["-created_at"]
    

# class FoodListView(ListView):
#     model = Food
#     template_name = "testing/food.html"
#     context_object_name = "supplies"
#     ordering = ["-created_at"]
    

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


def LogsViewSet(request):
    logs = Logs.objects.all().order_by("-id")
    if request.user.is_superuser:
        return render(request, "testing/logs.html", {"logs": logs})

    else:
        return redirect("main:layout")

# def justification(request, *args, **kwargs):
#     justifications = ProcessJustification.objects.filter(requirements_id=kwargs.get('pk'))\
#         .values("id", "justification", breakdown=F("Process_in_breakdown__breakdown"),
#                 time=F("Process_in_breakdown__time"), requirement_id=F("requirements__id"),
#                 Qty=F("Process_in_breakdown__Quantity"), total=F("Process_in_breakdown__total"))
#     if justifications:
#         justofication_dict = {}
#         justifications_ids = ProcessJustification.objects.filter(requirements_id=kwargs.get('pk')) \
#             .values_list("id", flat=True)
#         obj = ProcessBreakdown.objects.filter(process__id__in=justifications_ids)
#         total_time = obj.aggregate(Sum('total'))
#         total_qty = obj.aggregate(Sum('Quantity'))
#         for justification in justifications:
#             if justification.get('breakdown') == 'testing' or justification.get('breakdown') == 'creation':
#                 justofication_dict.update({justification.get('justification'): justification.get('justification'),
#                                            justification.get('justification') + justification.get('breakdown'):
#                                                justification.get('breakdown'),
#                                            justification.get('breakdown') + 'time': justification.get('time'),
#                                            justification.get('justification') + justification.get('breakdown') +
#                                            'quantity': justification.get('Qty'),
#                                            justification.get('justification') + justification.get('breakdown') +
#                                            'total': justification.get('total'),
#                                            'requirement_id': justification.get('requirement_id'),
#                                            })
#             else:
#                 justofication_dict.update({justification.get('justification'): justification.get('justification'),
#                                            justification.get('justification')+justification.get('breakdown'):
#                                                justification.get('breakdown'),
#                                            justification.get('breakdown')+'time': justification.get('time'),
#                                            justification.get('breakdown')+'quantity': justification.get('Qty'),
#                                            justification.get('breakdown')+'total': justification.get('total'),
#                                            'requirement_id': justification.get('requirement_id'),
#                                            })
#         return render(request, "testing/req_justifications.html", {"justifications": justofication_dict,
#                                                                    "total_time": total_time.get('total__sum'),
#                                                                     "total_qty": total_qty.get('Quantity__sum')
#         })
#     return render(request, "testing/req_justifications.html", {"active_requirement": kwargs.get('pk')})


# def add_requirement_justification(request):
#     requirement_id = request.POST.get('requirement_id')

#     requirement_obj = Requirement.objects.filter(id=requirement_id).first()
#     print("requirement_obj:==>",requirement_obj)
#     if not requirement_obj:
#         messages.warning(
#             request, "requirement id is wrong"
#         )
#         context={
#             "message":request.path_info
#         }
#         # return  HttpResponseRedirect(request.path_info)
#         return render (request, "main/messages/general.html",context) 
        
#     with transaction.atomic():
#         table = request.POST.get('Table')
#         if table:
#             justification_obj = None
#             obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="table")
#             if obj:
#                 justification_obj = obj.first()
#             else:
#                 justification_obj = ProcessJustification.objects.create(requirements=requirement_obj, justification="table")
#             dictionary = request.POST.get('Dictionary')
#             if dictionary:
#                 time = int(request.POST.get('dictionary_time'))
#                 qty = int(request.POST.get('dictionary_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="dictionary")
#                 if obj:
#                     dictionary_obj = obj.first()
#                     dictionary_obj.Quantity = qty
#                     dictionary_obj.total = time*qty
#                     dictionary_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=justification_obj, breakdown="dictionary", time=time,
#                                                     Quantity=qty, total=time*qty)
#             erd = request.POST.get('Erd')
#             if erd:
#                 time = int(request.POST.get('Erd_time'))
#                 qty = int(request.POST.get('Erd_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="erd")
#                 if obj:
#                     erd_obj = obj.first()
#                     erd_obj.Quantity = qty
#                     erd_obj.total = time * qty
#                     erd_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=justification_obj, breakdown="erd", time=time, Quantity=qty,
#                                                     total=time*qty)
#             table_model = request.POST.get('Table_model')
#             if table_model:
#                 time = int(request.POST.get('Table_time'))
#                 qty = int(request.POST.get('Table_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="table_model")
#                 if obj:
#                     table_model_obj = obj.first()
#                     table_model_obj.Quantity = qty
#                     table_model_obj.total = time * qty
#                     table_model_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=justification_obj, breakdown="table_model", time=time,
#                                                     Quantity=qty, total=time*qty)
#             testing = request.POST.get('Testing')
#             if testing:
#                 time = int(request.POST.get('Testing_time'))
#                 qty = int(request.POST.get('Testing_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="testing")
#                 if obj:
#                     testing_obj = obj.first()
#                     testing_obj.Quantity = qty
#                     testing_obj.total = time * qty
#                     testing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=justification_obj, breakdown="testing", time=time,
#                                                     Quantity=qty, total=time*qty)
#         view_obj = request.POST.get('view')
#         if view_obj:
#             view_instance = None
#             obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="view")
#             if obj:
#                 view_instance = obj.first()
#             else:
#                 view_instance = ProcessJustification.objects.create(requirements=requirement_obj, justification="view")
#             flow_diagram = request.POST.get('flow_diagram')
#             if flow_diagram:
#                 time = int(request.POST.get('flow_diagram_time'))
#                 qty = int(request.POST.get('flow_diagram_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="flow_diagram")
#                 if obj:
#                     flow_diagram_obj = obj.first()
#                     flow_diagram_obj.Quantity = qty
#                     flow_diagram_obj.total = time * qty
#                     flow_diagram_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="flow_diagram", time=time,
#                                                     Quantity=qty, total=time*qty)
#             create = request.POST.get('view_create')
#             if create:
#                 time = int(request.POST.get('create_time'))
#                 qty = int(request.POST.get('create_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="create")
#                 if obj:
#                     create_obj = obj.first()
#                     create_obj.Quantity = qty
#                     create_obj.total = time * qty
#                     create_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="create", time=time,
#                                                     Quantity=qty, total=time*qty)
#             detail = request.POST.get('detail')
#             if detail:
#                 time = int(request.POST.get('detail_time'))
#                 qty = int(request.POST.get('detail_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="detail")
#                 if obj:
#                     testing_obj = obj.first()
#                     testing_obj.Quantity = qty
#                     testing_obj.total = time * qty
#                     testing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="detail", time=time,
#                                                 Quantity=qty, total=time*qty)
#             list_obj = request.POST.get('list')
#             if list_obj:
#                 time = int(request.POST.get('list_time'))
#                 qty = int(request.POST.get('list_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="list")
#                 if obj:
#                     list_obj = obj.first()
#                     list_obj.Quantity = qty
#                     list_obj.total = time * qty
#                     list_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="list", time=time,
#                                                     Quantity=qty, total=time*qty)
#             update_obj = request.POST.get('update')
#             if update_obj:
#                 time = int(request.POST.get('update_time'))
#                 qty = int(request.POST.get('update_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="update")
#                 if obj:
#                     update_obj = obj.first()
#                     update_obj.Quantity = qty
#                     update_obj.total = time * qty
#                     update_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="update", time=time,
#                                                     Quantity=qty, total=time*qty)
#             delete_obj = request.POST.get('delete')
#             if delete_obj:
#                 time = int(request.POST.get('delete_time'))
#                 qty = int(request.POST.get('delete_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="delete")
#                 if obj:
#                     delete_obj = obj.first()
#                     delete_obj.Quantity = qty
#                     delete_obj.total = time * qty
#                     delete_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="delete", time=time,
#                                                     Quantity=qty, total=time*qty)
#             testing_view = request.POST.get('testing_view')
#             if testing_view:
#                 time = int(request.POST.get('testing_view_time'))
#                 qty = int(request.POST.get('testing_view_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="testing")
#                 if obj:
#                     testing_obj = obj.first()
#                     testing_obj.Quantity = qty
#                     testing_obj.total = time * qty
#                     testing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=view_instance, breakdown="testing", time=time,
#                                                     Quantity=qty, total=time*qty)

#         template_obj = request.POST.get('template')
#         if template_obj:
#             template_instance = None
#             obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="template")
#             if obj:
#                 template_instance = obj.first()
#             else:
#                 template_instance = ProcessJustification.objects.create(requirements=requirement_obj,
#                                                                         justification="template")
#             template_creation = request.POST.get('template_creation')
#             if template_creation:
#                 time = int(request.POST.get('template_creation_time'))
#                 qty = int(request.POST.get('template_creation_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=template_instance, breakdown="creation")
#                 if obj:
#                     creation_obj = obj.first()
#                     creation_obj.Quantity = qty
#                     creation_obj.total = time * qty
#                     creation_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=template_instance, breakdown="creation", time=time,
#                                                     Quantity=qty, total=time*qty)
#             template_testing = request.POST.get('template_testing')
#             if template_testing:
#                 time = int(request.POST.get('template_testing_time'))
#                 qty = int(request.POST.get('template_testing_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=template_instance, breakdown="testing")
#                 if obj:
#                     testing_obj = obj.first()
#                     testing_obj.Quantity = qty
#                     testing_obj.total = time * qty
#                     testing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=template_instance, breakdown="testing", time=time,
#                                                     Quantity=qty, total=time*qty)
#         forms = request.POST.get('forms')
#         if forms:
#             forms_instance = None
#             obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="forms")
#             if obj:
#                 forms_instance = obj.first()
#             else:
#                 forms_instance = ProcessJustification.objects.create(requirements=requirement_obj,
#                                                                      justification="forms")
#             form_creation = request.POST.get('form_creation')
#             if form_creation:
#                 time = int(request.POST.get('form_creation_time'))
#                 qty = int(request.POST.get('form_creation_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=forms_instance, breakdown="creation")
#                 if obj:
#                     creation_obj = obj.first()
#                     creation_obj.Quantity = qty
#                     creation_obj.total = time * qty
#                     creation_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=forms_instance, breakdown="creation", time=time,
#                                                     Quantity=qty, total=time*qty)
#             form_testing = request.POST.get('form_testing')
#             if form_testing:
#                 time = int(request.POST.get('form_testing_time'))
#                 qty = int(request.POST.get('form_testing_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=forms_instance, breakdown="testing")
#                 if obj:
#                     testing_obj = obj.first()
#                     testing_obj.Quantity = qty
#                     testing_obj.total = time * qty
#                     testing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=forms_instance, breakdown="testing", time=time,
#                                                     Quantity=qty, total=time*qty)
#         apis = request.POST.get('apis')
#         if apis:
#             apis_instance = None
#             obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="apis")
#             if obj:
#                 apis_instance = obj.first()
#             else:
#                 apis_instance = ProcessJustification.objects.create(requirements=requirement_obj,
#                                                                     justification="apis")
#             new_api = request.POST.get('new_api')
#             if new_api:
#                 time = int(request.POST.get('new_api_time'))
#                 qty = int(request.POST.get('new_api_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=apis_instance, breakdown="new")
#                 if obj:
#                     new_obj = obj.first()
#                     new_obj.Quantity = qty
#                     new_obj.total = time * qty
#                     new_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=apis_instance, breakdown="new", time=time,
#                                                     Quantity=qty, total=time * qty)
#             existing_api = request.POST.get('existing_api')
#             if existing_api:
#                 time = int(request.POST.get('existing_api_time'))
#                 qty = int(request.POST.get('existing_api_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=apis_instance, breakdown="existing")
#                 if obj:
#                     existing_obj = obj.first()
#                     existing_obj.Quantity = qty
#                     existing_obj.total = time * qty
#                     existing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=apis_instance, breakdown="existing", time=time,
#                                                     Quantity=qty, total=time * qty)
#             api_testing = request.POST.get('api_testing')
#             if api_testing:
#                 time = int(request.POST.get('api_testing_time'))
#                 qty = int(request.POST.get('api_testing_quantity'))
#                 obj = ProcessBreakdown.objects.filter(process=apis_instance, breakdown="testing")
#                 if obj:
#                     testing_obj = obj.first()
#                     testing_obj.Quantity = qty
#                     testing_obj.total = time * qty
#                     testing_obj.save()

#                 else:
#                     ProcessBreakdown.objects.create(process=apis_instance, breakdown="testing", time=time,
#                                                     Quantity=qty, total=time * qty)

#         active_requirements = Requirement.objects.all().filter(is_active=True)
#         context = {"active_requirements": active_requirements}
#         return render(request, "management/doc_templates/active_requirements.html", context)

